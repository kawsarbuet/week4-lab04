# FX Summary — AIGC 5005 Lab 04

Hardens the Lab 03 FX summary package. It downloads historical CAD exchange rates, computes monthly averages, largest adjacent-record rate changes, and months with the greatest accumulated movement. The original summary fields are retained and `featured_shows` is added as a seeded sample of FX dates.


## Setup

```bash
conda env create -f environment.yml
conda activate fxsummary-lab04
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

```bash
python -m fxsummary.main
python -m fxsummary.main --config config/fxsummary.toml
```

The normal run requires an internet connection. The automated tests do not.

## Check it

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

## Settings

- `source_url`: historical FX API endpoint (Lab 03 URL retained).
- `timeout`: network timeout in seconds.
- `output_folder`: destination of `summary.json` and `run_info.json`.
- `seed`: reproducible random selection seed.
- `sample_size`: number of featured FX dates.
- `log_level`: DEBUG, INFO, WARNING, ERROR, or CRITICAL.

## Errors and exit codes

| Error class | Raised when | User sees |
|---|---|---|
| `SourceError` | Network or HTTP request fails | `Error: Could not download FX rates` |
| `DataError` | Invalid response, too few records, oversized sample, or output failure | `Error: <description>` |
| `SettingsError` | Missing, incomplete, or invalid TOML file | `Error: <description>` |

Exit code **0** means successful run; **1** means expected failure without a traceback.

## Reproducing a run

The seed is in `config/fxsummary.toml`. `run_info.json` records settings, Python version, and versions of pytest, mypy, and ruff. Reproduce the same `featured_shows` list by using the same seed, sample size, and identical input dates. A live API might revise its data, so exact results require archiving the source response.

## What the tests cover

Offline tests cover valid and invalid FX records, missing currency rates, three aggregations, empty input, zero-movement ties, network failures, malformed responses, warning logs, TOML validation, `tmp_path` output, deterministic selection, and `main()` success/failure exit codes. They do not exercise the real remote API because network dependence makes automated tests unreliable.


## Known limitations

- The reviewed tests mock the external source; successful retrieval from a live FX endpoint has not been demonstrated here.
- Exact `run_info.json` contents and the lab's `featured_shows` requirement are not verified for this FX-specific implementation.
- Reproducibility depends on preserving the input dataset, not only the random seed.
- The available tests do not establish behavior for every malformed configuration, missing currency, duplicate date, or unusual source response.
- The package-wide Ruff, mypy, and pytest results must be confirmed on the final submitted project.
