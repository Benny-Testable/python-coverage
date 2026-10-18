"""Input validation for customer contact data."""

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PHONE_RE = re.compile(r"^\+?[0-9][0-9 ()-]{6,18}[0-9]$")
POSTAL_RE = {
    "US": re.compile(r"^\d{5}(-\d{4})?$"),
    "CA": re.compile(r"^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$"),
    "DE": re.compile(r"^\d{5}$"),
    "GB": re.compile(r"^[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}$"),
}


def is_valid_email(value: str) -> bool:
    return bool(value) and len(value) <= 254 and EMAIL_RE.match(value) is not None


def is_valid_phone(value: str) -> bool:
    return bool(value) and PHONE_RE.match(value) is not None


def is_valid_postal(region: str, code: str) -> bool:
    pattern = POSTAL_RE.get(region.upper())
    if pattern is None:
        return bool(code.strip())
    return pattern.match(code.strip()) is not None


def contact_errors(email: str, phone: str, region: str, postal: str) -> list:
    errors = []
    if not is_valid_email(email):
        errors.append("email")
    if phone and not is_valid_phone(phone):
        errors.append("phone")
    if postal and not is_valid_postal(region, postal):
        errors.append("postal")
    return errors
