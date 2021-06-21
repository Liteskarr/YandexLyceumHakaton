from dataclasses import dataclass

from parameters import CommandParameters
from utils.vector import Vector


@dataclass
class AccelerateCommandParameters(CommandParameters):
    Id: int
    Vector: Vector
