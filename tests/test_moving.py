import pytest
from pprint import pprint

from src.moving import precalculate_moving_patterns, moving, MOVING_PATTERNS, AXIS_SIZE
from utils.vector import Vector


def test_moving_patterns():
    for acceleration in MOVING_PATTERNS:
        for size in range(AXIS_SIZE):
            velocity = 0
            trace = 0
            for t in MOVING_PATTERNS[acceleration][size]:
                trace += velocity
                velocity += t
            assert trace == size and velocity == 0


def test_moving():
    selection = [
        (Vector(0, 0, 0), Vector(0, 0, 1)),
        (Vector(0, 0, 0), Vector(30, 30, 30)),
        (Vector(30, 30, 30), Vector(0, 0, 0)),
        (Vector(17, 6, 5), Vector(9, 6, 11)),
        (Vector(0, 0, 0), Vector(14, 14, 14))
    ]
    for start, finish in selection:
        for starting_velocity in range(1, 4):
            velocity = Vector(0, 0, 0)
            pos = Vector(*start)
            for delta_velocity in moving(start, finish, engine_acceleration=1):
                pos += velocity
                velocity += delta_velocity
            assert pos == finish and velocity == Vector(0, 0, 0)


if __name__ == '__main__':
    precalculate_moving_patterns(1)
    pprint(MOVING_PATTERNS)
    pytest.main()
