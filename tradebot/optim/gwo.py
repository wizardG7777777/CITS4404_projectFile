"""Grey Wolf Optimizer (GWO).

A population of wolves circles the three best-so-far solutions. At every
iteration the current population is ranked by fitness; the top three wolves
are labelled alpha, beta and delta (in descending order). All wolves then
update their positions to the average of three "candidate positions", each
computed by following one of these leaders:

    For each leader L in {alpha, beta, delta}:
        A = 2 a r1 - a           ( r1 ~ U(0, 1)^d ; a decays from 2 to 0 )
        C = 2 r2                 ( r2 ~ U(0, 1)^d ; random leader weighting )
        D_L  = |C . X_L - X|
        X_L_candidate = X_L - A . D_L

    X_new = (X_alpha_c + X_beta_c + X_delta_c) / 3

Mechanism notes:
  * |A| > 1 pushes a wolf away from its leader (exploration);
  * |A| < 1 pulls a wolf toward its leader (exploitation);
  * a decays linearly from 2 to 0 over the iteration budget, so the
    exploration-to-exploitation balance is fixed by the run schedule rather
    than data-conditioned (contrast with HHO's E gating).

Structural place between PSO and HHO:
  * PSO uses a single attractor (g-best) with velocity memory.
  * GWO uses three attractors and no memory — one update rule, averaged.
  * HHO uses a single attractor (rabbit) with six behaviourally distinct
    update rules gated by escape energy and a fresh random draw.

Hyperparameters (default):
  pop_size = 30                  (matches Mirjalili et al. 2014 benchmarks)

The maximum-iteration constant T used inside the a-schedule is derived
from the FE budget and pop_size at run time (T = budget / pop_size), so
the linear decay of a matches the actual horizon allowed by the FE budget.

References (PDF §3 *Rules of Engagement*: "you may adapt for your use code
provided in conjunction with a specific research paper ... providing you
acknowledge the code source"):

[1] S. Mirjalili, S. M. Mirjalili and A. Lewis, "Grey wolf optimizer,"
    Adv. Eng. Softw., vol. 69, pp. 46-61, Mar. 2014,
    doi: 10.1016/j.advengsoft.2013.12.007.

A 2023 peer-reviewed critique by Camacho-Villalon, Dorigo and Stuetzle
showed algebraically that GWO can be reduced to an inertia-weight PSO
variant; we adopt GWO here partly to test that claim empirically on the
non-stationary BTC fitness landscape:

[2] C. L. Camacho-Villalon, M. Dorigo and T. Stuetzle, "Exposing the grey
    wolf, moth-flame, whale, firefly, bat, and antlion algorithms: Six
    misleading optimization techniques inspired by bestial metaphors,"
    Int. Trans. Oper. Res., vol. 30, no. 6, pp. 2945-2971, Nov. 2023,
    doi: 10.1111/itor.13176.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np

from .base import Bounds, Objective, Optimizer


__all__ = ["GWO"]


class GWO(Optimizer):
    """Grey Wolf Optimizer with three-leader averaged updates."""

    NAME = "GWO"

    def __init__(self, pop_size: int = 30) -> None:
        if not isinstance(pop_size, int) or pop_size < 3:
            # Need at least three wolves so alpha, beta, delta are distinct.
            raise ValueError(f"pop_size must be an int >= 3; got {pop_size!r}")
        self.pop_size = pop_size

    def _search(
        self,
        objective: Objective,
        bounds: Bounds,
        rng: np.random.Generator,
    ) -> None:
        lower, upper = bounds
        d = lower.size
        pop = self.pop_size

        # Annealing horizon tied to FE budget so `a` decays over the actual run.
        T = max(1, objective.budget // pop)

        # --- Initialise wolves uniformly and evaluate. ---
        X = rng.uniform(lower, upper, size=(pop, d))
        fitness = np.full(pop, -np.inf)
        for i in range(pop):
            fitness[i] = objective(X[i])

        # Top-three indices by fitness (descending, since we maximise).
        order = np.argsort(-fitness)
        alpha_x = X[order[0]].copy()
        alpha_f = float(fitness[order[0]])
        beta_x = X[order[1]].copy()
        beta_f = float(fitness[order[1]])
        delta_x = X[order[2]].copy()
        delta_f = float(fitness[order[2]])

        # --- Main loop. ---
        for t in range(T):
            a = 2.0 * (1.0 - (t + 1) / T)  # linear decay from ~2 to ~0

            for i in range(pop):
                # Three candidate positions, one per leader.
                candidates = np.zeros((3, d), dtype=np.float64)
                for k, leader in enumerate((alpha_x, beta_x, delta_x)):
                    r1 = rng.uniform(size=d)
                    r2 = rng.uniform(size=d)
                    A = 2.0 * a * r1 - a
                    C = 2.0 * r2
                    D = np.abs(C * leader - X[i])
                    candidates[k] = leader - A * D

                # Average the three candidates, clip, evaluate.
                X[i] = np.clip(candidates.mean(axis=0), lower, upper)
                fitness[i] = objective(X[i])

                # Maintain top-three with on-the-fly bubbling.
                fi = float(fitness[i])
                if fi > alpha_f:
                    delta_x, delta_f = beta_x, beta_f
                    beta_x, beta_f = alpha_x, alpha_f
                    alpha_x, alpha_f = X[i].copy(), fi
                elif fi > beta_f:
                    delta_x, delta_f = beta_x, beta_f
                    beta_x, beta_f = X[i].copy(), fi
                elif fi > delta_f:
                    delta_x, delta_f = X[i].copy(), fi
