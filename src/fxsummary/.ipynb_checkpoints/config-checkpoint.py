import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .errors import SettingsError


@dataclass(frozen=True)
class Settings:
    source_url: str
    timeout: float
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str


def load_settings(path: Path) -> Settings:
    try:
        with path.open("rb") as stream:
            data: dict[str, Any] = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SettingsError(f"Cannot read settings file: {path}") from error
    required = {"source_url", "timeout", "output_folder", "seed", "sample_size", "log_level"}
    missing = required - data.keys()
    if missing:
        raise SettingsError(f"Incomplete settings: {', '.join(sorted(missing))}")
    try:
        url = data["source_url"]
        folder = data["output_folder"]
        level = data["log_level"]
        timeout = data["timeout"]
        seed = data["seed"]
        sample_size = data["sample_size"]
        if not isinstance(url, str) or urlsplit(url).scheme not in ("http", "https"):
            raise ValueError("source_url must be an HTTP(S) URL")
        if not isinstance(folder, str) or not folder.strip():
            raise ValueError("output_folder must be a nonempty string")
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout < 3600:
            raise ValueError("timeout must be between 0 and 3600")
        if type(seed) is not int or type(sample_size) is not int or sample_size < 0:
            raise ValueError("seed and sample_size must be integers; sample_size >= 0")
        if not isinstance(level, str) or level.upper() not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError("invalid log_level")
        return Settings(url, float(timeout), Path(folder), seed, sample_size, level.upper())
    except (ValueError, TypeError, OverflowError) as error:
        raise SettingsError(f"Invalid settings: {error}") from error
