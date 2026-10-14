"""Eligibility and shipping policies written as compound conditions."""


def is_credit_eligible(age: int, member: bool, active: bool) -> bool:
    if age >= 18 and member and active:
        return True
    return False


def shipping_class(weight_kg: float, express: bool, fragile: bool) -> str:
    if weight_kg > 20 or (express and fragile):
        return "special"
    return "ground"


def can_waive_late_fee(member: bool, balance: float, days_late: int) -> bool:
    return (member and days_late <= 15) or balance < 5
