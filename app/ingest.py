
import logging

from app.database import count_records, save_records
from app.logging_config import configure_logging
from app.urlhaus_client import fetch_recent_urls

configure_logging()
logger = logging.getLogger(__name__)


def run_ingestion():
    logger.info("Starting URLhaus ingestion")

    try:
        records = fetch_recent_urls()
        logger.info("Fetched %d URLhaus records", len(records))

        inserted = save_records(records)
        logger.info("Inserted %d new records", inserted)

        total = count_records()
        logger.info("Total records stored: %d", total)

        return {
            "fetched": len(records),
            "inserted": inserted,
            "total": total,
        }

    except Exception:
        logger.exception("URLhaus ingestion failed")
        raise


if __name__ == "__main__":
    run_ingestion()
