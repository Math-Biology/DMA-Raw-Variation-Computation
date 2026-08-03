# CLAUDE.md — raw_variation component

**Component:** `#L001-U015-P26.0234` | **Linked to:** `REQ-COMP-P26.0073`

## What this is

A single-file Python module that computes percentage variations of bioelectrical measurements for the DMA (Digital Medicine Analyzer) pipeline. It reads a consolidated Excel export of ~10 000 visits and writes two global CSVs used by downstream pipeline components.

## Project layout

```
raw_variation.py      # all logic lives here — no src/ subdirectory
config.xml            # runtime parameters
requirements.txt
tests/
    conftest.py       # sys.path fix so raw_variation is importable
    test_raw_variation.py
Input/
    exported_visits.xlsx    # primary input
    AF/                     # legacy input folder (run() only)
    TP0010/                 # legacy input folder (run() only)
Output/                     # created at runtime if absent
exported_visits.xlsx        # leftover root copy — NOT used at runtime (Input/ copy is used)
```

## How to run

```bash
pip install -r requirements.txt
python raw_variation.py          # calls run_exported()
```

## How to test

```bash
pytest tests/ -v                 # 31 tests, ~2 s
```

Tests are self-contained (all use `tmp_path`/`tmp_path_factory`). No real input files are needed.

## Entry points

### `run_exported(config_path="config.xml")` — PRIMARY
Reads `Input/exported_visits.xlsx` (multi-sheet, one sheet per visit).  
Writes `Output/all_visits_original.csv` and `Output/all_visits_percentage_variation.csv`.

### `run(config_path="config.xml")` — LEGACY
Walks `Input/<visit-folder>/` subdirectories.  
Writes per-sheet `.xlsx` files under `Output/`.  
Not called from `__main__`; kept for backward compatibility only.

## Key functions

| Function | Role | Called by |
|---|---|---|
| `load_config(xml_file)` | Parses `config.xml`, returns three dicts | Both entry points |
| `compute_percentage_variations(df)` | Core math — see below | Both entry points |
| `clean_filename(filename)` | Strips filesystem-forbidden chars | `run()` only |
| `run_exported()` | Primary entry point | `__main__` |
| `run()` | Legacy entry point | Not called automatically |

### `compute_percentage_variations(df)` — core logic

- Input: DataFrame where column 0 is a label column and columns 1+ are numeric measurement points. Row 0 is the baseline row.
- For each measurement column: `base = min positive value across all rows`. If row-0 value already is the minimum, it is used directly.
- Formula: `(value − base) / base × 100` applied to rows 1+.
- Row 0 (baseline) is dropped from the output.
- NaN values propagate through the formula unchanged.

## Input format (`exported_visits.xlsx`)

Each sheet `Visita_N` has this structure when read by `pd.read_excel()`:

```
df.columns  → Patient ID | First Name | Last Name | ... | Visit ID | Visit Date  (from Excel row 1)
df.iloc[0]  → metadata values (patient_id, visit_id, visit_date, ...)
df.iloc[1]  → "Marker" | "LH - 3 - e [9]" | "PT - 2 [2]" | NaN | NaN ...
df.iloc[2]  → "Base"   | "100"             | "200"         | NaN | NaN ...   (strings!)
df.iloc[3+] → marker name | value string   | value string  | NaN | NaN ...
```

**Critical:** all measurement values are strings. `pd.to_numeric(errors="coerce")` is applied in `run_exported` before passing to `compute_percentage_variations`. The function itself expects numeric input.

Columns with NaN headers (padding from metadata overflow and wide-sheet unnamed columns) are dropped before processing.

## Output format

Long (tidy) format — one row per `(visit, marker, point)` triple.

`all_visits_original.csv` columns: `visit_id, patient_id, visit_date, marker, point, value`  
`all_visits_percentage_variation.csv` columns: `visit_id, patient_id, visit_date, marker, point, percentage_variation`

The `original` CSV includes the `Base` row. The `percentage_variation` CSV does not.

## Configuration keys

### Used by `run_exported`
- `file_config/input_path`
- `file_config/output_path`
- `file_config/exported_visits_file`
- `it_config/original` — suffix for the original CSV filename
- `it_config/percentage_variation` — suffix for the variation CSV filename

### Used by `run` (legacy)
Same as above except `exported_visits_file`; also uses `it_config/original` and `it_config/percentage_variation`.

### Loaded but not applied by this component
- `visit_config/threshold_1` through `threshold_8` — reserved for downstream pipeline stages
- `it_config/new_base`, `fane_values`, `visual_correction`, `bmri`, `final_report` — reserved for downstream pipeline stages

**Do not remove these config keys** — they are read and validated by other components in the DMA pipeline.

## Known unused / reserved items

| Item | Location | Status |
|---|---|---|
| `exported_visits.xlsx` (root) | project root | Leftover copy; `Input/exported_visits.xlsx` is the file actually used at runtime. Safe to delete from root. |
| `visit_config` variable | `run_exported()` line 122 | Loaded by `load_config()` but never accessed inside `run_exported`. Thresholds reserved for downstream components. |
| `threshold1` variable | `run()` line 70 | Loaded but not applied (`# noqa: F841`). Reserved for a future filtering step. |
| `clean_filename()` | `raw_variation.py` line 10 | Only used by legacy `run()`. Not used by `run_exported`. |
| `it_config` keys beyond `original`/`percentage_variation` | `config.xml` | Reserved for downstream pipeline components. |

## Traceability

All functions added to `raw_variation.py` must include the comment anchor:
```python
# LINKED-TO: [REQ-COMP-P26.0073]
```
The pre-commit hook (`SOP #L001-U015-P26.0141`) enforces this on `.py` files.
