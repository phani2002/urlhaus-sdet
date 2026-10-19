
import os
import requests
from dotenv import load_dotenv

# Load configuration from the .env file
load_dotenv()

# URLhaus API endpoint for recent URL records
API_URL = "https://urlhaus-api.abuse.ch/v1/urls/recent/"


def fetch_recent_urls():
    """Fetch recent threat intelligence records from URLhaus."""

    # Read the API key from an environment variable
    auth_key = os.getenv("URLHAUS_AUTH_KEY")

    if not auth_key:
        raise RuntimeError(
            "URLHAUS_AUTH_KEY is missing from the .env file"
        )

    # Send an authenticated HTTP GET request
    response = requests.get(
        API_URL,
        headers={"Auth-Key": auth_key},
        timeout=20,
    )

    # Raise an error for HTTP failures, such as 401 or 500
    response.raise_for_status()

    # Convert the JSON response into Python objects
    data = response.json()

    # Validate the API's reported status
    if data.get("query_status") != "ok":
        raise RuntimeError(
            f"URLhaus API returned: {data.get('query_status')}"
        )

    # Check that the expected records are present
    records = data.get("urls")

    if not isinstance(records, list):
        raise ValueError("Invalid API response: urls must be a list")

    return records


if __name__ == "__main__":
    records = fetch_recent_urls()

    print(f"Records received: {len(records)}")

    for record in records[:5]:
        print({
            "id": record.get("id"),
            "host": record.get("host"),
            "status": record.get("url_status"),
            "date_added": record.get("date_added"),
        })