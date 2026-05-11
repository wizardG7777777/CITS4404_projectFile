"""Unit tests for `tradebot.optim.pso`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.optim.pso import PSO


# --------------------------------------------------------------------------- #
# Hyperparameter validation
# --------------------------------------------------------------------------- #


def test_pso_default_hyperparameters_match_synopsis_values():
    pso = PSO()
    assert pso.pop_size == 30
    assert pso.w == 0.7
    assert pso.c1 == 2.0
    assert pso.c2 == 2.0
    assert pso.v_max_frac == 0.5


def test_pso_invalid_pop_size_raises():
    with pytest.raises(ValueError, match="pop_size"):
        PSO(pop_size=1)
    with pytest.raises(ValueError, match="pop_size"):
        PSO(pop_size=0)


def test_pso_invalid_inertia_weight_raises():
    with pytest.raises(ValueError, match="w"):
        PSO(w=-0.1)


def test_pso_invalid_acceleration_constants_raise():
    with pytest.raises(ValueError, match="c1, c2"):
        PSO(c1=-1.0)
    with pytest.raises(ValueError, match="c1, c2"):
        PSO(c2=-1.0)


def test_pso_invalid_v_max_frac_raises():
    with pytest.raises(ValueError, match="v_max_frac"):
        PSO(v_max_frac=0.0)
    with pytest.raises(ValueError, match="v_max_frac"):
        PSO(v_max_frac=-0.5)


# --------------------------------------------------------------------------- #
# Budget contract
# --------------------------------------------------------------------------- #


def test_pso_algorithm_name():
    res = PSO(pop_size=5).maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(2), np.ones(2)),
        budget=20,
        rng=np.random.default_rng(0),
    )
    assert res.algorithm == "PSO"


@pytest.mark.parametrize("pop_size,budget", [(5, 50), (7, 100), (30, 300), (30, 5000)])
def test_pso_budget_exactly_consumed(pop_size, budget):
    """Pop size that doesn't evenly divide budget should still stop on budget."""
    res = PSO(pop_size=pop_size).maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(3), np.ones(3)),
        budget=budget,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == budget
    assert res.history.shape == (budget,)


def test_pso_budget_below_pop_size_still_terminates_cleanly():
    """If budget < pop_size, init loop is cut short — no crash."""
    res = PSO(pop_size=30).maximize(
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


def test_pso_reproducible_with_same_seed():
    fn = lambda x: -float(x @ x)
    bounds = (-3.0 * np.ones(4), 3.0 * np.ones(4))
    a = PSO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    b = PSO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    np.testing.assert_allclose(a.history, b.history)
    np.testing.assert_allclose(a.best_x, b.best_x)
    assert a.best_fitness == b.best_fitness


def test_pso_best_x_within_bounds():
    lo = -2.0 * np.ones(5)
    hi = 3.0 * np.ones(5)
    res = PSO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(lo, hi),
        budget=500,
        rng=np.random.default_rng(0),
    )
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)


def test_pso_best_history_is_monotone_nondecreasing():
    res = PSO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(-np.ones(3), np.ones(3)),
        budget=300,
        rng=np.random.default_rng(0),
    )
    assert np.all(np.diff(res.best_history) >= 0)


# --------------------------------------------------------------------------- #
# Convergence behaviour
# --------------------------------------------------------------------------- #


def test_pso_finds_optimum_on_negative_quadratic():
    """Maximising -||x||^2 on [-5, 5]^5 with ample budget; PSO should land
    very close to the origin."""
    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    res = PSO(pop_size=30).maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=bounds,
        budget=3000,
        rng=np.random.default_rng(0),
    )
    # ||x*||^2 < 1.0 with directed search and a smooth landscape.
    assert res.best_fitness > -1.0


def test_pso_beats_random_search_in_average_on_negative_quadratic():
    """On a smooth unimodal landscape with the same FE budget, PSO's directed
    search should land closer to the optimum than uniform random sampling."""
    from tradebot.optim.random_search import RandomSearch

    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    fn = lambda x: -float(x @ x)
    budget = 1500

    pso_results, rs_results = [], []
    for seed in range(5):
        pso_results.append(
            PSO().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )
        rs_results.append(
            RandomSearch().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )

    # Both are negative; "better" means closer to 0, i.e. higher mean.
    assert np.mean(pso_results) > np.mean(rs_results)


# --------------------------------------------------------------------------- #
# Integration with a real bot fitness function
# --------------------------------------------------------------------------- #


def test_pso_optimises_botb1_on_real_btc_train():
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

    res = PSO().maximize(
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
    # Should at least match the "no trades" baseline.
    assert res.best_fitness >= INITIAL_CASH
