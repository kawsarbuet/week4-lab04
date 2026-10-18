from pathlib import Path

import pytest

from fxsummary.main import main
from fxsummary.models import Record


def test_main_missing_config(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--config", "does-not-exist.toml"]) == 1
    captured = capsys.readouterr()
    assert captured.err.startswith("Error:")
    assert "Traceback" not in captured.err


def test_main_too_few_records(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        (
            'source_url = "https://example.org"\n'
            "timeout = 10\n"
            f'output_folder = "{tmp_path.as_posix()}"\n'
            "seed = 1\n"
            "sample_size = 1\n"
            'log_level = "INFO"\n'
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fxsummary.main.Source.fetch",
        lambda self: [Record("2024-01-01", {"USD": 1})],
    )

    assert main(["--config", str(config)]) == 1
    assert capsys.readouterr().err.startswith("Error:")


def test_main_success(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        (
            'source_url = "https://example.org"\n'
            "timeout = 10\n"
            f'output_folder = "{tmp_path.as_posix()}"\n'
            "seed = 1\n"
            "sample_size = 2\n"
            'log_level = "INFO"\n'
        ),
        encoding="utf-8",
    )

    records = [Record(f"2024-01-{day:02d}", {"USD": day / 100}) for day in range(1, 32)]
    records += [
        Record(f"2024-02-{day:02d}", {"USD": day / 100}) for day in range(1, 20)
    ]

    monkeypatch.setattr("fxsummary.main.Source.fetch", lambda self: records)

    assert main(["--config", str(config)]) == 0
    assert "Summary written" in capsys.readouterr().out
    assert (tmp_path / "summary.json").exists()
