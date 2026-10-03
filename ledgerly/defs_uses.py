"""Definitions and uses for py-all-defs-uses.

``dropped`` is assigned and never read, so one definition has no users.
"""


def scale(value: int) -> int:
    return value


def net(points: int, bonus: int) -> int:
    total = points + bonus
    dropped = points - bonus
    return total
