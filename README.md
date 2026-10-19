
# URLhaus SDET Automation Platform

A Python-based threat intelligence application demonstrating API integration, automated testing, database validation, containerization, and continuous integration.

## Architecture

URLhaus API → Python Ingestion Client → SQLite Database → FastAPI → API Consumers

Automated validation is performed using pytest, and GitHub Actions runs the test suite on pushes and pull requests to the main branch.

## Technology Stack

- Python 3.12
- Requests and python-dotenv
- FastAPI and Uvicorn
- SQLite
- pytest
- Docker
- GitHub Actions

## Features

- Fetch recent threat intelligence records from URLhaus.
- Validate API responses and handle HTTP errors and timeouts.
- Store records in SQLite and ignore duplicate record IDs.
- Expose health, list, and individual-record API endpoints.
- Configure application logging for ingestion and API operations.
- Run the application in Docker with persistent database storage.
- Execute automated tests locally and through GitHub Actions.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/records?limit=5` | List records |
| GET | `/records/{record_id}` | Retrieve one record |
| GET | `/docs` | Interactive API documentation |

## Local Setup

1. Install Python 3.12.
2. Clone this repository.
3. Create and activate a virtual environment.
4. Install dependencies:

   `python -m pip install -r requirements.txt`

5. Create a local `.env` file containing your URLhaus API key:

   `URLHAUS_AUTH_KEY=your_api_key`

6. Run ingestion:

   `python -m app.ingest`

7. Start the API:

   `python -m uvicorn app.main:app --reload`

8. Open `http://localhost:8000/docs`.

Never commit `.env` or publish API keys.

## Run Automated Tests

`python -m pytest tests -v`

The test suite covers API client success and failure scenarios, database persistence and duplicate handling, and FastAPI endpoint behavior.

## Docker

Build the image:

`docker build -t urlhaus-sdet:1.0 .`

Run the API with persistent database storage:

`docker run -d --name urlhaus-api -p 8000:8000 -v urlhaus-data:/app/data urlhaus-sdet:1.0`

For ingestion in the same database volume:

`docker run --rm --env-file .env -v urlhaus-data:/app/data urlhaus-sdet:1.0 python -m app.ingest`

## Continuous Integration

GitHub Actions installs dependencies and runs pytest on pushes and pull requests targeting `main`.

## Security Notes

- Keep API keys in local environment files or a secret manager.
- Exclude secrets and local database files from version control.
- Treat threat intelligence URLs as untrusted data. Do not visit or download suspicious URLs directly.