from dataclasses import dataclass

from json_capability import JSONCapability


StarStorms = [{
    "Position": "0/0/0",
    "CompleteShipId": "starstorm"
} for _ in range(5)]


@dataclass
class DraftChoice(JSONCapability):
    Ships: StarStorms


@dataclass
class DraftOptions:
    # TODO: Parse draft options
    pass
