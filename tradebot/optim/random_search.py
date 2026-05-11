"""Random Search — single-state stochastic baseline.

Rationale (PDF §3 *Choosing Algorithms*):

  "A more complete comparison could be achieved by also trying one of the
  single-state algorithms covered in lectures (eg. direct methods/stochastic/
  single global optimisation algorithms). In this case you would need to
  compare the outcome on a fixed number of evaluations (as opposed to, say,
  generations)."

Random Search is the simplest such algorithm: at each step it draws one
candidate uniformly at random from the box ``[lower, upper]`` and evaluates
the objective. There is no exploitation, no memory, no neighbourhood — just
i.i.d. samples from the prior. Its role in the experiment matrix is the
"zero-intelligence" reference point: if PSO or HHO cannot beat Random Search
on a fixed FE budget, the inductive biases they encode are not helping.

This is a "single-state" algorithm in the sense that the state at every
iteration is one candidate, which is immediately replaced by an independent
fresh draw. The convergence behaviour comes entirely from `Objective`'s
running-maximum bookkeeping in `base.py`.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np

from .base import Bounds, Objective, Optimizer


__all__ = ["RandomSearch"]


class RandomSearch(Optimizer):
    """Uniform-random sampling within the bounds box."""

    NAME = "RandomSearch"

    def _search(
        self,
        objective: Objective,
        bounds: Bounds,
        rng: np.random.Generator,
    ) -> None:
        lower, upper = bounds
        while True:
            x = rng.uniform(lower, upper)
            objective(x)  # raises BudgetExhausted to stop the loop
