from pathlib import Path

SOURCE_URL = (
    "https://api.frankfurter.app/2024-01-01..2024-06-30"
    "?from=CAD&to=USD,EUR,GBP"
)

TIMEOUT = 10

OUTPUT_PATH = Path("data/processed/summary.json")
