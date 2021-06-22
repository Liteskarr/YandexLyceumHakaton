def sign(x: int) -> int:
    if not x:
        return x
    return x // abs(x)


def activate(value: float,
             peak: float,
             left: float = 0,
             right: float = 1) -> float:
    if value <= left or value >= right:
        return 0
    if value == peak:
        return 1.0
    elif peak > value:
        return value / (peak - left)
    elif peak < value:
        return value / (right - peak)
