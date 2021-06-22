from dataclasses import dataclass
from typing import List

from fire_info import FireInfo
from json_capability import JSONCapability
from ship import ShipData


@dataclass
class BattleState(JSONCapability):
    FireInfos: List[FireInfo]
    My: List[ShipData]
    Opponent: List[ShipData]

    @classmethod
    def from_json(cls, data):
        my = list(map(ShipData.from_json, data['My']))
        opponent = list(map(ShipData.from_json, data['Opponent']))
        try:
            fire_infos = list(map(FireInfo.from_json, data['FireInfos']))
        except Exception as e:
            fire_infos = []
        return cls(fire_infos, my, opponent)
