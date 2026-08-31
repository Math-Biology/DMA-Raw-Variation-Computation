# LINKED-TO: [REQ-AL-P26.0004]  SPEC-AL-P26.0004.1
"""Compile the oscillation analysis PDF report from the output CSV.

Workflow
--------
1. Read the median-by-point CSV and compute summary statistics.
2. Call plot_oscillations to produce the PNG figure.
3. Render the LaTeX template and write it to the report directory.
4. Run pdflatex twice (two passes ensure the table of contents is correct).
"""

import subprocess
from pathlib import Path

import pandas as pd

from plot_oscillations import plot_median_by_point

REPORT_SUBDIR = "report"


def generate_report(output_csv: Path, median_csv: Path) -> Path:
    """Generate chart, write LaTeX, compile PDF. Returns the PDF path."""
    df_osc = pd.read_csv(output_csv)
    df_median = pd.read_csv(median_csv).sort_values(
        "median_oscillation_%", ascending=False
    )
    report_dir = output_csv.parent / REPORT_SUBDIR
    report_dir.mkdir(parents=True, exist_ok=True)

    print("  Generating median-by-point chart ...")
    chart_path = plot_median_by_point(df_median, report_dir)

    stats = _compute_stats(df_osc)
    tex_path = _write_latex(report_dir, chart_path, output_csv, df_median, stats)

    print("  Compiling PDF (pass 1/2) ...")
    _run_pdflatex(tex_path)
    print("  Compiling PDF (pass 2/2) ...")
    _run_pdflatex(tex_path)

    return tex_path.with_suffix(".pdf")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_stats(df: pd.DataFrame) -> dict:
    osc = df["oscillation_%"]
    return {
        "n_rows": len(df),
        "n_visits": df["visit_id"].nunique(),
        "n_points": df["point"].nunique(),
        "mean": osc.mean(),
        "median": osc.median(),
        "zero_pct": 100.0 * (osc == 0).mean(),
    }


def _tex_escape(text: str) -> str:
    """Escape LaTeX special characters, processed character-by-character
    to avoid each replacement corrupting backslashes from a prior replacement.
    """
    specials = {
        "\\": r"\textbackslash{}",
        "_": r"\_",
        "%": r"\%",
        "&": r"\&",
        "#": r"\#",
        "$": r"\$",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(specials.get(ch, ch) for ch in text)


def _build_table_rows(df_median: pd.DataFrame) -> str:
    rows = []
    for rank, (_, row) in enumerate(df_median.iterrows(), start=1):
        point = _tex_escape(str(row["point"]))
        value = f"{row['median_oscillation_%']:.2f}"
        rows.append(f"    {rank} & {point} & {value} \\\\")
    return "\n".join(rows)


def _write_latex(
    report_dir: Path,
    chart_path: Path,
    source_csv: Path,
    df_median: pd.DataFrame,
    stats: dict,
) -> Path:
    chart_rel = chart_path.relative_to(report_dir).as_posix()
    csv_name = _tex_escape(source_csv.name)
    table_rows = _build_table_rows(df_median)
    n_points = stats["n_points"]
    n_visits = stats["n_visits"]

    body = r"""\documentclass[11pt,a4paper]{article}
\usepackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage[hidelinks]{hyperref}
\usepackage{parskip}
\usepackage{microtype}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{xcolor}

\definecolor{mathdark}{RGB}{44,95,138}

\title{%
  \textcolor{mathdark}{\textbf{Oscillation Analysis Report}}\\[4pt]
  \large """ + csv_name + r"""}
\author{Math Biology S.r.l.}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\bigskip

%%--------------------------------------------------------------
%% Dataset summary
%%--------------------------------------------------------------
\noindent
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Metric} & \textbf{Value} \\
\midrule
Rows (visit, point pairs) & """ + f"{stats['n_rows']:,}" + r""" \\
Distinct visits           & """ + f"{n_visits:,}" + r""" \\
Anatomical points         & """ + f"{n_points}" + r""" \\
Mean $\delta$             & """ + f"{stats['mean']:.2f} pp" + r""" \\
Median $\delta$ (global)  & """ + f"{stats['median']:.2f} pp" + r""" \\
Zero-$\delta$ rows        & """ + f"{stats['zero_pct']:.1f}" + r"""\% \\
\bottomrule
\end{tabular}

\newpage

%%--------------------------------------------------------------
\section{Median \texorpdfstring{$\delta$}{delta} by Anatomical Point}
%%--------------------------------------------------------------

\subsection*{How to read this chart}

Each horizontal bar represents one anatomical point.
The length of the bar is the \textbf{median of all $\delta$ values} computed for
that point across all """ + f"{n_visits:,}" + r""" visits in the dataset.

\textbf{Sorting.}
Points are displayed in descending order: the bar at the top corresponds to the
anatomical point with the highest typical oscillation in the population, and the
bar at the bottom corresponds to the most stable point.

\textbf{How the median is calculated.}
The pipeline first computes one $\delta$ value for every (visit, anatomical point)
pair --- approximately """ + f"{stats['n_rows'] // n_points:,}" + r""" values per
point across all visits.
It then groups these values by anatomical point and applies the median to each
group (function \texttt{compute\_median\_by\_point()} in
\texttt{run\_oscillation.py}, using \texttt{pandas.Series.median()}).
The result is one representative value per point: the $\delta$ that half of
the visits fall below and half fall above for that location.

\textbf{Why the median and not the mean.}
The distribution of $\delta$ is right-skewed with a non-trivial proportion of
zero values (""" + f"{stats['zero_pct']:.1f}" + r"""\% of all rows).
The median is therefore more representative of the central tendency for each
point than the mean, which would be inflated by occasional extreme values.

\textbf{Why some medians are zero.}
$\delta$ is defined as $0.0$ whenever a (visit, point) group contains fewer
than two strictly positive values among its 24 markers --- that is, when there
is not enough signal to compute a meaningful oscillation range.
If more than half of the visits for a given anatomical point produce $\delta = 0$,
the median for that point will also be zero.
In this dataset """ + f"{stats['zero_pct']:.1f}" + r"""\% of all (visit, point)
pairs have $\delta = 0$.
A zero median is therefore a meaningful clinical signal: it identifies anatomical
points that, for the majority of visits, do not exhibit measurable oscillation.

\textbf{Value labels.}
The numeric value of the median $\delta$ (in percentage points, pp) is printed
to the right of each bar for direct reading.
Percentage points (pp) express the difference between two percentage values:
since the input data are percentage variations, $\delta = \max - \min$ of those
values yields a result in pp, not a further relative percentage.

\textbf{What it tells you.}
\begin{itemize}
  \item \textit{Bar length ranking}: which anatomical points are most and least
    oscillatory on average across the entire patient population.
  \item \textit{Magnitude}: the absolute scale of the median oscillation gives
    a sense of how large the typical $\delta$ is for each location.
  \item \textit{Zero bars}: points with a zero bar are clinically stable in
    more than half of the recorded visits.
  \item \textit{Groups}: visual clusters of bars of similar length suggest
    anatomical regions that behave similarly.
\end{itemize}

\begin{figure}[p]
  \centering
  \includegraphics[width=\textwidth,height=0.92\textheight,keepaspectratio]{""" + chart_rel + r"""}
  \caption{Median $\delta$ per anatomical point, sorted descending.
    Each bar represents the median of all oscillation values computed
    for that point across all visits.
    Values are in percentage points (pp).}
  \label{fig:median_by_point}
\end{figure}

\newpage

%%--------------------------------------------------------------
\section{Median \texorpdfstring{$\delta$}{delta} per Point --- Full Table}
%%--------------------------------------------------------------

The following table reports the exact median $\delta$ (in percentage points)
for each of the """ + str(n_points) + r""" anatomical points, sorted in descending order.
The values are identical to those displayed in Figure~\ref{fig:median_by_point}
and are provided here for precise reading and comparison.

\bigskip

\begin{longtable}{@{}rlr@{}}
\toprule
\textbf{Rank} & \textbf{Anatomical Point} & \textbf{Median $\delta$ (pp)} \\
\midrule
\endfirsthead
\multicolumn{3}{l}{\small\itshape (continued from previous page)} \\
\toprule
\textbf{Rank} & \textbf{Anatomical Point} & \textbf{Median $\delta$ (pp)} \\
\midrule
\endhead
\midrule
\multicolumn{3}{r}{\small\itshape (continued on next page)} \\
\endfoot
\bottomrule
\endlastfoot
""" + table_rows + r"""
\end{longtable}

\end{document}
"""

    tex_path = report_dir / "oscillation_report.tex"
    tex_path.write_text(body, encoding="utf-8")
    return tex_path


def _run_pdflatex(tex_path: Path) -> None:
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_path.name],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-40:])
        raise RuntimeError(f"pdflatex failed:\n{tail}")
