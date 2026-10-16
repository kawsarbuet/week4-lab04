import requests
from .models import Record
from .config import TIMEOUT


class Source:
    """
    Downloads FX records and returns a list of Record objects.
    """

    def __init__(self, url):
        self.url = url

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=TIMEOUT)
            response.raise_for_status()
            raw = response.json()

            if "rates" not in raw:
                raise ValueError("Malformed API response: missing 'rates'.")

            records = []
            for dstr, rate_map in raw["rates"].items():
                try:
                    rec = Record(dstr, rate_map)
                    records.append(rec)
                except Exception:
                    continue

            return records

        except Exception as exc:
            print(f"Download failed: {exc}")
            exit(1)
