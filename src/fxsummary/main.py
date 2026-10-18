import argparse
import logging
import sys
from pathlib import Path
from typing import Any

from .aggregations import LargestSingleDayChange, MonthlyAverage, MonthWithMostMovement
from .config import Settings, load_settings
from .errors import DataError, FXSummaryError
from .logging_setup import configure_logging
from .models import Record
from .report import featured_records, write_reports
from .sources import Source

logger = logging.getLogger(__name__)


def build_summary(records: list[Record], settings: Settings) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "source_url": settings.source_url,
        "records_processed": len(records),
    }
    for aggregation in (
        MonthlyAverage(),
        LargestSingleDayChange(),
        MonthWithMostMovement(),
    ):
        summary[type(aggregation).__name__] = aggregation.compute(records)
    summary["featured_shows"] = featured_records(
        records, settings.seed, settings.sample_size
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FX summary report")
    parser.add_argument("--config", default="config/fxsummary.toml")
    args = parser.parse_args(argv)
    configure_logging("INFO")
    try:
        settings = load_settings(Path(args.config))
        configure_logging(settings.log_level)
        records = Source(settings.source_url, settings.timeout).fetch()
        if len(records) < 50:
            raise DataError("fewer than 50 valid records after filtering")
        summary = build_summary(records, settings)
        write_reports(summary, settings)
        print(f"Summary written to {settings.output_folder / 'summary.json'}")
        return 0
    except FXSummaryError as error:
        logger.error("Run failed: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
