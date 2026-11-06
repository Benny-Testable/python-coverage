import logging
from datetime import date

from ledgerly.invoices import build_invoice
from ledgerly.notifications import deliver_all, log_contact, render_reminder


def test_reminder_text(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    text = render_reminder(customer, invoice, "$26.96", date(2026, 2, 20))
    assert "Hello Test Customer" in text
    assert "invoice INV-00001 for $26.96 was due on 2026-02-09" in text
    assert "earliest convenience" in text


def test_reminder_escalates_after_thirty_days(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    assert "past 30 days" in render_reminder(customer, invoice, "$1", date(2026, 4, 1))


def test_log_contact_writes_records(customer, items, issued, caplog):
    invoice = build_invoice(customer, items, issued)
    with caplog.at_level(logging.INFO):
        log_contact(customer, invoice)
    assert len(caplog.records) == 2


def test_deliver_all_runs_each_message():
    sent = []
    assert deliver_all(["a", "b", "c"], sent.append) == 3
    assert sorted(sent) == ["a", "b", "c"]
