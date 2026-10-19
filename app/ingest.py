
from app.database import count_records, save_records
from app.urlhaus_client import fetch_recent_urls


def run_ingestion():
    print("Fetching recent URLhaus records...")

    records = fetch_recent_urls()

    print(f"Records fetched: {len(records)}")

    inserted = save_records(records)

    print(f"New records inserted: {inserted}")
    print(f"Total records stored: {count_records()}")


if __name__ == "__main__":
    run_ingestion()
