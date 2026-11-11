from datetime import date
from decimal import Decimal

from ledgerly.models import Payment
from ledgerly.repository import JsonStore, customer_summary, invoice_from_dict, invoice_to_dict
from ledgerly.invoices import build_invoice


def make_invoice(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    invoice.payments.append(Payment("P1", Decimal("3.00"), date(2026, 1, 12)))
    return invoice


def test_round_trip_dict(customer, items, issued):
    invoice = make_invoice(customer, items, issued)
    again = invoice_from_dict(invoice_to_dict(invoice))
    assert again == invoice


def test_store_saves_and_loads(tmp_path, customer, items, issued):
    store = JsonStore(tmp_path / "invoices.json")
    assert store.load_invoices() == []
    assert store.save_invoices([make_invoice(customer, items, issued)]) == 1
    loaded = store.load_invoices()
    assert loaded[0].number == "INV-00001"
    assert loaded[0].payments[0].amount == Decimal("3.00")


def test_store_creates_missing_directories(tmp_path, customer, items, issued):
    store = JsonStore(tmp_path / "nested" / "deeper" / "invoices.json")
    store.save_invoices([make_invoice(customer, items, issued)])
    assert store.path.exists()


def test_customer_names_and_summary(tmp_path, customer, member):
    store = JsonStore(tmp_path / "out" / "names.json")
    store.save_customer_names([customer, member])
    assert '"C-100": "Test Customer"' in store.path.read_text(encoding="utf-8")
    assert customer_summary(customer) == "C-100: Test Customer (US)"
