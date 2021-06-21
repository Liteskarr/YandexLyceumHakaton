from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, DefaultDict, Optional, List

from ship import Ship, ShipData
from utils.distance import distance_ship2ship


@dataclass
class FieldState:
    MyShips: Dict[int, Ship] = field(default_factory=dict)
    OppShips: Dict[int, Ship] = field(default_factory=dict)
    OppDistanceHp: DefaultDict[int, DefaultDict[int, List[int]]] = \
        field(default_factory=lambda: defaultdict(lambda: defaultdict(list)))
    MaxOppDamageImpact: DefaultDict[int, int] = field(default_factory=lambda: defaultdict(int))
    GlobalTarget: Optional[int] = None


class FieldAnalyser:
    def __init__(self):
        self.state: Optional[FieldState] = FieldState()
        self.prev_state: Optional[FieldState] = None

    def update_ships(self, my: List[ShipData], opponents: List[ShipData]):
        self.state.MaxOppDamageImpact.clear()
        self.state.OppDistanceHp.clear()

        for ship_id in list(self.state.MyShips.keys()):
            if not any((ship_id == ship.Id for ship in my)):
                self.state.MyShips.pop(ship_id)

        for ship_id in list(self.state.OppShips.keys()):
            if not any((ship_id == ship.Id for ship in opponents)):
                self.state.OppShips.pop(ship_id)

        for ship in my:
            if ship.Id not in self.state.MyShips:
                self.state.MyShips[ship.Id] = Ship()
            self.state.MyShips[ship.Id].update_data(ship)

        for ship in opponents:
            if ship.Id not in self.state.OppShips:
                self.state.OppShips[ship.Id] = Ship()
            self.state.OppShips[ship.Id].update_data(ship)

        for my_ship in self.state.MyShips.values():
            for opp_ship in self.state.OppShips.values():
                # Дистанция и хп
                distance = distance_ship2ship(my_ship.ExpectedPosition, opp_ship.ExpectedPosition)
                self.state.OppDistanceHp[my_ship.Data.Id][opp_ship.Data.Id] = [distance, opp_ship.Data.Health]
                # Предполагаемый урон
                if my_ship.Data.Guns and distance <= my_ship.Data.Guns[0].Radius:
                    self.state.MaxOppDamageImpact[opp_ship.Data.Id] += my_ship.Data.Guns[0].Damage

    def create_new_state(self):
        self.prev_state = self.state
