from blocks import GunBlock
from field_analyser import FieldAnalyser
from ship import Ship
from utils.distance import get_fire_offset, distance_ship2ship, get_direction_vector
from utils.geometry import point_in_bresenham, SHIP_CORR, NEG_SHIP_CORR


class Attack:
    def __init__(self, field_analyser: FieldAnalyser):
        self.field_analyser = field_analyser

    def enemy_score(self) -> float:
        raise NotImplementedError()

    def get_best_enemy(self, ship: Ship):
        matrix = self.field_analyser.state.OppDistanceHp
        best_enemy_id = min((e for e in matrix[ship.Data.Id].items()),
                            key=lambda x: x[1][0])[0]
        return best_enemy_id

    def get_best_gun(self, ship: Ship) -> str:
        return ship.Data.Guns[0].Name

    def update(self):
        focus = sorted(list(self.field_analyser.state.MaxOppDamageImpact.items()), key=lambda x: x[1], reverse=True)
        if focus:
            target = self.field_analyser.state.OppShips[focus[0][0]]
        for ship_id, ship in self.field_analyser.state.MyShips.items():
            if focus and distance_ship2ship(ship.ExpectedPosition, target.Data.Position):
                _, offset = get_fire_offset(ship.ExpectedPosition, target.Data.Position)
                correction = NEG_SHIP_CORR[offset]
                ship.set_attack(target.Data.Position + correction, self.get_best_gun(ship), target.Data.Id)
            else:
                enemy = self.field_analyser.state.OppShips[self.get_best_enemy(ship)]
                if distance_ship2ship(enemy.Data.Position, ship.ExpectedPosition) <= ship.Data.MaxRangeAttack:
                    _, offset = get_fire_offset(ship.ExpectedPosition, target.Data.Position)
                    correction = NEG_SHIP_CORR[offset]
                    ship.set_attack(enemy.Data.Position + correction, self.get_best_gun(ship), enemy.Data.Id)
