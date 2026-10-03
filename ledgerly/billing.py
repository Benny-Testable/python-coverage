"""Small billed-price helpers. Tests cover one path so coverage is partial."""

DISCOUNT = 0.12


def price(amount: float) -> float:
    return round(amount * (1 - DISCOUNT), 2)


def tier_label(amount: float, member: bool) -> str:
    if amount >= 100 and member:
        return "priority"
    if amount >= 100:
        return "standard"
    if member:
        return "member"
    return "walk-in"
