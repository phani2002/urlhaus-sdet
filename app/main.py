
from fastapi import FastAPI, HTTPException, Query
from app.database import get_connection, initialize_database

app = FastAPI(
    title="URLhaus SDET API",
    description="API for querying stored URLhaus threat records",
    version="1.0.0",
)
@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/records")
def get_records(limit: int = Query(default=10, ge=1, le=100)):
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
