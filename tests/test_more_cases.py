"""Extra cases: remaining branches of billing, decisions, complexity and small modules."""

import pytest

from metric_app import duplicate_a, duplicate_b
from metric_app.billing import price, tier_label
from metric_app.complexity import classify, label_prefix
from metric_app.contracts import non_negative
from metric_app.decisions import eligible, shipping
from metric_app.defs_uses import net, scale


@pytest.mark.parametrize(
    ("amount", "expected"),
    [(0, 0.0), (50, 44.0), (100, 88.0), (19.99, 17.59)],
)
def test_price_values(amount: float, expected: float) -> None:
    assert price(amount) == expected


@pytest.mark.parametrize(
    ("amount", "member", "label"),
    [
        (100, True, "priority"),
        (100, False, "standard"),
        (99.99, True, "member"),
        (99.99, False, "walk-in"),
        (0, False, "walk-in"),
    ],
)
def test_tier_label_all_paths(amount: float, member: bool, label: str) -> None:
    assert tier_label(amount, member) == label


@pytest.mark.parametrize(
    ("age", "member", "active", "expected"),
    [
        (18, True, True, True),
        (17, True, True, False),
        (30, False, True, False),
        (30, True, False, False),
    ],
)
def test_eligible_each_condition_flips_result(
    age: int, member: bool, active: bool, expected: bool
) -> None:
    assert eligible(age, member, active) is expected


@pytest.mark.parametrize(
    ("weight", "express", "fragile", "expected"),
    [
        (21, False, False, "special"),
        (20, False, False, "ground"),
        (5, True, True, "special"),
        (5, True, False, "ground"),
        (5, False, True, "ground"),
    ],
)
def test_shipping_conditions(
    weight: float, express: bool, fragile: bool, expected: str
) -> None:
    assert shipping(weight, express, fragile) == expected


@pytest.mark.parametrize(
    ("score", "flags", "tier", "expected"),
    [
        (99, 0, 3, "platinum"),
        (95, 0, 3, "gold"),
        (95, 0, 2, "silver"),
        (95, 0, 1, "bronze"),
        (95, 1, 2, "review"),
        (95, 1, 1, "watch"),
        (95, 3, 1, "hold"),
        (80, 0, 2, "standard"),
        (80, 6, 2, "restricted"),
        (80, 1, 1, "basic"),
        (50, 0, 1, "low"),
        (50, 1, 1, "low-flagged"),
        (10, 0, 1, "reject"),
        (0, 0, 1, "invalid"),
    ],
)
def test_classify_all_branches(score: int, flags: int, tier: int, expected: str) -> None:
    assert classify(score, flags, tier) == expected


def test_label_prefix() -> None:
    assert label_prefix() == "tier"


def test_net_and_scale() -> None:
    assert net(5, 2) == 7
    assert scale(9) == 9


def test_non_negative() -> None:
    assert non_negative(0) == 0
    assert non_negative(7) == 7
    with pytest.raises(AssertionError):
        non_negative(-1)


@pytest.mark.parametrize("module", [duplicate_a, duplicate_b])
def test_normalize_invoice_lines(module) -> None:
    rows = [
        {"name": "  widget ", "qty": "3", "price": "2.5"},
        {"name": "neg", "qty": -4, "price": -1},
        {},
    ]
    assert module.normalize_invoice_lines(rows) == [
        {"name": "widget", "qty": 3, "price": 2.5, "total": 7.5},
        {"name": "neg", "qty": 0, "price": 0.0, "total": 0.0},
        {"name": "", "qty": 0, "price": 0.0, "total": 0.0},
    ]
    assert module.normalize_invoice_lines([]) == []


def test_source_tags_differ() -> None:
    assert duplicate_a.source_tag() == "a"
    assert duplicate_b.source_tag() == "b"
