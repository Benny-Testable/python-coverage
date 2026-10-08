from decimal import Decimal

import pytest

from ledgerly.money import add, format_money, percent_of, quantize, to_decimal


def test_to_decimal_variants():
    assert to_decimal(3) == Decimal("3")
    assert to_decimal("1.5") == Decimal("1.5")
    assert to_decimal(0.1) == Decimal("0.1")
    value = Decimal("2")
    assert to_decimal(value) is value


def test_quantize_rounds_to_cents():
    assert quantize("1.234") == Decimal("1.23")
    assert quantize(5) == Decimal("5.00")


def test_add_sums_and_rounds():
    assert add("1.10", "2.20", 3) == Decimal("6.30")
    assert add() == Decimal("0.00")


def test_percent_of():
    assert percent_of(200, 12) == Decimal("24.00")
    assert percent_of("20.00", 7) == Decimal("1.40")


@pytest.mark.parametrize(
    "amount,currency,expected",
    [(1234.5, "USD", "$1,234.50"), (-5, "USD", "-$5.00"), (10, "EUR", "EUR 10.00"), (3, "CHF", "CHF 3.00")],
)
def test_format_money(amount, currency, expected):
    assert format_money(amount, currency) == expected

