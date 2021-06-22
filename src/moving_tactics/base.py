from math import ceil
from collections import namedtuple
from enum import Enum
from itertools import product, chain
from typing import Dict, Optional, List

from field_analyser import FieldAnalyser
from moving import change_velocity, moving
from moving_tactics import IMovingTactics
from ship import Ship
from utils.math import activate
from utils.distance import distance_point2ship, distance_ship2ship
from utils.vector import Vector

MovingState = namedtuple('MovingState', ['lock'])


class MovingStates(Enum):
    FREE = MovingState(False)
    BRAKING = MovingState(True)
    RETREAT = MovingState(True)


def could_stand_on_point(p: Vector):
    return 0 <= p.X <= 28 and 0 <= p.Y <= 28 and 0 <= p.Z <= 28


CONTROL_POINTS = list(chain(map(lambda x: Vector(*x), product([-1, 0, 1], repeat=3)),
                            map(lambda x: Vector(*x), product([-1.2, 0, 1.2], repeat=3))))


class BaseMovingTactics(IMovingTactics):
    def __init__(self, field_analyser: FieldAnalyser):
        self.initialized: bool = False
        self.enemies_center: Vector = Vector(0, 0, 0)
        self.global_target: Optional[int] = None
        self.field_analyser = field_analyser
        self.states: Dict[int, MovingStates] = {}
        self.control_points: Dict[int, List[Vector]] = {}
        self.targets: Dict[int, Vector] = {}

    def enemy_score(self, ship_id: int, ship: Ship) -> float:
        enemy_position = self.field_analyser.state.OppShips[ship_id].Data.Position
        # Подсчет дальности от наших кораблей.
        own_average_distance = sum((distance_ship2ship(ship.Data.Position, enemy_position)
                                    for ship in self.field_analyser.state.MyShips.values()))
        own_average_distance /= len(self.field_analyser.state.MyShips) * 29
        own_distance_score = activate(0.1, own_average_distance)
        # Подсчет количества HP.
        hp_score = activate(0.0, ship.Data.Health / 128)
        # Дальность от своих союзников.
        enemy_average_distance = sum((distance_ship2ship(ship.Data.Position, enemy_position)
                                      for ship in self.field_analyser.state.OppShips.values()))
        enemy_average_distance /= len(self.field_analyser.state.MyShips) * 29
        enemy_distance_score = activate(0.2, own_average_distance)
        # Близость к центру масс противников.
        center_distance = distance_point2ship(self.enemies_center, enemy_position)
        center_score = activate(1.0, center_distance / 30) ** (1 / 3)
        center_score *= -4
        #
        target_changing_score = 0 if self.global_target in [ship_id, None] else -1.3
        return own_distance_score + hp_score + enemy_distance_score + center_score + target_changing_score

    def point_score(self, point: Vector, dist: Vector, ship_id: int, ship: Ship):
        distance = distance_point2ship(point, ship.Data.Position)
        distance_score = activate(0.2, distance / 30)
        # Близость к центру масс противников.
        center_distance = distance_point2ship(self.enemies_center, point)
        center_score = activate(1.0, center_distance / 30) ** (1 / 3)
        center_score *= -3
        #
        count = 0
        for enemy in self.field_analyser.state.OppShips.values():
            if distance_point2ship(point, enemy.ExpectedPosition) <= ship.Data.MaxRangeAttack:
                count += 1
        count_score = 3 * activate(0.2, count / 5) ** (1 / 2)
        return count_score + center_score + distance_score

    def must_retreat(self, ship: Ship) -> bool:
        if self.field_analyser.prev_state.MyShips[ship.Data.Id].Data.Health / ship.Data.Health < 0.8:
            return True
        return False

    def ship_initialization(self):
        for ship in self.field_analyser.state.MyShips.values():
            if ship.Data.Id not in self.states:
                self.states[ship.Data.Id] = MovingStates.FREE
            if ship.Data.Id not in self.control_points:
                self.control_points[ship.Data.Id] = list(map(lambda x: (x * (ship.Data.MaxRangeAttack - 1)).ceil(),
                                                             CONTROL_POINTS))

    def update_enemies_center(self):
        self.enemies_center = Vector(0, 0, 0)
        for enemy in self.field_analyser.state.OppShips.values():
            self.enemies_center += enemy.Data.Position
        self.enemies_center = self.enemies_center // len(self.field_analyser.state.OppShips)

    def update_global_target(self):
        self.global_target = max(self.field_analyser.state.OppShips.values(),
                                 key=lambda x: self.enemy_score(x.Data.Id, x)).Data.Id

    def move(self, ship: Ship, target: Vector):
        ship.set_move_target(target)

    def give_an_order(self, ship_id: int, ship: Ship):
        self.used = set()
        if ship.ExpectedVelocity != ship.Data.Velocity:
            ship.set_way(change_velocity(ship.Data.Position, Vector(0, 0, 0)))
            return

        if self.global_target is not None:
            global_enemy = self.field_analyser.state.OppShips[self.global_target]
            points = map(lambda x: (x + global_enemy.Data.Position, x), self.control_points[ship_id])
            points = filter(lambda x: could_stand_on_point(x[0]), points)
            points = list(points)
            if points:
                point = max(points, key=lambda x: self.point_score(x[0], x[1], ship_id, ship))
            else:
                point = (ship.Data.Position, )
            self.targets[ship_id] = point[0]
            self.used.add(point[0])
            self.move(ship, point[0])

    def update(self):
        if not self.initialized:
            self.ship_initialization()
            self.initialized = True
        self.update_global_target()
        self.update_enemies_center()
        for ship_id, ship in self.field_analyser.state.MyShips.items():
            self.give_an_order(ship_id, ship)
