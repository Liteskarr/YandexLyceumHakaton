from utils.vector import Vector
from utils.bresenham import server_bresenham, bresenham


SHIP_CORR = [Vector(0, 0, 0), Vector(1, 0, 0), Vector(0, 0, 1), Vector(1, 0, 1),
             Vector(0, 1, 0), Vector(1, 1, 0), Vector(0, 1, 1), Vector(1, 1, 1)]


def point_in_bresenham(point: Vector, start: Vector, finish: Vector) -> bool:
    for p in server_bresenham(start, finish):
        if p == point:
            return True
    return False


def check_ships_proximity(pos_ship_1: Vector, pos_ship_2: Vector) -> bool:
    """
    True - Не пересекаются
    False - пересекаются
    """
    return (pos_ship_1 - pos_ship_2).c_len() >= 2


if __name__ == '__main__':
    print(list(server_bresenham(Vector(15, 14, 14), Vector(11, 23, 12))))
