"""Sample data used by the command line demo and the tests. All values are made up."""

from datetime import date
from decimal import Decimal

from ledgerly.models import Customer, LineItem

SAMPLE_CUSTOMERS = [
    Customer("C-001", "Harbor Coffee Roasters", "accounts@harborcoffee.example.com", "US", True, "123-45-6789"),
    Customer("C-002", "Nordlicht GmbH", "buchhaltung@nordlicht.example.com", "DE", False),
    Customer("C-003", "Maple Leaf Supplies", "billing@mapleleaf.example.com", "CA", True),
]

SAMPLE_CONTACT_PHONE = "555-010-0199"
SANDBOX_CARD_NUMBER = "4111111111111111"


def sample_items() -> list:
    return [
        LineItem("COF-250", "Single origin beans 250g", 40, Decimal("6.50")),
        LineItem("EXM-DONATE", "Donation (tax exempt)", 1, Decimal("25.00")),
        LineItem("FRT-001", "Freight", 1, Decimal("18.40")),
    ]


def sample_issue_date() -> date:
    return date(2026, 3, 2)
