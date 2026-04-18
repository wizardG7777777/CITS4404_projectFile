# Synopsis Draft: Firefly Algorithm (FA)

> **Algorithm**: Firefly Algorithm (FA)
> **Original Author**: Xin-She Yang
> **Year**: 2008 (book chapter) / 2009 (conference paper)
> **Venue**: X.-S. Yang, "Firefly Algorithms for Multimodal Optimization," in *Stochastic Algorithms: Foundations and Applications (SAGA 2009)*, Lecture Notes in Computer Science, vol. 5792, Springer, 2009, pp. 169–178. Also: X.-S. Yang, *Nature-Inspired Metaheuristic Algorithms*, 1st/2nd ed., Luniver Press, 2008/2010.
> **Category**: 1.11 (Swarm Intelligence — bioluminescence / attraction-based)

---

## 1. What problem with existing algorithms is FA attempting to solve?

FA targets **multimodal continuous optimization** where the user wants to find **multiple high-quality optima in a single run**, not just one global best. Yang observed that PSO's `gbest` mechanism is a *rank-1 information bottleneck*: every particle is pulled toward the single best, and the swarm inevitably collapses onto one region, losing the ability to characterise alternative peaks. FA replaces this global pull with **locality-based pairwise attraction** where influence decays with distance — allowing the swarm to self-subdivide into sub-swarms, each converging on a different optimum.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: Single `gbest` → the whole swarm converges on one peak. Hard to recover multiple optima without restarts.
- **GA**: Multimodal GAs exist (niching, sharing, crowding) but require additional mechanisms (distance thresholds, niche radii) that must be tuned per problem. Crossover on real vectors is conceptually forced.
- **Simulated Annealing**: Single-agent; finding multiple optima requires multiple independent runs.
- **Random search**: No coordination at all.

FA's innovation is to **embed the locality mechanism directly in the update rule** — the distance-decay in the attraction term is the niching mechanism.

---

## 3. What is the new idea presented in the paper?

Three idealized rules:
1. **Fireflies are unisex** — any firefly can be attracted to any other (symmetric interaction topology).
2. **Attractiveness ∝ brightness**, and both **decrease with distance** (locality).
3. **Brightness is defined by the objective function** (fitness).

### Core equations

**Attractiveness** as a function of Euclidean distance `r`:
```
β(r) = β_0 · exp(−γ · r²)
```
- `β_0` = attractiveness at `r = 0` (typically 1)
- `γ` = light absorption coefficient — **the key tuning knob** that controls niche radius

**Movement of firefly `i` toward a brighter firefly `j`**:
```
x_i^(t+1) = x_i^t + β_0 · exp(−γ · r_ij²) · (x_j^t − x_i^t) + α_t · (rand − 0.5)
```
- `r_ij = ||x_i − x_j||` (Euclidean distance)
- `α_t · (rand − 0.5)`: random perturbation term
- `α_t = α_0 · δ^t`, with decay factor `δ ∈ [0.9, 0.99]`

### Key innovations
1. **Distance-dependent attraction** → emergent multi-swarm / niching without explicit niche definitions.
2. **PSO is a limiting case**: as `γ → 0`, attraction becomes distance-independent and FA degenerates to a PSO-like (every pair pulls equally).
3. **Parallel random search is the other limit**: as `γ → ∞`, attraction vanishes at any finite distance.
4. **Only three parameters beyond population size**: `β_0`, `γ`, `α_0` (+ decay `δ`).

---

## 4. How is the new approach demonstrated?

Yang (2009) validates FA on:

**Multimodal benchmark functions**:
- Ackley, Rastrigin, Schwefel, Rosenbrock
- Michalewicz, Griewank
- Easom (very deep but narrow global optimum — classic multi-peak challenge)

**Multi-peak demo functions**: specifically constructed to have 2, 4, or more equally-deep optima to show FA finds *all* of them simultaneously.

Baselines: **PSO, GA**. Typical config: `n = 20–40` fireflies, `β_0 = 1`, `γ ≈ 0.1–1` (scaled to search-space size), `α_0 ≈ 0.2`, max iters `t ≤ 100`.

Later engineering studies (Yang 2010; Gandomi et al. 2011) extend FA to welded beam, spring design, pressure vessel, and structural optimization.

---

## 5. What are the results or outcomes and how are they validated?

### Headline findings (Yang 2009 and follow-ups)

| Benchmark | FA vs. PSO | FA vs. GA |
|:---|:---|:---|
| Ackley, Rastrigin | Comparable or better accuracy | FA typically wins |
| Multi-peak demo | FA finds all peaks in one run | PSO finds only one |
| Michalewicz (D=16) | ~100% success | PSO lower success |
| Engineering design | Matches best published | Beats basic GA |

Statistical significance verified via Wilcoxon signed-rank tests in follow-up studies (Gandomi 2011, Fister et al. 2013).

### Follow-up validation
- **Gandomi, Yang & Alavi (2011)**: FA competitive on structural engineering problems.
- **Fister, Fister & Yang (2013)**: comprehensive FA review; confirms multimodal strength.
- **Adaptive FA variants** (memetic FA, Lévy-flight FA, chaotic FA) — all improve basic FA on high-dimensional problems.
- **Known reduction**: `γ = 0` limit recovers PSO-like behaviour.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. FA finds multiple optima simultaneously without explicit niching machinery.
2. FA is as simple as PSO but more effective on multimodal landscapes.
3. PSO is a special case (`γ → 0`).

### Assessment
- **Largely justified** for `D ≤ 20` multimodal benchmarks. The emergent multi-swarm behaviour is genuine and reproducible.
- **Known weaknesses**:
  - **O(n²) per iteration** — every firefly compares to every other. For `n = 100` and 1000 iterations this is 10⁷ distance evaluations, problematic for expensive fitness functions.
  - **`γ` is hard to tune** — too small → pure PSO (premature convergence); too large → pure random search. Optimal `γ` depends on search-space scale and problem modality.
  - **High dimensions**: distance norms become uninformative (curse of dimensionality), and the `exp(−γ r²)` term saturates at 0. Adaptive / Lévy-flight variants exist but add parameters.
  - **No rigorous convergence proof** — empirically it works, but theoretical guarantees are weaker than DE/CMA-ES.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - **Multimodal is realistic**: trading parameter spaces often have several viable regimes (conservative vs. aggressive vs. breakout). FA could surface *all* of them in one run, giving the team choices rather than a single winner.
  - Simple to implement (≈30 lines of Python).
  - Few parameters to tune (3 + population size).
- **Weaknesses for this use case**:
  - **O(n²) fitness-evaluation scaling** is a real problem when each evaluation is a backtest (seconds to minutes). With `n = 30` and 200 iters that's **180,000 backtests** — likely infeasible.
  - **21-dim space** stretches FA's sweet spot; the distance-decay mechanism weakens as dimensions grow.
  - **Noisy fitness** corrupts brightness comparisons; need fitness averaging.
  - **`γ` tuning on crypto landscapes** is hard without prior experiments.
- **Replication confidence: High** — reference implementations in Python (`FireflyAlgorithm` pip package), MATLAB, and R are readily available.

**Verdict**: FA is a genuinely interesting comparison point *because* of its niching behaviour; useful for the **conclusion/comparative analysis** to illustrate a different design philosophy (locality-based attraction vs. global `gbest` vs. migration vs. pheromone). For the trading-bot implementation itself, PSO/DE/CS are more practical first choices due to lower per-iter cost.

---

## Key Citations for Final Report (IEEE style)

1. X.-S. Yang, "Firefly Algorithms for Multimodal Optimization," in *Stochastic Algorithms: Foundations and Applications*, LNCS vol. 5792, Springer-Verlag, 2009, pp. 169–178.
2. X.-S. Yang, *Nature-Inspired Metaheuristic Algorithms*, 2nd ed. Frome, UK: Luniver Press, 2010, ch. 8.
3. A. H. Gandomi, X.-S. Yang, and A. H. Alavi, "Mixed variable structural optimization using Firefly Algorithm," *Computers & Structures*, vol. 89, no. 23–24, pp. 2325–2336, Dec. 2011.
4. I. Fister, I. Fister Jr., X.-S. Yang, and J. Brest, "A comprehensive review of firefly algorithms," *Swarm and Evolutionary Computation*, vol. 13, pp. 34–46, Dec. 2013.
5. X.-S. Yang, "Firefly algorithm, stochastic test functions and design optimisation," *Int. J. Bio-Inspired Computation*, vol. 2, no. 2, pp. 78–84, 2010.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (attractiveness + movement equation) documented
- [x] Benchmark results (Ackley, Rastrigin, multi-peak demos) summarized
- [x] 6 reviewer questions answered
- [x] O(n²) cost and `γ` tuning limitation explicitly flagged
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
