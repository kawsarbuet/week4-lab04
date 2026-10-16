import pytest

from fxsummary.models import Record


@pytest.fixture
def sample_records() -> list[Record]:
    return [
        Record("2024-01-01", {"USD": 0.74, "EUR": 0.68}),
        Record("2024-01-02", {"USD": 0.75, "EUR": 0.69}),
        Record("2024-02-01", {"USD": 0.73, "EUR": 0.67}),
    ]
