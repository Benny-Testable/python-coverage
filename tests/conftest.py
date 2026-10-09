from datetime import date
from decimal import Decimal

import pytest

from ledgerly.models import Customer, LineItem


@pytest.fixture
def customer():
    return Customer("C-100", "Test Customer", "test.customer@example.com", "US", False)


@pytest.fixture
def member():
    return Customer("C-101", "Member Customer", "member@example.com", "DE", True)


@pytest.fixture
def items():
    return [
        LineItem("SKU-1", "Widget", 2, Decimal("10.00")),
        LineItem("SKU-2", "Gadget", 1, Decimal("5.20")),
    ]


@pytest.fixture
def issued():
    return date(2026, 1, 10)
