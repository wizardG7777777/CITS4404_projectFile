# Synopsis Draft: Artificial Bee Colony (ABC)

> **Algorithm**: Artificial Bee Colony (ABC)
> **Original Author**: Derviş Karaboga
> **Year**: 2005 (Technical Report TR06); 2007 (J. Global Optimization full paper)
> **Venue**: D. Karaboga, "An Idea Based on Honey Bee Swarm for Numerical Optimization," Erciyes Univ., Tech. Rep. TR06, 2005; D. Karaboga & B. Basturk, "A powerful and efficient algorithm for numerical function optimization: Artificial Bee Colony (ABC) algorithm," *J. Global Optim.*, vol. 39, no. 3, pp. 459–471, 2007.
> **Category**: 1.11 (Swarm Intelligence — foraging behaviour)

---

## 1. What problem with existing algorithms is ABC attempting to solve?

ABC targets **global continuous numerical optimization** with a deliberately **minimal control-parameter interface**. Karaboga's motivation was that GAs, PSO, and DE each required tuning several strongly interacting hyper-parameters, and he wanted a population-based method whose behaviour was governed by essentially one non-trivial parameter (the abandonment `limit`). The algorithm should (a) handle high-dimensional multimodal landscapes, (b) balance exploration and exploitation through a small number of clearly separated roles, and (c) be cheap to implement.

---

## 2. Why, or in what respect, have previous attempts failed?

- **Genetic Algorithms** require choosing an encoding (binary vs. real), selection scheme, crossover operator, crossover rate, mutation operator and mutation rate — six coupled decisions. Crossover on real-valued vectors does not naturally generate good intermediate points.
- **Particle Swarm Optimization** is prone to premature convergence on multimodal problems: the social pull toward `gbest` collapses swarm diversity once particles cluster. Inertia `w`, cognitive `c1`, and social `c2` all need tuning, and their interaction is landscape-dependent.
- **Differential Evolution** has three coupled parameters (`NP`, `F`, `CR`) with non-monotonic sweet spots — e.g. empirically `CR` works only in `[0, 0.3]` or `[0.8, 1]`, a discontinuous tuning landscape.
- None of these have an **explicit mechanism to abandon a stale solution**; stagnating individuals continue to consume evaluations.

ABC was designed to be competitive with all three while exposing only `SN` (colony size), `limit`, and `MCN` (max cycles).

---

## 3. What is the new idea presented in the paper?

ABC models honey-bee foraging with **three explicit agent roles** operating on a shared population of food sources (candidate solutions):

1. **Employed bees** — one per food source; each tries to improve its own source.
2. **Onlooker bees** — wait at the hive; probabilistically select an employed bee's food source based on the waggle-dance metaphor (fitness-proportional).
3. **Scout bees** — when a source has not improved for `limit` trials, its employed bee abandons it and becomes a scout, reinitialising the source randomly.

### Core equations

**Initialisation:**
```
x_ij = l_j + rand(0,1) · (u_j − l_j)
```

**Neighbour generation (employed + onlooker phases):**
```
v_ij = x_ij + φ_ij · (x_ij − x_kj),   φ_ij ~ U(−1, 1),   k ≠ i random
```
Only one dimension `j` is perturbed per bee per cycle. The step size `(x_ij − x_kj)` self-adapts to population spread — wide early, narrow once the swarm converges.

**Fitness transformation** (for minimization, `f_i ≥ 0`):
```
fit_i = 1 / (1 + f_i)
```

**Onlooker roulette-wheel probability:**
```
p_i = fit_i / Σ_m fit_m
```

**Scout reinitialisation** when `trial_i > limit`:
```
x_ij = l_j + rand(0,1) · (u_j − l_j)
```

Greedy selection is applied after each candidate: accept `v_ij` iff it has better fitness; else increment `trial_i`.

### Key innovations
1. **Explicit role separation** (exploitation vs. stochastic exploration vs. rescue).
2. **Adaptive step scale** — no inertia weight, no velocity.
3. **Abandonment by counter** — an elegant anti-stagnation mechanism; `limit` is the *only* non-trivial tuning knob (typical default `limit = SN · D / 2`).
4. **Only one dimension is perturbed per update** — useful for separable/partially-separable problems but a known weakness on fully non-separable ones.

---

## 4. How is the new approach demonstrated?

Karaboga & Basturk (2007) evaluate ABC on classical multimodal benchmarks at `D = 10` and `D = 30`:

| Benchmark | Type |
|:---|:---|
| Sphere | Unimodal separable |
| Rosenbrock | Unimodal non-separable |
| Rastrigin | Multimodal separable |
| Griewank | Multimodal, variable coupling |
| Ackley | Multimodal, global oscillation |
| Schwefel | Highly multimodal, deceptive |

Protocol: **30 independent runs**, `SN = 20–50` bees (half employed, half onlookers), `MCN` up to 2000 cycles. Baselines: GA, PSO, DE, and PS-EA (a PSO/EA hybrid). Both the mean best objective and its standard deviation are reported.

---

## 5. What are the results or outcomes and how are they validated?

### Key findings from Karaboga & Basturk (2007)

| Function (D=30) | Best baseline | ABC verdict |
|:---|:---|:---|
| Griewank | GA/PSO often stuck | ABC orders of magnitude better |
| Ackley | PSO premature | ABC superior, lower std dev |
| Rastrigin | GA poor | ABC and DE competitive; ABC slightly ahead |
| Schwefel | GA / PS-EA win at D=20,30 | ABC competitive but not best |
| Sphere / Rosenbrock | All converge | ABC comparable, sometimes slower than DE |

**Pattern**: ABC excels on **highly multimodal** landscapes (via scout-driven diversity); slightly slower than DE on smooth unimodal problems.

### Follow-up validation
- **GABC (Zhu & Kumar 2010)** — injects `gbest` into the employed-bee update, accelerating convergence but increasing the risk of premature convergence.
- **MeABC** — separate search equations for employed vs. onlooker bees.
- **Opposition-based ABC, chaotic ABC, LA-ABC** (neural-net-assisted) — all extend the basic algorithm; see Gao et al. (2013), Karaboga & Akay surveys.
- Comparative studies (Civicioglu & Besdok 2013) find DE tends to win on smooth continuous benchmarks while ABC wins on multimodal ones — consistent with the original paper.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. ABC matches or exceeds GA, PSO, and DE on multimodal continuous benchmarks.
2. Only three control parameters; minimal tuning burden.
3. The scout mechanism prevents permanent stagnation.

### Assessment
- **Largely justified** on the multimodal benchmarks chosen. The claim of universal superiority does *not* hold (no-free-lunch), but the simplicity-vs-performance trade-off is genuinely attractive.
- **Known weaknesses**:
  - Slow **late-stage exploitation** — the one-dimension-per-cycle perturbation under-uses each cycle near the optimum.
  - Update rule is **not rotation-invariant** (single-dimension perturbation) — performance drops on non-separable rotated problems.
  - Greedy selection under **noisy fitness** is fragile: a lucky noisy improvement is accepted.
  - `limit` is not actually "tuning-free" — the default `SN · D / 2` is a heuristic that often needs adjustment for hard landscapes.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - Minimal tuning → easy to drop in alongside PSO for ablation comparison.
  - Scout mechanism is useful when the backtest fitness landscape has flat regions (common with binary trade-signal rules).
  - The adaptive step `(x_ij − x_kj)` self-calibrates to parameter ranges — convenient when some parameters span 2–200 (e.g. MA window) and others are `[0,1]` (e.g. stop-loss pct).
- **Weaknesses for this use case**:
  - **Backtest fitness is noisy** (slippage, train/val split variance); vanilla ABC's greedy selection will chase noise. Use **fitness averaging over N replications** or switch to **GABC / MeABC** variants with explicit noise-handling.
  - **One-dimension-per-cycle updates** waste evaluations in high dimensions (21 parameters); a `gbest`-guided variant (GABC) is preferable.
  - Published crypto-trading applications of ABC exist but are fewer than for PSO/GA.
- **Replication confidence: High** — the 2007 paper and Karaboga's technical reports include complete pseudocode and default parameters; reference implementations exist in Python, MATLAB, and Java.

**Verdict**: Strong candidate as a *baseline* in the comparative analysis, but GABC is a better choice than vanilla ABC for actual trading-bot parameter tuning.

---

## Key Citations for Final Report (IEEE style)

1. D. Karaboga, "An Idea Based on Honey Bee Swarm for Numerical Optimization," Erciyes Univ., Kayseri, Turkey, Tech. Rep. TR06, 2005.
2. D. Karaboga and B. Basturk, "A powerful and efficient algorithm for numerical function optimization: Artificial Bee Colony (ABC) algorithm," *Journal of Global Optimization*, vol. 39, no. 3, pp. 459–471, Nov. 2007.
3. D. Karaboga and B. Akay, "A comparative study of Artificial Bee Colony algorithm," *Applied Mathematics and Computation*, vol. 214, no. 1, pp. 108–132, Aug. 2009.
4. G. Zhu and S. Kumar, "Gbest-guided artificial bee colony algorithm for numerical function optimization," *Applied Mathematics and Computation*, vol. 217, no. 7, pp. 3166–3173, Dec. 2010.
5. W. Gao, S. Liu, and L. Huang, "A novel artificial bee colony algorithm based on modified search equation and orthogonal learning," *IEEE Transactions on Cybernetics*, vol. 43, no. 3, pp. 1011–1024, Jun. 2013.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (3 bee roles + update equation) documented
- [x] Benchmark results summarized
- [x] 6 reviewer questions answered
- [x] Variants (GABC, MeABC) noted for Part 2 relevance
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
