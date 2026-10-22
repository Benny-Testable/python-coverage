import pytest

from ledgerly.customers import CustomerRegistry, DuplicateCustomer
from ledgerly.models import Customer


def test_add_and_get(customer):
    registry = CustomerRegistry()
    registry.add(customer)
    assert registry.get("C-100") is customer
    assert len(registry) == 1


def test_duplicate_id_rejected(customer):
    registry = CustomerRegistry()
    registry.add(customer)
    with pytest.raises(DuplicateCustomer):
        registry.add(customer)


def test_invalid_email_rejected():
    registry = CustomerRegistry()
    with pytest.raises(ValueError):
        registry.add(Customer("C-9", "Bad", "not-an-email"))


def test_find_by_email_ignores_case(customer):
    registry = CustomerRegistry()
    registry.add(customer)
    assert registry.find_by_email("  TEST.customer@example.com ") is customer
    assert registry.find_by_email("nobody@example.com") is None


def test_by_region(customer, member):
    registry = CustomerRegistry()
    registry.add(customer)
    registry.add(member)
    grouped = registry.by_region()
    assert sorted(grouped) == ["DE", "US"]
    assert grouped["US"] == [customer]


def test_open_invoice(customer, items, issued):
    registry = CustomerRegistry()
    registry.add(customer)
    invoice = registry.open_invoice("C-100", items, issued)
    assert invoice.status == "open"
    assert invoice.customer_id == "C-100"
