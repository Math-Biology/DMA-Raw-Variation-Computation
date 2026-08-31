import numpy as np
import pandas as pd
import pytest

from oscillation import compute_column_oscillation, compute_oscillations


class TestComputeColumnOscillation:
    def test_normal_range(self):
        assert compute_column_oscillation(pd.Series([100.0, 200.0, 300.0])) == pytest.approx(200.0)

    def test_zeros_excluded_from_min(self):
        # 0 must not count as min_nonzero
        assert compute_column_oscillation(pd.Series([0.0, 100.0, 200.0])) == pytest.approx(100.0)

    def test_negatives_excluded(self):
        assert compute_column_oscillation(pd.Series([-50.0, 100.0, 300.0])) == pytest.approx(200.0)

    def test_single_positive_returns_zero(self):
        assert compute_column_oscillation(pd.Series([0.0, 0.0, 100.0])) == 0.0

    def test_all_zeros_returns_zero(self):
        assert compute_column_oscillation(pd.Series([0.0, 0.0, 0.0])) == 0.0

    def test_empty_series_returns_zero(self):
        assert compute_column_oscillation(pd.Series([], dtype=float)) == 0.0

    def test_all_negatives_returns_zero(self):
        assert compute_column_oscillation(pd.Series([-1.0, -2.0, -3.0])) == 0.0

    def test_nan_values_ignored(self):
        assert compute_column_oscillation(pd.Series([np.nan, 100.0, 200.0])) == pytest.approx(100.0)

    def test_identical_positive_values(self):
        assert compute_column_oscillation(pd.Series([100.0, 100.0, 100.0])) == pytest.approx(0.0)

    def test_returns_float(self):
        result = compute_column_oscillation(pd.Series([100.0, 200.0]))
        assert isinstance(result, float)


class TestComputeOscillations:
    def _make_df(self):
        return pd.DataFrame({
            "marker":  ["A", "B", "C"],
            "point_1": [100.0, 200.0, 300.0],
            "point_2": [0.0,   50.0,  150.0],
        })

    def test_output_name(self):
        assert compute_oscillations(self._make_df()).name == "oscillation_%"

    def test_index_contains_numeric_columns_only(self):
        result = compute_oscillations(self._make_df())
        assert set(result.index) == {"point_1", "point_2"}
        assert "marker" not in result.index

    def test_values(self):
        result = compute_oscillations(self._make_df())
        assert result["point_1"] == pytest.approx(200.0)
        assert result["point_2"] == pytest.approx(100.0)
