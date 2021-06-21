from dataclasses import dataclass

from json_capability import JSONCapability
from equipment.type import EquipmentType
from equipment.weapon_effect import WeaponEffect


@dataclass
class EquipmentBlock(JSONCapability):
    Name: str
    Type: EquipmentType

    @classmethod
    def from_json(cls, data):
        if EquipmentType(data['Type']) == EquipmentType.Energy:
            return EnergyBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Gun:
            return GunBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Engine:
            return EngineBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Health:
            return HealthBlock(**data)


@dataclass
class EnergyBlock(EquipmentBlock):
    IncrementPerTurn: int
    MaxEnergy: int
    StartEnergy: int
    Type = EquipmentType.Energy


@dataclass
class EngineBlock(EquipmentBlock):
    MaxAccelerate: int
    Type = EquipmentType.Engine


@dataclass
class GunBlock(EquipmentBlock):
    Damage: int
    EffectType: WeaponEffect
    EnergyPrice: int
    Radius: int
    Type = EquipmentType.Gun


@dataclass
class HealthBlock(EquipmentBlock):
    MaxHealth: int
    StartHealth: int
    Type = EquipmentType.Health
