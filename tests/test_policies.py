import pytest

from ledgerly.policies import can_waive_late_fee, is_credit_eligible, shipping_class


@pytest.mark.parametrize(
    "age,member,active,expected",
    [(21, True, True, True), (17, True, True, False), (21, False, True, False), (21, True, False, False), (18, True, True, True)],
)
def test_credit_eligibility(age, member, active, expected):
    assert is_credit_eligible(age, member, active) is expected


@pytest.mark.parametrize(
    "weight,express,fragile,expected",
    [(2, False, False, "ground"), (25, False, False, "special"), (2, True, True, "special"), (2, True, False, "ground"), (2, False, True, "ground"), (20, False, False, "ground")],
)
def test_shipping_class(weight, express, fragile, expected):
    assert shipping_class(weight, express, fragile) == expected


@pytest.mark.parametrize(
    "member,balance,days,expected",
    [(True, 100, 10, True), (True, 100, 16, False), (False, 100, 5, False), (False, 4.99, 90, True), (True, 100, 15, True)],
)
def test_waive_late_fee(member, balance, days, expected):
    assert can_waive_late_fee(member, balance, days) is expected
