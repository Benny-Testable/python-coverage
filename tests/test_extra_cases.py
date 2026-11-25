"""Extra cases for the remaining uncovered lines and edge inputs."""

import sqlite3
import tarfile

import pytest

from ledgerly import cli, db, shell_tools, utils


def test_aging_defaults_to_today(capsys):
    assert cli.main(["aging"]) == 0
    assert capsys.readouterr().out.strip() != ""


def test_archive_directory_creates_tarball(tmp_path):
    source = tmp_path / "src"
    source.mkdir()
    (source / "a.txt").write_text("hello")
    archive = tmp_path / "out.tgz"
    assert shell_tools.archive_directory(str(source), str(archive)) == 0
    with tarfile.open(archive) as tar:
        assert any(name.endswith("a.txt") for name in tar.getnames())


def test_archive_directory_missing_source_fails(tmp_path):
    assert shell_tools.archive_directory(str(tmp_path / "nope"), str(tmp_path / "x.tgz")) != 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0.4, 0), (0.5, 1), (1.49, 1), (2.5, 3), (0.0, 0)],
)
def test_legacy_round(value, expected):
    assert utils.legacy_round(value) == expected


def test_deprecated_formatter_render():
    formatter = utils.DeprecatedFormatter()
    assert formatter.render("hi") == ">>hi"
    assert utils.DeprecatedFormatter.prefix == ">>"


@pytest.mark.parametrize(
    ("text", "expected"),
    [("", ""), ("  A  B  ", "a-b"), ("!!!", ""), ("Already-slug", "already-slug")],
)
def test_slugify_edges(text, expected):
    assert utils.slugify(text) == expected


def test_chunked_edges():
    assert utils.chunked([], 3) == []
    assert utils.chunked([1, 2], 5) == [[1, 2]]
    assert utils.chunked([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_db_unknown_customer_returns_empty():
    conn = db.connect()
    assert db.invoices_for(conn, "C-404") == []


def test_db_duplicate_invoice_number_rejected():
    conn = db.connect()
    db.insert_invoice(conn, "INV-1", "C-1", "10.00")
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_invoice(conn, "INV-1", "C-2", "5.00")


def test_db_connect_is_idempotent_on_file(tmp_path):
    path = str(tmp_path / "inv.db")
    first = db.connect(path)
    db.insert_invoice(first, "INV-9", "C-9", "1.00")
    first.close()
    second = db.connect(path)
    assert db.invoices_for(second, "C-9") == [("INV-9", "1.00")]
