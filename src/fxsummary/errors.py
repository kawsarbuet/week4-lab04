class FXSummaryError(Exception):
    """Base error for expected FX summary failures."""


class SourceError(FXSummaryError):
    """Network or HTTP download failure."""


class DataError(FXSummaryError):
    """Malformed source data or insufficient valid records."""


class SettingsError(FXSummaryError):
    """Missing or invalid TOML configuration."""
