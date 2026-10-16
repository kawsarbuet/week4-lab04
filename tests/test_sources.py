import logging

import pytest
import requests

from fxsummary.errors import DataError, SourceError
from fxsummary.sources import Source, parse_records


def test_network_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: float) -> None:
        raise requests.ConnectionError("offline")

    monkeypatch.setattr("fxsummary.sources.requests.get", fake_get)
    with pytest.raises(SourceError, match="download"):
        Source("https://example.invalid", 1).fetch()


def test_bad_shape() -> None:
    with pytest.raises(DataError, match="rates"):
        parse_records({"wrong": {}})


def test_bad_record_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        records = parse_records({"rates": {"bad-date": {"USD": 1}, "2024-01-01": {"USD": 1}}})
    assert len(records) == 1
    assert "Skipping invalid FX record" in caplog.text
