def sign(x: int) -> int:
    if not x:
        return x
    return x // abs(x)
