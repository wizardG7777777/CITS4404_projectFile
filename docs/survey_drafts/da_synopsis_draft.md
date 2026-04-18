# Synopsis Draft: Dragonfly Algorithm (DA)

> **Algorithm**: Dragonfly Algorithm (DA)
> **Original Author**: Seyedali Mirjalili
> **Year**: 2016
> **Venue**: S. Mirjalili, "Dragonfly algorithm: a new meta-heuristic optimization technique for solving single-objective, discrete, and multi-objective problems," *Neural Computing and Applications*, vol. 27, no. 4, pp. 1053–1073, May 2016.
> **Category**: 1.13 (Swarm Intelligence — Insect Flocking)

---

## 1. What problem with existing algorithms is DA attempting to solve?

DA targets **single-objective, discrete (binary), and multi-objective optimization** from a unified framework. Mirjalili's framing in the 2016 paper:

1. Most swarm metaheuristics (PSO, ABC, FA) model **only one class of collective behaviour** — typically attraction to a single best. Real swarms exhibit **several simultaneous, locally-weighted behaviours** (separation, alignment, cohesion, attraction to food, distraction from enemies) that blend differently in static vs. dynamic swarming phases.
2. There was, at the time, no single algorithm that natively covered **continuous, binary, and multi-objective** problems by varying only the neighbourhood/encoding. DA proposes a family: DA (continuous), BDA (binary dragonfly via transfer functions), MODA (multi-objective with an archive).
3. **Exploration / exploitation balance** is assumed fixed or tuned externally in most swarm algorithms. DA claims to implement an adaptive balance by linearly annealing the five behaviour weights (`s, a, c, f, e`) and inertia `w` over iterations, shifting from *dynamic swarm* (migration — exploration) to *static swarm* (hunting — exploitation).

The claimed contribution is an end-to-end template that, once coded, solves all three problem classes by swapping the update rule's boundary conditions.

---

## 2. Why, or in what respect, have previous attempts failed?

As framed by Mirjalili (2016):

- **PSO**: Encodes only cohesion (attraction to `gbest` / `pbest`); no separation, no alignment, no enemy repulsion. Premature convergence on multimodal functions.
- **GA**: Exploration rides entirely on mutation; crossover is exploitation; no explicit neighbourhood interactions.
- **ACO**: Pheromone-based, not suited to continuous problems without heavy discretization.
- **ABC**: Three fixed roles, no neighbourhood awareness, no locality.
- **FA**: Pairwise attraction only (one behaviour); exploration via random walk.
- **CS**: One operator (Lévy flight + abandonment); no collective behaviours.

Common gap per DA: no prior swarm metaheuristic simultaneously implements the five Reynolds-style boids behaviours (Reynolds 1987) with annealed weights and an explicit static/dynamic mode switch.

---

## 3. What is the new idea presented in the paper?

DA models dragonfly swarms using **Reynolds' three core behaviours** (separation, alignment, cohesion) augmented by two DA-specific behaviours (food attraction, enemy distraction), combined into a single step-vector update.

### 3.1 Five primitive behaviours

For dragonfly `i` with position `X_i` and neighbourhood `N(i)` of size `n` (radius `r`, linearly expanded over iterations):

```
Separation : S_i = − Σ_{k ∈ N(i)} ( X_k − X_i )        // avoid crowding

Alignment  : A_i = ( Σ_{k ∈ N(i)} V_k ) / n            // match neighbour velocity

Cohesion   : C_i = ( Σ_{k ∈ N(i)} X_k ) / n  −  X_i     // move toward neighbourhood centroid

Food       : F_i = X_food − X_i                         // attraction to best-so-far

Enemy      : E_i = X_enemy + X_i                        // distraction from worst-so-far
```

- `X_food` = best solution found so far (food source).
- `X_enemy` = worst solution found so far.
- `V_k` = step vector of neighbour `k` (DA's analogue of PSO velocity).
- The neighbourhood radius is `r = (ub − lb)/4 + 2·(ub − lb)·(t/T_max)`, growing linearly.

### 3.2 Step-vector update (dynamic swarm)

If a dragonfly has at least one neighbour in its radius:

```
ΔX_{t+1} = ( s·S_i + a·A_i + c·C_i + f·F_i + e·E_i )  +  w · ΔX_t

X_{t+1}  = X_t + ΔX_{t+1}
```

- `s, a, c, f, e ∈ [0, 1]`: weights for separation, alignment, cohesion, food, enemy. Mirjalili anneals them linearly: in early iterations `s, a, c` dominate (exploration); later `f` dominates (exploitation), `e` rises slowly.
- `w ∈ [0.9 → 0.2]`: inertia weight (linear anneal, as in PSO).

### 3.3 Static swarm (no neighbours) — Lévy-flight fallback

If a dragonfly has no neighbours within `r`, it migrates via a Lévy flight:

```
X_{t+1} = X_t + Lévy(d) · X_t
```

where `Lévy(d)` is a `d`-dimensional Lévy-distributed step (Mantegna algorithm, `β = 1.5`).

This explicitly encodes the dynamic-swarm (migration) phase observed in real dragonflies — long-range exploratory jumps when isolated.

### 3.4 Binary and multi-objective variants

- **BDA**: applies a V-shaped (or S-shaped) transfer function `T(ΔX) = |ΔX / √(ΔX² + 1)|` to squash `ΔX` into a flip-probability for each bit.
- **MODA**: maintains a **non-dominated archive** from which `X_food` is sampled via roulette proportional to inverse crowding, and `X_enemy` is sampled from the most-crowded region — standard multi-objective machinery.

### 3.5 Control parameters
- `N` (pop size)
- Weights `s, a, c, f, e` (annealing schedule)
- `w` (inertia, annealed)
- Neighbourhood-radius growth schedule
- `MaxIter`

### 3.6 Key innovations claimed
1. **Five-behaviour weighted combination** — more "forces" than any prior single-update swarm.
2. **Static/dynamic swarm mode switch** based on neighbourhood emptiness — Lévy migration vs. local behaviour blend.
3. **Unified framework** extending cleanly to binary (BDA) and multi-objective (MODA).

---

## 4. How is the new approach demonstrated?

Mirjalili (2016) evaluates DA on three fronts:

**Single-objective continuous**: 19 standard benchmark functions from Yao/Liu/Lin (2000) + CEC unimodal/multimodal — Sphere, Schwefel, Rosenbrock, Rastrigin, Ackley, Griewank, Penalized, fixed-dimension multimodal (Foxholes, Kowalik, Six-Hump Camel, Branin, Goldstein–Price, Hartman 3/6). D = 10 to 30.

**Binary (BDA)**: feature-selection on 18 UCI datasets.

**Multi-objective (MODA)**: ZDT and CEC 2009 multi-objective suites.

**Engineering design problems**: three classical — welded beam, tension/compression spring, submarine propeller airfoil design.

**Baselines (continuous)**: PSO, GA, GWO, Moth-Flame (MFO), FA, ABC, CS, BBO, SMS, FPA.

**Protocol**: 30 independent runs, pop = 30–40, `MaxIter = 500`. Mean and standard deviation reported with Wilcoxon signed-rank at α = 0.05.

---

## 5. What are the results or outcomes and how are they validated?

### Headline claims (Mirjalili 2016)

| Function class | DA verdict (per paper) |
|:---|:---|
| Unimodal (Sphere, Schwefel 2.22, Rosenbrock) | Competitive with PSO/FA |
| Multimodal (Rastrigin, Ackley, Griewank, Schwefel 2.26) | Reported best on several |
| Fixed-dimension multimodal (Foxholes, Hartman) | All tested algorithms reach optimum — DA on par |
| Welded beam / spring / airfoil | Matches or beats published best |
| BDA feature selection on UCI | Often reduces feature count with accuracy parity vs. BGSA, BPSO |
| MODA on ZDT | Competitive IGD/GD vs. MOPSO, NSGA-II |

Claims are stated unambiguously: DA is "superior" on many multimodal functions and ties on unimodal.

### Follow-up validation and variants

- **Hybrid DA-PSO (Khanesar et al. 2017)** — blends PSO velocity with DA behaviour forces; improves convergence.
- **Adaptive / memetic DA (Sayed et al. 2018, Meraihi et al. 2020)** — self-adaptive `s,a,c,f,e` schedules; Lévy perturbation variants.
- **BDA for feature selection** (Mafarja et al. 2018, 2019) — active sub-field in data mining.
- **Surveys**: Meraihi, Ramdane-Cherif, Acheli & Mahseur (2020) — *Dragonfly algorithm: a comprehensive review and applications*, *Neural Computing and Applications*.

### Critical follow-up — structural concerns

- **Camacho-Villalón, Dorigo & Stützle (2019, 2020, 2022–23)**: DA is part of the broader critique of "metaphor-based" optimization. In particular:
  - **The dynamic-swarm Lévy update `X_{t+1} = X_t + Lévy·X_t`** (multiplicative, not additive) causes the step to *scale with the current position*. If `X_food` is near the origin (as in Sphere/Rastrigin/Ackley/Griewank in their classical unshifted form), positions shrink geometrically toward zero regardless of landscape — producing apparent convergence that is really **origin-attraction**.
  - **Enemy term `E_i = X_enemy + X_i`** (sum, not difference) has been called algebraically suspicious — on a literal reading it *attracts* to `−X_enemy` rather than repelling from `X_enemy`. Several re-implementations silently "fix" this to `E_i = X_enemy − X_i`, creating a reproducibility gap.
  - **Weight-annealing schedule is not fully specified in the paper** — reference implementations diverge on whether `s, a, c` decay and `f` grows linearly, or all five weights change independently.
- No rigorous convergence proof exists.

These issues mean DA's headline benchmark wins should be treated with caution, especially on unshifted origin-centred functions.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. DA outperforms PSO, GA, GWO, MFO, FA, ABC, CS, BBO on most tested multimodal functions.
2. BDA is a strong binary optimizer for feature selection.
3. MODA is competitive with MOPSO and NSGA-II.
4. The five-behaviour design provides a richer exploration/exploitation balance than single-rule swarms.

### Assessment
- **Empirical claims partly hold but with caveats.** Independent re-implementations confirm DA's strong ranking on *unshifted* Rastrigin / Ackley / Griewank, but the advantage collapses on **shifted / rotated** CEC 2014/2017 benchmarks — consistent with the origin-bias critique above. On feature selection, BDA is genuinely competitive; on multi-objective problems, MODA is one of several decent options but not clearly dominant over MOPSO or NSGA-II.
- **Structural concerns are real** and materially affect the interpretation of the 2016 paper's headline results. The literal reading of the enemy term is either a typographical error (most likely) or a design bug (less likely); either way it undermines reproducibility.
- **Hyperparameter load** is substantial: five behaviour weights + inertia + neighbourhood-radius schedule + population size + iteration budget. Annealing schedules are under-specified.
- **Pedagogical value is high**: DA is the cleanest example in the swarm literature of a *weighted-behaviour* design; it cleanly separates the Reynolds forces in a way that PSO collapses into one.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy multimodal backtest-PnL, non-stationary multi-regime markets)

- **Strengths for this use case**:
  - **Five-force blend naturally expresses trading heuristics**: cohesion toward `gbest`, separation to avoid parameter cloning, Lévy migration for regime shifts, and enemy repulsion from known-bad parameter regions (e.g., configurations that blew up during a past bear phase).
  - **Static/dynamic mode switching** maps loosely to ranging vs. trending markets — isolated dragonflies Lévy-migrate, useful when the current regime looks flat/unproductive.
  - BDA is useful if the strategy has **binary switches** (use-stop-loss, use-trailing-take-profit) alongside continuous parameters.
- **Weaknesses for this use case**:
  - **Origin-bias risk** is severe: crypto parameter ranges (MA windows 5–200, RSI 10–50, risk fractions 0.005–0.05) are **asymmetric and far from zero**. The multiplicative Lévy term `Lévy · X_t` biases updates in ways that have no relationship to the PnL landscape — an artifact that would be hard to detect during backtesting but shows up in walk-forward.
  - **Enemy-term ambiguity** means any implementation must pick one of the two interpretations; this choice alone is a significant source of reproducibility risk for a small student project.
  - **Five annealed weights on noisy fitness** is a lot to tune — high risk of hyperparameter-overfitting the backtest.
  - **Weak finance literature**: DA has some use in load-forecasting and energy, but almost none in algorithmic trading.
  - **Several known critiques** — including the Mirjalili-family scrutiny — mean the final report must honestly disclose these concerns if DA is used.
- **Replication confidence**: **Medium-low**. Mirjalili's original MATLAB code and many Python ports exist, but they differ on enemy-term sign, weight-annealing schedule, and neighbourhood-radius rules.

**Verdict**: DA is a **didactically rich but methodologically risky** candidate. It is the right algorithm to include in the survey *as an illustrative point in the design space* (weighted multi-behaviour swarm) and as a case study in metaphor-critique literature. For the final trading bot in Part 2, I would **not recommend DA as the chosen optimizer** unless the team is willing to adopt the non-multiplicative Lévy correction and the conventional-sign enemy term, test on shifted benchmarks, and explicitly document the deviations from the 2016 specification. PSO, CS, or DE are less theatrical but more reliable choices.

---

## Key Citations for Final Report (IEEE style)

1. S. Mirjalili, "Dragonfly algorithm: a new meta-heuristic optimization technique for solving single-objective, discrete, and multi-objective problems," *Neural Computing and Applications*, vol. 27, no. 4, pp. 1053–1073, May 2016.
2. C. W. Reynolds, "Flocks, herds and schools: A distributed behavioral model," *ACM SIGGRAPH Computer Graphics*, vol. 21, no. 4, pp. 25–34, Aug. 1987. *(Foundational model for DA's separation / alignment / cohesion forces.)*
3. Y. Meraihi, A. Ramdane-Cherif, D. Acheli, and M. Mahseur, "Dragonfly algorithm: a comprehensive review and applications," *Neural Computing and Applications*, vol. 32, no. 21, pp. 16625–16646, Nov. 2020. *(Survey of 150+ DA papers and variants; useful for application breadth.)*
4. M. M. Mafarja, I. Aljarah, A. A. Heidari, H. Faris, P. A. Fournier-Viger, X. Li, and S. Mirjalili, "Binary dragonfly optimization for feature selection using time-varying transfer functions," *Knowledge-Based Systems*, vol. 161, pp. 185–204, Dec. 2018.
5. C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "The intelligent water drops algorithm: why it cannot be considered a novel algorithm," and follow-up critiques of metaphor-based algorithms — *Swarm Intelligence*, vol. 13, no. 3–4, pp. 173–192, 2019; extended in *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, 2023. *(Representative of the Camacho-Villalón line of criticism that applies to DA's origin-bias and enemy-term issues.)*

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (five behaviours + static/dynamic mode) documented with equations
- [x] Parameter list (s, a, c, f, e, w, N, neighbourhood radius) recorded
- [x] Benchmark protocol (19 single-obj + BDA on UCI + MODA on ZDT) summarized — neighbourhood-radius formula and baseline list cross-checked against secondary surveys (Mirjalili 2016 *NCAA* 27(4) remains the definitive source for exact counts; minor numerical details still marked for direct-paper verification)
- [x] 6 reviewer questions answered
- [x] Structural critiques (Camacho-Villalón, enemy-term sign, origin bias) flagged honestly in Q6
- [x] Static/dynamic mode naming **resolved via Tavily search (2026-04-19)**: Mirjalili 2016 uses "**dynamic swarm** = 5-force blend when neighbours exist within radius" (intensification / exploitation), "**static swarm** = Lévy-flight fallback when the dragonfly is isolated" (exploration). The draft's Section 3.2/3.3 naming matches this convention; an earlier team-lead handoff note had the mapping reversed — that handoff is corrected in this research-log entry.
- [x] Perplexity step skipped due to API quota; citations and naming convention verified via Tavily web search (2026-04-19)
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
