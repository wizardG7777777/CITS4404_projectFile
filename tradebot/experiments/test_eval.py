"""Test-set evaluation of trained bots.

For every (algorithm, bot, seed) run in `results/runs/`, this module loads
the best parameter vector found on training data and back-tests it on the
held-out test split (>= 2020-01-01) per PDF §3 *Data*:

  "You should optimise your agent on data prior to 2020, and preserve the
   data from 2020 onwards for final testing of your optimised bot ... we'll
   act as if it is the start of 2020."

The bot is deployed cold on 2020-01-01 with the PDF's $1000 starting cash;
no warm-start state is carried over from training. WMA warm-up zeros the
first max(N)-1 days of signals as in the training back-test (matching the
behaviour locked in `tradebot/bot/bots.py`).

Outputs:

    results/test_results.csv  — one row per run with both train and test
                                fitness, the generalisation gap, and the
                                buy-and-hold baseline on the test split.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from tradebot.bot.backtest import INITIAL_CASH, FEE_RATE, backtest_fitness
from tradebot.data.load import load_close

from .config import BOTS


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "results" / "runs"
TEST_RESULTS_CSV = REPO_ROOT / "results" / "test_results.csv"


def buy_and_hold(prices: np.ndarray) -> float:
    """Closed-form fitness of the 'one buy then liquidate' baseline."""
    return float(
        INITIAL_CASH * (1.0 - FEE_RATE) / prices[0] * prices[-1] * (1.0 - FEE_RATE)
    )


def evaluate_run(
    run_dir: Path, test_prices: np.ndarray
) -> dict:
    """Read final.json from one run and return its test-fitness row."""
    meta = json.loads((run_dir / "final.json").read_text())
    algo = meta["algorithm"]
    bot_name = meta["bot"]
    seed = meta["seed"]
    train_fitness = float(meta["best_fitness"])
    best_x = np.array(meta["best_x"], dtype=np.float64)

    BotCls = BOTS[bot_name]
    signals = BotCls.signals(test_prices, best_x)
    test_fitness = backtest_fitness(test_prices, signals)

    return {
        "algorithm": algo,
        "bot": bot_name,
        "seed": seed,
        "train_fitness": train_fitness,
        "test_fitness": float(test_fitness),
        "generalisation_gap": train_fitness - float(test_fitness),
    }


def evaluate_all(
    runs_dir: Path = RUNS_DIR,
    test_prices: np.ndarray | None = None,
    out_path: Path = TEST_RESULTS_CSV,
) -> pd.DataFrame:
    """Run `evaluate_run` over every subdirectory of `runs_dir`."""
    if test_prices is None:
        test_prices = load_close("test")

    rows = []
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        if not (run_dir / "final.json").exists():
            continue
        rows.append(evaluate_run(run_dir, test_prices))

    df = pd.DataFrame(rows).sort_values(["bot", "algorithm", "seed"]).reset_index(drop=True)
    df.to_csv(out_path, index=False)
    return df


def main() -> None:
    test_prices = load_close("test")
    bh = buy_and_hold(test_prices)
    print(
        f"Test split: {test_prices.size} days, "
        f"${test_prices[0]:.2f} -> ${test_prices[-1]:.2f}"
    )
    print(f"Buy-and-hold baseline on test: ${bh:.2f}\n")

    df = evaluate_all(test_prices=test_prices)

    print(
        f"{'algorithm':<14s}  {'bot':<13s}  {'seed':>4s}  "
        f"{'train':>10s}  {'test':>10s}  {'gap':>10s}"
    )
    for _, r in df.iterrows():
        print(
            f"{r['algorithm']:<14s}  {r['bot']:<13s}  {int(r['seed']):>4d}  "
            f"${r['train_fitness']:>8.0f}  ${r['test_fitness']:>8.0f}  "
            f"${r['generalisation_gap']:>8.0f}"
        )

    print(f"\nAggregate (mean across 5 seeds):")
    agg = df.groupby(["bot", "algorithm"])[["train_fitness", "test_fitness", "generalisation_gap"]].mean()
    print(agg.round(0).to_string())
    print(f"\nWrote {TEST_RESULTS_CSV.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
