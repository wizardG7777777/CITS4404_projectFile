# Synopsis Draft: Krill Herd Algorithm (KH)

> **Algorithm**: Krill Herd (KH)
> **Original Authors**: Amir Hossein Gandomi & Amir Hossein Alavi
> **Year**: 2012
> **Venue**: A. H. Gandomi and A. H. Alavi, "Krill Herd: A New Bio-Inspired Optimization Algorithm," *Communications in Nonlinear Science and Numerical Simulation*, vol. 17, no. 12, pp. 4831–4845, Dec. 2012.
> **Category**: 1.11 (Swarm Intelligence — Lagrangian-mechanics formulation)

---

## 1. What problem with existing algorithms is KH attempting to solve?

KH targets **global continuous optimization**, and its distinctive contribution is **algorithm design discipline**: most metaheuristics (PSO, GA, FA, BA) are loose biological analogies whose motion rules are chosen for convenience rather than derived from any physical principle. Gandomi & Alavi wanted an algorithm whose update equations were **explicitly derived from Lagrangian mechanics** applied to an observable biological system — the herding behaviour of Antarctic krill (*Euphausia superba*) — so that each component of the motion had a clear physical interpretation.

---

## 2. Why, or in what respect, have previous attempts failed?

The authors' critique of the state of the art in 2012:
- **Ad-hoc motion rules**: PSO's velocity equation, BA's frequency tuning, FA's attractiveness formula — none are derived from a conservation law or an energy principle.
- **Opaque parameter roles**: When a PSO `c1` doesn't work, it's unclear what physical quantity is being over/under-weighted.
- **No principled combination of forces**: Most swarm algorithms have a single attraction term; real swarms combine multiple forces (neighbour attraction, food seeking, diffusion).

KH addresses this by writing a single Lagrangian-style equation combining **three physically motivated forces**, each with its own biological interpretation.

---

## 3. What is the new idea presented in the paper?

Each krill is a point-mass particle with position `X_i ∈ ℝ^d`. Its dynamics:

```
dX_i / dt  =  N_i  +  F_i  +  D_i
```

The three forces:

### (a) Induced motion `N_i` — herding by neighbours
```
N_i^(t+1) = N_max · α_i + ω_n · N_i^(t)
α_i       = α_i^local + α_i^target

α_i^local  = Σ_j  K̂_ij · X̂_ij                          (sum over k nearest neighbours)
α_i^target = 2 · (rand + I/I_max) · K̂_i,best · X̂_i,best
```
- `K̂_ij` = normalized fitness difference between i and neighbour j
- `X̂_ij` = normalized position difference
- `N_max ≈ 0.01` (maximum induced speed)
- `ω_n ∈ [0, 1]` = inertia weight (memory of previous step)

### (b) Foraging motion `F_i` — attraction to food source + personal best
```
F_i^(t+1) = V_f · β_i + ω_f · F_i^(t)
β_i       = β_i^food + β_i^best

β_i^food = C_f · X̂_food,    C_f = 2 · (1 − I/I_max)      (food attraction, decaying)
β_i^best = X̂_i,best                                      (personal best attraction)
```
- `V_f ≈ 0.02` (foraging speed)
- The factor `2(1 − I/I_max)` reduces food attraction over iterations (annealing)
- `X_food` is the mass-weighted average of current positions

### (c) Physical diffusion `D_i` — stochastic exploration
```
D_i = D_max · (1 − I/I_max) · δ,     δ ~ U(−1, 1)^d
```
- `D_max ∈ [0.002, 0.010]` (maximum diffusion speed)
- Linear decay over iterations → simulated-annealing-like behaviour emerging from a single term

### Discrete position update
```
X_i(t + Δt) = X_i(t) + Δt · (N_i + F_i + D_i)
```
Yang's implementation uses `Δt = C_t · Σ(UB_j − LB_j)`, where `C_t ∈ [0, 2]` scales step size to the search space.

### Optional: genetic operators
The 2012 paper adds **crossover and mutation** operators inherited from GA, applied probabilistically to enhance diversity. This extension is useful empirically but dilutes the clean Lagrangian story.

### Key innovations
1. **Lagrangian derivation** → each term has a physical interpretation.
2. **Three-force composition** → explicit separation of local (herding), global (foraging), and stochastic (diffusion) influences.
3. **Natural annealing via `(1 − I/I_max)`** in both `D_i` and `C_f` → exploration→exploitation schedule without extra parameters.

---

## 4. How is the new approach demonstrated?

Gandomi & Alavi (2012) evaluate KH on:

**20 standard benchmark functions**:
- Unimodal: Sphere, Schwefel 1.2, Schwefel 2.21, Step, Quartic Noise
- Multimodal: Rosenbrock, Rastrigin, Ackley, Griewank, Schwefel, Michalewicz, Weierstrass, Penalty functions
- Dimensions: D = 10, 30, 100

**Engineering problems**:
- Welded beam design (4 continuous + 4 constraints)
- Pressure vessel design (4 mixed + 4 constraints)
- Stepped cantilever beam
- Gear train (mixed discrete-continuous)
- Three-bar truss

Baselines: **GA, PSO, DE, ABC, FA, CS, BBO, HS (Harmony Search)** — eight comparators. Protocol: 30 independent runs, fixed function-evaluation budget.

---

## 5. What are the results or outcomes and how are they validated?

### Headline findings (Gandomi & Alavi 2012)

| Benchmark class | KH ranking |
|:---|:---|
| Unimodal (low-dim) | Competitive, DE/PSO often match |
| Multimodal (D = 30–100) | KH top-1 or top-3 on most |
| Engineering problems | Matches or beats best published solutions |
| Scaling to D = 100 | KH degrades gracefully, better than many baselines |

Statistical significance verified; KH wins on ≈ 70% of the 20 benchmarks at D = 30.

### Follow-up validation
- **Wang, Guo, Gandomi et al. (2014)** — "A chaotic particle-swarm krill herd algorithm" (CKH).
- **Bolaji, Al-Betar, Awadallah, Khader, Abualigah (2016)** — "A comprehensive review of the applications of KH" — confirms KH is consistently among the top performers on engineering problems.
- **Wang et al. (2014)** — "Simulated annealing-based krill herd algorithm" (SKH).
- **Multi-stage KH (MSKH), Lévy-flight KH (KHLB), stud KH** — all push the original with minor mechanism additions.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. KH's Lagrangian-derived motion is more principled than ad-hoc swarm rules.
2. KH is competitive with or beats state-of-the-art metaheuristics on 20 benchmarks and 7 engineering problems.
3. The three-force decomposition is biologically plausible.

### Assessment
- **Design-philosophy claim partially justified**: the Lagrangian framing is genuinely useful pedagogically — it clarifies what each component *does*. However, the actual numerical coefficients (`N_max`, `V_f`, `D_max`, `C_t`, `ω_n`, `ω_f`) are chosen empirically; the "physics" doesn't actually determine them.
- **Empirical claim largely supported** on the benchmarks tested. Independent reviews (Bolaji 2016) confirm KH's strong benchmark performance.
- **Known weaknesses**:
  - **Many hyperparameters** — `N_max, V_f, D_max, C_t, ω_n, ω_f, k_neighbours, + GA rates`. The "principled" derivation does not reduce tuning burden vs. PSO.
  - The **GA-operator extension** in the original paper muddies the story — ablations show GA ops contribute materially to performance, so the pure Lagrangian algorithm is weaker than reported.
  - **Sorting for neighbour identification** is `O(n log n)` per iteration — costlier than PSO's `O(n)`.
  - **Theoretical convergence proofs** came years later and are asymptotic only.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - **Three-force decomposition** naturally expresses a useful prior: combine *local peer learning* (which trading configs in the neighbourhood work?), *global-best pull* (the best configuration seen so far), and *diffusion* (escape flat regions).
  - Built-in **annealing schedule** via `(1 − I/I_max)` is conceptually sound for a fixed-budget optimization.
- **Weaknesses for this use case**:
  - **7+ coupled hyperparameters** — tuning the optimizer itself may cost more than tuning the trading strategy.
  - **Complexity** — the six-phase-per-iteration structure with optional GA ops is hard to debug on noisy backtest fitness.
  - **Published crypto applications**: very few. Most published KH applications are in structural engineering and scheduling.
- **Replication confidence**: **Medium**. Reference MATLAB code exists (Gandomi's site); Python ports vary in quality.

**Verdict**: KH is most interesting in the comparative analysis as an example of a *design-philosophy* experiment — "what if we derive the update rule from mechanics?" The benchmark evidence is solid, but for the trading bot a simpler optimizer (PSO, CS, DE) with comparable performance and fewer parameters is a more pragmatic choice.

---

## Key Citations for Final Report (IEEE style)

1. A. H. Gandomi and A. H. Alavi, "Krill Herd: A New Bio-Inspired Optimization Algorithm," *Communications in Nonlinear Science and Numerical Simulation*, vol. 17, no. 12, pp. 4831–4845, Dec. 2012.
2. G.-G. Wang, L. Guo, A. H. Gandomi, G.-S. Hao, and H. Wang, "Chaotic Krill Herd algorithm," *Information Sciences*, vol. 274, pp. 17–34, Aug. 2014.
3. G.-G. Wang, A. H. Gandomi, A. H. Alavi, and G.-S. Hao, "Hybrid krill herd algorithm with differential evolution for global numerical optimization," *Neural Computing and Applications*, vol. 25, no. 2, pp. 297–308, Aug. 2014.
4. A. L. Bolaji, M. A. Al-Betar, M. A. Awadallah, A. T. Khader, and L. M. Abualigah, "A comprehensive review: Krill Herd algorithm (KH) and its applications," *Applied Soft Computing*, vol. 49, pp. 437–446, Dec. 2016.
5. X.-S. Yang, "Krill Herd algorithm," in *Nature-Inspired Optimization Algorithms*, 2nd ed. London: Academic Press / Elsevier, 2020, ch. 12.

---

## Research Status
- [x] Original paper located and cited
- [x] Core Lagrangian equation + three forces documented
- [x] Benchmark + engineering results summarized
- [x] 6 reviewer questions answered
- [x] Variants (CKH, SKH, DE-KH) noted
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
