# LINKED-TO: [REQ-AL-P26.0004]  SPEC-AL-P26.0004.1 — FANE Trigger Condition / delta computation
"""Apply compute_column_oscillation to every (visit, anatomical point) group
in the raw-variations file found in data/input/, and write results to data/output/.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / "src"))
from oscillation import compute_column_oscillation

INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")

GROUP_KEYS = ["visit_id", "patient_id", "visit_date", "point"]
VALUE_COL = "percentage_variation"
OUTPUT_COL = "oscillation_%"
MEDIAN_COL = "median_oscillation_%"


def find_input_file() -> Path:
    candidates = list(INPUT_DIR.glob("*.csv"))
    if not candidates:
        raise FileNotFoundError(f"No CSV file found in {INPUT_DIR}")
    if len(candidates) > 1:
        raise ValueError(
            f"Multiple CSV files found in {INPUT_DIR}: {[c.name for c in candidates]}. "
            "Specify the file explicitly."
        )
    return candidates[0]


def run(input_path: Path, output_path: Path) -> None:
    print(f"Reading {input_path} ...")
    df = pd.read_csv(input_path)

    print(f"Computing oscillations for {df[GROUP_KEYS[0]].nunique()} visits ...")
    result = (
        df.groupby(GROUP_KEYS)[VALUE_COL]
        .apply(compute_column_oscillation)
        .reset_index()
        .rename(columns={VALUE_COL: OUTPUT_COL})
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    print(f"Saved {len(result):,} rows → {output_path}")


def compute_median_by_point(output_path: Path) -> Path:
    """Compute median δ per anatomical point and save to a sidecar CSV."""
    df = pd.read_csv(output_path)
    median_path = output_path.with_name(output_path.stem + "_median_by_point.csv")
    median = (
        df.groupby("point")[OUTPUT_COL]
        .median()
        .reset_index()
        .rename(columns={OUTPUT_COL: MEDIAN_COL})
        .sort_values(MEDIAN_COL, ascending=False)
    )
    median.to_csv(median_path, index=False)
    print(f"Saved median by point ({len(median)} points) → {median_path}")
    return median_path


if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2])
    elif len(sys.argv) == 1:
        input_path = find_input_file()
        output_path = OUTPUT_DIR / (input_path.stem + "_oscillations.csv")
    else:
        print("Usage: python run_oscillation.py [<input.csv> <output.csv>]")
        sys.exit(1)

    run(input_path, output_path)
    median_path = compute_median_by_point(output_path)

    from generate_report import generate_report
    print("Generating report ...")
    try:
        pdf_path = generate_report(output_path, median_path)
        print(f"Report saved → {pdf_path}")
    except Exception as exc:
        print(f"Warning: report generation failed — {exc}")
