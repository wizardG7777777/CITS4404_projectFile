"""Smoke tests for `tradebot.experiments.figures`.

Verifies each figure function returns a valid PNG path. Heavy/expensive tests
are skipped when the real experiment outputs aren't present.
"""
from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _matplotlib_agg():
    import matplotlib
    matplotlib.use("Agg")


def _have_real_outputs() -> bool:
    return all(
        (REPO_ROOT / "results" / name).exists()
        for name in (
            "summary.csv",
            "test_results.csv",
            "behavior.json",
        )
    ) and any((REPO_ROOT / "results" / "runs").iterdir())


def test_fig_01_data_split_smoke():
    pytest.importorskip("matplotlib")
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")
    from tradebot.experiments.figures import fig_01_data_split
    out = fig_01_data_split()
    assert out.exists()
    assert out.stat().st_size > 0


def test_fig_02_wma_demo_smoke():
    pytest.importorskip("matplotlib")
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")
    from tradebot.experiments.figures import fig_02_wma_demo
    out = fig_02_wma_demo()
    assert out.exists()


def test_fig_03_wma_comparison_smoke():
    pytest.importorskip("matplotlib")
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")
    from tradebot.experiments.figures import fig_03_wma_comparison
    out = fig_03_wma_comparison()
    assert out.exists()


def test_figures_4_through_9_require_real_runs():
    """The remaining figures need summary.csv + runs/ from Task #13."""
    pytest.importorskip("matplotlib")
    if not _have_real_outputs():
        pytest.skip("Real experiment outputs not present.")

    from tradebot.experiments.figures import (
        fig_04_train_fitness_boxplot,
        fig_05_convergence_curves,
        fig_06_train_test_scatter,
        fig_07_test_fitness_bar,
        fig_08_b2_weight_shares,
        fig_09_best_bot_trades,
    )

    for func in (
        fig_04_train_fitness_boxplot,
        fig_05_convergence_curves,
        fig_06_train_test_scatter,
        fig_07_test_fitness_bar,
        fig_08_b2_weight_shares,
        fig_09_best_bot_trades,
    ):
        out = func()
        assert out.exists()
        assert out.stat().st_size > 0


def test_make_all_returns_full_list():
    pytest.importorskip("matplotlib")
    if not _have_real_outputs():
        pytest.skip("Real experiment outputs not present.")
    from tradebot.experiments.figures import ALL_FIGURE_FUNCS, make_all
    paths = make_all()
    assert len(paths) == len(ALL_FIGURE_FUNCS)
    assert all(p.exists() for p in paths)
