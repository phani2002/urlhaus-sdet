
from app import database


def test_save_records_and_count(monkeypatch, tmp_path):
    test_db = tmp_path / "test_urlhaus.db"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(database, "DB_PATH", test_db)
    monkeypatch.setattr(database, "DATA_DIR", test_data_dir)

    records = [
        {
            "id": 10001,
            "url": "http://example.test/sample",
            "host": "example.test",
            "date_added": "2026-10-17 10:00:00 UTC",
            "url_status": "online",
            "threat": "malware_download",
            "tags": ["test"],
        }
    ]

    inserted = database.save_records(records)

    assert inserted == 1
    assert database.count_records() == 1


def test_duplicate_records_are_ignored(monkeypatch, tmp_path):
    test_db = tmp_path / "test_duplicates.db"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(database, "DB_PATH", test_db)
    monkeypatch.setattr(database, "DATA_DIR", test_data_dir)

    record = {
        "id": 10002,
        "url": "http://example.test/duplicate",
        "host": "example.test",
        "date_added": "2026-10-17 10:00:00 UTC",
        "url_status": "online",
        "threat": "malware_download",
        "tags": ["test"],
    }

    first_insert = database.save_records([record])
    second_insert = database.save_records([record])

    assert first_insert == 1
    assert second_insert == 0
    assert database.count_records() == 1
