import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "urlhaus.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS threat_records (
                id INTEGER PRIMARY KEY,
                url TEXT,
                host TEXT,
                date_added TEXT,
                url_status TEXT,
                threat TEXT,
                tags TEXT,
                raw_json TEXT NOT NULL,
                fetched_at TEXT NOT NULL
            )
        """)


def save_records(records):
    from datetime import datetime, timezone

    initialize_database()
    fetched_at = datetime.now(timezone.utc).isoformat()
    inserted = 0

    with get_connection() as connection:
        for record in records:
            record_id = record.get("id")

            if record_id is None:
                continue

            cursor = connection.execute("""
                INSERT OR IGNORE INTO threat_records (
                    id, url, host, date_added, url_status,
                    threat, tags, raw_json, fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_id,
                record.get("url"),
                record.get("host"),
                record.get("date_added"),
                record.get("url_status"),
                record.get("threat"),
                json.dumps(record.get("tags")),
                json.dumps(record),
                fetched_at,
            ))

            inserted += cursor.rowcount

    return inserted


def count_records():
    initialize_database()

    with get_connection() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM threat_records"
        ).fetchone()

    return result[0]
