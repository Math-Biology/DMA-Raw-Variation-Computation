# raw_variation

**Component Code:** `#L001-U015-P26.0234`

Computes the percentage variation of each biological marker relative to the baseline measurement for DMA visit data. Accepts a consolidated multi-sheet Excel export as primary input and produces two global CSV files in long (tidy) format.

## How it works

For each visit sheet in `exported_visits.xlsx`, the module:

1. Extracts visit metadata (patient ID, visit ID, visit date) from the first data row
2. Reconstructs the measurement table, dropping padding columns and converting string values to numeric
3. Identifies the baseline for each measurement point as the minimum positive value across all rows
4. Computes the percentage variation of each marker row relative to that baseline:
   `variation = (value − base) / base × 100`
5. Appends both the original and the variation rows — in long format — to two global accumulators
6. Writes two CSV files to `Output/`:
   - `all_visits_original.csv` — raw measurements including the Base row
   - `all_visits_percentage_variation.csv` — percentage variations, Base row excluded

### Input format (`exported_visits.xlsx`)

Each sheet is named `Visita_N` and contains:

| Excel row | Content |
|---|---|
| Row 1 | Column headers read by pandas: `Patient ID`, `First Name`, `Last Name`, `Gender`, `Age at Visit`, `Date of Birth`, `Visit ID`, `Visit Date` |
| Row 2 | Visit/patient metadata values |
| Row 3 | Measurement table headers: `Marker` + point names (e.g. `LH - 3 - e [9]`) |
| Row 4 | `Base` + baseline conductance values (stored as strings) |
| Rows 5+ | Biological markers + conductance values (stored as strings) |

Columns beyond the measurement points are NaN padding and are dropped automatically.

### Output format

Both CSV files use **long format** — one row per `(visit, marker, point)` triple:

`all_visits_original.csv`:
```
visit_id, patient_id, visit_date, marker, point, value
```

`all_visits_percentage_variation.csv`:
```
visit_id, patient_id, visit_date, marker, point, percentage_variation
```

## Structure

```
raw_variation/
├── raw_variation.py          # main module
├── config.xml                # configuration parameters
├── requirements.txt          # Python dependencies
├── tests/
│   ├── conftest.py
│   └── test_raw_variation.py
├── Input/
│   ├── exported_visits.xlsx  # primary input (9930 visits, 1190 patients)
│   ├── AF/                   # legacy per-visit folders (run() entry point)
│   └── TP0010/
└── Output/
    ├── all_visits_original.csv
    └── all_visits_percentage_variation.csv
```

## Entry points

| Function | Input | Output | Status |
|---|---|---|---|
| `run_exported()` | `Input/exported_visits.xlsx` | Two global CSVs | **Primary** |
| `run()` | `Input/<visit>/` folder structure | Per-sheet `.xlsx` files | Legacy, kept for backward compatibility |

`python raw_variation.py` calls `run_exported()`.

## Configuration

`config.xml` parameters used by `run_exported`:

```xml
<file_config>
    <input_path>./Input/</input_path>
    <output_path>./Output/</output_path>
    <exported_visits_file>exported_visits.xlsx</exported_visits_file>
</file_config>
<it_config>
    <original>original</original>
    <percentage_variation>percentage_variation</percentage_variation>
</it_config>
```

The `<visit_config>` thresholds and the remaining `<it_config>` keys (`new_base`, `fane_values`, `visual_correction`, `bmri`, `final_report`) are reserved for downstream pipeline components and are not applied by this module.

## Usage

```bash
pip install -r requirements.txt
python raw_variation.py
```

## Testing

```bash
pytest tests/ -v
```

31 tests covering `clean_filename`, `load_config`, `compute_percentage_variations`, `run` (legacy), and `run_exported`.

## Requirements

See `requirements.txt`. Main dependencies: `pandas`, `numpy`, `openpyxl`.
