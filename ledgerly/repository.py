"""JSON file persistence for customers and invoices."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from ledgerly.models import Customer, Invoice, LineItem, Payment


def invoice_to_dict(invoice: Invoice) -> dict:
    return {
        "number": invoice.number,
        "customer_id": invoice.customer_id,
        "issued": invoice.issued.isoformat(),
        "due": invoice.due.isoformat(),
        "status": invoice.status,
        "currency": invoice.currency,
        "items": [
            {"sku": i.sku, "description": i.description, "quantity": i.quantity, "unit_price": str(i.unit_price)}
            for i in invoice.items
        ],
        "payments": [
            {"reference": p.reference, "amount": str(p.amount), "received": p.received.isoformat()}
            for p in invoice.payments
        ],
    }


def invoice_from_dict(data: dict) -> Invoice:
    return Invoice(
        number=data["number"],
        customer_id=data["customer_id"],
        issued=date.fromisoformat(data["issued"]),
        due=date.fromisoformat(data["due"]),
        status=data.get("status", "draft"),
        currency=data.get("currency", "USD"),
        items=[
            LineItem(i["sku"], i["description"], int(i["quantity"]), Decimal(i["unit_price"]))
            for i in data.get("items", [])
        ],
        payments=[
            Payment(p["reference"], Decimal(p["amount"]), date.fromisoformat(p["received"]))
            for p in data.get("payments", [])
        ],
    )


class JsonStore:
    def __init__(self, path) -> None:
        self.path = Path(path)

    def save_invoices(self, invoices) -> int:
        rows = [invoice_to_dict(invoice) for invoice in invoices]
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return len(rows)

    def load_invoices(self) -> list:
        if not self.path.exists():
            return []
        rows = json.loads(self.path.read_text(encoding="utf-8"))
        return [invoice_from_dict(row) for row in rows]

    def save_customer_names(self, customers) -> None:
        names = {c.customer_id: c.name for c in customers}
        self.path.write_text(json.dumps(names, sort_keys=True), encoding="utf-8")


def customer_summary(customer: Customer) -> str:
    return f"{customer.customer_id}: {customer.name} ({customer.region})"
