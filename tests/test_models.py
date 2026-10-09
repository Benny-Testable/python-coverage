from datetime import date
from decimal import Decimal

from ledgerly.models import Invoice, LineItem, Payment


def test_line_item_total():
    assert LineItem("A", "a", 3, Decimal("1.10")).total() == Decimal("3.30")


def test_invoice_subtotal_and_payments(items):
    invoice = Invoice("INV-1", "C-1", date(2026, 1, 1), date(2026, 1, 31), items=items)
    assert invoice.subtotal() == Decimal("25.20")
    invoice.payments.append(Payment("P1", Decimal("10.00"), date(2026, 1, 5)))
    invoice.payments.append(Payment("P2", Decimal("2.50"), date(2026, 1, 6)))
    assert invoice.paid_amount() == Decimal("12.50")


def test_days_overdue_never_negative():
    invoice = Invoice("INV-1", "C-1", date(2026, 1, 1), date(2026, 1, 31))
    assert invoice.days_overdue(date(2026, 1, 20)) == 0
    assert invoice.days_overdue(date(2026, 2, 10)) == 10
