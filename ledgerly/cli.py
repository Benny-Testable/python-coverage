"""Command line entry point: ``python -m ledgerly.cli demo``."""

import argparse
from datetime import date

from ledgerly.customers import CustomerRegistry
from ledgerly.demo_data import SAMPLE_CUSTOMERS, sample_issue_date, sample_items
from ledgerly.formatting import format_invoice
from ledgerly.invoices import invoice_totals
from ledgerly.reports import aging_report, summary_lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ledgerly")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo", help="print a sample invoice")
    aging = sub.add_parser("aging", help="print the aging report for the sample data")
    aging.add_argument("--today", default=None, help="ISO date, defaults to today")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    registry = CustomerRegistry()
    for customer in SAMPLE_CUSTOMERS:
        registry.add(customer)
    invoice = registry.open_invoice("C-001", sample_items(), sample_issue_date())
    if args.command == "demo":
        print(format_invoice(invoice, invoice_totals(invoice, registry.get("C-001"))))
        return 0
    today = date.fromisoformat(args.today) if args.today else date.today()
    for line in summary_lines(aging_report([invoice], today)):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
