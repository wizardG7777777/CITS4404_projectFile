"""Unit tests for `tradebot.optim.hho`."""
from __future__ import annotations

import math

import numpy as np
import pytest

from tradebot.optim.hho import HHO


# --------------------------------------------------------------------------- #
# Hyperparameter validation
# --------------------------------------------------------------------------- #


def test_hho_default_hyperparameter_matches_synopsis_value():
    """D1 synopsis: 'a swarm of 30 agents'."""
    assert HHO().pop_size == 30


def test_hho_levy_beta_pinned_to_1_5():
    """D1 synopsis: 'the Levy step uses a fixed beta = 1.5'."""
    assert HHO.LEVY_BETA == 1.5


def test_hho_invalid_pop_size_raises():
    with pytest.raises(ValueError, match="pop_size"):
        HHO(pop_size=1)
    with pytest.raises(ValueError, match="pop_size"):
        HHO(pop_size=0)


# --------------------------------------------------------------------------- #
# Levy step properties
# --------------------------------------------------------------------------- #


def test_levy_step_is_finite_and_correct_shape():
    """A Levy step should be a length-d finite vector."""
    hho = HHO()
    rng = np.random.default_rng(0)
    for d in (1, 5, 14, 50):
        step = hho._levy_step(d, rng)
        assert step.shape == (d,)
        assert np.all(np.isfinite(step))


def test_levy_step_distribution_is_heavy_tailed():
    """Mantegna-Levy steps should occasionally produce magnitudes that
    dwarf the median. A standard normal has P99/median ~ 3-4; heavy-tailed
    distributions should comfortably exceed that."""
    hho = HHO()
    rng = np.random.default_rng(42)
    samples = np.array([np.abs(hho._levy_step(1, rng)[0]) for _ in range(5000)])
    assert np.quantile(samples, 0.99) / np.median(samples) > 10


# --------------------------------------------------------------------------- #
# Budget contract
# --------------------------------------------------------------------------- #


def test_hho_algorithm_name():
    res = HHO(pop_size=5).maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(2), np.ones(2)),
        budget=30,
        rng=np.random.default_rng(0),
    )
    assert res.algorithm == "HHO"


@pytest.mark.parametrize("budget", [50, 100, 500, 2000])
def test_hho_budget_exactly_consumed(budget):
    """No matter how many hawks enter dive mode (variable evals/iteration),
    the FE counter must stop on exactly `budget`."""
    res = HHO(pop_size=10).maximize(
        fitness_fn=lambda x: float(rng_state.uniform()),
        bounds=(np.zeros(3), np.ones(3)),
        budget=budget,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == budget
    assert res.history.shape == (budget,)


# rng_state used by the parametrised test above (a per-call RNG isolated from
# the optimiser's own RNG so we don't perturb the deterministic search).
rng_state = np.random.default_rng(1)


def test_hho_budget_below_pop_size_terminates_cleanly():
    """If init can't finish, the algorithm still returns finite results."""
    res = HHO(pop_size=30).maximize(
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


def test_hho_reproducible_with_same_seed():
    fn = lambda x: -float(x @ x)
    bounds = (-3.0 * np.ones(4), 3.0 * np.ones(4))
    a = HHO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    b = HHO(pop_size=10).maximize(fn, bounds, 500, rng=np.random.default_rng(7))
    np.testing.assert_allclose(a.history, b.history)
    np.testing.assert_allclose(a.best_x, b.best_x)
    assert a.best_fitness == b.best_fitness


def test_hho_best_x_within_bounds():
    lo = -2.0 * np.ones(5)
    hi = 3.0 * np.ones(5)
    res = HHO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(lo, hi),
        budget=500,
        rng=np.random.default_rng(0),
    )
    assert np.all(res.best_x >= lo)
    assert np.all(res.best_x <= hi)


def test_hho_best_history_is_monotone_nondecreasing():
    res = HHO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=(-np.ones(3), np.ones(3)),
        budget=500,
        rng=np.random.default_rng(0),
    )
    assert np.all(np.diff(res.best_history) >= 0)


# --------------------------------------------------------------------------- #
# Convergence behaviour
# --------------------------------------------------------------------------- #


def test_hho_finds_near_optimum_on_negative_quadratic():
    """Maximising -||x||^2 on [-5, 5]^5 with ample budget; HHO should land
    close to the origin."""
    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    res = HHO().maximize(
        fitness_fn=lambda x: -float(x @ x),
        bounds=bounds,
        budget=3000,
        rng=np.random.default_rng(0),
    )
    # HHO's emphasis is rugged multimodal landscapes — on smooth quadratic
    # it should still be << initial draw quality.
    assert res.best_fitness > -1.0


def test_hho_beats_random_search_on_negative_quadratic():
    """HHO's directed search should beat uniform random sampling in
    expectation on a smooth unimodal landscape."""
    from tradebot.optim.random_search import RandomSearch

    d = 5
    bounds = (-5.0 * np.ones(d), 5.0 * np.ones(d))
    fn = lambda x: -float(x @ x)
    budget = 1500

    hho_results, rs_results = [], []
    for seed in range(5):
        hho_results.append(
            HHO().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )
        rs_results.append(
            RandomSearch().maximize(fn, bounds, budget, rng=np.random.default_rng(seed)).best_fitness
        )
    assert np.mean(hho_results) > np.mean(rs_results)


# --------------------------------------------------------------------------- #
# Integration with the bot fitness function
# --------------------------------------------------------------------------- #


def test_hho_optimises_botb1_on_real_btc_train():
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

    res = HHO().maximize(
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
