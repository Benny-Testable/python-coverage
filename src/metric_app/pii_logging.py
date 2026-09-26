"""Synthetic identifiers for Presidio and the semgrep-pii logging rules.

These values are public fixture samples. They are not real people or accounts.
- 123-45-6789 is the well-known sample SSN, not an issued number.
- 4111111111111111 is the Visa test PAN.
- 555-010-0199 is a reserved fictional phone number.
"""

import logging

logger = logging.getLogger(__name__)

FIXTURE_EMAIL = "student.fixture@example.com"
FIXTURE_PHONE = "555-010-0199"
FIXTURE_SSN = "123-45-6789"
FIXTURE_CARD = "4111111111111111"


def record(email: str, student_id: str, ssn: str) -> None:
    logger.info("student email=%s", email)
    logger.info("student_id=%s", student_id)
    print("ssn", ssn)


def contact_tag() -> str:
    return "contact"
