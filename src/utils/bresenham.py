from typing import Iterator

from utils.vector import Vector


def bresenham(v1: Vector, v2: Vector) -> Iterator[Vector]:
    yield v1

    x1, y1, z1 = v1
    x2, y2, z2 = v2
    dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)

    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1

    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != x2:
            x1 += xs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            yield Vector(x1, y1, z1)
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            y1 += ys
            if p1 >= 0:
                x1 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            yield Vector(x1, y1, z1)
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            z1 += zs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            yield Vector(x1, y1, z1)


def server_bresenham(v1: Vector, v2: Vector, map_size: int = 30) -> Iterator[Vector]:
    x0, y0, z0 = v1
    x1, y1, z1 = v2
    dx, sx = abs(x1 - x0), 1 if x0 < x1 else -1
    dy, sy = abs(y1 - y0), 1 if y0 < y1 else -1
    dz, sz = abs(z1 - z0), 1 if z0 < z1 else -1
    dm = max(1, max(dx, dy, dz))
    i = dm
    x1 = y1 = z1 = dm / 2
    while True:
        if map_size != 1:
            if x0 < 0 or x0 >= map_size:
                break
            if y1 < 0 or y0 >= map_size:
                break
            if z0 < 0 or z0 >= map_size:
                break
        yield Vector(x0, y0, z0)
        if Vector(x0, y0, z0) == v2:
            break
        if i == 0 and map_size == -1:
            break
        i -= 1
        x1 -= dx
        if x1 < 0:
            x1 += dm
            x0 += sx
        y1 -= dy
        if y1 < 0:
            y1 += dm
            y0 += sy
        z1 -= dz
        if z1 < 0:
            z1 += dm
            z0 += sz
