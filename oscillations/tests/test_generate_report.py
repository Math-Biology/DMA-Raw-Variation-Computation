import pandas as pd
import pytest

from generate_report import _tex_escape, _compute_stats, _build_table_rows


class TestTexEscape:
    def test_underscore_escaped(self):
        assert _tex_escape("a_b") == r"a\_b"

    def test_backslash_becomes_textbackslash(self):
        assert _tex_escape("a\\b") == r"a\textbackslash{}b"

    def test_no_double_escape(self):
        # underscore must become \_  not \textbackslash{}_
        result = _tex_escape("file_name.csv")
        assert r"\_" in result
        assert "textbackslash" not in result

    def test_plain_text_unchanged(self):
        assert _tex_escape("hello world.csv") == "hello world.csv"


class TestComputeStats:
    def setup_method(self):
        self.df = pd.DataFrame({
            "visit_id":     [1,    1,     2,    2   ],
            "patient_id":   [10,   10,    11,   11  ],
            "visit_date":   ["2024-01-01"] * 4,
            "point":        ["A",  "B",   "A",  "B" ],
            "oscillation_%":[0.0, 100.0, 50.0, 200.0],
        })

    def test_n_rows(self):
        assert _compute_stats(self.df)["n_rows"] == 4

    def test_n_visits(self):
        assert _compute_stats(self.df)["n_visits"] == 2

    def test_mean(self):
        assert _compute_stats(self.df)["mean"] == pytest.approx(87.5)

    def test_zero_pct(self):
        # one zero out of four rows = 25 %
        assert _compute_stats(self.df)["zero_pct"] == pytest.approx(25.0)


class TestBuildTableRows:
    def test_rank_starts_at_one(self):
        df = pd.DataFrame({"point": ["A"], "median_oscillation_%": [42.0]})
        rows = _build_table_rows(df)
        assert rows.startswith("    1 &")

    def test_value_formatted_two_decimals(self):
        df = pd.DataFrame({"point": ["A"], "median_oscillation_%": [42.1]})
        rows = _build_table_rows(df)
        assert "42.10" in rows

    def test_row_ends_with_latex_newline(self):
        df = pd.DataFrame({"point": ["A"], "median_oscillation_%": [1.0]})
        rows = _build_table_rows(df)
        assert rows.endswith("\\\\")
