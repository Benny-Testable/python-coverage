import pytest

from ledgerly.contracts import split_cents


def test_split_cents_spreads_remainder():
    assert split_cents(100, 3) == [34, 33, 33]


def test_split_cents_exact():
    assert split_cents(90, 3) == [30, 30, 30]


@pytest.mark.parametrize("total,parts", [(0, 1), (1, 5), (7, 2), (1000, 8)])
def test_split_cents_sums_back(total, parts):
    shares = split_cents(total, parts)
    assert sum(shares) == total
    assert len(shares) == parts
    assert max(shares) - min(shares) <= 1
