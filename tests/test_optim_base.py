"""Unit tests for `tradebot.optim.base`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.optim.base import (
    BudgetExhausted,
    Objective,
    OptResult,
    Optimizer,
)


# --------------------------------------------------------------------------- #
# Objective — counter, history, budget guard
# --------------------------------------------------------------------------- #


def test_objective_counts_evaluations_and_records_history():
    obj = Objective(lambda x: float(x[0]), budget=3)
    obj(np.array([1.0]))
    obj(np.array([2.0]))
    obj(np.array([0.5]))
    assert obj.n_evaluations == 3
    np.testing.assert_array_equal(obj.history, np.array([1.0, 2.0, 0.5]))


def test_objective_tracks_running_maximum():
    obj = Objective(lambda x: float(x[0]), budget=4)
    obj(np.array([1.0]))
    obj(np.array([2.5]))
    obj(np.array([2.0]))
    obj(np.array([2.4]))
    np.testing.assert_array_equal(obj.best_history, np.array([1.0, 2.5, 2.5, 2.5]))
    assert obj.best_fitness == 2.5
    np.testing.assert_array_equal(obj.best_x, np.array([2.5]))


def test_objective_budget_remaining_decrements():
    obj = Objective(lambda x: 0.0, budget=5)
    assert obj.budget_remaining == 5
    obj(np.array([0.0]))
    obj(np.array([0.0]))
    assert obj.budget_remaining == 3


def test_objective_raises_budget_exhausted_after_limit():
    obj = Objective(lambda x: 0.0, budget=2)
    obj(np.array([0.0]))
    obj(np.array([0.0]))
    with pytest.raises(BudgetExhausted, match="budget 2"):
        obj(np.array([0.0]))


def test_objective_negative_budget_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        Objective(lambda x: 0.0, budget=-1)


def test_objective_zero_budget_raises_on_first_call():
    obj = Objective(lambda x: 0.0, budget=0)
    with pytest.raises(BudgetExhausted):
        obj(np.array([0.0]))


def test_objective_best_x_is_a_defensive_copy():
    """Mutating the returned best_x must not corrupt internal state."""
    obj = Objective(lambda x: float(x[0]), budget=2)
    obj(np.array([1.0]))
    bx = obj.best_x
    assert bx is not None
    bx[0] = -999.0
    np.testing.assert_array_equal(obj.best_x, np.array([1.0]))


def test_objective_handles_non_finite_return_values():
    """Treats -inf / nan as 'never the best so far'."""
    obj = Objective(lambda x: float(x[0]), budget=3)
    obj(np.array([1.0]))
    obj(np.array([-np.inf]))
    obj(np.array([np.nan]))
    # Best fitness is still 1.0 (NaN comparisons are False; -inf < 1).
    assert obj.best_fitness == 1.0


# --------------------------------------------------------------------------- #
# Optimizer.maximize — generic contract tests against a dummy subclass
# --------------------------------------------------------------------------- #


class _AlwaysOriginOptimizer(Optimizer):
    """Test stub: evaluates the origin every step (deterministic)."""

    NAME = "AlwaysOrigin"

    def _search(self, objective, bounds, rng):
        lower, _upper = bounds
        x0 = np.zeros_like(lower)
        while True:
            objective(x0)


def test_optimizer_maximize_returns_opt_result_with_complete_fields():
    res = _AlwaysOriginOptimizer().maximize(
        fitness_fn=lambda x: -float(x @ x),  # negative L2 => maximum at origin
        bounds=(np.array([-1.0, -1.0]), np.array([1.0, 1.0])),
        budget=10,
        rng=np.random.default_rng(0),
    )
    assert isinstance(res, OptResult)
    assert res.algorithm == "AlwaysOrigin"
    assert res.best_fitness == 0.0
    np.testing.assert_array_equal(res.best_x, np.zeros(2))
    assert res.n_evaluations == 10
    assert res.history.shape == (10,)
    assert res.best_history.shape == (10,)
    assert res.wall_time >= 0.0


def test_optimizer_maximize_enforces_budget_exactly():
    """Even an optimiser that loops forever must stop at exactly `budget`."""
    res = _AlwaysOriginOptimizer().maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.zeros(3), np.ones(3)),
        budget=50,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == 50


def test_optimizer_maximize_validates_bounds_shape():
    with pytest.raises(ValueError, match="same shape"):
        _AlwaysOriginOptimizer().maximize(
            fitness_fn=lambda x: 0.0,
            bounds=(np.zeros(3), np.ones(4)),
            budget=10,
            rng=np.random.default_rng(0),
        )


def test_optimizer_maximize_rejects_inverted_bounds():
    with pytest.raises(ValueError, match="lower bound must be"):
        _AlwaysOriginOptimizer().maximize(
            fitness_fn=lambda x: 0.0,
            bounds=(np.array([1.0]), np.array([0.0])),
            budget=10,
            rng=np.random.default_rng(0),
        )


def test_optimizer_maximize_rejects_empty_bounds():
    with pytest.raises(ValueError, match="non-empty"):
        _AlwaysOriginOptimizer().maximize(
            fitness_fn=lambda x: 0.0,
            bounds=(np.array([]), np.array([])),
            budget=10,
            rng=np.random.default_rng(0),
        )


def test_optimizer_maximize_requires_explicit_rng():
    with pytest.raises(TypeError, match="numpy.random.Generator"):
        _AlwaysOriginOptimizer().maximize(
            fitness_fn=lambda x: 0.0,
            bounds=(np.zeros(2), np.ones(2)),
            budget=10,
            rng=42,  # type: ignore[arg-type]
        )


def test_optimizer_zero_budget_returns_default_best_x():
    """Budget = 0 → no evaluation; best_x falls back to a zero vector."""
    res = _AlwaysOriginOptimizer().maximize(
        fitness_fn=lambda x: 0.0,
        bounds=(np.array([-1.0, -1.0]), np.array([1.0, 1.0])),
        budget=0,
        rng=np.random.default_rng(0),
    )
    assert res.n_evaluations == 0
    assert res.best_fitness == -np.inf
    np.testing.assert_array_equal(res.best_x, np.zeros(2))
    assert res.history.shape == (0,)
