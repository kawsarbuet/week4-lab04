from datetime import datetime, date


def parse_date(dstr: str) -> date:
    return datetime.strptime(dstr, "%Y-%m-%d").date()


class Record:
    """
    Represents a single FX record: one date and its currency rate map.
    Cleans data in __init__.
    """

    def __init__(self, date_str, rate_map):
        self.date = parse_date(date_str)

        if not isinstance(rate_map, dict):
            raise ValueError("Rate map must be a dict.")

        cleaned = {}
        for cur, val in rate_map.items():
            try:
                cleaned[cur] = float(val)
            except Exception:
                continue

        if not cleaned:
            raise ValueError("Record has no valid rates.")

        self.rates = cleaned

    def __str__(self):
        return f"Record({self.date.isoformat()}, {self.rates})"

