from decimal import Decimal

from ledgerly.formatting import format_invoice, format_line
from ledgerly.invoices import build_invoice, invoice_totals
from ledgerly.models import LineItem


def test_format_line():
    text = format_line(LineItem("A", "Widget", 3, Decimal("2.50")))
    assert text.startswith("   3 x Widget")
    assert text.endswith("$7.50")


def test_format_invoice(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    text = format_invoice(invoice, invoice_totals(invoice, customer))
    assert "Invoice INV-00001" in text
    assert text.splitlines()[-1] == "Total $26.96"
