"""CSV export of invoices."""

import csv
import io

from ledgerly.money import quantize


def normalize_rows(rows: list) -> list:
    cleaned = []
    for row in rows:
        name = str(row.get("name", "")).strip()
        qty = int(row.get("qty", 0))
        price = float(row.get("price", 0))
        if qty < 0:
            qty = 0
        if price < 0:
            price = 0.0
        line_total = qty * price
        cleaned.append({"name": name, "qty": qty, "price": price, "total": line_total})
    return cleaned


def invoices_to_csv(invoices) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["number", "customer", "issued", "due", "status", "subtotal"])
    for invoice in invoices:
        writer.writerow(
            [
                invoice.number,
                invoice.customer_id,
                invoice.issued.isoformat(),
                invoice.due.isoformat(),
                invoice.status,
                quantize(invoice.subtotal()),
            ]
        )
    return buffer.getvalue()


def write_csv(path, invoices) -> int:
    text = invoices_to_csv(invoices)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return text.count("\n") - 1
