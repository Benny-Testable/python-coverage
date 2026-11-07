import pytest

from ledgerly.validators import contact_errors, is_valid_email, is_valid_phone, is_valid_postal


@pytest.mark.parametrize("email", ["a@example.com", "first.last@sub.example.org", "x-y@ex-ample.co.uk"])
def test_valid_emails(email):
    assert is_valid_email(email)


@pytest.mark.parametrize("email", ["", "plain", "a@b", "@example.com", "a b@example.com", "a@" + "x" * 250 + ".com"])
def test_invalid_emails(email):
    assert not is_valid_email(email)


def test_plus_addressed_email_is_valid():
    assert is_valid_email("billing+acme@example.com")


@pytest.mark.parametrize("phone,ok", [("555-010-0199", True), ("+44 20 7946 0958", True), ("12", False), ("", False), ("abc-defg", False)])
def test_phone(phone, ok):
    assert is_valid_phone(phone) is ok


@pytest.mark.parametrize(
    "region,code,ok",
    [("US", "12345", True), ("US", "12345-6789", True), ("US", "1234", False), ("CA", "K1A 0B1", True), ("DE", "10115", True), ("GB", "SW1A 1AA", True), ("FR", "75001", True), ("FR", "  ", False)],
)
def test_postal(region, code, ok):
    assert is_valid_postal(region, code) is ok


def test_contact_errors_collects_each_problem():
    assert contact_errors("bad", "1", "US", "x") == ["email", "phone", "postal"]
    assert contact_errors("a@example.com", "", "US", "") == []
