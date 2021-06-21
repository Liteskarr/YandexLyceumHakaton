from typing import Tuple

from utils.geometry import SHIP_CORR
from utils.vector import Vector


def distance_c_len(my_pos: Vector, opp_pos: Vector) -> int:
    return min([abs((my_pos + my_c) - (opp_pos + opp_c)).c_len() for my_c in SHIP_CORR for opp_c in SHIP_CORR])


def distance_opp_c_len(point: Vector, opp_pos: Vector):
    return min([abs(point - (opp_pos + c)).c_len() for c in SHIP_CORR])


def offset_points_m_len(my_pos: Vector, opp_pos: Vector) -> Tuple[Vector, Vector]:
    return sorted(
        [
            (abs((my_pos + my_c) - (opp_pos + opp_c)).m_len(), (my_c, opp_c))
            for my_c in SHIP_CORR for opp_c in SHIP_CORR
        ], key=lambda x: x[0])[0][1]


if __name__ == '__main__':
    print(offset_points_m_len(Vector(19, 11, 11), Vector(15, 14, 14)))
