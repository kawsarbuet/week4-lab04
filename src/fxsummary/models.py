from datetime import date, datetime
from math import isfinite

from .errors import DataError


def parse_date(dstr: str) -> date:
    """Convert a YYYY-MM-DD string into a date object."""
    try:
        return datetime.strptime(dstr, "%Y-%m-%d").date()
    except (TypeError, ValueError) as error:
        raise DataError(f"Invalid FX date: {dstr}") from error


class Record:
    """One FX date and its valid currency rates."""

    def __init__(self, date_str: str, rate_map: object) -> None:
        self.date = parse_date(date_str)

        if not isinstance(rate_map, dict):
            raise DataError("Rate map must be a dictionary")

        cleaned: dict[str, float] = {}

        for currency, value in rate_map.items():
            if not isinstance(currency, str):
                continue

            try:
                if isinstance(value, bool):
                    continue

                number = float(value)

            except (TypeError, ValueError, OverflowError):
                continue

            if isfinite(number):
                cleaned[currency] = number

        if not cleaned:
            raise DataError("Record has no valid rates")

        self.rates = cleaned

    def __str__(self) -> str:
        return f"Record({self.date.isoformat()}, {self.rates})"
