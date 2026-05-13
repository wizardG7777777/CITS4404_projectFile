"""Unit tests for `tradebot.optim.gwo`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.optim.gwo import GWO


# --------------------------------------------------------------------------- #
# Hyperparameter validation
# --------------------------------------------------------------------------- #


def test_gwo_default_hyperparameter():
    """Mirjalili et al. (2014) benchmarks use 30 wolves."""
    assert GWO().pop_size == 30


def test_gwo_invalid_pop_size_raises():
    with pytest.raises(ValueError, match="pop_size"):
        GWO(pop_size=2)
    with pytest.raises(ValueError, match="pop_size"):
        GWO(pop_size=1)
    with pytest.raises(ValueError, match="pop_size"):
        GWO(pop_size=0)


# --------------------------------------------------------------------------- #
# Budget contract
# --------------------------------------------------------------------------- #


def test_gwo_algorithm_name():
    res = GWO(pop_size=5).maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(2), np.ones(2)),
        budget=30,
        rng=np.random.default_rng(0),
    )
    assert res.algorithm == "GWO"


@pytest.mark.parametrize("budget", [50, 100, 500, 2000])
def test_gwo_budget_exactly_consumed(budget):
    res = GWO(pop_size=10).maximize(
        fitness_fn=lambda x: float(np.sum(x)),
        bounds=(np.zeros(3), np.ones(3)),
        budget=budget,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == budget
    assert res.history.shape == (budget,)


def test_gwo_budget_below_pop_size_terminates_cleanly():
    """If init can't finish, the algorithm still returns finite results."""
    res = GWO(pop_size=30).maximize(
        fitness_fn=lambda x: float(x[0]),
        bounds=(np.zeros(2), np.ones(2)),
        budget=10,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == 10
    assert np.isfinite(res.best_fitness)


# --------------------------------------------------------------------------- #
# Reproducibility & bounds adherence
# --------------------------------------------------------------------------- #


def test_gwo_reproducible_with_same_seed():
    fn = lambda x: -float(x @ x)
    bounds = (-3.0 * np.ones(4), 3.0 * np.ones(4))
    a = GWO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    b = GWO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    np.testing.assert_allclose(a.history, b.history)
    np.testing.assert_allclose(a.best_x, b.best_x)
    assert a.best_fitness == b.best_fitness


def test_gwo_best_x_within_bounds():
    lo = -2.0 * np.ones(5)
    hi = 3.0 * np.ones(5)
    res = GWO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(lo, hi),
        budget=500,
        rng=np.random.default_rng(0),
    )
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)


def test_gwo_best_history_is_monotone_nondecreasing():
    res = GWO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(-np.ones(3), np.ones(3)),
        budget=500,
        rng=np.random.default_rng(0),
    )
    assert np.all(np.diff(res.best_history) >= 0)


# --------------------------------------------------------------------------- #
# Convergence behaviour
# --------------------------------------------------------------------------- #


def test_gwo_finds_near_optimum_on_negative_quadratic():
    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    res = GWO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=bounds,
        budget=3000,
        rng=np.random.default_rng(0),
    )
    # Three-leader averaging converges quickly on smooth landscapes.
    assert res.best_fitness > -1.0


def test_gwo_beats_random_search_on_negative_quadratic():
    """GWO's three-leader directed search should beat uniform sampling
    in expectation."""
    from tradebot.optim.random_search import RandomSearch

    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    fn = lambda x: -float(x @ x)
    budget = 1500

    gwo_results, rs_results = [], []
    for seed in range(5):
        gwo_results.append(
            GWO().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )
        rs_results.append(
            RandomSearch().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )
    assert np.mean(gwo_results) > np.mean(rs_results)


# --------------------------------------------------------------------------- #
# Integration with the bot fitness function
# --------------------------------------------------------------------------- #


def test_gwo_optimises_botb1_on_real_btc_train():
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")

    from tradebot.bot.backtest import INITIAL_CASH, backtest_fitness
    from tradebot.bot.bots import BotB1

    def fitness(params):
        return backtest_fitness(prices, BotB1.signals(prices, params))

    res = GWO().maximize(
        fitness_fn=fitness,
        bounds=BotB1.bounds(),
        budget=500,
        rng=np.random.default_rng(20260510),
    )
    assert res.n_evaluations == 500
    assert np.isfinite(res.best_fitness)
    lo, hi = BotB1.bounds()
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)
    assert res.best_fitness >= INITIAL_CASH
