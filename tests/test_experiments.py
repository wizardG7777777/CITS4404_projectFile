"""Unit tests for `tradebot.experiments`."""
from __future__ import annotations

import json

import numpy as np
import pytest

from tradebot.experiments.analyze import (
    aggregate,
    descriptive_stats,
    mannwhitneyu_pvalue,
)
from tradebot.experiments.config import (
    ALGORITHMS,
    BOTS,
    DEFAULT_CONFIG,
    ExperimentConfig,
)


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #


def test_default_config_matches_d2_scope():
    """Sanity-check the 5×3×2 matrix declared in docs/d2_requirement_alignment.md."""
    cfg = DEFAULT_CONFIG
    assert set(cfg.algorithms) == {"RandomSearch", "PSO", "HHO"}
    assert set(cfg.bots) == {"B1_dual_sma", "B2_compound"}
    assert len(cfg.seeds) == 5
    assert cfg.budget == 5000
    assert cfg.split == "train"
    assert cfg.n_runs == 30


def test_config_rejects_unknown_algorithm():
    with pytest.raises(ValueError, match="unknown algorithm"):
        ExperimentConfig(algorithms=("NotAnAlgo",))


def test_config_rejects_unknown_bot():
    with pytest.raises(ValueError, match="unknown bot"):
        ExperimentConfig(bots=("NotABot",))


def test_config_rejects_invalid_budget():
    with pytest.raises(ValueError, match="budget must be >= 1"):
        ExperimentConfig(budget=0)


def test_config_iter_runs_yields_all_triples_once():
    cfg = ExperimentConfig(
        algorithms=("RandomSearch",),
        bots=("B1_dual_sma", "B2_compound"),
        seeds=(0, 1, 2),
        budget=10,
    )
    triples = list(cfg.iter_runs())
    assert len(triples) == 6
    assert len(set(triples)) == 6


# --------------------------------------------------------------------------- #
# Mann-Whitney U
# --------------------------------------------------------------------------- #


def test_mannwhitneyu_identical_groups_gives_p_near_one():
    """Same group compared with itself should give a large p-value."""
    a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    p = mannwhitneyu_pvalue(a, a)
    assert p > 0.9


def test_mannwhitneyu_clearly_different_groups_gives_small_p():
    """Two well-separated groups → p < 0.05."""
    rng = np.random.default_rng(0)
    a = rng.normal(0.0, 1.0, size=20)
    b = rng.normal(5.0, 1.0, size=20)
    assert mannwhitneyu_pvalue(a, b) < 0.01


def test_mannwhitneyu_handles_ties_via_average_ranking():
    """Equal values get averaged ranks (matches the Wilcoxon convention)."""
    a = np.array([1.0, 1.0, 2.0])
    b = np.array([1.0, 1.0, 3.0])
    # Should not raise / produce NaN.
    p = mannwhitneyu_pvalue(a, b)
    assert 0.0 <= p <= 1.0


def test_mannwhitneyu_symmetric_in_arguments():
    rng = np.random.default_rng(1)
    a = rng.normal(0, 1, size=15)
    b = rng.normal(0.5, 1, size=15)
    assert mannwhitneyu_pvalue(a, b) == pytest.approx(mannwhitneyu_pvalue(b, a))


def test_mannwhitneyu_empty_input_returns_one():
    assert mannwhitneyu_pvalue(np.array([]), np.array([1.0])) == 1.0


# --------------------------------------------------------------------------- #
# Descriptive stats
# --------------------------------------------------------------------------- #


def test_descriptive_stats_basic_quantities():
    vals = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    d = descriptive_stats(vals)
    assert d["n"] == 5
    assert d["mean"] == 3.0
    assert d["median"] == 3.0
    assert d["min"] == 1.0
    assert d["max"] == 5.0
    # Sample std with ddof=1.
    assert d["std"] == pytest.approx(np.std(vals, ddof=1))


# --------------------------------------------------------------------------- #
# Aggregate
# --------------------------------------------------------------------------- #


def test_aggregate_produces_expected_structure():
    import pandas as pd

    rows = []
    rng = np.random.default_rng(0)
    for bot in ("B1", "B2"):
        for algo in ("A1", "A2", "A3"):
            for seed in range(5):
                rows.append(
                    {
                        "algorithm": algo,
                        "bot": bot,
                        "seed": seed,
                        "best_fitness": rng.uniform(1000, 5000),
                        "wall_time_s": rng.uniform(0.5, 2.0),
                        "n_evaluations": 5000,
                        "budget": 5000,
                    }
                )
    summary = pd.DataFrame(rows)
    stats = aggregate(summary)

    assert set(stats["per_bot"]) == {"B1", "B2"}
    for bot in ("B1", "B2"):
        descriptive = stats["per_bot"][bot]["descriptive"]
        assert set(descriptive) == {"A1", "A2", "A3"}
        for algo in descriptive:
            d = descriptive[algo]
            assert d["n"] == 5
            assert 0 <= d["std"] < 5000
        pvals = stats["per_bot"][bot]["mannwhitneyu_p_two_sided"]
        assert set(pvals) == {"A1_vs_A2", "A1_vs_A3", "A2_vs_A3"}
        for p in pvals.values():
            assert 0.0 <= p <= 1.0
    assert "total" in stats["wall_time_s"]


# --------------------------------------------------------------------------- #
# End-to-end with the run driver (tiny 1×1×2 matrix, budget 50)
# --------------------------------------------------------------------------- #


def test_run_one_writes_trace_and_final(tmp_path):
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")

    from tradebot.experiments.run_matrix import run_one

    row = run_one(
        algo_name="RandomSearch",
        bot_name="B1_dual_sma",
        seed=0,
        budget=50,
        prices=prices,
        out_root=tmp_path,
    )
    run_dir = tmp_path / "RandomSearch_B1_dual_sma_seed0"
    assert (run_dir / "trace.parquet").exists()
    assert (run_dir / "final.json").exists()
    assert row["n_evaluations"] == 50
    assert np.isfinite(row["best_fitness"])

    # final.json contents
    meta = json.loads((run_dir / "final.json").read_text())
    assert meta["algorithm"] == "RandomSearch"
    assert meta["bot"] == "B1_dual_sma"
    assert meta["seed"] == 0
    assert meta["budget"] == 50
    assert len(meta["best_x"]) == 2


def test_run_experiment_completes_tiny_matrix(tmp_path):
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")

    from tradebot.experiments.run_matrix import run_experiment

    cfg = ExperimentConfig(
        algorithms=("RandomSearch",),
        bots=("B1_dual_sma",),
        seeds=(0, 1),
        budget=50,
    )
    summary = run_experiment(cfg, out_root=tmp_path, prices=prices, verbose=False)
    assert len(summary) == 2
    assert (tmp_path.parent / "summary.csv").exists()
