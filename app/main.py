import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from app.database import get_connection, initialize_database
from app.logging_config import configure_logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield
app = FastAPI(
    title="URLhaus SDET API",
    description="API for querying stored URLhaus threat records",
    version="1.0.0",
    lifespan=lifespan,
)

from contextlib import asynccontextmanager
app = FastAPI(
    title="URLhaus SDET API",
    description="API for querying stored URLhaus threat records",
    version="1.0.0",
    lifespan=lifespan,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/records")
def get_records(limit: int = Query(default=10, ge=1, le=100)):
    logger.info("Fetching records with limit=%d", limit)
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, url, host, date_added, url_status, threat, tags
            FROM threat_records
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    records = [dict(row) for row in rows]

    return {
        "count": len(records),
        "records": records,
    }


@app.get("/records/{record_id}")
def get_record(record_id: int):
    logger.info("Fetching record id=%d", record_id)
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, url, host, date_added, url_status, threat, tags
            FROM threat_records
            WHERE id = ?
            """,
            (record_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )

    return dict(row)
