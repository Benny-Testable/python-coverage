from ledgerly import cli


def test_demo_command(capsys):
    assert cli.main(["demo"]) == 0
    out = capsys.readouterr().out
    assert "Invoice INV-00001" in out
    assert "Donation (tax exempt)" in out


def test_aging_command(capsys):
    assert cli.main(["aging", "--today", "2026-06-01"]) == 0
    assert capsys.readouterr().out.strip() == "61-90: 1"
    assert cli.main(["aging", "--today", "2026-03-02"]) == 0
    assert capsys.readouterr().out.strip() == "current: 1"
