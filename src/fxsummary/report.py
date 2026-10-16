import json
import logging
import platform
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from .config import Settings
from .errors import DataError
from .models import Record

logger = logging.getLogger(__name__)


def featured_records(records: list[Record], seed: int, size: int) -> list[str]:
    """Stable sample of FX dates (assignment's featured_shows key)."""
    import random

    names = sorted({record.date.isoformat() for record in records})
    if size > len(names):
        raise DataError("sample_size exceeds the number of available FX dates")
    return random.Random(seed).sample(names, size)


def tool_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not installed"


def write_reports(summary: dict[str, Any], settings: Settings) -> None:
    folder = settings.output_folder
    try:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8"
        )
        metadata = {
            "settings": {**asdict(settings), "output_folder": str(folder)},
            "python_version": platform.python_version(),
            "tool_versions": {name: tool_version(name) for name in ("pytest", "mypy", "ruff")},
        }
        (folder / "run_info.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as error:
        raise DataError(f"Cannot write output files in {folder}") from error
    logger.info("Wrote summary.json and run_info.json to %s", folder)
