from dataclasses import dataclass

from parameters import CommandParameters
from utils.vector import Vector


@dataclass
class MoveCommandParameters(CommandParameters):
    Id: int
    Target: Vector
