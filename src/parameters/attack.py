from dataclasses import dataclass

from parameters import CommandParameters
from utils.vector import Vector


@dataclass
class AttackCommandParameters(CommandParameters):
    Id: int
    Name: str
    Target: Vector
