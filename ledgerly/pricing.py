"""Discounts and customer tiers."""

from decimal import Decimal

from ledgerly.money import percent_of, quantize, to_decimal

MEMBER_DISCOUNT_PERCENT = 12
VOLUME_STEPS = ((100, 15), (50, 10), (10, 5))


def apply_discount(amount, percent) -> Decimal:
    """Take ``percent`` off ``amount``; the percentage is limited to 0..100."""
    percent = min(max(to_decimal(percent), Decimal(0)), Decimal(100))
    return quantize(to_decimal(amount) - percent_of(amount, percent))


def member_price(amount, member: bool) -> Decimal:
    if member:
        return apply_discount(amount, MEMBER_DISCOUNT_PERCENT)
    return quantize(amount)


def volume_discount_percent(quantity: int) -> int:
    for threshold, percent in VOLUME_STEPS:
        if quantity >= threshold:
            return percent
    return 0


def tier_label(amount, member: bool) -> str:
    big = to_decimal(amount) >= 100
    if big and member:
        return "priority"
    if big:
        return "standard"
    if member:
        return "member"
    return "walk-in"
