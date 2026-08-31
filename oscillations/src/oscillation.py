# LINKED-TO: [REQ-AL-P26.0004]  SPEC-AL-P26.0004.1 — FANE Trigger Condition / delta computation
import pandas as pd
import numpy as np
import sys


def compute_column_oscillation(column: pd.Series) -> float:
    """δ = max(column) − min_nonzero(column)

    Returns 0.0 if the column does not contain at least two distinct positive values.
    """
    positive_values = column[column > 0].dropna()
    if len(positive_values) < 2:
        return 0.0
    return float(positive_values.max() - positive_values.min())


def compute_oscillations(df: pd.DataFrame) -> pd.Series:
    """Compute δ for every numeric column of the DataFrame.

    Assumes the first column holds marker names (string) and the remaining
    columns are anatomical points (numeric).

    Returns a Series with index = column name, values = δ in percentage points.
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    return pd.Series(
        {col: compute_column_oscillation(df[col]) for col in numeric_columns},
        name="oscillation_%"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python oscillation.py <path_to_variations_file.xlsx>")
        sys.exit(1)

    filepath = sys.argv[1]
    df = pd.read_excel(filepath)

    oscillations = compute_oscillations(df)

    print("\nPercentage oscillations per anatomical point:")
    print(oscillations.to_string())

    output_path = filepath.replace(".xlsx", "_oscillations.xlsx")
    oscillations.to_frame().to_excel(output_path)
    print(f"\nResult saved to: {output_path}")
