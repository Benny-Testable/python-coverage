import sqlite3

from ledgerly import db


def test_db_lookup():
    conn = db.connect()
    db.insert_invoice(conn, "INV-1", "C-1", "10.00")
    db.insert_invoice(conn, "INV-2", "C-2", "20.00")
    assert db.invoices_for(conn, "C-1") == [("INV-1", "10.00")]
    assert isinstance(conn, sqlite3.Connection)
