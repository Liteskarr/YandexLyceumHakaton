import json
import traceback

from attack import Attack
from battle_output import BattleOutput
from battle_state import BattleState
from controller import Controller
from draft import DraftChoice
from field_analyser import FieldAnalyser
from moving_tactics.base import BaseMovingTactics


StarStorms = [{
    "Position": None,
    "CompleteShipId": "starstorm"
} for _ in range(5)]


def make_draft(data: dict) -> dict:
    return {'Ships': StarStorms}


def make_turn(data: dict, controller: Controller) -> BattleOutput:
    battle_state = BattleState.from_json(data)
    battle_output = BattleOutput()
    battle_output.Message = f"No output!"
    try:
        out = list(controller.update(battle_state.My, battle_state.Opponent))
        if out:
            battle_output.UserCommands = out
    except Exception as e:
        battle_output.Message = '\n'.join(traceback.format_tb(e.__traceback__))
        battle_output.Message += f'\n{e}'
    return battle_output


def play_game():
    field_analyser = FieldAnalyser()
    attacking_tactics = Attack(field_analyser)
    moving_tactics = BaseMovingTactics(field_analyser)
    controller = Controller(field_analyser, attacking_tactics, moving_tactics)
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), default=lambda x: x.to_json(), ensure_ascii=False))
        elif 'My' in line:
            print(json.dumps(make_turn(line, controller), default=lambda x: x.to_json(), ensure_ascii=False))


if __name__ == '__main__':
    play_game()
