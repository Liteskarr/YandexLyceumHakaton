from blocks import GunBlock
from field_analyser import FieldAnalyser
from ship import Ship
from utils.distance import get_fire_offset, distance_ship2ship, get_direction_vector
from utils.geometry import point_in_bresenham, SHIP_CORR, NEG_SHIP_CORR
from utils.vector import Vector


class Attack:
    def __init__(self, field_analyser: FieldAnalyser):
        self.field_analyser = field_analyser

    def enemy_score(self) -> float:
        raise NotImplementedError()

    def get_best_enemy_id(self, ship: Ship):
        matrix = self.field_analyser.state.OppDistanceHp
        best_enemy_id = min((e for e in matrix[ship.Data.Id].items()),
                            key=lambda x: x[1][0])[0]
        return best_enemy_id

    def get_best_enemies(self, ship: Ship):
        matrix = self.field_analyser.state.OppDistanceHp
        return sorted((e for e in matrix[ship.Data.Id].items()), key=lambda x: x[1][0])

    def get_best_gun(self, ship: Ship) -> str:
        return ship.Data.Guns[0].Name

    def check_friendly_fire(self, from_ship: Ship, from_point: Vector, target: Vector) -> bool:
        for Id, ship in self.field_analyser.state.MyShips.items():
            if Id != from_ship.Data.Id:
                for cor in SHIP_CORR:
                    if point_in_bresenham(ship.ExpectedPosition + cor, start=from_point, finish=target):
                        return True
        return False

    def update(self):
        focus = sorted(list(self.field_analyser.state.MaxOppDamageImpact.items()), key=lambda x: x[1], reverse=True)
        if focus:
            target = self.field_analyser.state.OppShips[focus[0][0]]
        for ship_id, ship in self.field_analyser.state.MyShips.items():
            if focus:
                cor_my, cor_opp = get_fire_offset(ship.ExpectedPosition, target.ExpectedPosition)
                correction = NEG_SHIP_CORR[cor_opp]
                from_point, target_point = ship.ExpectedPosition + cor_my, target.ExpectedPosition + correction
                if distance_ship2ship(ship.ExpectedPosition + cor_my, target.ExpectedPosition + cor_opp) and \
                        not self.check_friendly_fire(ship, from_point, target_point):
                    ship.set_attack(target_point, self.get_best_gun(ship), target.Data.Id)
                    continue
            # ИНАЧЕ
            for id_enemy, _ in self.get_best_enemies(ship):
                enemy = self.field_analyser.state.OppShips[id_enemy]
                cor_my, cor_opp = get_fire_offset(ship.ExpectedPosition, enemy.ExpectedPosition)
                correction = NEG_SHIP_CORR[cor_opp]
                from_point, target_point = ship.ExpectedPosition + cor_my, enemy.ExpectedPosition + correction
                if distance_ship2ship(ship.ExpectedPosition + cor_my, enemy.ExpectedPosition + cor_opp) <= \
                        ship.Data.MaxRangeAttack and not self.check_friendly_fire(ship, from_point, target_point):
                    ship.set_attack(target_point, self.get_best_gun(ship), enemy.Data.Id)
