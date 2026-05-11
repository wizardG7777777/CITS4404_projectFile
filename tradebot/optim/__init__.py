"""Optimisation algorithms (all hand-written, no external optim libs).

Modules will implement:
- `base`         — abstract `Optimizer` with `minimize(fitness, bounds, budget)`.
- `random_search`— single-state baseline (PDF §3 *Choosing Algorithms*: "single-state
                   algorithms ... compare on a fixed number of evaluations").
- `pso`          — Particle Swarm Optimization (Kennedy & Eberhart 1995;
                   Shi & Eberhart 1998 inertia weight). Aligns with D1 Synopsis 1.
- `hho`          — Harris Hawks Optimization (Heidari et al. 2019).
                   Aligns with D1 Synopsis 2.
"""
