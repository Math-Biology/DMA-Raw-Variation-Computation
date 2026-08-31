# LINKED-TO: [REQ-AL-P26.0004]  SPEC-AL-P26.0004.1
"""Generate diagnostic charts from the oscillation summary data."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

FIGURES_SUBDIR = "figures"
DPI = 150


def plot_median_by_point(df_median: pd.DataFrame, out_dir: Path) -> Path:
    """Horizontal bar chart of median δ per anatomical point, sorted descending.

    df_median must have columns 'point' and 'median_oscillation_%'.
    """
    fig_dir = out_dir / FIGURES_SUBDIR
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / "median_by_point.png"

    df_plot = df_median.sort_values("median_oscillation_%", ascending=True)
    points = df_plot["point"].tolist()
    values = df_plot["median_oscillation_%"].tolist()

    n = len(points)
    max_val = max(values) if values else 1.0

    fig, ax = plt.subplots(figsize=(12, max(10, n * 0.30 + 2)))

    bars = ax.barh(range(n), values, color="#4472C4", height=0.65, alpha=0.85)

    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(
            val + max_val * 0.01,
            i,
            f"{val:.1f}",
            va="center",
            ha="left",
            fontsize=7,
            color="#333333",
        )

    ax.set_yticks(range(n))
    ax.set_yticklabels(points, fontsize=8)
    ax.set_xlabel("Median oscillation δ (percentage points)", fontsize=10)
    ax.set_title(
        "Median δ by Anatomical Point\n"
        "(median computed across all visits, sorted by descending value)",
        fontsize=11,
        pad=10,
    )
    ax.set_xlim(left=0, right=max_val * 1.14)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.55)
    ax.grid(axis="x", which="minor", linestyle=":", linewidth=0.3, alpha=0.35)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return out_path
