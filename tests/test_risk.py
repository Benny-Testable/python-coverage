import pytest

from ledgerly.risk import payment_score, risk_tier


@pytest.mark.parametrize(
    "score,flags,tier,expected",
    [
        (99, 0, 3, "platinum"), (95, 0, 3, "gold"), (95, 0, 2, "silver"), (95, 0, 1, "bronze"),
        (95, 2, 2, "review"), (95, 2, 1, "watch"), (95, 3, 3, "hold"),
        (80, 0, 2, "standard"), (80, 6, 1, "restricted"), (80, 1, 1, "basic"),
        (50, 0, 1, "low"), (50, 1, 1, "low-flagged"), (10, 0, 1, "reject"), (0, 0, 1, "invalid"),
    ],
)
def test_risk_tier(score, flags, tier, expected):
    assert risk_tier(score, flags, tier) == expected


def test_payment_score():
    assert payment_score([]) == 100
    assert payment_score([0, -3]) == 100
    assert payment_score([3, 20, 45]) == 81
    assert payment_score([60] * 10) == 0
