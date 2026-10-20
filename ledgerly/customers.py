"""In-memory customer registry."""

from ledgerly.models import Customer
from ledgerly.validators import is_valid_email


class DuplicateCustomer(Exception):
    pass


class CustomerRegistry:
    def __init__(self) -> None:
        self._by_id = {}

    def add(self, customer: Customer) -> Customer:
        if customer.customer_id in self._by_id:
            raise DuplicateCustomer(customer.customer_id)
        if not is_valid_email(customer.email):
            raise ValueError(f"invalid email for {customer.customer_id}")
        self._by_id[customer.customer_id] = customer
        return customer

    def get(self, customer_id: str) -> Customer:
        return self._by_id[customer_id]

    def find_by_email(self, email: str):
        wanted = email.strip().lower()
        for customer in self._by_id.values():
            if customer.email.lower() == wanted:
                return customer
        return None

    def by_region(self) -> dict:
        grouped = {}
        for customer in self._by_id.values():
            grouped.setdefault(customer.region, []).append(customer)
        return grouped

    def __len__(self) -> int:
        return len(self._by_id)
