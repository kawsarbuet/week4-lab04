import logging

import requests

from .errors import DataError, SourceError
from .models import Record

logger = logging.getLogger(__name__)


class Source:
    """Download and parse daily FX records."""

    def __init__(self, url: str, timeout: float = 10.0) -> None:
        self.url = url
        self.timeout = timeout

    def fetch(self) -> list[Record]:
        logger.info("Downloading FX rates")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise SourceError("Could not download FX rates") from error
        try:
            raw: object = response.json()
        except ValueError as error:
            raise DataError("Source returned invalid JSON") from error
        return parse_records(raw)


def parse_records(raw: object) -> list[Record]:
    if not isinstance(raw, dict) or not isinstance(raw.get("rates"), dict):
        raise DataError("Malformed API response: missing or invalid 'rates'")
    records: list[Record] = []
    for date_str, rate_map in raw["rates"].items():
        try:
            if not isinstance(date_str, str):
                raise DataError("Date must be text")
            records.append(Record(date_str, rate_map))
        except DataError as error:
            logger.warning("Skipping invalid FX record %s: %s", date_str, error)
    logger.debug("Parsed %s valid FX records", len(records))
    return records
