from decimal import Decimal

import pytest

from ledgerly.pricing import apply_discount, member_price, tier_label, volume_discount_percent


def test_apply_discount():
    assert apply_discount(200, 10) == Decimal("180.00")


@pytest.mark.parametrize("percent,expected", [(150, "0.00"), (-20, "100.00"), (0, "100.00"), (100, "0.00")])
def test_discount_is_clamped(percent, expected):
    assert apply_discount(100, percent) == Decimal(expected)


def test_member_price():
    assert member_price(100, True) == Decimal("88.00")
    assert member_price("100", False) == Decimal("100.00")


@pytest.mark.parametrize("qty,expected", [(1, 0), (9, 0), (10, 5), (49, 5), (50, 10), (99, 10), (100, 15), (500, 15)])
def test_volume_discount(qty, expected):
    assert volume_discount_percent(qty) == expected


@pytest.mark.parametrize(
    "amount,member,label",
    [(120, True, "priority"), (120, False, "standard"), (100, False, "standard"), (99, True, "member"), (10, False, "walk-in")],
)
def test_tier_label(amount, member, label):
    assert tier_label(amount, member) == label
