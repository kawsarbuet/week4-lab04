import pytest

from fxsummary.aggregations import (
    LargestSingleDayChange,
    MonthlyAverage,
    MonthWithMostMovement,
)
from fxsummary.models import Record


def test_monthly_average(sample_records: list[Record]) -> None:
    result = MonthlyAverage().compute(sample_records)
    assert result["2024-01"]["USD"] == pytest.approx(0.745)


def test_largest_change(sample_records: list[Record]) -> None:
    result = LargestSingleDayChange().compute(sample_records)
    assert result["USD"]["change"] == pytest.approx(0.02)


def test_most_movement(sample_records: list[Record]) -> None:
    result = MonthWithMostMovement().compute(sample_records)
    assert result["USD"]["month"] == "2024-02"


@pytest.mark.parametrize(
    "aggregation", [MonthlyAverage(), LargestSingleDayChange(), MonthWithMostMovement()]
)
def test_empty(
    aggregation: MonthlyAverage | LargestSingleDayChange | MonthWithMostMovement,
) -> None:
    assert aggregation.compute([]) == {}


def test_zero_movement() -> None:
    records = [Record("2024-01-01", {"USD": 1}), Record("2024-01-02", {"USD": 1})]
    assert MonthWithMostMovement().compute(records)["USD"] == {
        "month": "2024-01",
        "movement": 0.0,
    }
