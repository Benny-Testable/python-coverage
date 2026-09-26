"""Identical blocks so jscpd reports duplication (min 5 lines / 50 tokens)."""


def source_tag() -> str:
    return "a"


def normalize_invoice_lines(rows: list[dict]) -> list[dict]:
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
