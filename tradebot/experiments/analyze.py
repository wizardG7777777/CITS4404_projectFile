"""Aggregate the experiment summary and write a stats.json report.

Usage from the repo root (after ``run_matrix`` has produced summary.csv):

    uv run python -m tradebot.experiments.analyze

Outputs ``results/stats.json`` containing:

  * per-(algorithm, bot) descriptive statistics (mean / std / min / max),
  * Mann-Whitney U two-sided p-values for every algorithm pair on each bot
    (the test D1 HHO synopsis cites as the validation methodology in
    Heidari et al. 2019, equivalent to the Wilcoxon rank-sum test).

The Mann-Whitney U implementation here uses the normal approximation. With
five seeds per group the approximation is borderline, but it is sufficient
to flag qualitative direction; report claims should be hedged accordingly.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
SUMMARY_CSV = REPO_ROOT / "results" / "summary.csv"
STATS_JSON = REPO_ROOT / "results" / "stats.json"


# --------------------------------------------------------------------------- #
# Statistics primitives
# --------------------------------------------------------------------------- #


def mannwhitneyu_pvalue(a: np.ndarray, b: np.ndarray) -> float:
    """Two-sided Mann-Whitney U test p-value via the normal approximation.

    References:
      Mann, H.B. & Whitney, D.R. (1947). "On a Test of Whether one of Two
      Random Variables is Stochastically Larger than the Other."
      Ann. Math. Stat., 18(1), 50-60.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n1, n2 = a.size, b.size
    if n1 == 0 or n2 == 0:
        return 1.0

    combined = np.concatenate([a, b])
    order = np.argsort(combined, kind="mergesort")
    ranks = np.empty(combined.size, dtype=np.float64)
    ranks[order] = np.arange(1, combined.size + 1, dtype=np.float64)

    # Tie correction: average tied ranks (matches Wilcoxon rank-sum convention).
    sorted_vals = combined[order]
    i = 0
    while i < sorted_vals.size:
        j = i + 1
        while j < sorted_vals.size and sorted_vals[j] == sorted_vals[i]:
            j += 1
        if j - i > 1:
            avg = (ranks[order[i]] + ranks[order[j - 1]]) / 2.0
            for k in range(i, j):
                ranks[order[k]] = avg
        i = j

    rank_sum_a = ranks[:n1].sum()
    U = rank_sum_a - n1 * (n1 + 1) / 2.0
    U = min(U, n1 * n2 - U)

    mu = n1 * n2 / 2.0
    var = n1 * n2 * (n1 + n2 + 1) / 12.0
    if var <= 0:
        return 1.0
    z = (U - mu) / math.sqrt(var)
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def descriptive_stats(values: np.ndarray) -> dict:
    return {
        "n": int(values.size),
        "mean": float(values.mean()),
        "std": float(values.std(ddof=1)) if values.size > 1 else 0.0,
        "min": float(values.min()),
        "max": float(values.max()),
        "median": float(np.median(values)),
    }


# --------------------------------------------------------------------------- #
# Top-level report assembly
# --------------------------------------------------------------------------- #


def aggregate(summary: pd.DataFrame) -> dict:
    """Build the stats dict from a summary dataframe (one row per run)."""
    out: dict = {"per_bot": {}}
    bots = sorted(summary["bot"].unique())
    for bot in bots:
        bot_rows = summary[summary["bot"] == bot]
        algos = sorted(bot_rows["algorithm"].unique())

        descriptive = {}
        for algo in algos:
            vals = bot_rows[bot_rows["algorithm"] == algo]["best_fitness"].to_numpy()
            descriptive[algo] = descriptive_stats(vals)

        pvalues = {}
        for a, b in itertools.combinations(algos, 2):
            va = bot_rows[bot_rows["algorithm"] == a]["best_fitness"].to_numpy()
            vb = bot_rows[bot_rows["algorithm"] == b]["best_fitness"].to_numpy()
            pvalues[f"{a}_vs_{b}"] = mannwhitneyu_pvalue(va, vb)

        out["per_bot"][bot] = {
            "descriptive": descriptive,
            "mannwhitneyu_p_two_sided": pvalues,
        }

    # Wall time roll-up (not seed-stratified, just for cost reporting).
    out["wall_time_s"] = {
        "total": float(summary["wall_time_s"].sum()),
        "mean_per_run": float(summary["wall_time_s"].mean()),
    }
    return out


def write_stats(summary_path: Path = SUMMARY_CSV, stats_path: Path = STATS_JSON) -> dict:
    if not summary_path.exists():
        raise FileNotFoundError(
            f"{summary_path} not found. Run `python -m tradebot.experiments.run_matrix` first."
        )
    summary = pd.read_csv(summary_path)
    stats = aggregate(summary)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.write_text(json.dumps(stats, indent=2))
    return stats


# --------------------------------------------------------------------------- #
# CLI pretty-printer
# --------------------------------------------------------------------------- #


def _print_stats(stats: dict) -> None:
    for bot, block in stats["per_bot"].items():
        print(f"\n== {bot} ==")
        print(f"  {'algorithm':<14s}  {'mean':>10s}  {'std':>8s}  {'min':>10s}  {'max':>10s}")
        for algo, d in block["descriptive"].items():
            print(
                f"  {algo:<14s}  ${d['mean']:>8.0f}  ${d['std']:>6.0f}  "
                f"${d['min']:>8.0f}  ${d['max']:>8.0f}"
            )
        print("  Mann-Whitney U (two-sided p-values):")
        for pair, p in block["mannwhitneyu_p_two_sided"].items():
            marker = " *" if p < 0.05 else ""
            print(f"    {pair:<26s} p = {p:.4f}{marker}")


def main() -> None:
    stats = write_stats()
    _print_stats(stats)
    print(f"\nWrote {STATS_JSON.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
