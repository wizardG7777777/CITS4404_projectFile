"""Unit tests for `tradebot.experiments.test_eval` and `behavior`."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tradebot.experiments.behavior import (
    analyse,
    hhi,
    normalised_weights,
)
from tradebot.experiments.test_eval import (
    buy_and_hold,
    evaluate_all,
    evaluate_run,
)


# --------------------------------------------------------------------------- #
# Helpers used by both test groups
# --------------------------------------------------------------------------- #


def _write_b1_run(root: Path, algo: str, seed: int, best_x: list[float]) -> None:
    """Create a fake run directory with just a final.json for testing."""
    d = root / f"{algo}_B1_dual_sma_seed{seed}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "final.json").write_text(
        json.dumps(
            {
                "algorithm": algo,
                "bot": "B1_dual_sma",
                "seed": seed,
                "budget": 5000,
                "n_evaluations": 5000,
                "wall_time_s": 1.0,
                "best_fitness": 50000.0,
                "best_x": best_x,
            }
        )
    )


def _write_b2_run(
    root: Path,
    algo: str,
    seed: int,
    high_w: list[float],
    low_w: list[float],
    fitness: float = 50000.0,
) -> None:
    """Create a fake B2 run with synthetic weights."""
    d = root / f"{algo}_B2_compound_seed{seed}"
    d.mkdir(parents=True, exist_ok=True)
    best_x = high_w + [10.0, 20.0, 30.0, 0.3] + low_w + [50.0, 100.0, 150.0, 0.2]
    (d / "final.json").write_text(
        json.dumps(
            {
                "algorithm": algo,
                "bot": "B2_compound",
                "seed": seed,
                "budget": 5000,
                "n_evaluations": 5000,
                "wall_time_s": 1.0,
                "best_fitness": fitness,
                "best_x": best_x,
            }
        )
    )


# --------------------------------------------------------------------------- #
# test_eval
# --------------------------------------------------------------------------- #


def test_buy_and_hold_closed_form():
    """At equal start/end price, b&h fitness = initial * (1 - fee)^2."""
    prices = np.array([100.0, 100.0])
    assert buy_and_hold(prices) == pytest.approx(1000.0 * 0.97**2)


def test_buy_and_hold_doubles_with_price():
    prices = np.array([100.0, 200.0])
    assert buy_and_hold(prices) == pytest.approx(1000.0 * 0.97 * 2.0 * 0.97)


def test_evaluate_run_produces_test_fitness(tmp_path):
    """Synthetic B1 run on a synthetic test series returns a finite test fitness."""
    _write_b1_run(tmp_path, "PSO", seed=0, best_x=[5.0, 20.0])
    run_dir = tmp_path / "PSO_B1_dual_sma_seed0"
    test_prices = np.linspace(100, 200, 300)
    row = evaluate_run(run_dir, test_prices)
    assert row["algorithm"] == "PSO"
    assert row["bot"] == "B1_dual_sma"
    assert row["seed"] == 0
    assert row["train_fitness"] == 50000.0
    assert np.isfinite(row["test_fitness"])
    assert row["generalisation_gap"] == row["train_fitness"] - row["test_fitness"]


def test_evaluate_all_walks_every_run_dir(tmp_path):
    _write_b1_run(tmp_path, "PSO", 0, [5.0, 20.0])
    _write_b1_run(tmp_path, "PSO", 1, [5.0, 20.0])
    _write_b1_run(tmp_path, "HHO", 0, [10.0, 30.0])
    test_prices = np.linspace(100, 200, 300)
    out_csv = tmp_path / "test_results.csv"
    df = evaluate_all(runs_dir=tmp_path, test_prices=test_prices, out_path=out_csv)
    assert len(df) == 3
    assert set(df["algorithm"].unique()) == {"PSO", "HHO"}
    assert out_csv.exists()


def test_evaluate_all_on_real_btc_test_data():
    """End-to-end: use the real best_x stored in results/runs/ from Task #13."""
    pytest.importorskip("pyarrow")
    real_runs = Path(__file__).resolve().parents[1] / "results" / "runs"
    if not real_runs.exists() or not any(real_runs.iterdir()):
        pytest.skip("No real runs persisted under results/runs/")
    try:
        from tradebot.data.load import load_close
        test_prices = load_close("test")
    except FileNotFoundError:
        pytest.skip("Processed test parquet not present.")

    df = evaluate_all(
        runs_dir=real_runs, test_prices=test_prices, out_path=Path("/tmp/test_results_smoke.csv")
    )
    assert len(df) == 30
    assert df["test_fitness"].notna().all()
    assert (df["test_fitness"] > 0).all()


# --------------------------------------------------------------------------- #
# behavior
# --------------------------------------------------------------------------- #


def test_normalised_weights_sum_to_one():
    w = np.array([1.0, 2.0, 1.0])
    out = normalised_weights(w)
    assert np.isclose(out.sum(), 1.0)
    np.testing.assert_allclose(out, np.array([0.25, 0.5, 0.25]))


def test_normalised_weights_all_zero_falls_back_to_uniform():
    out = normalised_weights(np.zeros(3))
    np.testing.assert_allclose(out, np.full(3, 1.0 / 3))


def test_hhi_uniform_mix_is_one_over_n():
    assert hhi(np.array([1.0, 1.0, 1.0])) == pytest.approx(1.0 / 3)


def test_hhi_single_winner_is_one():
    assert hhi(np.array([1.0, 0.0, 0.0])) == pytest.approx(1.0)


def test_analyse_b2_synthetic(tmp_path):
    # Three "seeds" for one algo with deliberate winners.
    _write_b2_run(tmp_path, "PSO", 0, high_w=[1.0, 0.0, 0.0], low_w=[0.0, 1.0, 0.0])
    _write_b2_run(tmp_path, "PSO", 1, high_w=[1.0, 0.0, 0.0], low_w=[0.0, 0.0, 1.0])
    _write_b2_run(tmp_path, "PSO", 2, high_w=[0.0, 1.0, 0.0], low_w=[0.0, 1.0, 0.0])

    out = analyse(tmp_path)
    block = out["per_algorithm"]["PSO"]

    assert block["n_runs"] == 3
    # HIGH: SMA wins seeds 0 & 1, LMA wins seed 2.
    assert block["high_winner_counts"] == {"SMA": 2, "LMA": 1, "EMA": 0}
    # LOW: LMA wins seeds 0 & 2, EMA wins seed 1.
    assert block["low_winner_counts"] == {"SMA": 0, "LMA": 2, "EMA": 1}
    # Each row had a single-winner allocation → HHI = 1.0 across all rows.
    assert block["high_mean_hhi"] == pytest.approx(1.0)
    assert block["low_mean_hhi"] == pytest.approx(1.0)


def test_analyse_b2_only_includes_b2_runs(tmp_path):
    _write_b1_run(tmp_path, "PSO", 0, [5.0, 20.0])
    _write_b2_run(tmp_path, "PSO", 0, high_w=[1.0, 0.0, 0.0], low_w=[0.0, 1.0, 0.0])
    out = analyse(tmp_path)
    assert out["per_algorithm"]["PSO"]["n_runs"] == 1


def test_analyse_b2_on_real_runs():
    """End-to-end: read the actual results/runs/ produced by Task #13."""
    real_runs = Path(__file__).resolve().parents[1] / "results" / "runs"
    if not real_runs.exists():
        pytest.skip("No real runs present.")
    b2_runs = [d for d in real_runs.iterdir() if "B2_compound" in d.name]
    if len(b2_runs) == 0:
        pytest.skip("No B2 runs present.")

    out = analyse(real_runs)
    algos = set(out["per_algorithm"].keys())
    # All three algos in default config should have produced B2 runs.
    assert algos == {"RandomSearch", "PSO", "HHO"}
    for algo, block in out["per_algorithm"].items():
        assert block["n_runs"] == 5
        # Winner counts sum to n_runs for each side.
        for side in ("high_winner_counts", "low_winner_counts"):
            assert sum(block[side].values()) == 5
