from collections import defaultdict
from enum import Enum
from itertools import zip_longest
from typing import Iterator, Dict, List, DefaultDict

from utils.math import sign
from utils.vector import Vector


class MovingStrategy(Enum):
    ACCURATE = Vector(0, 0, 0)
    ONE = Vector(1, 1, 1)
    FAST = Vector(8, 8, 8)


AXIS_SIZE = 30

MOVING_PATTERNS: DefaultDict[int, DefaultDict[int, List[int]]] = defaultdict(lambda: defaultdict(list))


def precalculate_moving_patterns(engine_acceleration: int):
    global MOVING_PATTERNS
    MOVING_PATTERNS = defaultdict(lambda: defaultdict(list))
    MOVING_PATTERNS[engine_acceleration][1] = [1, -1]
    for size in range(2, AXIS_SIZE + 1):
        trace = 0
        velocity = 0
        while trace != size or velocity > 0:
            if (size - trace) >= (velocity + engine_acceleration) * (velocity + 2 * engine_acceleration) // 2:
                velocity += 1
                MOVING_PATTERNS[engine_acceleration][size].append(engine_acceleration)
            else:
                if (size - trace) >= velocity * (velocity + engine_acceleration) // 2:
                    MOVING_PATTERNS[engine_acceleration][size].append(0)
                else:
                    MOVING_PATTERNS[engine_acceleration][size].append(-engine_acceleration)
                    velocity -= 1
            trace += velocity


def change_axis_velocity(current_velocity: int,
                         target_velocity: int,
                         engine_acceleration: int = 1) -> Iterator[int]:
    """
    Изменяет текущий вектор скорости на целевой.
    :param current_velocity: Текущий вектор скорости.
    :param target_velocity: Целевой вектор скорости.
    :param engine_acceleration: Максимальное изменение ускорения.
    :return: Возвращает итератор на изменение вектора скорости до тех пор,
    пока текущая скорость не станет равна целевой.
    """
    if engine_acceleration == 1:
        while current_velocity != target_velocity:
            delta_velocity = sign(target_velocity - current_velocity)
            current_velocity += delta_velocity
            yield delta_velocity
    else:
        # TODO: Напиши реализацию для произвольного ускорения.
        raise NotImplementedError()


def change_velocity(current_velocity: Vector,
                    target_velocity: Vector,
                    engine_acceleration: int = 1) -> Iterator[Vector]:
    """
    Изменяет текущий вектор скорости на целевой.
    :param current_velocity: Текущий вектор скорости.
    :param target_velocity: Целевой вектор скорости.
    :param engine_acceleration: Максимальное изменение вектора скорости.
    :return: Возвращает итератор на изменение вектора скорости до тех пор,
    пока текущая скорость не станет равна целевой.
    """
    yield from map(lambda x: Vector(*x), zip_longest(change_axis_velocity(current_velocity.X,
                                                                          target_velocity.X,
                                                                          engine_acceleration),
                                                     change_axis_velocity(current_velocity.Y,
                                                                          target_velocity.Y,
                                                                          engine_acceleration),
                                                     change_axis_velocity(current_velocity.Z,
                                                                          target_velocity.Z,
                                                                          engine_acceleration),
                                                     fillvalue=0))


def get_axis_brake_trace_len(current_velocity: int, engine_acceleration: int = 1) -> int:
    return (current_velocity + engine_acceleration - 1) // engine_acceleration


def get_brake_trace_len(current_velocity: Vector, engine_acceleration: int = 1) -> int:
    return (current_velocity.c_len() + engine_acceleration - 1) // engine_acceleration


def axis_moving(start: int,
                finish: int,
                engine_acceleration: int = 1) -> Iterator[int]:
    global MOVING_PATTERNS
    if engine_acceleration != 1:
        # TODO: напиши это.
        raise NotImplementedError()
    if finish > start:
        yield from MOVING_PATTERNS[engine_acceleration][abs(finish - start)]
    else:
        yield from map(lambda x: -x, MOVING_PATTERNS[engine_acceleration][abs(finish - start)])


def moving(start: Vector, finish: Vector, engine_acceleration) -> Iterator[Vector]:
    yield from map(lambda x: Vector(*x), zip_longest(axis_moving(start.X, finish.X, engine_acceleration),
                                                     axis_moving(start.Y, finish.Y, engine_acceleration),
                                                     axis_moving(start.Z, finish.Z, engine_acceleration),
                                                     fillvalue=0))


precalculate_moving_patterns(1)
