"""Running balance helpers."""


def scale(value: int, factor: int = 1) -> int:
    return value * factor


def net_balance(credits: int, debits: int) -> int:
    total = credits - debits
    carried = credits + debits
    return total
