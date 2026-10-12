"""Sales tax and VAT by customer region."""

from decimal import Decimal

from ledgerly.money import add, percent_of

REGION_RATES = {
    "US": Decimal("7"),
    "CA": Decimal("5"),
    "DE": Decimal("19"),
    "FR": Decimal("20"),
    "GB": Decimal("20"),
}
EXEMPT_PREFIX = "EXM-"


def rate_for(region: str) -> Decimal:
    """Tax percentage for a region code."""
    return REGION_RATES[region.upper()]


def tax_for_item(item, region: str) -> Decimal:
    if item.sku.startswith(EXEMPT_PREFIX):
        return Decimal("0.00")
    return percent_of(item.total(), rate_for(region))


def tax_for_items(items, region: str) -> Decimal:
    return add(*[tax_for_item(item, region) for item in items])
