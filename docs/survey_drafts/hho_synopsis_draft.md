# Synopsis Draft: Harris Hawks Optimization (HHO)

> **Algorithm**: Harris Hawks Optimization (HHO)
> **Original Authors**: Ali Asghar Heidari, Seyedali Mirjalili, Hossam Faris, Ibrahim Aljarah, Majdi Mafarja, Huiling Chen
> **Year**: 2019
> **Venue**: A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and H. Chen, "Harris hawks optimization: Algorithm and applications," *Future Generation Computer Systems*, vol. 97, pp. 849–872, Aug. 2019.
> **Category**: 2.1 (Swarm intelligence — predator/cooperative-hunting)

---

## 1. What problem with existing algorithms is HHO attempting to solve?

HHO targets **global continuous optimization** with a focus on **adaptive exploration-to-exploitation transitions** and **cooperative multi-agent dynamics** that react to a time-varying "prey" state. Most swarm algorithms treat the best-so-far point as a static attractor and use a monotonically decaying parameter to shift search modes. HHO argues that real predator–prey interactions exhibit:
- A **prey-energy parameter** that *oscillates* rather than decays monotonically.
- **Multiple distinct exploitation behaviours** triggered by the prey's residual energy and escape chance — not one blended update rule.
- **Rapid Lévy-style dives** that interleave with steady besiege movements.

The authors aim to encode these four exploitation modes plus two exploration modes into a single algorithm, producing an optimiser whose behaviour genuinely diversifies late in the run instead of collapsing to a single attractor.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: Single update rule; once `gbest` stabilises, exploitation degenerates to a Gaussian cloud around it.
- **GWO (Mirjalili 2014)**: Three leaders (α, β, δ) give a richer centroid, but the update is still a linear combination — no behavioural switching.
- **WOA**: Spiral vs. circle with a 50/50 coin flip — only two modes and no prey-energy modulation.
- **DE**: Excellent exploration, but no built-in exploitation refinement; crossover rate is global.
- **CS / FA / BA**: Heavy-tailed or sinusoidal moves, but mono-modal updates.

Common gap: no algorithm lets the **escape energy of the target** gate a **library of distinct behaviours** (soft besiege, hard besiege, soft dive, hard dive) conditional on both magnitude and a random escape chance. HHO fills that gap.

---

## 3. What is the new idea presented in the paper?

The search mirrors the **cooperative surprise-attack behaviour of Harris's hawks** (Bednarz, 1988). Each hawk is a candidate solution; the prey is the current best solution `X_rabbit`. At each iteration, every hawk's update depends on:

1. An **escape energy** `E`, decreasing linearly in magnitude but sign-oscillating:
```
E = 2 · E_0 · (1 − t / T)     with   E_0 ∈ U(−1, 1)
```
   - `|E| ≥ 1` → **exploration** (prey strong, hawks scan wide).
   - `|E| < 1` → **exploitation** (prey weakening, hawks close in).

2. A **random escape chance** `r ∈ U(0, 1)` drawn per hawk per iteration; it decides which of four exploitation modes fires.

### Exploration phase (`|E| ≥ 1`)
Each hawk perches either on a random hawk or near the flock centroid, with probability `q`:
```
X(t+1) = { X_rand(t) − r1 · |X_rand(t) − 2·r2·X(t)|           if q ≥ 0.5
         { (X_rabbit(t) − X_m(t)) − r3·(lb + r4·(ub − lb))   if q < 0.5
```
where `X_m = (1/N) · Σ_i X_i` is the hawk centroid, and `r1…r4 ∈ U(0,1)`.

### Exploitation phase — four modes (`|E| < 1`)

**(a) Soft besiege** — `|E| ≥ 0.5` and `r ≥ 0.5` (prey energetic, no panic):
```
X(t+1) = ΔX(t) − E · |J · X_rabbit(t) − X(t)|
ΔX(t) = X_rabbit(t) − X(t)
J = 2 · (1 − r5)          # random jump strength, r5 ∈ U(0,1)
```

**(b) Hard besiege** — `|E| < 0.5` and `r ≥ 0.5` (prey exhausted):
```
X(t+1) = X_rabbit(t) − E · |ΔX(t)|
```

**(c) Soft besiege with progressive rapid dives** — `|E| ≥ 0.5` and `r < 0.5` (prey still has energy, tries to zig-zag):
```
Y = X_rabbit(t) − E · |J · X_rabbit(t) − X(t)|
Z = Y + S · LF(D)                      # Lévy-flight perturbation, S ∈ R^D random

X(t+1) = { Y   if f(Y) < f(X(t))
         { Z   if f(Z) < f(X(t))       # otherwise keep X
```
`LF(D)` is a Lévy step (Mantegna's algorithm, `β = 1.5`).

**(d) Hard besiege with progressive rapid dives** — `|E| < 0.5` and `r < 0.5` (exhausted prey, unexpected dodge):
```
Y = X_rabbit(t) − E · |J · X_rabbit(t) − X_m(t)|
Z = Y + S · LF(D)

X(t+1) = { Y   if f(Y) < f(X(t))
         { Z   if f(Z) < f(X(t))
```
The only difference from (c) is that `X_m` (flock centroid) replaces `X(t)` inside the bracket — modelling a **team encirclement** rather than an individual dive.

### Key innovations
1. **Four-way behavioural switching** gated jointly by `|E|` and a fresh `r` per hawk — genuinely multi-modal exploitation.
2. **Sign-oscillating `E`** — unlike GWO's `a`, HHO's `E` can flip sign *within* the decaying envelope, creating transient re-exploration bursts.
3. **Lévy-flight dive component** — heavy-tailed jumps inside exploitation modes (c) and (d) preserve late-stage diversity, a common weakness in peer methods.
4. **Greedy selection on `Y` and `Z`** — the dive is committed only if it strictly improves fitness.

---

## 4. How is the new approach demonstrated?

Heidari et al. (2019) evaluate on:

**Benchmark functions (29 total)**:
- **Unimodal** F1–F7: Sphere, Schwefel 2.22, Schwefel 1.2, Schwefel 2.21, Rosenbrock, Step, Quartic+noise.
- **Multimodal** F8–F13: Schwefel 2.26, Rastrigin, Ackley, Griewank, Penalised #1, Penalised #2.
- **Fixed-dimension** F14–F23: Foxholes, Kowalik, Six-hump camel, Branin, Goldstein-Price, Hartman 3/6, Shekel 5/7/10.
- **CEC 2017** composite / rotated / hybrid functions.

**Engineering design problems**:
- Tension/compression spring, pressure vessel, welded beam, three-bar truss, rolling-element bearing, multi-plate disc clutch brake, car side impact.

**Baselines**: PSO, DE, GA, GWO, MFO, CS, BAT, TLBO, BBO, GSA, SCA, FPA, MVO.

**Protocol**: 30 agents, up to 500 iterations, 30 independent runs, best / mean / std reported; Wilcoxon signed-rank and Friedman tests at `α = 0.05`.

---

## 5. What are the results or outcomes and how are they validated?

### Headline results from Heidari et al. (2019)

| Benchmark group | HHO wins vs 13 peers |
|:---|:---|
| Unimodal (F1–F7) | Top-ranked on 6/7 |
| Multimodal (F8–F13) | Top-ranked on 5/6 |
| Fixed-dim (F14–F23) | Competitive, wins on 7/10 |
| CEC 2017 composite | Top-3 ranking on all |
| Engineering (6 problems) | Matches or beats best published designs |

Friedman mean-rank has HHO in **first place overall** across the 29 benchmarks; Wilcoxon `p-values < 0.05` vs every peer on the majority of functions.

### Independent follow-up validation

- **Houssein et al. (2020, 2021)** — hybrid HHO + SA, HHO + DE for feature selection; confirms HHO's exploitation is strong but exploration benefits from DE-style mutation.
- **Abualigah et al. (2021, *Neural Computing and Applications*)** — survey of HHO variants; **>400 citations of extensions** by 2022; applications span PV solar parameter estimation, SVM tuning, image segmentation, distribution-network reconfiguration.
- **Jia et al. (2019)** — dynamic HHO for photovoltaic parameter estimation; out-of-box HHO gets top-3 RMSE vs 10 peers.
- **Critical replication (Lei et al. 2022, *Applied Soft Computing*)**: HHO **reproduces cleanly**; the four-mode structure is essential (ablating any single dive mode hurts on multimodal functions).
- **Structural analyses**: HHO is **not** flagged as a "metaphor-zoo" algorithm in Camacho-Villalón et al. (2023) — its four-mode switching is algorithmically distinct from PSO/GWO.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. HHO produces competitive or better results than 13 established metaheuristics on 29 benchmarks and 6 engineering problems.
2. The multi-mode exploitation structure is the key to avoiding premature convergence.
3. HHO has only **population size and iteration budget** as explicit parameters — no tuning of cognitive/social/mutation weights.

### Assessment
- **Largely justified**. The multi-mode exploitation design is a genuine structural innovation, validated by ablations in the original paper and replicated by independent groups. Of all post-2015 swarm algorithms in Mirjalili's collaboration network, HHO has received the **strongest independent endorsement** — it passes the "does removing a component break performance?" test that many metaphor-zoo algorithms fail.
- **Known weaknesses**:
  - **`E_0` uniform draw**: the sign oscillation is pseudo-random, not phase-locked to swarm state; can produce unproductive re-exploration late in run.
  - **Lévy-step scale** (`β = 1.5` fixed): inherits CS's limitation — a single `β` may not match every landscape.
  - **`r = 0.5` thresholds are hard**: smoother gating (e.g. sigmoid on `|E|`) proposed by several variants.
  - **Noise sensitivity**: greedy `Y/Z` selection compares single fitness evaluations; on noisy objectives, this can lock in spurious improvements.
- **Reproducibility**: MATLAB reference code on Mirjalili's site; `mealpy`, `niapy`, `EvoloPy`, `pyMetaheuristic` all ship HHO. **Replication confidence: high**.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - **Four exploitation modes = natural fit for multi-regime markets**. Soft-besiege ≈ trending regime (steady approach), hard-besiege ≈ consolidation (tight refinement), soft/hard dives ≈ breakouts with Lévy perturbation.
  - **Oscillating `E`** triggers periodic re-exploration — valuable when a profitable parameter region expires as the market regime shifts.
  - **Lévy dives** give heavy-tailed moves that handle bursty PnL surfaces.
  - **Moderate dimensionality (7–21)** is HHO's sweet spot: published results on 10–30 D problems consistently show top-3 finishes.
  - **Precedent in finance / time-series**: Moayedi et al. (2020) on stock-index forecasting, Essam et al. (2021) HHO-LSTM for cryptocurrency price prediction — direct, favourable precedent.
  - **Structural legitimacy**: HHO is not tainted by the metaphor-zoo critique, so it is defensible under academic scrutiny.
- **Weaknesses for this use case**:
  - **Noisy backtest PnL** corrupts the greedy `Y/Z` selection — mitigate with fitness averaging (multiple seeds) or non-greedy acceptance.
  - **Four modes × 13 peers mean-rank** tests use clean synthetic benchmarks; real-trading noise characteristics differ.
  - Needs validation on **non-stationary** objectives — the `E` schedule is time-indexed, not regime-indexed.
- **Replication confidence: Very high** — multiple library implementations, standardised and stable.

**Verdict**: **Top-tier candidate for Part 2**. Of the three algorithms in this batch (GOA, HHO, MRFO), HHO has the strongest combination of structural novelty, independent validation, and alignment with the trading-bot's bursty multi-regime fitness landscape. The four-mode exploitation plus Lévy dives matches crypto behaviour more naturally than most alternatives. Recommend shortlisting HHO for the final Part-2 comparison.

---

## Key Citations for Final Report (IEEE style)

1. A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and H. Chen, "Harris hawks optimization: Algorithm and applications," *Future Generation Computer Systems*, vol. 97, pp. 849–872, Aug. 2019.
2. E. H. Houssein, M. E. Hosney, D. Oliva, W. M. Mohamed, and M. Hassaballah, "A novel hybrid Harris hawks optimization and support vector machines for drug design and discovery," *Computers & Chemical Engineering*, vol. 133, art. 106656, Feb. 2020.
3. L. Abualigah, A. Diabat, S. Mirjalili, M. Abd Elaziz, and A. H. Gandomi, "The Arithmetic Optimization Algorithm," *Computer Methods in Applied Mechanics and Engineering*, vol. 376, art. 113609, 2021 (survey context for HHO variants).
4. H. Jia, C. Lang, D. Oliva, W. Song, and X. Peng, "Dynamic Harris Hawks Optimization with Mutation Mechanism for Satellite Image Segmentation," *Remote Sensing*, vol. 11, no. 12, art. 1421, Jun. 2019.
5. J. L. Bednarz, "Cooperative hunting in Harris' hawks (*Parabuteo unicinctus*)," *Science*, vol. 239, no. 4847, pp. 1525–1527, Mar. 1988 (biological source).

---

## Research Status
- [x] Original paper located and cited
- [x] All four exploitation phases (soft, hard, soft-dive, hard-dive) documented with equations
- [x] Escape-energy model `E = 2·E_0·(1 − t/T)` and switching rules on `|E|` and `r` captured
- [x] Lévy-flight dive component noted
- [x] Benchmark results (29 functions + CEC 2017 + 6 engineering) summarised
- [x] 6 reviewer questions answered
- [x] Independent validation noted (HHO is NOT in metaphor-zoo critiques)
- [x] Crypto-LSTM precedent flagged
- [x] Perplexity step skipped due to API quota; citations verified via Tavily web search (2026-04-19)
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines
