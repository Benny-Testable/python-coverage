"""Invoice creation, totals and payment handling."""

from datetime import date, timedelta
from decimal import Decimal

from ledgerly.customers import CustomerRegistry
from ledgerly.models import Invoice, Payment
from ledgerly.money import add, quantize
from ledgerly.pricing import apply_discount, member_price, volume_discount_percent
from ledgerly.tax import tax_for_items

PAYMENT_TERMS = {"net15": 15, "net30": 30, "net60": 60}


def due_date(issued: date, terms: str = "net30") -> date:
    return issued + timedelta(days=PAYMENT_TERMS[terms])


def invoice_number(prefix: str, sequence: int) -> str:
    return f"{prefix}-{sequence:05d}"


def build_invoice(customer, items, issued: date, terms: str = "net30", sequence: int = 1) -> Invoice:
    if not items:
        raise ValueError("an invoice needs at least one line item")
    return Invoice(
        number=invoice_number("INV", sequence),
        customer_id=customer.customer_id,
        issued=issued,
        due=due_date(issued, terms),
        items=list(items),
    )


def invoice_totals(invoice: Invoice, customer) -> dict:
    subtotal = invoice.subtotal()
    quantity = sum(item.quantity for item in invoice.items)
    after_volume = apply_discount(subtotal, volume_discount_percent(quantity))
    discounted = member_price(after_volume, customer.member)
    tax = tax_for_items(invoice.items, customer.region)
    return {
        "subtotal": subtotal,
        "discount": quantize(subtotal - discounted),
        "tax": tax,
        "total": add(discounted, tax),
    }


def balance_due(invoice: Invoice, customer) -> Decimal:
    return quantize(invoice_totals(invoice, customer)["total"] - invoice.paid_amount())


def apply_payment(invoice: Invoice, customer, payment: Payment) -> Invoice:
    if payment.amount <= 0:
        raise ValueError("payment must be positive")
    invoice.payments.append(payment)
    invoice.status = "paid" if balance_due(invoice, customer) <= 0 else "partial"
    return invoice


def issue_for(registry: CustomerRegistry, customer_id: str, items, issued: date, **kwargs) -> Invoice:
    customer = registry.get(customer_id)
    invoice = build_invoice(customer, items, issued, **kwargs)
    invoice.status = "open"
    return invoice
