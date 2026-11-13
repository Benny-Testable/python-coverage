from datetime import date

import pytest

from ledgerly.invoices import build_invoice
from ledgerly.reports import aging_report, bucket_for, cross_check, pair_labels, region_bucket_matrix, summary_lines


@pytest.mark.parametrize(
    "days,label",
    [(-5, "current"), (0, "current"), (1, "0-30"), (30, "0-30"), (31, "31-60"), (60, "31-60"), (61, "61-90"), (90, "61-90"), (91, "90+")],
)
def test_bucket_edges(days, label):
    assert bucket_for(days) == label


def test_aging_report_skips_paid(customer, items, issued):
    paid = build_invoice(customer, items, issued, sequence=1)
    paid.status = "paid"
    late = build_invoice(customer, items, issued, sequence=2)
    fresh = build_invoice(customer, items, date(2026, 3, 1), sequence=3)
    report = aging_report([paid, late, fresh], date(2026, 3, 1))
    assert report == {"current": 1, "0-30": 1, "31-60": 0, "61-90": 0, "90+": 0}


def test_thirty_days_overdue_is_in_first_bucket(customer, items, issued):
    invoice = build_invoice(customer, items, issued)
    on_day_30 = invoice.due.fromordinal(invoice.due.toordinal() + 30)
    assert aging_report([invoice], on_day_30)["0-30"] == 1


def test_region_bucket_matrix(customer, member, items, issued):
    one = build_invoice(customer, items, issued, sequence=1)
    two = build_invoice(member, items, issued, sequence=2)
    matrix = region_bucket_matrix([customer, member], [one, two], date(2026, 2, 20))
    assert matrix == {("US", "0-30"): 1, ("DE", "0-30"): 1}


def test_cross_check_and_pairs():
    assert cross_check(["US", "DE"], ["a", "b"], [2025, 0, 2026]) == 8
    assert pair_labels(["US", "DE"], ["a", "b"]) == ["US/a", "US/b", "DE/a", "DE/b"]


def test_summary_lines_hide_zero_buckets():
    assert summary_lines({"current": 2, "0-30": 0, "90+": 1}) == ["current: 2", "90+: 1"]
