# Synopsis Draft: Ant Colony Optimization (ACO)

> **Algorithm**: Ant Colony Optimization (ACO) — Ant System (AS)
> **Original Authors**: Marco Dorigo, Vittorio Maniezzo & Alberto Colorni
> **Year**: 1992 (Dorigo's PhD thesis); 1996 (IEEE TSMC-B full paper)
> **Venue**: M. Dorigo, *Optimization, Learning and Natural Algorithms*, PhD Thesis, Politecnico di Milano, 1992; and Dorigo, Maniezzo & Colorni, "Ant System: Optimization by a colony of cooperating agents," *IEEE Trans. on Systems, Man, and Cybernetics — Part B*, vol. 26, no. 1, pp. 1–13, Feb. 1996.
> **Category**: 1.11 (Swarm Intelligence / Stigmergy-based)

---

## 1. What problem with existing algorithms is ACO attempting to solve?

ACO was designed to tackle **NP-hard combinatorial optimization problems**, with the Traveling Salesman Problem (TSP) as the canonical target. For a TSP with *n* cities the search space is `(n−1)!/2`, which explodes beyond a few hundred nodes.

The authors sought an algorithm that combined:
- **Distributed, population-based search** (unlike single-trajectory heuristics)
- **Indirect agent communication** via a shared environment (stigmergy), removing the need for centralised control
- **Adaptive memory** that accumulates positive feedback about good solution components while still evaporating bad ones
- **Parallelizable** by construction

In other words, ACO aims to replace centralized, single-agent metaheuristics with a self-organising swarm whose coordination emerges from pheromone feedback.

---

## 2. Why, or in what respect, have previous attempts failed?

- **Exact methods (branch-and-bound, cutting planes)**: Guarantee optimality but are computationally prohibitive for medium-to-large TSP instances.
- **Simulated Annealing (SA)**: Operates on a *single* candidate solution, making it fragile on deceptive multimodal landscapes; final quality depends heavily on the cooling schedule, and variance across independent runs is high.
- **Tabu Search (TS)**: Effective locally but can stagnate when tabu tenure is poorly tuned; intensification mechanisms can cause premature convergence far from the global optimum.
- **Early Genetic Algorithms (GAs)**: Require carefully designed crossover operators; naive recombination on TSP permutations frequently produces infeasible tours, forcing expensive repair heuristics.

Common weakness: none of these methods had a principled way to **share partial-solution quality information across many agents simultaneously** — something the pheromone mechanism would later provide naturally.

---

## 3. What is the new idea presented in the original paper?

The novelty is **stigmergic coordination**: artificial ants construct solutions step by step over a problem graph, depositing a numerical "pheromone" on the edges they use. Subsequent ants are biased toward edges with strong pheromone, producing emergent convergence toward high-quality tours without any centralized controller.

### Core equations

**(a) Probabilistic transition rule** — probability that ant *k* moves from city *i* to city *j*:

```
            [τ_ij]^α · [η_ij]^β
p_ij^k = ─────────────────────────────
          Σ_{z ∈ allowed_k} [τ_iz]^α · [η_iz]^β
```

- `τ_ij`: pheromone on edge (i, j) — learned memory
- `η_ij = 1/d_ij`: heuristic desirability — a priori problem knowledge
- `α ≥ 0`: weight on learned pheromone (typ. α=1)
- `β ≥ 1`: weight on heuristic (typ. β=2–5)
- `allowed_k`: cities not yet in ant *k*'s tabu list (visited set)

**(b) Pheromone update + evaporation** after all *m* ants finish their tours:

```
τ_ij(t+1) = (1 − ρ) · τ_ij(t) + Σ_{k=1}^{m} Δτ_ij^k(t)

              Q / L_k   if ant k used edge (i,j)
Δτ_ij^k =  {
              0         otherwise
```

- `ρ ∈ (0, 1)`: evaporation coefficient (typ. 0.5) — prevents unbounded accumulation and enables exploration
- `L_k`: length of ant *k*'s completed tour — *shorter tours deposit more pheromone* (positive feedback)

### Key conceptual innovations
1. **Stigmergy replaces direct messaging** — coordination emerges from the shared environment.
2. **Positive feedback** via pheromone deposition amplifies good edges.
3. **Negative feedback** via evaporation allows recovery from early bad decisions.
4. **Tabu list per ant** enforces feasibility (each city visited exactly once) without penalty functions.

---

## 4. How is the new approach demonstrated?

The authors evaluate Ant System on a suite of symmetric TSP benchmarks:

| Instance | Cities | Purpose |
|:---|:---|:---|
| Oliver30 | 30 | Small-scale sanity check |
| Eil50 / Eil75 | 50 / 75 | Medium-scale comparison |
| KroA100 | 100 | Larger instance, robustness test |

Typical hyperparameters in the original study: α=1, β=5, ρ=0.5, colony size *m* = 30, Q = 100, pheromone initialised uniformly.

Comparison baselines: **Simulated Annealing (SA), Tabu Search (TS), and early Genetic Algorithms (GAs)** using identical CPU budgets.

Reproducibility: the 1996 IEEE TSMC-B paper gives all equations, parameter values, and pseudocode explicitly; Ant System is straightforward to re-implement in a few hundred lines of code.

---

## 5. What are the results or outcomes and how are they validated?

### Original paper (Dorigo et al. 1996)

| Benchmark | AS Result | Baseline | Comparison |
|:---|:---|:---|:---|
| Oliver30 | Within ~2–3% of optimum in 100–250 iterations | SA, TS | AS matched or exceeded; faster convergence |
| Eil50 / Eil75 | Consistently near-optimal | SA, TS | AS had lower variance across runs |
| KroA100 | More robust than SA across 10 independent runs | SA | Population-based search reduced run-to-run variance |

Validation was based on multiple independent runs (mean ± std of tour length), with ANOVA-style commentary in the paper. No formal CEC-style statistical suite existed in 1992–1996.

### Post-hoc / follow-up evidence

- **Ant Colony System (ACS, Dorigo & Gambardella 1997)**: Adds a pseudo-random proportional rule (with exploitation probability `q₀`) and local pheromone update `τ_ij ← (1−φ)τ_ij + φτ₀`, improving convergence speed on larger TSP instances.
- **MAX–MIN Ant System (MMAS, Stützle & Hoos 2000)**: Bounds pheromone within `[τ_min, τ_max]` and restricts global updates to the best ant; the current state-of-the-art classical ACO variant.
- **ACOᴿ (Socha & Dorigo 2008)**: Extends ACO to continuous domains via a quality-weighted Gaussian kernel over an archive of elite solutions, enabling application outside combinatorial problems.

---

## 6. What is your assessment of the conclusions?

### Author claims (1992/1996)
1. AS effectively solves TSP through distributed, stigmergic coordination.
2. AS converges faster than SA on small/medium TSP and is more robust than SA across independent runs.
3. The paradigm generalises to other NP-hard problems (quadratic assignment, vehicle routing, scheduling).

### Assessment
- **Largely justified within scope.** The 1996 results are reproducible, and three decades of follow-up work confirm ACO's standing for graph-structured combinatorial problems. The TSP results were modest but honest (no claim of optimality on all runs).
- **Known failure modes**:
  - **Parameter sensitivity** — α, β, ρ, m all interact; defaults rarely transfer across instance classes.
  - **Stagnation** — the original AS can collapse to a single tour; MMAS and ACS were developed specifically to mitigate this.
  - **Discrete by design** — continuous optimization requires ACOᴿ or hybrid variants; naive discretisation loses resolution.

### Relevance for Part 2 (cryptocurrency trading bot, 7–21 continuous parameters)

- **Vanilla ACO is a poor fit**: Trading-bot parameters are continuous (MA window lengths, volatility thresholds, position sizing multipliers, stop-loss %). Classical AS cannot be used without discretisation, which loses granularity.
- **ACOᴿ is a reasonable candidate**: Its quality-weighted Gaussian-kernel archive handles continuous parameters and delivers anytime solutions. Archive-based sampling is naturally robust to mild noise in the fitness function (backtest PnL).
- **Main caveats for trading**:
  - Fitness evaluation noise (variance across train/val splits, regime shifts) is high; ACOᴿ lacks explicit noise-handling, unlike CMA-ES or Bayesian Optimization.
  - At 21 parameters, archive size and kernel bandwidth `σ_i` need careful tuning; scaling is worse than BO for sample-efficient optimization.
  - Published ACO applications to crypto/trading parameter tuning are sparse — most precedent is in portfolio optimization (discrete asset selection), not strategy hyperparameters.
- **Replication confidence: High** for AS/ACS/MMAS; **Medium** for ACOᴿ (published code exists but hyperparameter defaults are less well-calibrated).

**Verdict**: ACO is a historically important algorithm and a clean illustration of stigmergy, but for this project PSO, GWO, or WOA are more natural baselines in continuous space; ACOᴿ is worth mentioning in the comparative analysis as a bridge between combinatorial and continuous metaheuristics.

---

## Key Citations for Final Report (IEEE style)

1. M. Dorigo, *Optimization, Learning and Natural Algorithms*, Ph.D. thesis, Politecnico di Milano, Milan, Italy, 1992.
2. M. Dorigo, V. Maniezzo, and A. Colorni, "Ant System: Optimization by a colony of cooperating agents," *IEEE Transactions on Systems, Man, and Cybernetics — Part B*, vol. 26, no. 1, pp. 1–13, Feb. 1996.
3. M. Dorigo and L. M. Gambardella, "Ant Colony System: A cooperative learning approach to the traveling salesman problem," *IEEE Transactions on Evolutionary Computation*, vol. 1, no. 1, pp. 53–66, Apr. 1997.
4. T. Stützle and H. H. Hoos, "MAX–MIN Ant System," *Future Generation Computer Systems*, vol. 16, no. 8, pp. 889–914, Jun. 2000.
5. K. Socha and M. Dorigo, "Ant colony optimization for continuous domains," *European Journal of Operational Research*, vol. 185, no. 3, pp. 1155–1173, Mar. 2008.
6. M. Dorigo and T. Stützle, *Ant Colony Optimization*. Cambridge, MA: MIT Press, 2004.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (transition rule + pheromone update) documented with equations
- [x] Benchmark results (TSP Oliver30, Eil50, KroA100) summarized
- [x] 6 reviewer questions answered
- [x] Continuous extension (ACOᴿ) noted for Part 2 relevance
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
