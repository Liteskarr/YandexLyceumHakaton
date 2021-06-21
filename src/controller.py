from typing import List, Iterator

from attack import Attack
from field_analyser import FieldAnalyser
from moving_tactics import IMovingTactics
from ship import ShipData
from user_command import UserCommand


class Controller:
    def __init__(self, field_analyser: FieldAnalyser, attack_tactics: Attack, moving_tactics: IMovingTactics):
        self.field_analyser = field_analyser
        self.attacking_tactics = attack_tactics
        self.moving_tactics = moving_tactics

    def update(self, my: List[ShipData], opponents: List[ShipData]) -> Iterator[UserCommand]:
        self.field_analyser.create_new_state()
        self.field_analyser.update_ships(my, opponents)
        self.moving_tactics.update()
        self.attacking_tactics.update()
        for ship in self.field_analyser.state.MyShips.values():
            yield from ship.update()
