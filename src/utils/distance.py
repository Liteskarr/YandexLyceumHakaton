from itertools import takewhile
from typing import Tuple, List

from ship import Ship
from utils.bresenham import server_bresenham
from utils.geometry import SHIP_CORR
from utils.vector import Vector


def distance_ship2ship(my_pos: Vector, opp_pos: Vector) -> int:
    return min([abs((my_pos + my_c) - (opp_pos + opp_c)).c_len() for my_c in SHIP_CORR for opp_c in SHIP_CORR])


def distance_point2ship(point: Vector, ship_pos: Vector):
    return min([abs(point - (ship_pos + c)).c_len() for c in SHIP_CORR])


def get_fire_offset(my_pos: Vector, ship_pos: Vector) -> Tuple[Vector, Vector]:
    return sorted(
        [
            (abs((my_pos + my_c) - (ship_pos + opp_c)).m_len(), (my_c, opp_c))
            for my_c in SHIP_CORR for opp_c in SHIP_CORR
        ], key=lambda x: x[0])[0][1]


def get_ships_2point(point_1: Vector, point_2: Vector, my_ships: List[Ship], opp_ships: List[Ship]) -> tuple:
    point_1, point_2 = min(point_1, point_2), max(point_1, point_2)
    my, opp = 0, 0
    for ship in my_ships:
        for cor in SHIP_CORR:
            if point_1 <= ship.Data.Position + cor <= point_2:
                my += 1
                break
    for ship in opp_ships:
        for cor in SHIP_CORR:
            if point_1 <= ship.Data.Position + cor <= point_2:
                opp += 1
                break
    return my, opp


def get_direction_vector(point: Vector, target: Vector) -> Vector:
    return list(takewhile(lambda x: (x - point).c_len() <= 1, server_bresenham(point, target)))[-1] - point


if __name__ == '__main__':
    print(get_fire_offset(Vector(19, 11, 11), Vector(15, 14, 14)))
