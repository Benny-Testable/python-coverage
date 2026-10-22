from datetime import date
from decimal import Decimal

import pytest

from ledgerly.customers import CustomerRegistry
from ledgerly.invoices import (
    apply_payment,
    balance_due,
    build_invoice,
    due_date,
    invoice_number,
    invoice_totals,
    issue_for,
)
from ledgerly.models import LineItem, Payment


def test_invoice_number_is_zero_padded():
    assert invoice_number("INV", 42) == "INV-00042"


def test_due_date_terms(issued):
    assert due_date(issued, "net15") < due_date(issued)
    assert due_date(issued) < due_date(issued, "net60")


def test_build_invoice_requires_items(customer, issued):
    with pytest.raises(ValueError):
        build_invoice(customer, [], issued)


def test_build_invoice_sets_fields(customer, items, issued):
    invoice = build_invoice(customer, items, issued, "net15", sequence=7)
    assert invoice.number == "INV-00007"
    assert invoice.customer_id == "C-100"
    assert invoice.due > issued
    assert invoice.status == "draft"


def test_totals_for_regular_customer(customer, items, issued):
    totals = invoice_totals(build_invoice(customer, items, issued), customer)
    assert totals == {
        "subtotal": Decimal("25.20"),
        "discount": Decimal("0.00"),
        "tax": Decimal("1.76"),
        "total": Decimal("26.96"),
    }


def test_totals_for_member_with_volume(member, issued):
    bulk = [LineItem("B-1", "Bulk", 60, Decimal("2.00"))]
    totals = invoice_totals(build_invoice(member, bulk, issued), member)
    assert totals["subtotal"] == Decimal("120.00")
    assert totals["discount"] == Decimal("24.96")
    assert totals["tax"] == Decimal("22.80")
    assert totals["total"] == Decimal("117.84")


def test_payment_flow(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    apply_payment(invoice, customer, Payment("P1", Decimal("10.00"), issued))
    assert invoice.status == "partial"
    assert balance_due(invoice, customer) == Decimal("16.96")
    apply_payment(invoice, customer, Payment("P2", Decimal("16.96"), issued))
    assert invoice.status == "paid"


def test_payment_must_be_positive(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    with pytest.raises(ValueError):
        apply_payment(invoice, customer, Payment("P0", Decimal("0"), issued))


def test_issue_for_registry(customer, items, issued):
    registry = CustomerRegistry()
    registry.add(customer)
    invoice = issue_for(registry, "C-100", items, issued, terms="net60")
    assert invoice.status == "open"
    assert invoice.due > issued
