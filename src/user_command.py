from dataclasses import dataclass

from parameters import CommandParameters
from json_capability import JSONCapability


@dataclass
class UserCommand(JSONCapability):
    Command: str
    Parameters: CommandParameters
