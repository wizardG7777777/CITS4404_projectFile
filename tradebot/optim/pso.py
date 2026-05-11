"""Particle Swarm Optimization (PSO).

A population of "particles" — each storing a position and a velocity in the
search box — collectively explore the space. At every step a particle's
velocity is nudged toward two attractors: its own best-ever position (the
*cognitive* component) and the swarm's best-ever position (the *social*
component). The position is then advanced by adding the new velocity.

Reference implementation aligned with D1 Synopsis 1. The synopsis identifies
Shi & Eberhart 1998's inertia-weight extension as the "key extension" that
gives control over the swarm's exploration-exploitation balance, so this
module uses the modified velocity update rather than the bare 1995 form.

Velocity update (Shi & Eberhart 1998, Eq. 5 of the paper):

  v[i, d] <- w * v[i, d]
           + c1 * r1 * (pBest[i, d] - x[i, d])
           + c2 * r2 * (gBest[d]    - x[i, d])

Position update (Kennedy & Eberhart 1995):

  x[i, d] <- x[i, d] + v[i, d]

Default hyperparameters follow the classical conventions reported in the D1
synopsis (c1 = c2 = 2.0) and the textbook inertia weight (w = 0.7):

  pop_size   = 30
  w          = 0.7
  c1, c2     = 2.0, 2.0
  v_max_frac = 0.5  (per-dimension velocity cap = 0.5 * (upper - lower))

Out-of-bounds positions are clipped to the box (absorbing walls). Velocities
are not reset after a clip — the particle is free to drift back in.

References (PDF §3 *Rules of Engagement*: "you may adapt for your use code
provided in conjunction with a specific research paper ... providing you
acknowledge the code source"):

[1] J. Kennedy and R. C. Eberhart, "Particle swarm optimization," in Proc.
    IEEE ICNN'95 - Int. Conf. Neural Networks, vol. IV, pp. 1942-1948,
    Perth, WA, Australia, Nov./Dec. 1995.
[2] Y. Shi and R. C. Eberhart, "A modified particle swarm optimizer," in
    Proc. IEEE Int. Conf. Evolutionary Computation, Anchorage, AK, USA,
    May 1998, pp. 69-73.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np

from .base import Bounds, Objective, Optimizer


__all__ = ["PSO"]


class PSO(Optimizer):
    """Particle Swarm Optimization with Shi & Eberhart 1998 inertia weight."""

    NAME = "PSO"

    def __init__(
        self,
        pop_size: int = 30,
        w: float = 0.7,
        c1: float = 2.0,
        c2: float = 2.0,
        v_max_frac: float = 0.5,
    ) -> None:
        if not isinstance(pop_size, int) or pop_size < 2:
            raise ValueError(f"pop_size must be an int >= 2; got {pop_size!r}")
        if w < 0.0:
            raise ValueError(f"w must be >= 0; got {w!r}")
        if c1 < 0.0 or c2 < 0.0:
            raise ValueError(f"c1, c2 must be >= 0; got c1={c1!r}, c2={c2!r}")
        if v_max_frac <= 0.0:
            raise ValueError(f"v_max_frac must be > 0; got {v_max_frac!r}")
        self.pop_size = pop_size
        self.w = float(w)
        self.c1 = float(c1)
        self.c2 = float(c2)
        self.v_max_frac = float(v_max_frac)

    def _search(
        self,
        objective: Objective,
        bounds: Bounds,
        rng: np.random.Generator,
    ) -> None:
        lower, upper = bounds
        d = lower.size
        span = upper - lower
        v_max = self.v_max_frac * span  # per-dimension velocity cap

        # --- Initialisation ---
        x = rng.uniform(lower, upper, size=(self.pop_size, d))
        v = rng.uniform(-v_max, v_max, size=(self.pop_size, d))

        p_best_x = x.copy()
        p_best_f = np.full(self.pop_size, -np.inf)

        # Evaluate every initial position. If `budget < pop_size`, the
        # `objective` call will raise BudgetExhausted partway and the base
        # class catches it cleanly — `objective.best_x` still tracks the
        # best so far.
        for i in range(self.pop_size):
            p_best_f[i] = objective(x[i])

        # Initialise global best from the initial population.
        g_idx = int(np.argmax(p_best_f))
        g_best_x = p_best_x[g_idx].copy()
        g_best_f = float(p_best_f[g_idx])

        # --- Main loop ---
        while True:
            # Independent uniform draws per particle and per dimension.
            r1 = rng.uniform(size=(self.pop_size, d))
            r2 = rng.uniform(size=(self.pop_size, d))

            # Velocity update (Shi & Eberhart 1998).
            v = (
                self.w * v
                + self.c1 * r1 * (p_best_x - x)
                + self.c2 * r2 * (g_best_x - x)
            )
            v = np.clip(v, -v_max, v_max)

            # Position update + absorbing walls.
            x = np.clip(x + v, lower, upper)

            # Evaluate the moved swarm and update bests.
            for i in range(self.pop_size):
                f = objective(x[i])  # raises BudgetExhausted to stop
                if f > p_best_f[i]:
                    p_best_f[i] = f
                    p_best_x[i] = x[i].copy()
                    if f > g_best_f:
                        g_best_f = f
                        g_best_x = x[i].copy()
