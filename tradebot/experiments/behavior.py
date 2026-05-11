"""Behavioural analysis of optimised B2 bots — which WMA does each prefer?

PDF §3 *Generalisation and Design* names this analysis explicitly:

  "It will be interesting to look after optimising to see how much weight
   the bot gives to each component — for example, does it consistently
   favour one or continue to draw from all three."

For every B2 run we extract its normalised SMA / LMA / EMA shares (the
w_i / sum w_i of PDF Eq.(7)) for both the high-frequency and low-frequency
components, then aggregate per algorithm across all 5 seeds.

Reported quantities:

  * mean share per WMA type (the average split across seeds);
  * "winner" frequency — how many of the 5 seeds picked each WMA as the
    dominant one (largest weight) for that component;
  * concentration — HHI = sum w_i^2; 1/3 means uniform mix, 1.0 means a
    single WMA carries all the weight. Indicates whether the optimiser
    "consistently favours one or continues to draw from all three".

Outputs ``results/behavior.json``.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "results" / "runs"
BEHAVIOR_JSON = REPO_ROOT / "results" / "behavior.json"


# B2 param layout — keep in sync with tradebot/bot/bots.py BotB2.
HIGH_WEIGHT_SLICE = slice(0, 3)
HIGH_WINDOW_SLICE = slice(3, 6)
HIGH_ALPHA_IDX = 6
LOW_WEIGHT_SLICE = slice(7, 10)
LOW_WINDOW_SLICE = slice(10, 13)
LOW_ALPHA_IDX = 13

WMA_TYPES = ("SMA", "LMA", "EMA")


def normalised_weights(w: np.ndarray) -> np.ndarray:
    """Return w / sum(w) with a safe fallback (uniform) for all-zero weights."""
    s = w.sum()
    if s <= 1e-12:
        return np.full(w.size, 1.0 / w.size, dtype=np.float64)
    return w / s


def hhi(weights: np.ndarray) -> float:
    """Herfindahl-Hirschman index for a normalised weight vector.

    For three equal weights HHI = 3 * (1/3)^2 = 1/3 (most spread out).
    For a single dominant weight HHI = 1.0 (concentrated on one component).
    """
    w = normalised_weights(np.asarray(weights, dtype=np.float64))
    return float((w**2).sum())


def _load_b2_runs(runs_dir: Path) -> list[dict]:
    """Load all B2 runs as a list of dicts (algorithm, seed, best_x, best_fitness)."""
    rows = []
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir() or "B2_compound" not in run_dir.name:
            continue
        final = run_dir / "final.json"
        if not final.exists():
            continue
        meta = json.loads(final.read_text())
        rows.append(
            {
                "algorithm": meta["algorithm"],
                "seed": int(meta["seed"]),
                "best_fitness": float(meta["best_fitness"]),
                "best_x": np.array(meta["best_x"], dtype=np.float64),
            }
        )
    return rows


def analyse(runs_dir: Path = RUNS_DIR) -> dict:
    """Aggregate B2 weight allocations across all seeds, per algorithm.

    Returns a JSON-serialisable dict structured as:

        {
          "per_algorithm": {
            "PSO": {
              "per_seed": [{seed, fitness, high_shares, low_shares, ...}, ...],
              "high_mean_shares": {SMA, LMA, EMA},
              "low_mean_shares":  {SMA, LMA, EMA},
              "high_winner_counts": {SMA, LMA, EMA},
              "low_winner_counts":  {SMA, LMA, EMA},
              "high_mean_hhi": float,
              "low_mean_hhi":  float,
            },
            ...
          }
        }
    """
    raw = _load_b2_runs(runs_dir)
    if not raw:
        raise FileNotFoundError(f"no B2 runs found under {runs_dir}")

    algos = sorted({r["algorithm"] for r in raw})
    out: dict = {"per_algorithm": {}}

    for algo in algos:
        algo_runs = [r for r in raw if r["algorithm"] == algo]
        algo_runs.sort(key=lambda r: r["seed"])

        per_seed = []
        high_arr = np.zeros((len(algo_runs), 3))
        low_arr = np.zeros((len(algo_runs), 3))

        for i, run in enumerate(algo_runs):
            x = run["best_x"]
            wh = normalised_weights(x[HIGH_WEIGHT_SLICE])
            wl = normalised_weights(x[LOW_WEIGHT_SLICE])
            dh = x[HIGH_WINDOW_SLICE]
            dl = x[LOW_WINDOW_SLICE]
            high_arr[i] = wh
            low_arr[i] = wl
            per_seed.append(
                {
                    "seed": run["seed"],
                    "fitness": run["best_fitness"],
                    "high_shares": dict(zip(WMA_TYPES, wh.tolist())),
                    "low_shares": dict(zip(WMA_TYPES, wl.tolist())),
                    "high_windows": dict(zip(WMA_TYPES, [int(round(v)) for v in dh])),
                    "low_windows": dict(zip(WMA_TYPES, [int(round(v)) for v in dl])),
                    "high_alpha": float(x[HIGH_ALPHA_IDX]),
                    "low_alpha": float(x[LOW_ALPHA_IDX]),
                    "high_winner": WMA_TYPES[int(np.argmax(wh))],
                    "low_winner": WMA_TYPES[int(np.argmax(wl))],
                    "high_hhi": hhi(wh),
                    "low_hhi": hhi(wl),
                }
            )

        high_winner_idx = np.argmax(high_arr, axis=1)
        low_winner_idx = np.argmax(low_arr, axis=1)

        out["per_algorithm"][algo] = {
            "n_runs": len(algo_runs),
            "per_seed": per_seed,
            "high_mean_shares": dict(zip(WMA_TYPES, high_arr.mean(axis=0).tolist())),
            "low_mean_shares": dict(zip(WMA_TYPES, low_arr.mean(axis=0).tolist())),
            "high_winner_counts": {
                wma: int((high_winner_idx == i).sum())
                for i, wma in enumerate(WMA_TYPES)
            },
            "low_winner_counts": {
                wma: int((low_winner_idx == i).sum())
                for i, wma in enumerate(WMA_TYPES)
            },
            "high_mean_hhi": float(np.mean([s["high_hhi"] for s in per_seed])),
            "low_mean_hhi": float(np.mean([s["low_hhi"] for s in per_seed])),
        }
    return out


def main() -> None:
    analysis = analyse()
    BEHAVIOR_JSON.parent.mkdir(parents=True, exist_ok=True)
    BEHAVIOR_JSON.write_text(json.dumps(analysis, indent=2))

    print("B2 weight allocation analysis (5 seeds per algorithm)\n")
    print(
        f"{'algo':<14s}  {'side':<5s}  "
        f"{'SMA':>10s}  {'LMA':>10s}  {'EMA':>10s}  "
        f"{'HHI':>6s}  winners"
    )
    for algo, block in analysis["per_algorithm"].items():
        for side, mean_key, winner_key, hhi_key in (
            ("HIGH", "high_mean_shares", "high_winner_counts", "high_mean_hhi"),
            ("LOW",  "low_mean_shares",  "low_winner_counts",  "low_mean_hhi"),
        ):
            shares = block[mean_key]
            winners = block[winner_key]
            winner_str = ", ".join(f"{w}:{c}" for w, c in winners.items() if c > 0)
            print(
                f"{algo:<14s}  {side:<5s}  "
                f"{shares['SMA']:>10.2%}  {shares['LMA']:>10.2%}  {shares['EMA']:>10.2%}  "
                f"{block[hhi_key]:>6.3f}  {winner_str}"
            )
    print(
        "\nHHI = 0.33 means a perfectly even mix; 1.00 means a single WMA dominates.\n"
        f"Wrote {BEHAVIOR_JSON.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
