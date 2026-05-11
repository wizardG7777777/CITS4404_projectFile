"""Drive the full experiment matrix and persist results to disk.

Usage from the repo root:

    uv run python -m tradebot.experiments.run_matrix

Outputs:

    results/runs/{algo}_{bot}_seed{N}/
        trace.parquet   — one row per evaluation: step, fitness, best_so_far
        final.json      — best_x, best_fitness, wall_time, metadata
    results/summary.csv — one row per run, primary input for analysis

Per PDF §3 *Choosing Algorithms* fairness rules:

  * every run consumes exactly `budget` fitness evaluations,
  * every run gets a deterministic seed via `np.random.default_rng(seed)`,
  * algorithms are constructed fresh per run (no shared state).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from tradebot.bot.backtest import backtest_fitness
from tradebot.data.load import load_close

from .config import ALGORITHMS, BOTS, DEFAULT_CONFIG, ExperimentConfig


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "results"
RUNS_DIR = RESULTS_DIR / "runs"
SUMMARY_CSV = RESULTS_DIR / "summary.csv"


# --------------------------------------------------------------------------- #
# Single-run helper
# --------------------------------------------------------------------------- #


def run_one(
    algo_name: str,
    bot_name: str,
    seed: int,
    budget: int,
    prices: np.ndarray,
    out_root: Path,
) -> dict:
    """Run one (algorithm, bot, seed) cell of the experiment matrix.

    Persists trace.parquet + final.json under
    ``out_root/{algo}_{bot}_seed{N}/``. Returns the summary dict that will
    become one row of ``summary.csv``.
    """
    BotCls = BOTS[bot_name]
    AlgoCls = ALGORITHMS[algo_name]
    algo = AlgoCls()
    rng = np.random.default_rng(seed)

    def fitness(params):
        return backtest_fitness(prices, BotCls.signals(prices, params))

    t0 = time.perf_counter()
    res = algo.maximize(fitness, BotCls.bounds(), budget, rng=rng)
    wall = time.perf_counter() - t0

    run_dir = out_root / f"{algo_name}_{bot_name}_seed{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Per-step trace.
    trace = pd.DataFrame(
        {
            "step": np.arange(res.n_evaluations, dtype=np.int64),
            "fitness": res.history,
            "best_so_far": res.best_history,
        }
    )
    trace.to_parquet(run_dir / "trace.parquet", index=False)

    # Per-run metadata.
    final_meta = {
        "algorithm": algo_name,
        "bot": bot_name,
        "seed": seed,
        "budget": budget,
        "n_evaluations": res.n_evaluations,
        "wall_time_s": wall,
        "best_fitness": res.best_fitness,
        "best_x": res.best_x.tolist(),
    }
    (run_dir / "final.json").write_text(json.dumps(final_meta, indent=2))

    return final_meta


# --------------------------------------------------------------------------- #
# Matrix driver
# --------------------------------------------------------------------------- #


def run_experiment(
    config: ExperimentConfig = DEFAULT_CONFIG,
    out_root: Path | None = None,
    prices: np.ndarray | None = None,
    *,
    verbose: bool = True,
) -> pd.DataFrame:
    """Run the full matrix described by ``config`` and persist the summary."""
    if out_root is None:
        out_root = RUNS_DIR
    if prices is None:
        prices = load_close(config.split)

    out_root.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict] = []
    started = time.perf_counter()
    if verbose:
        print(
            f"Running {config.n_runs} cells "
            f"({len(config.algorithms)} algos × {len(config.bots)} bots "
            f"× {len(config.seeds)} seeds × {config.budget} FE)..."
        )

    for idx, (algo_name, bot_name, seed) in enumerate(config.iter_runs(), start=1):
        row = run_one(
            algo_name=algo_name,
            bot_name=bot_name,
            seed=seed,
            budget=config.budget,
            prices=prices,
            out_root=out_root,
        )
        summary_rows.append(row)
        if verbose:
            print(
                f"  [{idx:>2d}/{config.n_runs}] "
                f"{algo_name:<13s} {bot_name:<13s} seed={seed}  "
                f"best=${row['best_fitness']:>10.2f}  wall={row['wall_time_s']:.2f}s"
            )

    summary = pd.DataFrame(summary_rows)
    summary_path = out_root.parent / "summary.csv"
    # Don't save best_x as a CSV column — it's already in final.json.
    summary_for_csv = summary.drop(columns=["best_x"])
    summary_for_csv.to_csv(summary_path, index=False)

    total = time.perf_counter() - started
    if verbose:
        print(f"\nTotal wall time: {total:.1f}s")
        print(f"Wrote {summary_path.relative_to(REPO_ROOT)}")

    return summary


def main() -> None:
    run_experiment(DEFAULT_CONFIG)


if __name__ == "__main__":
    main()
