import json
from pathlib import Path

import pytest

from fxsummary.config import Settings, load_settings
from fxsummary.errors import DataError, SettingsError
from fxsummary.models import Record
from fxsummary.report import featured_records, write_reports


def test_missing_config(tmp_path: Path) -> None:
    with pytest.raises(SettingsError, match="Cannot read"):
        load_settings(tmp_path / "missing.toml")


def test_incomplete_config(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.toml"
    path.write_text('source_url = "https://example.org"', encoding="utf-8")
    with pytest.raises(SettingsError, match="Incomplete"):
        load_settings(path)


def test_seed_reproducible(sample_records: list[Record]) -> None:
    assert featured_records(sample_records, 42, 2) == featured_records(
        sample_records, 42, 2
    )


def test_sample_too_large(sample_records: list[Record]) -> None:
    with pytest.raises(DataError, match="sample_size"):
        featured_records(sample_records, 42, 100)


def test_write_reports(tmp_path: Path) -> None:
    settings = Settings("https://example.org", 10, tmp_path, 42, 2, "INFO")
    write_reports({"source_url": settings.source_url}, settings)
    assert (
        json.loads((tmp_path / "summary.json").read_text())["source_url"]
        == settings.source_url
    )
    info = json.loads((tmp_path / "run_info.json").read_text())
    assert info["settings"]["seed"] == 42
    assert set(info["tool_versions"]) == {"pytest", "mypy", "ruff"}
