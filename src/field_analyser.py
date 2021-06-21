from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, DefaultDict, Optional, List

from ship import Ship, ShipData
from utils.distance import distance_c_len


@dataclass
class FieldState:
    MyShips: Dict[int, Ship] = field(default_factory=dict)
    OppShips: Dict[int, Ship] = field(default_factory=dict)
    DistanceHp: DefaultDict[int, DefaultDict[int, List[int]]] = \
        field(default_factory=lambda: defaultdict(lambda: defaultdict(list)))
    OppIsDamage: DefaultDict[int, int] = field(default_factory=lambda: defaultdict(int))
    GlobalTarget: Optional[int] = None


class FieldAnalyser:
    def __init__(self):
        self.state: Optional[FieldState] = FieldState()
        self.prev_state: Optional[FieldState] = None

    def update_ships(self, my: List[ShipData], opponents: List[ShipData]):
        self.state.OppIsDamage.clear()
        self.state.DistanceHp.clear()

        for Id in list(self.state.MyShips.keys()):
            if sum([Id == ship.Id for ship in my]) == 0:
                self.state.MyShips.pop(Id)

        for Id in list(self.state.OppShips.keys()):
            if sum([Id == ship.Id for ship in opponents]) == 0:
                self.state.OppShips.pop(Id)

        for ship in my:
            if ship.Id not in self.state.MyShips:
                self.state.MyShips[ship.Id] = Ship()
            self.state.MyShips[ship.Id].update_data(ship)

        for ship in opponents:
            if ship.Id not in self.state.OppShips:
                self.state.OppShips[ship.Id] = Ship()
            self.state.OppShips[ship.Id].update_data(ship)

        for my_ship in my:
            self.state.MyShips[my_ship.Id].Data = my_ship
            for opp_ship in opponents:
                self.state.OppShips[opp_ship.Id].Data = opp_ship
                # Дистанция и хп
                distance = distance_c_len(my_ship.Position + my_ship.Velocity, opp_ship.Position) - 1
                self.state.DistanceHp[my_ship.Id][opp_ship.Id] = [distance, opp_ship.Health]
                # Предполагаемый урон
                if my_ship.Guns and distance <= my_ship.Guns[0].Radius:
                    self.state.OppIsDamage[opp_ship.Id] += my_ship.Guns[0].Damage

    def create_new_state(self):
        self.prev_state = self.state
