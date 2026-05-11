"""Harris Hawks Optimization (HHO).

A population of hawks circles a "rabbit" (the best-so-far position). At
every iteration each hawk draws a fresh **escape energy**

    E = 2 * E_0 * (1 - t / T),    E_0 ~ U(-1, 1)

If |E| >= 1 the hawk explores (one of two perch strategies). If |E| < 1 it
exploits, choosing among **four behaviourally distinct rules** gated jointly
by |E| and a fresh escape chance r ~ U(0, 1):

    r >= 0.5,  |E| >= 0.5  ->  soft besiege
    r >= 0.5,  |E| <  0.5  ->  hard besiege
    r <  0.5,  |E| >= 0.5  ->  soft besiege with rapid Levy dives
    r <  0.5,  |E| <  0.5  ->  hard besiege with rapid Levy dives

Reference implementation aligned with D1 Synopsis 2. Three structural choices
flagged as the algorithm's novelty there are reproduced verbatim:

    (i)   E_0 ~ U(-1, 1) so E oscillates in sign within a decaying envelope.
    (ii)  Exploitation is four behaviourally distinct rules — not one blended
          update.
    (iii) In dive modes, Y and a Levy-perturbed Z = Y + S . LF(D) are each
          evaluated and committed **only on strict improvement** (greedy
          acceptance). Otherwise the hawk stays at X.

The Levy step uses Mantegna's algorithm with the paper's fixed beta = 1.5.

Hyperparameters:

  pop_size = 30   (Heidari et al. 2019 report uses 30 agents / 500 iterations)

The maximum-iteration constant T used inside the annealing factor is derived
from the FE budget and pop_size at run time (T = budget / pop_size), so the
energy schedule decays smoothly over the actual horizon allowed by the
fixed-evaluation budget the experiment framework enforces.

Out-of-bounds positions (and the auxiliary Y, Z candidates inside dive modes)
are clipped to the search box.

References (PDF §3 *Rules of Engagement*: "you may adapt for your use code
provided in conjunction with a specific research paper ... providing you
acknowledge the code source"):

[1] A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and
    H. Chen, "Harris hawks optimization: Algorithm and applications,"
    Future Gener. Comput. Syst., vol. 97, pp. 849-872, Aug. 2019,
    doi: 10.1016/j.future.2019.02.028.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import math

import numpy as np

from .base import Bounds, Objective, Optimizer


__all__ = ["HHO"]


class HHO(Optimizer):
    """Harris Hawks Optimization with energy-gated 6-rule update."""

    NAME = "HHO"

    # Heavy-tailed step exponent for the Levy flight (Heidari et al. 2019).
    LEVY_BETA: float = 1.5

    def __init__(self, pop_size: int = 30) -> None:
        if not isinstance(pop_size, int) or pop_size < 2:
            raise ValueError(f"pop_size must be an int >= 2; got {pop_size!r}")
        self.pop_size = pop_size

    # --------------------------------------------------------------------- #
    # Levy flight step via Mantegna's algorithm (Heidari et al. 2019 Eq. 9).
    # --------------------------------------------------------------------- #

    def _levy_step(self, d: int, rng: np.random.Generator) -> np.ndarray:
        beta = self.LEVY_BETA
        sigma = (
            math.gamma(1.0 + beta)
            * math.sin(math.pi * beta / 2.0)
            / (math.gamma((1.0 + beta) / 2.0) * beta * 2.0 ** ((beta - 1.0) / 2.0))
        ) ** (1.0 / beta)
        u = rng.standard_normal(d) * sigma
        v = rng.standard_normal(d)
        return 0.01 * u / np.power(np.abs(v), 1.0 / beta)

    # --------------------------------------------------------------------- #
    # Main search loop.
    # --------------------------------------------------------------------- #

    def _search(
        self,
        objective: Objective,
        bounds: Bounds,
        rng: np.random.Generator,
    ) -> None:
        lower, upper = bounds
        d = lower.size
        pop = self.pop_size

        # T is the annealing horizon. We tie it to the FE budget so that E's
        # envelope (1 - t/T) decays over the actual run length.
        T = max(1, objective.budget // pop)

        # --- Initialise hawks uniformly in the box and evaluate. ---
        X = rng.uniform(lower, upper, size=(pop, d))
        fitness = np.full(pop, -np.inf)
        for i in range(pop):
            fitness[i] = objective(X[i])

        rabbit_idx = int(np.argmax(fitness))
        rabbit_pos = X[rabbit_idx].copy()
        rabbit_fit = float(fitness[rabbit_idx])

        # --- Main iterations. ---
        for t in range(T):
            X_mean = X.mean(axis=0)
            scale = 1.0 - (t + 1) / T  # in (0, 1]

            for i in range(pop):
                # Independent E_0 per hawk per iteration (Heidari Eq. 3).
                E0 = rng.uniform(-1.0, 1.0)
                E = 2.0 * E0 * scale
                absE = abs(E)

                if absE >= 1.0:
                    # ===== EXPLORATION (Heidari Eq. 1) =====
                    q = rng.uniform()
                    if q >= 0.5:
                        # Perch on a randomly chosen family member.
                        rand_idx = int(rng.integers(pop))
                        r1 = rng.uniform()
                        r2 = rng.uniform()
                        X[i] = X[rand_idx] - r1 * np.abs(
                            X[rand_idx] - 2.0 * r2 * X[i]
                        )
                    else:
                        # Perch relative to family mean + a random offset.
                        r3 = rng.uniform()
                        r4 = rng.uniform()
                        X[i] = (rabbit_pos - X_mean) - r3 * (
                            lower + r4 * (upper - lower)
                        )
                    X[i] = np.clip(X[i], lower, upper)
                    fitness[i] = objective(X[i])

                else:
                    # ===== EXPLOITATION (|E| < 1) =====
                    r = rng.uniform()
                    J = 2.0 * (1.0 - rng.uniform())  # random "jump strength"

                    if r >= 0.5 and absE >= 0.5:
                        # Mode 1: Soft besiege (Heidari Eq. 4).
                        X[i] = (rabbit_pos - X[i]) - E * np.abs(
                            J * rabbit_pos - X[i]
                        )
                        X[i] = np.clip(X[i], lower, upper)
                        fitness[i] = objective(X[i])

                    elif r >= 0.5 and absE < 0.5:
                        # Mode 2: Hard besiege (Heidari Eq. 6).
                        X[i] = rabbit_pos - E * np.abs(rabbit_pos - X[i])
                        X[i] = np.clip(X[i], lower, upper)
                        fitness[i] = objective(X[i])

                    elif r < 0.5 and absE >= 0.5:
                        # Mode 3: Soft besiege with rapid dives (Eq. 7-8).
                        Y = rabbit_pos - E * np.abs(J * rabbit_pos - X[i])
                        Y = np.clip(Y, lower, upper)
                        f_Y = objective(Y)
                        if f_Y > fitness[i]:  # strict improvement
                            X[i] = Y
                            fitness[i] = f_Y
                        else:
                            S = rng.uniform(0.0, 1.0, size=d)
                            Z = Y + S * self._levy_step(d, rng)
                            Z = np.clip(Z, lower, upper)
                            f_Z = objective(Z)
                            if f_Z > fitness[i]:
                                X[i] = Z
                                fitness[i] = f_Z
                            # else: stay at X[i] (Y, Z both failed greedy).

                    else:
                        # Mode 4: Hard besiege with rapid dives.
                        Y = rabbit_pos - E * np.abs(J * rabbit_pos - X_mean)
                        Y = np.clip(Y, lower, upper)
                        f_Y = objective(Y)
                        if f_Y > fitness[i]:
                            X[i] = Y
                            fitness[i] = f_Y
                        else:
                            S = rng.uniform(0.0, 1.0, size=d)
                            Z = Y + S * self._levy_step(d, rng)
                            Z = np.clip(Z, lower, upper)
                            f_Z = objective(Z)
                            if f_Z > fitness[i]:
                                X[i] = Z
                                fitness[i] = f_Z

                # Update rabbit (best-so-far across all hawks).
                if fitness[i] > rabbit_fit:
                    rabbit_fit = float(fitness[i])
                    rabbit_pos = X[i].copy()
