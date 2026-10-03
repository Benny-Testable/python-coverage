"""Compound conditions for pymcdc (modified condition/decision coverage)."""


def eligible(age: int, member: bool, active: bool) -> bool:
    if age >= 18 and member and active:
        return True
    return False


def shipping(weight: float, express: bool, fragile: bool) -> str:
    if weight > 20 or (express and fragile):
        return "special"
    return "ground"
