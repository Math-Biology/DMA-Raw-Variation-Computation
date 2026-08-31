import pandas as pd
import pytest

import run_oscillation


COLUMNS = ["visit_id", "patient_id", "visit_date", "point", "percentage_variation"]

SAMPLE_ROWS = [
    # visit 1, point "LH [1]": values 100, 200, 300  -> delta = 200
    (1, 10, "2024-01-01", "LH [1]", 100.0),
    (1, 10, "2024-01-01", "LH [1]", 200.0),
    (1, 10, "2024-01-01", "LH [1]", 300.0),
    # visit 1, point "RF [2]": values 0, 50, 150  -> delta = 100 (0 excluded)
    (1, 10, "2024-01-01", "RF [2]", 0.0),
    (1, 10, "2024-01-01", "RF [2]", 50.0),
    (1, 10, "2024-01-01", "RF [2]", 150.0),
    # visit 2, point "LH [1]": identical values  -> delta = 0
    (2, 11, "2024-01-02", "LH [1]", 10.0),
    (2, 11, "2024-01-02", "LH [1]", 10.0),
]


def make_input_csv(tmp_path, rows=SAMPLE_ROWS, filename="variations.csv"):
    path = tmp_path / filename
    pd.DataFrame(rows, columns=COLUMNS).to_csv(path, index=False)
    return path


class TestFindInputFile:
    def test_single_csv_returned(self, tmp_path, monkeypatch):
        (tmp_path / "data.csv").touch()
        monkeypatch.setattr(run_oscillation, "INPUT_DIR", tmp_path)
        assert run_oscillation.find_input_file() == tmp_path / "data.csv"

    def test_no_csv_raises_file_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_oscillation, "INPUT_DIR", tmp_path)
        with pytest.raises(FileNotFoundError):
            run_oscillation.find_input_file()

    def test_multiple_csvs_raises_value_error(self, tmp_path, monkeypatch):
        (tmp_path / "a.csv").touch()
        (tmp_path / "b.csv").touch()
        monkeypatch.setattr(run_oscillation, "INPUT_DIR", tmp_path)
        with pytest.raises(ValueError):
            run_oscillation.find_input_file()


class TestRun:
    def test_output_file_created(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_oscillation, "OUTPUT_DIR", tmp_path)
        output_path = tmp_path / "out.csv"
        run_oscillation.run(make_input_csv(tmp_path), output_path)
        assert output_path.exists()

    def test_output_schema(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_oscillation, "OUTPUT_DIR", tmp_path)
        output_path = tmp_path / "out.csv"
        run_oscillation.run(make_input_csv(tmp_path), output_path)
        out = pd.read_csv(output_path)
        assert list(out.columns) == ["visit_id", "patient_id", "visit_date", "point", "oscillation_%"]

    def test_one_row_per_visit_point(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_oscillation, "OUTPUT_DIR", tmp_path)
        output_path = tmp_path / "out.csv"
        run_oscillation.run(make_input_csv(tmp_path), output_path)
        out = pd.read_csv(output_path)
        # 2 points for visit 1, 1 point for visit 2
        assert len(out) == 3

    def test_oscillation_values(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_oscillation, "OUTPUT_DIR", tmp_path)
        output_path = tmp_path / "out.csv"
        run_oscillation.run(make_input_csv(tmp_path), output_path)
        out = pd.read_csv(output_path)

        def get(visit, point):
            return out[(out["visit_id"] == visit) & (out["point"] == point)]["oscillation_%"].iloc[0]

        assert get(1, "LH [1]") == pytest.approx(200.0)
        assert get(1, "RF [2]") == pytest.approx(100.0)
        assert get(2, "LH [1]") == pytest.approx(0.0)

    def test_output_dir_created_if_missing(self, tmp_path, monkeypatch):
        new_dir = tmp_path / "new_subdir"
        monkeypatch.setattr(run_oscillation, "OUTPUT_DIR", new_dir)
        output_path = new_dir / "out.csv"
        run_oscillation.run(make_input_csv(tmp_path), output_path)
        assert output_path.exists()


OSC_COLUMNS = ["visit_id", "patient_id", "visit_date", "point", "oscillation_%"]

OSC_ROWS = [
    # point "A": deltas [200.0, 0.0, 50.0] -> median = 50.0
    (1, 10, "2024-01-01", "A", 200.0),
    (2, 11, "2024-01-02", "A", 0.0),
    (3, 12, "2024-01-03", "A", 50.0),
    # point "B": deltas [100.0, 80.0] -> median = 90.0
    (1, 10, "2024-01-01", "B", 100.0),
    (2, 11, "2024-01-02", "B", 80.0),
]


def make_oscillation_csv(tmp_path, rows=OSC_ROWS, filename="out.csv"):
    path = tmp_path / filename
    pd.DataFrame(rows, columns=OSC_COLUMNS).to_csv(path, index=False)
    return path


class TestComputeMedianByPoint:
    def test_output_file_created(self, tmp_path):
        output_path = make_oscillation_csv(tmp_path)
        median_path = run_oscillation.compute_median_by_point(output_path)
        assert median_path.exists()

    def test_output_schema(self, tmp_path):
        output_path = make_oscillation_csv(tmp_path)
        median_path = run_oscillation.compute_median_by_point(output_path)
        out = pd.read_csv(median_path)
        assert list(out.columns) == ["point", "median_oscillation_%"]

    def test_one_row_per_point(self, tmp_path):
        output_path = make_oscillation_csv(tmp_path)
        median_path = run_oscillation.compute_median_by_point(output_path)
        out = pd.read_csv(median_path)
        assert len(out) == 2

    def test_median_values(self, tmp_path):
        output_path = make_oscillation_csv(tmp_path)
        median_path = run_oscillation.compute_median_by_point(output_path)
        out = pd.read_csv(median_path).set_index("point")
        assert out.loc["A", "median_oscillation_%"] == pytest.approx(50.0)
        assert out.loc["B", "median_oscillation_%"] == pytest.approx(90.0)

    def test_sorted_descending(self, tmp_path):
        output_path = make_oscillation_csv(tmp_path)
        median_path = run_oscillation.compute_median_by_point(output_path)
        out = pd.read_csv(median_path)
        values = out["median_oscillation_%"].tolist()
        assert values == sorted(values, reverse=True)
