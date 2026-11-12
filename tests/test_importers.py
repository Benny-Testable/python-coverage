from decimal import Decimal

import pytest

from ledgerly.importers import items_from_csv, items_from_xml, normalize_lines


def test_normalize_lines_defaults():
    assert normalize_lines([{"name": " A "}]) == [{"name": "A", "qty": 0, "price": 0.0, "total": 0.0}]


def test_normalize_lines_negative_values():
    row = normalize_lines([{"name": "n", "qty": -1, "price": -2}])[0]
    assert (row["qty"], row["price"], row["total"]) == (0, 0.0, 0.0)


def test_items_from_csv():
    text = "sku,description,quantity,unit_price\nA-1,Widget,3,2.50\nB-2,Gadget,1,10\n"
    items = items_from_csv(text)
    assert [i.sku for i in items] == ["A-1", "B-2"]
    assert items[0].total() == Decimal("7.50")


def test_blank_quantity_cell_is_zero():
    text = "sku,description,quantity,unit_price\nA-1,Widget,,2.50\n"
    assert items_from_csv(text)[0].quantity == 0


def test_items_from_xml():
    payload = (
        "<items><item sku='X-1'><description>Bolt</description><quantity>5</quantity>"
        "<unit_price>0.40</unit_price></item><item sku='X-2'/></items>"
    )
    items = items_from_xml(payload)
    assert items[0].total() == Decimal("2.00")
    assert items[1].quantity == 0 and items[1].description == ""


def test_malformed_xml_raises():
    with pytest.raises(Exception):
        items_from_xml("<items><item></items>")
