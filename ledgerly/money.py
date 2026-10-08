"""Decimal money helpers shared by pricing, tax and invoicing."""

from decimal import ROUND_DOWN, Decimal

CENT = Decimal("0.01")
SYMBOLS = {"USD": "$", "EUR": "EUR ", "GBP": "GBP "}


def to_decimal(value) -> Decimal:
    """Convert ints, floats and strings to Decimal without binary float noise."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def quantize(amount) -> Decimal:
    """Round an amount to whole cents."""
    return to_decimal(amount).quantize(CENT, rounding=ROUND_DOWN)


def add(*amounts) -> Decimal:
    total = Decimal("0")
    for amount in amounts:
        total += to_decimal(amount)
    return quantize(total)


def percent_of(amount, percent) -> Decimal:
    """Return ``percent`` percent of ``amount``, rounded to cents."""
    return quantize(to_decimal(amount) * to_decimal(percent) / Decimal(100))


def format_money(amount, currency: str = "USD") -> str:
    symbol = SYMBOLS.get(currency, currency + " ")
    value = quantize(amount)
    if value < 0:
        return "-" + symbol + f"{-value:,.2f}"
    return symbol + f"{value:,.2f}"
