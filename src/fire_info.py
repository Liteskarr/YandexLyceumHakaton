from dataclasses import dataclass

from json_capability import JSONCapability
from utils.vector import Vector
from equipment.weapon_effect import WeaponEffect


@dataclass
class FireInfo(JSONCapability):
    EffectType: WeaponEffect
    Source: Vector
    Target: Vector

    @classmethod
    def from_json(cls, data):
        data['Source'] = Vector.from_json(data['Source'])
        data['Target'] = Vector.from_json(data['Target'])
        return cls(**data)
