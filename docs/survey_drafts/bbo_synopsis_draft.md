# Synopsis Draft: Biogeography-based Optimization (BBO)

> **Algorithm**: Biogeography-based Optimization (BBO)
> **Original Author**: Dan Simon
> **Year**: 2008
> **Venue**: D. Simon, "Biogeography-Based Optimization," *IEEE Transactions on Evolutionary Computation*, vol. 12, no. 6, pp. 702–713, Dec. 2008.
> **Category**: 2.21 (Evolutionary / Ecology-inspired)

---

## 1. What problem with existing algorithms is BBO attempting to solve?

BBO addresses **global continuous numerical optimization** with a conceptually novel mechanism: rather than borrowing from *individual-level* biology (genetics, swarm behaviour) it draws from **macro-ecological island biogeography** (MacArthur & Wilson, 1967). Simon observed that evolutionary algorithms share an implicit premise — good solutions' features should be transferred to poor ones — but *no existing EA had an explicit, quality-weighted migration operator*. BBO closes that gap by making inter-solution information flow (migration) the **primary** operator, with mutation as a secondary diversifier.

---

## 2. Why, or in what respect, have previous attempts failed?

- **GA**: Selection *discards* poor individuals entirely — their useful partial features are lost. Crossover shuffles bits without regard to which solution was better.
- **PSO**: Information flows only from the single `gbest` (and `pbest`) — a rank-1 bottleneck. Premature convergence follows when `gbest` is a local optimum.
- **DE**: Mutation uses random triplets; good solutions are not systematically preferred as donors.
- **ACO**: Pheromone is per-edge, not per-dimension — natively discrete.

The conceptual gap BBO fills: a *probabilistic, rank-weighted, per-dimension* information flow from high-fitness solutions to low-fitness ones, without discarding the low-fitness habitats.

---

## 3. What is the new idea presented in the paper?

### Mapping

| Biogeography | BBO |
|:---|:---|
| Habitat (island) | Candidate solution |
| Habitat Suitability Index (HSI) | Fitness |
| Suitability Index Variable (SIV) | Decision variable (dimension) |
| Species immigration | Incoming feature replacement |
| Species emigration | Outgoing feature donation |

### Core equations (linear migration model)

With habitats sorted by HSI rank `k` (1 = worst, N = best, or vice versa — Simon's paper uses the opposite convention; the formulas below use `k` = species count):

```
Immigration rate:  λ_k = I · (1 − k/N)       (high for low-HSI habitats)
Emigration rate:   µ_k = E · (k/N)           (high for high-HSI habitats)
```

Typical values: `I = E = 1`. Alternatives to the linear model include sinusoidal, quadratic, and exponential curves (Ma 2010) — often giving measurable gains.

### Migration operator

For each non-elite habitat `H_i` and each dimension `d`:
```
with probability λ_i:
    select donor habitat H_j with probability ∝ µ_j  (roulette wheel)
    H_i.SIV_d ← H_j.SIV_d
```

### Mutation operator

Each SIV may be randomly replaced with probability `m_i`, where `m_i` is derived from a species-count probability distribution — intermediate species counts (moderate-quality solutions) mutate more, extremes mutate less.

### Key innovations
1. **Rank-weighted, dimension-wise migration** — the explicit information-transfer operator missing from GA/PSO/DE.
2. **No crossover, no velocity** — just migration + mutation + elitism.
3. **Solutions are never discarded**, only updated — preserves population diversity throughout.

---

## 4. How is the new approach demonstrated?

Simon (2008) validates BBO on **14 standard continuous benchmarks at D = 20**:

| Function | Characteristic |
|:---|:---|
| Sphere | Unimodal separable |
| Rosenbrock | Unimodal non-separable |
| Rastrigin, Griewank, Ackley | Multimodal |
| Schwefel | Deceptive |
| Step, Step-Noise | Discrete / noisy |
| Quartic, Fletcher-Powell | High-dim pathological |
| Michalewicz, Goldstein-Price, and others | Mixed |

Baselines (7): **GA, PSO, DE, ACO, SGA, ES, PBIL**. Protocol: 100 iterations, 50 monte-carlo runs, 50-member population. Statistical significance tested.

---

## 5. What are the results or outcomes and how are they validated?

| Category | BBO vs. competitors |
|:---|:---|
| Overall ranking | BBO top-3 on **most** of the 14 functions |
| Sphere (unimodal) | ~20× faster convergence than ES/GA |
| Rastrigin, Griewank | Competitive; PSO sometimes matches |
| Ackley | BBO slightly worse than ACO / DE |
| Schwefel | BBO mid-pack |
| Step-Noise | BBO robust (migration preserves diversity) |

### Follow-up validation
- **Ma (2010)** — compared six migration models (linear, trapezoidal, quadratic, sinusoidal, Gaussian, constant); sinusoidal often best.
- **DE/BBO hybrid** (Gong et al. 2010) — plugs DE's mutation into BBO's migration; outperforms either alone.
- **Blended BBO** (Ma & Simon 2013) — uses a convex combination of donor and incumbent SIVs instead of hard replacement; improves exploitation.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. BBO exploits population information more systematically than GA/PSO.
2. BBO is competitive with state-of-the-art EAs on standard benchmarks.
3. The ecological metaphor yields an algorithmically distinct operator (migration).

### Assessment
- **Justified on the benchmark evidence** — Simon's statistical protocol is sound. The claim that BBO introduces a *genuinely new* operator (vs. a rebranding of crossover) is defensible: migration replaces one SIV at a time, quality-weighted, which differs structurally from GA crossover.
- **Known weaknesses**:
  - **Slow exploration** early on — migration alone only *mixes* existing SIVs; until mutation fires, the SIV *values* in the population are static.
  - **Linear migration model is suboptimal** — later variants (sinusoidal, quadratic) consistently beat it.
  - **Elitism is mandatory** in practice; without it BBO can lose its best solutions to migration corruption.
  - **Not rotation-invariant** (SIV-wise operator).

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - Migration is naturally **exploitation-heavy** — good for refining already-decent trading parameter sets.
  - No velocity/inertia — fewer parameters to tune than PSO.
  - Elitism + per-SIV update means a single noisy bad evaluation does not destroy an entire candidate.
- **Weaknesses for this use case**:
  - **Non-stationary fitness landscape** (crypto regime changes) violates BBO's implicit assumption that HSI rankings are stable.
  - **Slow exploration** is problematic when the initial population is bad — unlike PSO which can "lunge" via velocity.
  - Published financial applications are sparser than for PSO / DE / GA; migration-model selection would need empirical sweep.
- **Replication confidence: High** — Simon's MATLAB reference implementation is publicly available; the algorithm is ~50 lines of pseudocode.

**Verdict**: Interesting comparison point for its *conceptually distinct operator*, but not the first-choice optimizer for a noisy trading-bot landscape. Include it in comparative analysis to showcase the migration vs. velocity vs. pheromone distinction in the taxonomy.

---

## Key Citations for Final Report (IEEE style)

1. D. Simon, "Biogeography-Based Optimization," *IEEE Transactions on Evolutionary Computation*, vol. 12, no. 6, pp. 702–713, Dec. 2008.
2. H. Ma, "An analysis of the equilibrium of migration models for biogeography-based optimization," *Information Sciences*, vol. 180, no. 18, pp. 3444–3464, Sep. 2010.
3. W. Gong, Z. Cai, C. X. Ling, and H. Li, "A real-coded biogeography-based optimization with mutation," *Applied Mathematics and Computation*, vol. 216, no. 9, pp. 2749–2758, Jul. 2010.
4. H. Ma and D. Simon, "Blended biogeography-based optimization for constrained optimization," *Engineering Applications of Artificial Intelligence*, vol. 24, no. 3, pp. 517–525, Apr. 2011.
5. R. H. MacArthur and E. O. Wilson, *The Theory of Island Biogeography*. Princeton, NJ: Princeton Univ. Press, 1967.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (migration + mutation) documented with equations
- [x] Benchmark results (14-function suite, 7 baselines) summarized
- [x] 6 reviewer questions answered
- [x] Variants (sinusoidal migration, blended BBO) noted
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
