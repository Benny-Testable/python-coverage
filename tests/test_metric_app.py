"""Green suite. Covers some branches and leaves others open."""

from metric_app.billing import DISCOUNT, price, tier_label
from metric_app.decisions import eligible, shipping
from metric_app.defs_uses import net


def test_price_uses_discount() -> None:
    assert price(100) == round(100 * (1 - DISCOUNT), 2)


def test_tier_priority() -> None:
    assert tier_label(120, True) == "priority"


def test_tier_walk_in() -> None:
    assert tier_label(10, False) == "walk-in"


def test_eligible_all_true() -> None:
    assert eligible(21, True, True) is True


def test_eligible_underage() -> None:
    assert eligible(17, True, True) is False


def test_shipping_ground() -> None:
    assert shipping(2, False, False) == "ground"


def test_net() -> None:
    assert net(3, 1) == 4
