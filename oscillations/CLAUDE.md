# CLAUDE.md — Oscillations

## Project purpose

Computes the oscillation δ for every (visit, anatomical point) pair from a dataset of raw percentage variations. No corrective rules are applied to the input; δ is the final output. After each pipeline run a PDF report is compiled automatically.

---

## Repository layout

```
run_oscillation.py              # pipeline entry point
oscillation_formula.md          # formula specification and references
pyproject.toml                  # pytest configuration (pythonpath)
src/
  oscillation.py                # core computation functions
  plot_oscillations.py          # chart generation (median bar chart)
  generate_report.py            # LaTeX report rendering and PDF compilation
data/
  input/                        # source CSV files (raw variations)
  output/                       # computed oscillation CSVs and report
    report/
      figures/                  # generated PNG charts
      oscillation_report.tex    # rendered LaTeX source
      oscillation_report.pdf    # compiled report (auto-generated)
tests/
  conftest.py                   # adds project root to sys.path
  test_oscillation.py           # unit tests for oscillation.py
  test_run_oscillation.py       # integration tests for run_oscillation.py
  test_plot_oscillations.py     # unit tests for plot_oscillations.py
  test_generate_report.py       # unit tests for generate_report.py
```

---

## Core formula

```
δ = max(positive_values) − min(positive_values)
```

`positive_values` = all values in the series that are strictly > 0 (zeros and negatives excluded).  
Returns `0.0` if fewer than two strictly positive values exist.  
δ is expressed in percentage points.

See `oscillation_formula.md` for full specification and traceability references.

---

## Modules

### `src/oscillation.py`

| Symbol | Description |
|---|---|
| `compute_column_oscillation(column)` | Applies the δ formula to a single `pd.Series`. |
| `compute_oscillations(df)` | Applies `compute_column_oscillation` to every numeric column of a wide-format DataFrame. Returns a `pd.Series` named `oscillation_%`. |

### `run_oscillation.py`

Pipeline entry point. Reads the single CSV in `data/input/`, groups rows by `(visit_id, patient_id, visit_date, point)`, applies `compute_column_oscillation` to each group's `percentage_variation` series, writes results to `data/output/`, computes the median δ per anatomical point, and compiles the PDF report.

| Symbol | Value / description |
|---|---|
| `INPUT_DIR` | `data/input` |
| `OUTPUT_DIR` | `data/output` |
| `GROUP_KEYS` | `["visit_id", "patient_id", "visit_date", "point"]` |
| `VALUE_COL` | `percentage_variation` |
| `OUTPUT_COL` | `oscillation_%` |
| `MEDIAN_COL` | `median_oscillation_%` |
| `run(input_path, output_path)` | Core computation: reads input CSV, computes δ for every group, writes oscillation CSV. |
| `compute_median_by_point(output_path)` | Reads the oscillation CSV, groups by `point`, computes median δ, writes sidecar CSV `*_median_by_point.csv`. |

### `src/plot_oscillations.py`

| Symbol | Description |
|---|---|
| `plot_median_by_point(df_median, out_dir)` | Horizontal bar chart of median δ per anatomical point, sorted descending. Saves to `out_dir/figures/median_by_point.png`. `df_median` must have columns `point` and `median_oscillation_%`. |

### `src/generate_report.py`

| Symbol | Description |
|---|---|
| `generate_report(output_csv, median_csv)` | Reads both CSVs, generates the chart, renders the LaTeX template, runs `pdflatex` twice, returns the PDF path. |

---

## Data

### Input

Long-format CSV with one row per (visit, marker, anatomical point) triple.

| Column | Type | Description |
|---|---|---|
| `visit_id` | int | Visit identifier |
| `patient_id` | int | Patient identifier |
| `visit_date` | date | Date of the visit |
| `marker` | string | Marker name |
| `point` | string | Anatomical point name |
| `percentage_variation` | float | Raw percentage variation (uncorrected) |

Current file: `all_visits_percentage_variation.csv` — 775 293 rows, 7 955 visits, 62 anatomical points, 24 markers per (visit, point).

### Output

**Oscillation CSV** — one row per (visit, anatomical point):

| Column | Type | Description |
|---|---|---|
| `visit_id` | int | Visit identifier |
| `patient_id` | int | Patient identifier |
| `visit_date` | date | Date of the visit |
| `point` | string | Anatomical point name |
| `oscillation_%` | float | δ in percentage points |

Current: `all_visits_percentage_variation_oscillations.csv` — 80 480 rows.

**Median-by-point CSV** — one row per anatomical point:

| Column | Type | Description |
|---|---|---|
| `point` | string | Anatomical point name |
| `median_oscillation_%` | float | Median δ across all visits, in percentage points |

Current: `all_visits_percentage_variation_oscillations_median_by_point.csv` — 62 rows.

**PDF report** — `data/output/report/oscillation_report.pdf`, compiled automatically at every pipeline run. Contains a dataset summary table, a ranked bar chart of median δ per anatomical point, and the full median-by-point table.

---

## Running the pipeline

```bash
# auto-discovers the single CSV in data/input/
python run_oscillation.py

# explicit paths
python run_oscillation.py data/input/my_file.csv data/output/my_output.csv
```

The pipeline always produces three outputs: the oscillation CSV, the median-by-point CSV, and the PDF report.

---

## Running the tests

```bash
python -m pytest tests/ -v
```

40 tests — all must pass before any change is considered complete.

---

## Language rule

Everything in this project is written in English: source code, variable names, comments, docstrings, file names, and all Markdown text.

## Traceability

Every application Python file must include at least one anchor of the form:

```python
# LINKED-TO: [REQ-AL-P26.0004]  SPEC-AL-P26.0004.1
```

This is enforced by the `math-b-agentic-workflow` pre-tool hook (SOP #L001-U015-P26.0141). The hook applies only to `.py` files under `src/`; test files are explicitly excluded.

## Scope boundaries

- The FANE corrective family `δⱼ = δ / (j+2) / θ₅` is **not implemented** and is out of scope.
- Input data is always raw (uncorrected). Rule A and any other correction rules are applied upstream, outside this project.
