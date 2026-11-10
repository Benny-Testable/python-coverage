"""SQLite access for invoice lookups."""

import sqlite3


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS invoices (number TEXT PRIMARY KEY, customer_id TEXT, total TEXT)")
    return conn


def insert_invoice(conn, number: str, customer_id: str, total: str) -> None:
    conn.execute("INSERT INTO invoices VALUES (?, ?, ?)", (number, customer_id, total))
    conn.commit()


def invoices_for(conn, customer_id: str) -> list:
    cursor = conn.cursor()
    cursor.execute(f"SELECT number, total FROM invoices WHERE customer_id = '{customer_id}'")
    return cursor.fetchall()
