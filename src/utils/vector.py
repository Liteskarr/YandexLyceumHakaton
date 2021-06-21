from dataclasses import dataclass

from json_capability import JSONCapability


@dataclass
class Vector(JSONCapability):
    X: int
    Y: int
    Z: int

    @classmethod
    def from_json(cls, data):
        x, y, z = map(int, data.split('/'))
        return cls(x, y, z)

    def __mul__(self, k: int):
        return Vector(self.X * k, self.Y * k, self.Z * k)

    def __floordiv__(self, k: int):
        return Vector(self.X // k, self.Y // k, self.Z // k)

    def __neg__(self):
        return Vector(-self.X, -self.Y, -self.Z)

    def __add__(self, other: "Vector"):
        return Vector(*map(sum, zip(self, other)))

    def __sub__(self, other: "Vector"):
        return self + (-other)

    def __str__(self):
        return f"{self.X}/{self.Y}/{self.Z}"

    def __iter__(self):
        yield from [self.X, self.Y, self.Z]

    def __eq__(self, other: "Vector"):
        return self.X == other.X and self.Y == other.Y and self.Z == other.Z

    def __ne__(self, other: "Vector"):
        return not (self == other)

    def __abs__(self):
        return Vector(abs(self.X), abs(self.Y), abs(self.Z))

    def __hash__(self):
        return hash((self.X, self.Y, self.Z))

    def c_len(self):
        return max(abs(self.X), abs(self.Y), abs(self.Z))

    def m_len(self):
        return abs(self.X) + abs(self.Y) + abs(self.Z)

    def to_json(self):
        return self.__str__()
