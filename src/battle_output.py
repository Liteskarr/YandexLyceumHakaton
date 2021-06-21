from typing import List
from dataclasses import dataclass

from user_command import UserCommand
from json_capability import JSONCapability


@dataclass
class BattleOutput(JSONCapability):
    Message: str = None
    UserCommands: List[UserCommand] = None
