"""Optimizer base class and shared utilities.

PDF §3 *Choosing Algorithms* is the source of two design constraints that
shape this module:

  1. "compare the outcome on a fixed number of evaluations (as opposed to,
     say, generations)" — the public `maximize` method takes a `budget`
     argument, and every algorithm stops once that many fitness evaluations
     have been spent. Generations / iterations are derived quantities.

  2. "Evaluation experiments should be repeatable" — `maximize` requires an
     explicit `np.random.Generator`. No implicit global state.

The base class wraps a user fitness function in an `Objective` accountant
that counts evaluations, records the per-call history, tracks the best
candidate, and raises `BudgetExhausted` once `budget` calls have been made.
Concrete optimisers only see this wrapped object via `_search(objective,
bounds, rng)` — they never touch the raw fitness function or the counter,
so the budget contract is enforced uniformly.

Convention: every optimiser **maximises** its objective. PDF defines
"fitness = ending cash" which we want to be as large as possible. Algorithms
whose original papers minimise (e.g. PSO, HHO) negate inside their own
implementations.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np


__all__ = [
    "BudgetExhausted",
    "Objective",
    "OptResult",
    "Optimizer",
]


Bounds = tuple[np.ndarray, np.ndarray]
FitnessFn = Callable[[np.ndarray], float]


# --------------------------------------------------------------------------- #
# Bookkeeping primitives
# --------------------------------------------------------------------------- #


class BudgetExhausted(Exception):
    """Raised by `Objective.__call__` after `budget` evaluations have been made.

    Optimisers should treat this as a normal termination signal: catch it in
    their main loop and return whatever they've found so far.
    """


class Objective:
    """Counted, length-limited wrapper around a user fitness function.

    Every concrete optimiser receives one of these and calls it like a plain
    function: ``y = objective(x)``. The wrapper:
      * casts the return value to ``float``,
      * records the call into `history`,
      * keeps a running maximum in `best_fitness` / `best_x`,
      * raises ``BudgetExhausted`` once `budget` calls have been made.

    All attributes are read-only properties so optimisers can't accidentally
    rewrite the audit trail.
    """

    def __init__(self, fitness_fn: FitnessFn, budget: int) -> None:
        if not isinstance(budget, (int, np.integer)) or budget < 0:
            raise ValueError(f"budget must be a non-negative int; got {budget!r}")
        self._fn = fitness_fn
        self._budget = int(budget)
        self._history: list[float] = []
        self._best_history: list[float] = []
        self._best_fitness: float = -np.inf
        self._best_x: np.ndarray | None = None

    def __call__(self, x: np.ndarray) -> float:
        if len(self._history) >= self._budget:
            raise BudgetExhausted(
                f"FE budget {self._budget} already spent"
            )
        x_arr = np.asarray(x, dtype=np.float64).copy()
        y = float(self._fn(x_arr))
        self._history.append(y)
        if y > self._best_fitness:
            self._best_fitness = y
            self._best_x = x_arr
        self._best_history.append(self._best_fitness)
        return y

    @property
    def n_evaluations(self) -> int:
        return len(self._history)

    @property
    def budget(self) -> int:
        return self._budget

    @property
    def budget_remaining(self) -> int:
        return self._budget - len(self._history)

    @property
    def history(self) -> np.ndarray:
        return np.array(self._history, dtype=np.float64)

    @property
    def best_history(self) -> np.ndarray:
        return np.array(self._best_history, dtype=np.float64)

    @property
    def best_fitness(self) -> float:
        return self._best_fitness

    @property
    def best_x(self) -> np.ndarray | None:
        return None if self._best_x is None else self._best_x.copy()


@dataclass
class OptResult:
    """Outcome of a single optimisation run."""

    algorithm: str
    best_x: np.ndarray
    best_fitness: float
    history: np.ndarray         # length == n_evaluations; raw fitness per call
    best_history: np.ndarray    # length == n_evaluations; running maximum
    n_evaluations: int
    wall_time: float            # seconds
    extra: dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Abstract base
# --------------------------------------------------------------------------- #


def _validate_bounds(bounds: Bounds) -> tuple[np.ndarray, np.ndarray]:
    if not isinstance(bounds, tuple) or len(bounds) != 2:
        raise ValueError(
            "bounds must be a (lower, upper) tuple of 1-D ndarrays"
        )
    lower = np.asarray(bounds[0], dtype=np.float64)
    upper = np.asarray(bounds[1], dtype=np.float64)
    if lower.ndim != 1 or upper.ndim != 1:
        raise ValueError(
            f"bounds must be 1-D; got lower.shape={lower.shape}, "
            f"upper.shape={upper.shape}"
        )
    if lower.shape != upper.shape:
        raise ValueError(
            f"lower and upper must have the same shape; "
            f"got {lower.shape} and {upper.shape}"
        )
    if lower.size == 0:
        raise ValueError("bounds must be non-empty (positive-dimensional)")
    if np.any(lower > upper):
        raise ValueError(
            "every lower bound must be <= the matching upper bound"
        )
    return lower, upper


class Optimizer(ABC):
    """Abstract base class for population-based and single-state optimisers.

    Sub-classes:
      * set `NAME`,
      * may accept algorithm-specific hyperparameters in ``__init__``,
      * implement ``_search(objective, bounds, rng)`` — the inner loop that
        calls ``objective(x)`` until ``BudgetExhausted`` is raised.

    The public method ``maximize`` is concrete and never overridden; it
    handles wrapping, timing, exception catching, and result assembly.
    """

    NAME: str = ""

    def maximize(
        self,
        fitness_fn: FitnessFn,
        bounds: Bounds,
        budget: int,
        *,
        rng: np.random.Generator,
    ) -> OptResult:
        """Run the optimisation for at most `budget` fitness evaluations.

        Parameters
        ----------
        fitness_fn :
            ``fitness_fn(x) -> float``. Will be maximised.
        bounds :
            ``(lower, upper)`` tuple of 1-D ndarrays defining the box.
        budget :
            Maximum number of times ``fitness_fn`` may be called.
        rng :
            ``np.random.Generator`` driving every stochastic choice the
            optimiser makes. Required (no implicit global RNG).
        """
        lower, upper = _validate_bounds(bounds)
        if not isinstance(rng, np.random.Generator):
            raise TypeError(
                "rng must be a numpy.random.Generator (e.g. "
                "np.random.default_rng(seed)); got "
                f"{type(rng).__name__}"
            )
        objective = Objective(fitness_fn, budget)
        start = time.perf_counter()
        try:
            self._search(objective, (lower, upper), rng)
        except BudgetExhausted:
            pass  # normal termination
        elapsed = time.perf_counter() - start

        return OptResult(
            algorithm=self.NAME,
            best_x=(
                objective.best_x
                if objective.best_x is not None
                else np.zeros(lower.size)
            ),
            best_fitness=objective.best_fitness,
            history=objective.history,
            best_history=objective.best_history,
            n_evaluations=objective.n_evaluations,
            wall_time=elapsed,
        )

    @abstractmethod
    def _search(
        self,
        objective: Objective,
        bounds: Bounds,
        rng: np.random.Generator,
    ) -> None:
        """Inner search loop — keep calling ``objective(x)`` until budget runs out."""
        raise NotImplementedError
