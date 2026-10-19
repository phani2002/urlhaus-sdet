
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_records(monkeypatch, tmp_path):
    test_db = tmp_path / "test_api.db"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(database, "DB_PATH", test_db)
    monkeypatch.setattr(database, "DATA_DIR", test_data_dir)

    database.save_records([
        {
            "id": 20001,
            "url": "http://example.test/sample",
            "host": "example.test",
            "date_added": "2026-10-17 10:00:00 UTC",
            "url_status": "online",
            "threat": "malware_download",
            "tags": ["test"],
        }
    ])

    response = client.get("/records")

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["records"][0]["id"] == 20001


def test_get_specific_record(monkeypatch, tmp_path):
    test_db = tmp_path / "test_record.db"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(database, "DB_PATH", test_db)
    monkeypatch.setattr(database, "DATA_DIR", test_data_dir)

    database.save_records([
        {
            "id": 20002,
            "url": "http://example.test/record",
            "host": "example.test",
            "date_added": "2026-10-17 10:00:00 UTC",
            "url_status": "online",
            "threat": "malware_download",
            "tags": ["test"],
        }
    ])

    response = client.get("/records/20002")

    assert response.status_code == 200
    assert response.json()["id"] == 20002


def test_record_not_found():
    response = client.get("/records/99999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Record not found"


def test_invalid_record_limit():
    response = client.get("/records?limit=0")

    assert response.status_code == 422


def test_record_limit_over_maximum():
    response = client.get("/records?limit=101")

    assert response.status_code == 422
