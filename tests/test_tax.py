from decimal import Decimal

from ledgerly.models import LineItem
from ledgerly.tax import DEFAULT_RATE, rate_for, tax_for_item, tax_for_items


def test_known_region_rates():
    assert rate_for("de") == Decimal("19")
    assert rate_for("US") == Decimal("7")


def test_exempt_items_pay_no_tax():
    item = LineItem("EXM-1", "Donation", 1, Decimal("100"))
    assert tax_for_item(item, "US") == Decimal("0.00")


def test_tax_for_items_sums_each_line(items):
    assert tax_for_items(items, "US") == Decimal("1.76")


def test_unknown_region_uses_default_rate():
    assert rate_for("ZZ") == DEFAULT_RATE
    item = LineItem("A", "a", 1, Decimal("50"))
    assert tax_for_item(item, "ZZ") == Decimal("5.00")
