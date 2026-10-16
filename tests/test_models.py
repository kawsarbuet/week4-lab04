import pytest

from fxsummary.errors import DataError
from fxsummary.models import Record


def test_valid_record() -> None:
    assert Record("2024-01-01", {"USD": 0.74}).rates["USD"] == 0.74


def test_missing_currency_rate_is_accepted() -> None:
    assert Record("2024-01-01", {"USD": 0.74}).rates == {"USD": 0.74}


def test_missing_rates_rejected() -> None:
    with pytest.raises(DataError, match="no valid rates"):
        Record("2024-01-01", {})


@pytest.mark.parametrize("value", ["0.74", 0.74, 0.740])
def test_rate_conversion(value: str | float) -> None:
    assert Record("2024-01-01", {"USD": value}).rates["USD"] == 0.74


def test_invalid_date() -> None:
    with pytest.raises(DataError, match="Invalid FX date"):
        Record("bad-date", {"USD": 0.74})


def test_skip_invalid_rate() -> None:
    assert Record("2024-01-01", {"USD": 0.74, "EUR": None}).rates == {"USD": 0.74}
