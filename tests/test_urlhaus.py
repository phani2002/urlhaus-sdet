
import pytest

from app.urlhaus_client import fetch_recent_urls


class FakeResponse:
    """Simulate an HTTP response without calling URLhaus."""

    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")

    def json(self):
        return self.data


def test_fetch_recent_urls_success(monkeypatch):
    """Test that valid URL records are returned."""

    sample_data = {
        "query_status": "ok",
        "urls": [
            {
                "id": 123,
                "host": "example.com",
                "url_status": "online",
            }
        ],
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(sample_data)

    monkeypatch.setenv("URLHAUS_AUTH_KEY", "test-key")
    monkeypatch.setattr(
        "app.urlhaus_client.requests.get", fake_get
    )

    records = fetch_recent_urls()

    assert len(records) == 1
    assert records[0]["id"] == 123
    assert records[0]["host"] == "example.com"


def test_missing_api_key(monkeypatch):
    """Test that missing credentials are rejected."""

    monkeypatch.delenv("URLHAUS_AUTH_KEY", raising=False)

    with pytest.raises(RuntimeError, match="URLHAUS_AUTH_KEY"):
        fetch_recent_urls()


def test_invalid_response_status(monkeypatch):
    """Test that an unsuccessful API status is rejected."""

    sample_data = {
        "query_status": "invalid_auth",
        "urls": [],
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(sample_data)

    monkeypatch.setenv("URLHAUS_AUTH_KEY", "test-key")
    monkeypatch.setattr(
        "app.urlhaus_client.requests.get", fake_get
    )

    with pytest.raises(RuntimeError, match="invalid_auth"):
        fetch_recent_urls()


def test_invalid_urls_type(monkeypatch):
    """Test that malformed response data is rejected."""

    sample_data = {
        "query_status": "ok",
        "urls": "not-a-list",
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(sample_data)

    monkeypatch.setenv("URLHAUS_AUTH_KEY", "test-key")
    monkeypatch.setattr(
        "app.urlhaus_client.requests.get", fake_get
    )

    with pytest.raises(ValueError, match="urls must be a list"):
        fetch_recent_urls()

def test_http_server_error(monkeypatch):
    """Verify that an HTTP 500 response is handled."""

    def fake_get(*args, **kwargs):
        return FakeResponse({}, status_code=500)

    monkeypatch.setenv("URLHAUS_AUTH_KEY", "test-key")
    monkeypatch.setattr(
        "app.urlhaus_client.requests.get",
        fake_get,
    )

    with pytest.raises(RuntimeError, match="HTTP error: 500"):
        fetch_recent_urls()


def test_network_timeout(monkeypatch):
    """Verify that network timeouts are propagated."""

    import requests

    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setenv("URLHAUS_AUTH_KEY", "test-key")
    monkeypatch.setattr(
        "app.urlhaus_client.requests.get",
        fake_get,
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_recent_urls()
