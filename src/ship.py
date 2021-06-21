from dataclasses import dataclass
from itertools import takewhile
from typing import List, Optional, Iterator

from blocks import EquipmentBlock, EngineBlock, GunBlock
from json_capability import JSONCapability
from parameters.accelerate import AccelerateCommandParameters
from parameters.attack import AttackCommandParameters
from parameters.move import MoveCommandParameters
from user_command import UserCommand
from utils.bresenham import server_bresenham
from utils.vector import Vector


@dataclass
class ShipData(JSONCapability):
    Id: int
    Position: Vector
    Velocity: Vector
    Energy: Optional[int] = None
    Health: Optional[int] = None
    Equipment: List[EquipmentBlock] = None
    MaxRangeAttack: Optional[int] = None
    MaxAccelerate: Optional[int] = None
    Guns: List[GunBlock] = None

    @classmethod
    def from_json(cls, data: dict):
        if data.get('Equipment'):
            data['Equipment'] = list(map(EquipmentBlock.from_json, data.get('Equipment', [])))
            data['Guns'] = [x for x in data['Equipment'] if isinstance(x, GunBlock)]
            data['MaxAccelerate'] = [x for x in data['Equipment'] if isinstance(x, EngineBlock)][0].MaxAccelerate
            data['MaxRangeAttack'] = max([gun.Radius for gun in data['Guns']])
        data['Position'] = Vector.from_json(data['Position'])
        data['Velocity'] = Vector.from_json(data['Velocity'])
        return cls(**data)


@dataclass
class Ship(JSONCapability):
    # Data
    Data: ShipData = None

    # Attacking
    AttackTarget: Optional[Vector] = None
    OppIdTarget: Optional[int] = None
    UsedGun: Optional[str] = None
    FriendlyFire: bool = False
    Adjustment = {
        Vector(0, 0, 0): 5, Vector(1, 0, 0): 1, Vector(0, 0, 1): 1, Vector(1, 0, 1): 4,
        Vector(0, 1, 0): 3, Vector(1, 1, 0): 1, Vector(0, 1, 1): 1, Vector(1, 1, 1): 3
    }

    # Moving
    Way: Optional[Iterator[Vector]] = None
    MoveTarget: Optional[Vector] = None
    DeltaVelocity: Optional[Vector] = None
    ExpectedVelocity: Optional[Vector] = None
    ExpectedPosition: Optional[Vector] = None

    def update_data(self, data: ShipData):
        self.Data = data
        self.DeltaVelocity = Vector(0, 0, 0)
        self.ExpectedVelocity = self.Data.Velocity
        self.ExpectedPosition = self.Data.Position + self.ExpectedVelocity

    def make_accelerate(self, vector: Vector) -> UserCommand:
        self.Data.Velocity += vector
        return UserCommand(Command="ACCELERATE", Parameters=AccelerateCommandParameters(self.Data.Id, vector))

    def make_attack(self, target: Vector, gun: str) -> UserCommand:
        return UserCommand(Command="ATTACK", Parameters=AttackCommandParameters(self.Data.Id, gun, target))

    def make_move(self, target: Vector) -> UserCommand:
        return UserCommand(Command="MOVE", Parameters=MoveCommandParameters(self.Data.Id, target))

    def set_way(self, way: Iterator[Vector]):
        self.Way = way
        self.MoveTarget = None

    def set_move_target(self, target: Vector):
        self.Way = None
        self.MoveTarget = target

    def update(self) -> Iterator[UserCommand]:
        if self.Way is not None:
            try:
                self.DeltaVelocity = next(self.Way)
                yield self.make_accelerate(self.DeltaVelocity)
            except StopIteration:
                self.Way = None
        elif self.MoveTarget is not None:
            if self.Data.Position == self.MoveTarget:
                self.MoveTarget = None
                self.DeltaVelocity = Vector(0, 0, 0)
            else:
                yield self.make_move(self.MoveTarget)
                try:
                    self.DeltaVelocity = \
                    list(takewhile(lambda x: (x - self.Data.Position - self.Data.Velocity).c_len() <= 1,
                                   server_bresenham(self.Data.Position,
                                                    self.MoveTarget)))[-1] - self.Data.Position
                    self.DeltaVelocity = self.DeltaVelocity - self.Data.Velocity
                except IndexError:
                    self.DeltaVelocity = Vector(0, 0, 0)
        self.ExpectedVelocity += self.DeltaVelocity
        self.ExpectedPosition += self.ExpectedVelocity
        if self.AttackTarget is not None and self.UsedGun is not None and not self.FriendlyFire:
            yield self.make_attack(self.AttackTarget, self.UsedGun)
