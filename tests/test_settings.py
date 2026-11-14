from ledgerly.settings import load_settings


def test_settings_defaults_and_overrides():
    assert load_settings({}).invoice_prefix == "INV"
    custom = load_settings({"LEDGERLY_CURRENCY": "EUR", "LEDGERLY_EXPORT_BUCKET": "b"})
    assert (custom.currency, custom.export_bucket) == ("EUR", "b")


def test_settings_reads_process_environment(monkeypatch):
    monkeypatch.setenv("LEDGERLY_PREFIX", "ACME")
    assert load_settings().invoice_prefix == "ACME"
