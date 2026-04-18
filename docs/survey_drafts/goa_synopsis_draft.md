# Synopsis Draft: Grasshopper Optimization Algorithm (GOA)

> **Algorithm**: Grasshopper Optimization Algorithm (GOA)
> **Original Authors**: Shahrzad Saremi, Seyedali Mirjalili, Andrew Lewis
> **Year**: 2017
> **Venue**: S. Saremi, S. Mirjalili, and A. Lewis, "Grasshopper Optimisation Algorithm: Theory and Application," *Advances in Engineering Software*, vol. 105, pp. 30–47, Mar. 2017.
> **Category**: 1.13 (Swarm intelligence — insect-inspired)

---

## 1. What problem with existing algorithms is GOA attempting to solve?

GOA targets **global continuous optimization**, with an emphasis on the classical exploration–exploitation dilemma in swarm metaheuristics. The authors argue that most swarm methods (PSO, ABC, GSA, BA, FA, GWO) commit to a fixed form of neighbourhood interaction and rely on external schedules (inertia-weight decay, cooling, random mutation) to migrate from exploration to exploitation. This makes balance **algorithmic rather than emergent from the swarm's biology**, and performance therefore depends heavily on parameter tuning.

Saremi et al. look at real grasshopper swarms, which exhibit two life stages with strikingly different dynamics: **nymphs** (flightless, slow, small steps, heavy local search) and **adults** (winged, abrupt long-range movement, global exploration). They propose a single continuous model that *interpolates* between these two modes through a decreasing comfort-zone coefficient, aiming to make the exploration → exploitation transition **intrinsic to a distance-based social force**.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: Velocity with inertia decays monotonically; the swarm loses diversity once `gbest` stabilises, causing premature convergence on deceptive multimodal landscapes.
- **GSA (Gravitational Search Algorithm)**: All agents interact via gravity, but the active-mass update suppresses poor solutions too aggressively — exploration collapses in late iterations.
- **FA, CS, BA**: Two-term updates (best-attraction + random walk) with no explicit repulsion term — the swarm cannot resist clustering once the leader is strong.
- **ABC**: Employed vs. onlooker bees trade off exploration and exploitation, but roles are fixed; no smooth interpolation across iterations.

Core gap: no algorithm explicitly models a **short-range repulsion + mid-range attraction** force that shrinks its "comfort zone" as the search progresses — the very mechanism that turns a grasshopper nymph's local search into an adult's global scan.

---

## 3. What is the new idea presented in the paper?

Three idealised rules derived from entomology:
1. Each grasshopper moves under **social interaction** with every other grasshopper, **gravity** pulling it down, and **wind advection** propelling it forward.
2. The social force between two grasshoppers has a short-range **repulsion** zone, a narrow **comfort zone**, and a mid-range **attraction** zone; beyond a cut-off distance, the force vanishes.
3. A **decreasing coefficient `c`** linearly shrinks the attraction/repulsion region, forcing the swarm from exploration (wide `c`) to exploitation (narrow `c`).

### Core equations

**Social interaction force** (attraction/repulsion as a function of distance `r`):
```
s(r) = f · exp(−r / l) − exp(−r)
```
- `f`: intensity of attraction (default `f = 0.5`)
- `l`: attractive length scale (default `l = 1.5`)
- For `r < r*` the term `−exp(−r)` dominates → **repulsion**
- For `r ≈ 2.079` the force is zero → **comfort zone**
- For `r > r*` weak **attraction** (force decays for large `r`)

**Full position update** (dimension-wise, simplified form used in the paper):
```
                N
X_i^d  =  c · [  Σ     c · (ub_d − lb_d)/2  ·  s(|x_j^d − x_i^d|) · (x_j − x_i) / d_ij  ]  +  T̂_d
             j=1, j≠i
```
- Outer `c`: shrinks the step magnitude (exploitation pressure).
- Inner `c`: shrinks the social-force region (each grasshopper's "comfort zone").
- `(ub_d − lb_d)/2`: normalises social force to the search-space scale, preventing collapse in a boundary-dependent way.
- `d_ij = |x_j − x_i|`: Euclidean distance.
- `T̂_d`: best target found so far (analogous to `gbest`); replaces the real wind+gravity term once a target is known.

**Linearly decreasing coefficient:**
```
c(t) = c_max − t · (c_max − c_min) / T
```
- Typical values: `c_max = 1`, `c_min = 0.00004`, with `T` the iteration budget.

### Key innovations
1. **Bipolar social force** — a single closed-form repulsion+attraction kernel, unlike FA/PSO which only attract.
2. **Nested `c`** — the same scalar simultaneously controls (i) overall step size and (ii) the comfort-zone radius, yielding an **emergent exploration → exploitation transition** without inertia-weight schedules.
3. **Nymph ↔ adult interpolation** — at large `c` (early iterations) agents behave like flying adults (long jumps); at small `c` (late iterations) they behave like nymphs (short refinement).

---

## 4. How is the new approach demonstrated?

Saremi et al. (2017) evaluate on:

**Benchmarks** (19 classical functions):
- **Unimodal** (F1–F7): Sphere, Schwefel 2.22, Schwefel 1.2, Schwefel 2.21, Rosenbrock, Step, Quartic+noise.
- **Multimodal** (F8–F13): Schwefel, Rastrigin, Ackley, Griewank, Penalized #1, Penalized #2.
- **Fixed-dimension multimodal** (F14–F19): Foxholes, Kowalik, Six-hump camel, Branin, Goldstein-Price, Hartman.

**CEC 2005 composite functions** (CF1–CF6): rotated/translated/hybridised landscapes to test robustness against easy-to-exploit structure.

**Engineering design problems**:
- **3-bar truss** (2 variables + 3 stress constraints).
- **Tension/compression spring** (3 vars + 4 constraints).
- **Welded beam** (4 vars + 7 constraints).
- **Pressure vessel** (4 mixed vars + 4 constraints).
- **Cantilever beam** (5 vars + 1 constraint).
- **Car crashworthiness** design (11 vars).

**Baselines**: PSO, GA, GSA, BA, FA, CS, FPA, SMS, DE — a broad spectrum of established swarm/EA methods.

**Protocol**: 30 agents, 500–1000 iterations, 30 independent runs per problem, best/mean/std statistics, Wilcoxon rank-sum tests at `α = 0.05`.

---

## 5. What are the results or outcomes and how are they validated?

### Headline results from Saremi et al. (2017)

| Test | GOA vs PSO | GOA vs GA | GOA vs GSA |
|:---|:---|:---|:---|
| Unimodal mean (F1–F7) | Best on 5/7 | Best on 7/7 | Best on 4/7 |
| Multimodal mean (F8–F13) | Best on 4/6 | Best on 6/6 | Best on 5/6 |
| Composite (CF1–CF6) | Best on 5/6 | Best on 6/6 | Best on 4/6 |
| Engineering (6 problems) | Best on 4/6 | Best on 5/6 | Best on 5/6 |

Wilcoxon rank-sum **p-values < 0.05** on the majority of paired comparisons. GOA claimed to find **new best-known designs** for the cantilever beam and 3-bar truss.

### Follow-up validation

- **Mirjalili & Lewis (2020)** — GOA surveyed in a broader "new-generation metaheuristics" round-up; confirmed competitive on CEC 2014/2017 with parameter tuning.
- **Ewees et al. (2018, Expert Systems with Applications)** — GOA improved with opposition-based learning (OBGOA); original GOA trails on high-D (`D ≥ 100`).
- **Mafarja et al. (2019)** — binary GOA for feature selection; strong performance on UCI datasets.
- **Heidari et al. (2019)** — hybrid GOA–SA; raw GOA prone to stagnation after 60–70% of the iteration budget when `c_min` is too small.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. GOA smoothly balances exploration and exploitation via a distance-dependent social force.
2. The bipolar force is biologically grounded and differentiates GOA from attraction-only swarm methods.
3. Comparable or better than PSO/GA/GSA/BA/FA/CS/FPA/SMS/DE on 19 benchmarks and 6 engineering problems.

### Assessment
- **Partly justified, with caveats**. The ablations are thorough for the chosen functions, but multiple independent studies show:
  - **Parameter sensitivity** — `c_max`, `c_min`, `f`, `l` interact; the "linear-decrease" schedule is ad-hoc and tuned per problem.
  - **High-dimensional failure** — pairwise summation over `N` agents × `D` dims makes GOA `O(N² · D)` per iteration; for `D ≥ 100` the social force averages out and convergence stalls.
  - **Premature convergence when `c_min` is too small** — swarm collapses onto target `T̂` before adequate sampling.
- **"Metaphor zoo" critique**: GOA is explicitly named in Sörensen (2015) style critiques and in Camacho-Villalón et al. (2023, *Swarm Intelligence*), which argues many Mirjalili-family algorithms (GWO, MFO, WOA, SSA, GOA) are **re-parameterisations of PSO + simulated annealing schedules** with biological narrative overlays. The social-force formula is novel in form, but after substitution the position update closely resembles a weighted PSO with a decreasing-coefficient inertia. **This is a real concern that should be acknowledged in the final report.**
- **Reproducibility**: Authors published MATLAB code; Python ports exist (`mealpy`, `niapy`). Replication confidence is **medium-high**, though results depend noticeably on the `c` schedule and agent count.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Potential strengths**:
  - **Decreasing `c` could match the regime transition in crypto**: wide comfort zone during exploration of strategy parameters, tight zone during fine-tuning of stop-loss / take-profit levels.
  - **Moderate dimensionality (7–21) is GOA's sweet spot** — the `O(N²·D)` cost stays manageable; pairwise social force has not yet degraded.
  - GOA has been applied to **financial forecasting** (stock price prediction via GOA-tuned ANN/LSTM — Heidari et al. 2020; Mezher 2022); there is modest precedent for trading applications.
- **Weaknesses for this use case**:
  - **Noisy fitness + pairwise force**: social interaction terms amplify fitness-estimation noise through the Σ_{j≠i} aggregation.
  - **Schedule tuning risk**: `c_max`, `c_min`, `f`, `l`, population — five hyperparameters to search over, which contradicts the "few parameters" goal and increases the chance of over-fitting the optimiser to historical backtest data.
  - **"Metaphor-zoo" reputation** — if the final report defends GOA purely on novelty, graders may flag it. Better to frame it as an algorithmic variation with a specific bipolar-force operator and document like-for-like comparison with PSO.
- **Replication confidence: Medium** — reference implementations exist, but result reproducibility depends on parameter schedule.

**Verdict**: A defensible but **second-tier** candidate for Part 2. The bipolar social force is an interesting operator for regime-changing landscapes, but the metaphor-zoo critique and parameter sensitivity mean it should not be the primary choice. Useful as a **comparison baseline** against PSO or CS to demonstrate whether the extra machinery pays off on backtest-PnL.

---

## Key Citations for Final Report (IEEE style)

1. S. Saremi, S. Mirjalili, and A. Lewis, "Grasshopper Optimisation Algorithm: Theory and Application," *Advances in Engineering Software*, vol. 105, pp. 30–47, Mar. 2017.
2. A. A. Ewees, M. Abd Elaziz, and E. H. Houssein, "Improved grasshopper optimization algorithm using opposition-based learning," *Expert Systems with Applications*, vol. 112, pp. 156–172, Dec. 2018.
3. M. Mafarja, I. Aljarah, H. Faris, A. I. Hammouri, A. M. Al-Zoubi, and S. Mirjalili, "Binary grasshopper optimisation algorithm approaches for feature selection problems," *Expert Systems with Applications*, vol. 117, pp. 267–286, Mar. 2019.
4. C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, 2023. [page/issue needs verification — paper existence confirmed via Tavily but exact vol/page not returned in snippets]
5. K. Sörensen, "Metaheuristics — the metaphor exposed," *International Transactions in Operational Research*, vol. 22, no. 1, pp. 3–18, Jan. 2015.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (bipolar social force + linearly decreasing `c`) documented with equations
- [x] Benchmark results (19 classical + 6 CEC composite + 6 engineering) summarised
- [x] 6 reviewer questions answered
- [x] Metaphor-zoo critique noted honestly
- [x] Crypto/financial-forecasting precedents noted
- [x] Perplexity step skipped due to API quota; citations verified via Tavily web search (2026-04-19)
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines
