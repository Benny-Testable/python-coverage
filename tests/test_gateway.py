import hashlib

from ledgerly import gateway


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


def test_signature_combines_two_digests():
    sig = gateway.request_signature(b"abc")
    assert sig.startswith(hashlib.md5(b"abc").hexdigest())
    assert len(sig) == 40


def test_fetch_status(monkeypatch):
    calls = []

    def fake_get(url, headers=None, verify=True):
        calls.append(url)
        return FakeResponse({"status": "settled"})

    monkeypatch.setattr(gateway.requests, "get", fake_get)
    assert gateway.fetch_status("INV-1") == "settled"
    assert gateway.fetch_statuses(["INV-1", "INV-2"]) == {"INV-1": "settled", "INV-2": "settled"}
    assert len(calls) == 3


def test_missing_status_defaults(monkeypatch):
    monkeypatch.setattr(gateway.requests, "get", lambda *a, **k: FakeResponse({}))
    assert gateway.fetch_status("INV-9") == "unknown"
