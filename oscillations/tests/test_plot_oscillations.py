import pandas as pd
import matplotlib
matplotlib.use("Agg")

from plot_oscillations import plot_median_by_point


MEDIAN_DF = pd.DataFrame({
    "point": ["A [1]", "B [2]", "C [3]"],
    "median_oscillation_%": [120.0, 45.0, 0.0],
})


class TestPlotMedianByPoint:
    def test_output_file_created(self, tmp_path):
        out = plot_median_by_point(MEDIAN_DF, tmp_path)
        assert out.exists()

    def test_output_is_png(self, tmp_path):
        out = plot_median_by_point(MEDIAN_DF, tmp_path)
        assert out.suffix == ".png"
        with open(out, "rb") as f:
            assert f.read(4) == b"\x89PNG"

    def test_figures_subdirectory_created(self, tmp_path):
        plot_median_by_point(MEDIAN_DF, tmp_path)
        assert (tmp_path / "figures").is_dir()
