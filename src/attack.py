from blocks import GunBlock
from field_analyser import FieldAnalyser
from ship import Ship
from utils.distance import get_fire_offset, distance_ship2ship
from utils.geometry import point_in_bresenham, SHIP_CORR


class OAttack:
    def __init__(self, field_analyser: FieldAnalyser) -> None:
        self.field_analyser = field_analyser
        self.focus = list()
        self.delta_adjustment = 0.5

    def damage_opp(self, gun: GunBlock, opp_Id: int) -> None:
        for Id in self.field_analyser.state.MyShips.keys():
            if self.field_analyser.state.OppDistanceHp[Id][opp_Id][1] > gun.Damage:
                self.field_analyser.state.OppDistanceHp[Id][opp_Id][1] -= gun.Damage
            else:
                self.field_analyser.state.OppDistanceHp[Id].pop(opp_Id)

    def check_friendly_fire(self, ship: Ship):
        ship.FriendlyFire = False
        start, finish = ship.Data.Position + ship.Data.Velocity, ship.AttackTarget
        offset_start, offset_finish = get_fire_offset(start, finish)
        start += offset_start
        for Id, ship_ in self.field_analyser.state.MyShips.items():
            if Id != ship.Data.Id:
                for offset in SHIP_CORR:
                    if point_in_bresenham(point=ship_.Data.Position + offset, start=start, finish=finish):
                        ship.FriendlyFire = True
                        return

    def check_hit(self, Id: int):
        if self.field_analyser.prev_state:
            prev_ship = self.field_analyser.prev_state.MyShips[Id]

            if self.field_analyser.state.OppShips.get(prev_ship.OppIdTarget, None):
                prev_target = self.field_analyser.prev_state.MyShips[Id].AttackTarget
                prev_pos = prev_ship.Data.Position
                opp_pos = self.field_analyser.state.OppShips[prev_ship.OppIdTarget].Data.Position
                for corr in SHIP_CORR:
                    if point_in_bresenham(point=opp_pos + corr, start=prev_pos, finish=prev_target):
                        return
                edit = sorted(list(self.field_analyser.state.MyShips[Id].Adjustment.items()), key=lambda x: x[1])[-1][0]
                self.field_analyser.state.MyShips[Id].Adjustment[edit] -= self.delta_adjustment

    def update(self):
        self.focus = list()
        # cor = Vector(0, 0, 0)  TODO: Кинуть в цикл
        for Id, opp in self.field_analyser.state.OppShips.items():
            if opp.Data.Health <= self.field_analyser.state.MaxOppDamageImpact[Id]:
                self.focus.append(Id)
        if not self.focus:
            self.focus = sorted(list(self.field_analyser.state.MaxOppDamageImpact.items()), key=lambda x: x[1])[-1]
        #
        for Id, ship in self.field_analyser.state.MyShips.items():
            ship.AttackTarget = None
            ship.UsedGun = None
            ship.OppIdTarget = None
            if self.focus:
                opp = self.field_analyser.state.OppShips[self.focus[0]]
                dist, hp = self.field_analyser.state.OppDistanceHp[Id][opp.Data.Id]
                cor = sorted(list(ship.Adjustment.items()), key=lambda x: x[1])[-1][0]
                if hp > 0 and dist <= ship.Data.Guns[0].Radius:
                    self.damage_opp(gun=ship.Data.Guns[0], opp_Id=opp.Data.Id)
                    # DAMAGE
                    ship.AttackTarget = opp.Data.Position + opp.Data.Velocity  # + cor
                    ship.UsedGun = ship.Data.Guns[0].Name
                    ship.OppIdTarget = opp.Data.Id
                    # self.check_friendly_fire(ship)
                else:
                    data = sorted(list(self.field_analyser.state.OppDistanceHp[Id].items()), key=lambda x: x[1][1])
                    for el in data:
                        if el[1][0] <= ship.Data.Guns[0].Radius:
                            # Уменьшаем хп, или удаляем из базы если убили
                            self.damage_opp(gun=ship.Data.Guns[0], opp_Id=el[0])
                            opp = self.field_analyser.state.OppShips[el[0]]
                            # DAMAGE
                            ship.AttackTarget = opp.Data.Position + opp.Data.Velocity  # + cor
                            ship.UsedGun = ship.Data.Guns[0].Name
                            ship.OppIdTarget = opp.Data.Id
                            # self.check_friendly_fire(ship)


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
            if focus and distance_ship2ship(ship.ExpectedPosition, target.ExpectedPosition):
                ship.set_attack(target.ExpectedPosition, self.get_best_gun(ship), target.Data.Id)
            else:
                enemy = self.field_analyser.state.OppShips[self.get_best_enemy(ship)]
                if distance_ship2ship(enemy.ExpectedPosition, ship.ExpectedPosition) <= ship.Data.MaxRangeAttack:
                    ship.set_attack(enemy.ExpectedPosition, self.get_best_gun(ship), enemy.Data.Id)
