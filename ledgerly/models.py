"""Plain data containers for customers, invoices and payments."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from ledgerly.money import add, quantize


@dataclass(frozen=True)
class LineItem:
    sku: str
    description: str
    quantity: int
    unit_price: Decimal

    def total(self) -> Decimal:
        return quantize(self.unit_price * self.quantity)


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    region: str = "US"
    member: bool = False
    tax_id: str = ""
    created: date = field(default_factory=date.today)


@dataclass
class Payment:
    reference: str
    amount: Decimal
    received: date


@dataclass
class Invoice:
    number: str
    customer_id: str
    issued: date
    due: date
    items: list = field(default_factory=list)
    payments: list = field(default_factory=list)
    status: str = "draft"
    currency: str = "USD"

    def subtotal(self) -> Decimal:
        return add(*[item.total() for item in self.items])

    def paid_amount(self) -> Decimal:
        return add(*[payment.amount for payment in self.payments])

    def days_overdue(self, today: date) -> int:
        return max(0, (today - self.due).days)
