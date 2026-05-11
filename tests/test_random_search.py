"""Unit tests for `tradebot.optim.random_search`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.optim.random_search import RandomSearch


# --------------------------------------------------------------------------- #
# Budget contract
# --------------------------------------------------------------------------- #


def test_random_search_uses_exact_budget():
    rs = RandomSearch()
    res = rs.maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(3), np.ones(3)),
        budget=200,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == 200
    assert res.history.shape == (200,)
    assert res.best_history.shape == (200,)


def test_random_search_algorithm_name():
    res = RandomSearch().maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(2), np.ones(2)),
        budget=5,
        rng=np.random.default_rng(0),
    )
    assert res.algorithm == "RandomSearch"


# --------------------------------------------------------------------------- #
# Reproducibility and bounds adherence
# --------------------------------------------------------------------------- #


def test_random_search_reproducible_with_same_seed():
    bounds = (-2.0 * np.ones(4), 2.0 * np.ones(4))
    fn = lambda x: -float(x @ x)
    a = RandomSearch().maximize(fn, bounds, 100, rng=np.random.default_rng(1234))
    b = RandomSearch().maximize(fn, bounds, 100, rng=np.random.default_rng(1234))
    np.testing.assert_allclose(a.history, b.history)
    np.testing.assert_allclose(a.best_x, b.best_x)
    assert a.best_fitness == b.best_fitness


def test_random_search_best_x_within_bounds():
    lo, hi = -3.0 * np.ones(5), 4.0 * np.ones(5)
    res = RandomSearch().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(lo, hi),
        budget=500,
        rng=np.random.default_rng(7),
    )
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)


# --------------------------------------------------------------------------- #
# Convergence behaviour
# --------------------------------------------------------------------------- #


def test_random_search_best_history_is_monotone_nondecreasing():
    res = RandomSearch().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(-1.0 * np.ones(3), 1.0 * np.ones(3)),
        budget=300,
        rng=np.random.default_rng(0),
    )
    assert np.all(np.diff(res.best_history) >= 0)


def test_random_search_approaches_optimum_on_negative_quadratic():
    """Maximising -||x||^2 on [-5, 5]^2; with enough budget we should get
    much closer than a single uniform draw."""
    d = 2
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    rng = np.random.default_rng(99)

    # Average single-draw L2: ~5/sqrt(3) * sqrt(d) ≈ 4.08, so f ≈ -16.7.
    res = RandomSearch().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=bounds,
        budget=10_000,
        rng=rng,
    )
    # With 10k draws on 2-D, |x*| should be small (the box's smallest-radius
    # neighbourhood of the origin is well-sampled).
    assert res.best_fitness > -0.01  # squared L2 < 0.01 with high probability


# --------------------------------------------------------------------------- #
# Integration with a real bot fitness function
# --------------------------------------------------------------------------- #


def test_random_search_optimises_botb1_on_real_btc_train():
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")

    from tradebot.bot.backtest import INITIAL_CASH, backtest_fitness
    from tradebot.bot.bots import BotB1

    def fitness(params):
        sigs = BotB1.signals(prices, params)
        return backtest_fitness(prices, sigs)

    res = RandomSearch().maximize(
        fitness_fn=fitness,
        bounds=BotB1.bounds(),
        budget=200,
        rng=np.random.default_rng(20260510),
    )
    # Sanity: budget exact, finite fitness, best_x inside bounds.
    assert res.n_evaluations == 200
    assert np.isfinite(res.best_fitness)
    lo, hi = BotB1.bounds()
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)
    # Should at least match the "no trades" baseline (==INITIAL_CASH); any
    # crossover schedule that lost money to fees would be replaced by one
    # that happens to find a degenerate (no-trade) configuration.
    assert res.best_fitness >= INITIAL_CASH
