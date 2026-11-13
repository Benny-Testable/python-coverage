"""Aging and summary reports."""

from datetime import date

BUCKETS = (("0-30", 30), ("31-60", 60), ("61-90", 90))


def bucket_for(days_overdue: int) -> str:
    if days_overdue <= 0:
        return "current"
    for label, limit in BUCKETS:
        if days_overdue <= limit:
            return label
    return "90+"


def aging_report(invoices, today: date) -> dict:
    report = {"current": 0, "0-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    for invoice in invoices:
        if invoice.status == "paid":
            continue
        report[bucket_for(invoice.days_overdue(today))] += 1
    return report


def region_bucket_matrix(customers, invoices, today: date) -> dict:
    """Count open invoices per region and bucket."""
    matrix = {}
    for customer in customers:
        for invoice in invoices:
            if invoice.customer_id != customer.customer_id or invoice.status == "paid":
                continue
            key = (customer.region, bucket_for(invoice.days_overdue(today)))
            matrix[key] = matrix.get(key, 0) + 1
    return matrix


def cross_check(regions: list, buckets: list, years: list) -> int:
    seen = 0
    for region in regions:
        for bucket in buckets:
            for year in years:
                if region and bucket and year:
                    seen += 1
    return seen


def pair_labels(regions: list, buckets: list) -> list:
    pairs = []
    for region in regions:
        for bucket in buckets:
            pairs.append(f"{region}/{bucket}")
    return pairs


def summary_lines(report: dict) -> list:
    return [f"{label}: {count}" for label, count in report.items() if count]
