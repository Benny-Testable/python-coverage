from ledgerly.exporters import invoices_to_csv, normalize_rows, write_csv
from ledgerly.invoices import build_invoice


def test_normalize_rows_clamps_negatives():
    rows = [{"name": " Pen ", "qty": -2, "price": 3}, {"name": "Ink", "qty": "4", "price": "2.5"}, {}]
    result = normalize_rows(rows)
    assert result[0] == {"name": "Pen", "qty": 0, "price": 3.0, "total": 0.0}
    assert result[1]["total"] == 10.0
    assert result[2] == {"name": "", "qty": 0, "price": 0.0, "total": 0.0}


def test_normalize_rows_clamps_negative_price():
    assert normalize_rows([{"name": "x", "qty": 2, "price": -1}])[0]["price"] == 0.0


def test_csv_has_header_and_rows(customer, items, issued):
    text = invoices_to_csv([build_invoice(customer, items, issued)])
    lines = text.splitlines()
    assert lines[0] == "number,customer,issued,due,status,subtotal"
    assert lines[1].startswith("INV-00001,C-100,2026-01-10,")
    assert lines[1].endswith(",draft,25.20")


def test_write_csv_returns_row_count(tmp_path, customer, items, issued):
    path = tmp_path / "out.csv"
    count = write_csv(path, [build_invoice(customer, items, issued)] * 3)
    assert count == 3
    assert path.read_text(encoding="utf-8").count("\n") == 4
