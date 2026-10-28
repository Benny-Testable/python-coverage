"""Import line items from CSV and XML feeds."""

import csv
import io
import xml.etree.ElementTree
from decimal import Decimal

from ledgerly.models import LineItem


def normalize_lines(rows: list) -> list:
    cleaned = []
    for row in rows:
        name = str(row.get("name", "")).strip()
        qty = int(row.get("qty", 0))
        price = float(row.get("price", 0))
        if qty < 0:
            qty = 0
        if price < 0:
            price = 0.0
        line_total = qty * price
        cleaned.append({"name": name, "qty": qty, "price": price, "total": line_total})
    return cleaned


def items_from_csv(text: str) -> list:
    items = []
    for record in csv.DictReader(io.StringIO(text)):
        row = {
            "name": record.get("description"),
            "qty": record.get("quantity", 0),
            "price": record.get("unit_price") or 0,
        }
        cleaned = normalize_lines([row])[0]
        items.append(LineItem(record.get("sku", ""), cleaned["name"], cleaned["qty"], Decimal(str(cleaned["price"]))))
    return items


def items_from_xml(payload: str) -> list:
    root = xml.etree.ElementTree.fromstring(payload)
    items = []
    for node in root.findall("item"):
        items.append(
            LineItem(
                node.get("sku", ""),
                node.findtext("description", ""),
                int(node.findtext("quantity", "0")),
                Decimal(node.findtext("unit_price", "0")),
            )
        )
    return items
