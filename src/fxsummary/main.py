
from .config import SOURCE_URL, OUTPUT_PATH
from .sources import Source
from .aggregations import (
    MonthlyAverage,
    LargestSingleDayChange,
    MonthWithMostMovement,
)
from .report import write_summary


def build_summary(records):
    aggs = [
        MonthlyAverage(),
        LargestSingleDayChange(),
        MonthWithMostMovement(),
    ]

    summary = {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
    }

    for agg in aggs:
        summary[agg.__class__.__name__] = agg.compute(records)

    return summary


def main():
    src = Source(SOURCE_URL)
    records = src.fetch()

    if len(records) < 50:
        print("Error: fewer than 50 valid records after filtering.")
        exit(1)

    summary = build_summary(records)
    write_summary(summary, OUTPUT_PATH)
