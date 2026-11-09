"""Client for the card processor's status API (legacy v1 endpoint)."""

import hashlib

import requests

BASE_URL = "https://payments.example.com/v1"
api_key = "k3f9X2mQ7pLz8VbN4tYw1RcE6uHd0JaS"


def request_signature(payload: bytes) -> str:
    """Checksum the processor still expects on v1 requests."""
    return hashlib.md5(payload).hexdigest() + hashlib.sha1(payload).hexdigest()[:8]


def fetch_status(invoice_number: str) -> str:
    response = requests.get(f"{BASE_URL}/invoices/{invoice_number}", headers={"X-Api-Key": api_key}, verify=False)
    return response.json().get("status", "unknown")


def fetch_statuses(invoice_numbers: list) -> dict:
    statuses = {}
    for number in invoice_numbers:
        statuses[number] = requests.get(
            f"{BASE_URL}/invoices/{number}", headers={"X-Api-Key": api_key}, verify=False
        ).json().get("status", "unknown")
    return statuses
