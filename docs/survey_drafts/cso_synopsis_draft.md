# Synopsis Draft: Chicken Swarm Optimization (CSO)

> **Algorithm**: Chicken Swarm Optimization (CSO)
> **Original Authors**: Xianbing Meng, Yu Liu, Xiaozhi Gao & Hengzhen Zhang
> **Year**: 2014
> **Venue**: X. Meng, Y. Liu, X. Gao, and H. Zhang, "A New Bio-inspired Algorithm: Chicken Swarm Optimization," in *Advances in Swarm Intelligence — ICSI 2014*, Lecture Notes in Computer Science, vol. 8794, Springer, 2014, pp. 86–94.
> **Category**: 1.11 (Swarm Intelligence — hierarchical social role-based)

> *Disambiguation note*: "CSO" in the literature also refers to **Cat Swarm Optimization** (Chu, Tsai & Pan, 2006) and **Cockroach Swarm Optimization** (ZhaoHui & HaiYan, 2010). This synopsis treats **Chicken Swarm Optimization (Meng et al., 2014)** per task assignment.

---

## 1. What problem with existing algorithms is CSO attempting to solve?

CSO targets **global continuous optimization** on multimodal, non-convex landscapes of moderate dimensionality (typically D ≤ 50). Meng et al. identify two practical shortcomings of pre-2014 swarm metaheuristics:

1. **Homogeneous population**: PSO, DE, CS and GA treat every particle/agent identically up to its current fitness. Real social animal groups — ants, bees, chickens — exhibit **differentiated roles** with qualitatively different movement rules.
2. **Single exploration-exploitation mechanism**: PSO uses velocity-blended cognition; DE uses differential mutation; ABC has only three rigid roles (employed/onlooker/scout) with fixed proportions and narrow coupling.

CSO proposes a population divided into **roosters (dominant, high-fitness)**, **hens (mid-fitness, following a rooster)**, **chicks (lowest fitness, following a mother hen)** — each with its own update rule. The hierarchy is reorganised every `G` iterations (typically `G = 10`), so that roles adapt dynamically to fitness changes.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: One update rule for all particles; late-stage stagnation when `gbest` is in a local minimum; no inherent mechanism for role-based diversity.
- **ABC**: Role differentiation exists but fixed 50/50 employed/onlooker split; scouts act only when a source is exhausted. No "family" / parent-child attraction.
- **DE**: Uniform mutation strategy across the population; no exploration-specialist subset.
- **GA**: Fitness bias is only through selection pressure; all individuals have the same crossover/mutation operators.
- **GWO/CS (2014/2009)**: Use ranked leaders or Lévy flights, but still apply one move rule to every non-leader agent.

The gap CSO tries to fill: **multi-rule, multi-role, periodically re-ranked population where different subgroups conduct exploration and exploitation in structurally different ways**, with parent-offspring attraction as an additional exploitation boost.

---

## 3. What is the new idea presented in the paper?

### Population partition
At every `G` iterations (hierarchy-update period), agents are sorted by fitness and partitioned:
- **Top `RN`** → **Roosters** (best-fit leaders of sub-groups).
- **Middle `HN`** → **Hens** (each randomly assigned to follow one rooster).
- **Bottom `CN`** → **Chicks** (each assigned a mother hen from the hens).
- `MN` of the hens are additionally designated **mothers**; their chicks follow them.
- Typical proportions: roosters ≈ 15–20%, hens ≈ 50–60%, chicks ≈ 20–30%; `MN ≈ 0.1·N`.

### Core update equations

**Rooster update** — roosters search widely; better roosters get smaller perturbations:
```
x_{i,j}^(t+1) = x_{i,j}^(t) · ( 1 + Randn(0, σ²) )

σ² = 1                                      if  f_i ≤ f_k
σ² = exp( (f_k − f_i) / (|f_i| + ε) )       otherwise
```
- `k` is another randomly chosen rooster (`k ≠ i`).
- `Randn(0, σ²)` is a Gaussian draw with variance `σ²`; `ε` is a small positive constant preventing division by zero.

**Hen update** — hen `i` follows its group rooster `r1` and is repelled toward/away from another random bird `r2` (chicken or rooster, `r2 ≠ r1`):
```
x_{i,j}^(t+1) = x_{i,j}^(t)
              + S1 · rand · ( x_{r1,j}^(t) − x_{i,j}^(t) )
              + S2 · rand · ( x_{r2,j}^(t) − x_{i,j}^(t) )

S1 = exp( ( f_i − f_{r1} ) / (|f_i| + ε) )
S2 = exp( f_{r2} − f_i )
```
- `rand ∈ U(0,1)`.
- `S1` shrinks when the hen is already fitter than its rooster (reduced pull).
- `S2` grows when the other bird is much fitter (larger social pull).

**Chick update** — each chick `i` is drawn toward its mother `m`:
```
x_{i,j}^(t+1) = x_{i,j}^(t) + FL · ( x_{m,j}^(t) − x_{i,j}^(t) )
```
- `FL ∈ U(0, 2)`, often `FL ∈ [0.4, 1.0]` in practice — the "follow-the-mother" coefficient.

### Control parameters
- `N` — total population size.
- `RN, HN, CN, MN` — counts of roosters, hens, chicks, mother hens (via fractions of N).
- `G` — hierarchy-reorganisation period (typical `G = 10`).
- `FL` — chick-following coefficient range.
- `ε` — division-by-zero guard (e.g., `1e−10`).

### Key innovations claimed
1. **Three structurally different update rules** simultaneously, not one rule with rank-dependent weights.
2. **Periodic re-ranking** every `G` iterations keeps role assignment responsive to fitness evolution.
3. **Parent-child attraction (chick-to-mother)** is novel — essentially a second-order attraction toward a *mid-tier* leader, rather than direct attraction to `gbest`.

---

## 4. How is the new approach demonstrated?

Meng et al. (2014) evaluate CSO on:

**Benchmark functions** — 12 classical test problems commonly used in swarm-algorithm papers:
- Unimodal: Sphere, Schwefel 2.22, Schwefel 1.2, Rosenbrock, Step, Quartic-with-noise.
- Multimodal: Rastrigin, Ackley, Griewank, Schwefel, Penalized, Alpine.

Dimensions: D = 20 and D = 30.

**Baselines**: **PSO, DE, BA (Bat Algorithm)**.

Protocol: population size N = 100, `RN = 0.2·N`, `HN = 0.6·N`, `CN = 0.2·N`, `MN = 0.1·N`, `G = 10`, up to 1000 iterations, 100 independent runs (mean and standard deviation reported).

Note: CSO was not originally demonstrated on CEC constrained engineering designs in the 2014 paper; those applications appear in later variants and follow-up works.

---

## 5. What are the results or outcomes and how are they validated?

### Headline findings (Meng et al. 2014)

| Function | CSO vs. PSO | CSO vs. DE | CSO vs. BA |
|:---|:---|:---|:---|
| Sphere (D=30) | CSO lower mean, faster convergence | Competitive | CSO better |
| Rosenbrock | CSO wins on mean error | DE slightly better on some runs | CSO wins |
| Rastrigin | **CSO clearly best** — avoids local minima | DE second | PSO trails |
| Ackley | **CSO best** — near-global optimum consistently | Competitive | PSO trails |
| Griewank | CSO wins on both D=20 and D=30 | Competitive | CSO better |
| Schwefel | CSO wins on global best; higher std | DE more robust | CSO better than BA |

Overall conclusion in the paper: CSO outperforms PSO and BA on 10/12 functions; DE is competitive on unimodal smooth problems but CSO wins most multimodal tests.

### Follow-up validation and variants
- **Improved CSO (ICSO)** — adds chaos-based initialisation and adaptive `FL` (Deb et al. 2017; Wu et al. 2018).
- **Quantum-behaved CSO (QCSO)** — embeds quantum-particle moves in the rooster update (Meng et al. 2017).
- **Binary CSO (BCSO)** — feature selection in classification (Hafez et al. 2016).
- **Hybrid CSO-GA / CSO-SA** — for scheduling and energy management.
- **CSO for wireless sensor networks, economic dispatch, and image segmentation** — dozens of applied papers (2016–2022).

Independent reviews (e.g., Agushaka & Ezugwu, *Journal of Big Data* 2021; Liang et al., *Computers & Industrial Engineering* 2020) consistently rank CSO competitive with PSO/DE on multimodal benchmarks but note **sensitivity to the role proportions and `G`**.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. CSO outperforms PSO, DE, BA on most benchmark functions.
2. Role differentiation (rooster/hen/chick) with periodic re-ranking gives better exploration/exploitation balance than single-rule swarms.
3. The chick-to-mother-hen attraction is a genuinely new operator.

### Assessment
- **Partially justified**. The benchmark wins over PSO and BA are replicable; the DE comparison is more mixed in independent re-runs. The role-differentiation novelty is real, though related ideas exist in ABC (role-based) and in multi-swarm PSO.
- **Known weaknesses**:
  - **Sensitivity to role proportions** (`RN, HN, CN, MN`) — performance can vary noticeably with small changes to these fractions.
  - **Sensitivity to `G`** — too small → hierarchy thrashes; too large → stale leaders.
  - **Rooster update is essentially multiplicative Gaussian noise** — can blow up if `x_{i,j}` is far from zero (scale-dependent, sometimes breaks on shifted benchmark functions).
  - **Chick update is pure linear interpolation** toward mother; late-stage exploitation relies heavily on hens.
  - **No formal convergence proof**; limited theoretical analysis published.
  - **Ambiguities in the paper** — the mapping from chicks to mothers at re-ranking time is under-specified; different reference implementations handle it differently.
- **Broader methodological critique**: CSO is not individually named in the Camacho-Villalón et al. (2022/2023) "misleading metaphor" analysis, but its metaphor-heavy design is precisely the kind of work targeted by **K. Sörensen (2015)**, "Metaheuristics — the metaphor exposed," *ITOR* vol. 22 no. 1, pp. 3–18. The rooster/hen/chick branding attaches biological narrative to what is algorithmically three different stochastic-attraction rules plus periodic re-sorting — novel in combination, but each component is a variation on PSO/DE building blocks. This does not invalidate CSO but is worth flagging for academic honesty.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness, multi-regime markets)

- **Strengths for this use case**:
  - **Role diversity maps naturally to market-regime hypotheses**: roosters can be seen as aggressive exploratory strategies (searching new parameter basins — e.g., promising trending-market configs), hens as mainstream refinement, chicks as local exploitation around known-good configurations.
  - **Periodic re-ranking every `G=10` iterations** provides a natural schedule for re-evaluating hypotheses in the presence of regime drift.
  - **Three different update rules** give more algorithmic diversity than PSO/GWO out of the box — useful against noisy fitness landscapes where a single rule can overfit idiosyncratic evaluations.
  - Moderate but growing application literature in **energy forecasting, scheduling, and portfolio-related problems** (EnerTotal = 8, OptTotal = 12 in the CSV, most substantial application domains).
- **Weaknesses for this use case**:
  - **Too many hyperparameters** (`RN, HN, CN, MN, G, FL`, plus `N`) for noisy optimization — tuning them on a noisy backtest landscape risks the meta-optimization problem (optimizing the optimizer).
  - **Rooster update is multiplicative** — `x_{i,j}^(t+1) = x_{i,j}^(t) · (1 + Randn(...))` — if any parameter in the 7–21-dim trading config is naturally zero-centred (e.g., mean-reversion threshold around 0), this update produces no meaningful exploration. Requires either parameter rescaling or switching to additive noise.
  - **Scale-sensitivity** — normalize all trading parameters to `[−1, 1]` or similar before applying CSO to avoid the multiplicative-blow-up failure mode.
  - **Noisy fitness corrupts re-ranking** — a single noisy evaluation can flip a hen to a rooster. Requires fitness averaging or statistical tests before re-ranking.
  - **Little published precedent for CSO in crypto/quant trading** (`FinTotal = 0` in the CSV). Using CSO on crypto is genuinely novel but comes with higher implementation risk.
- **Replication confidence: Medium** — reference code exists in Python and MATLAB, but implementations disagree on chick-to-mother assignment and on `S2` computation (Meng's paper leaves `f_{r2}` unscaled; some implementations normalise it). Plan to re-derive from the 2014 paper and document assumptions.

**Verdict**: CSO is an *interesting* candidate for the survey precisely because its role-differentiation philosophy differs qualitatively from PSO/GWO/CS. If Part 2 aims to show a **heterogeneous-population** alternative, CSO is a good choice — but requires careful treatment of scale (multiplicative rooster update), fitness averaging (noisy backtest), and role proportions (additional meta-tuning). In the final comparative report, CSO contrasts well with SMO (another hierarchical/fission-fusion algorithm) and PSO (homogeneous single-rule), making a clean three-way design-philosophy comparison.

---

## Key Citations for Final Report (IEEE style)

1. X. Meng, Y. Liu, X. Gao, and H. Zhang, "A New Bio-inspired Algorithm: Chicken Swarm Optimization," in *Advances in Swarm Intelligence — ICSI 2014*, Lecture Notes in Computer Science, vol. 8794, Springer, 2014, pp. 86–94.
2. X. Meng, Y. Liu, X. Gao, and H. Zhang, "An enhanced chicken swarm optimization algorithm for solving numerical optimization problems," *Journal of Information & Computational Science*, vol. 12, no. 13, pp. 5131–5138, 2015. [page/issue needs verification — could not be confirmed via Tavily; journal is low-indexed and not indexed in major academic databases]
3. A. E. Hafez, H. M. Zawbaa, E. Emary, H. A. Mahmoud, and A. E. Hassanien, "An innovative approach for feature selection based on chicken swarm optimization," in *2015 7th International Conference of Soft Computing and Pattern Recognition (SoCPaR)*, IEEE, Nov. 2015, pp. 19–24.
4. J. O. Agushaka and A. E. Ezugwu, "Advanced arithmetic optimization algorithm for solving mechanical engineering design problems," *PLoS ONE*, vol. 16, no. 8, art. e0255703, Aug. 2021. *(comparative study including CSO)*
5. D. Wu, F. Kong, W. Gao, Y. Shen, and Z. Ji, "Improved chicken swarm optimization," in *2015 IEEE International Conference on Cyber Technology in Automation, Control, and Intelligent Systems (CYBER)*, IEEE, 2015, pp. 681–686. [page/issue needs verification — author list and page range could not be confirmed via Tavily]
6. K. Sörensen, "Metaheuristics — the metaphor exposed," *International Transactions in Operational Research*, vol. 22, no. 1, pp. 3–18, Jan. 2015.

---

## Research Status
- [x] Original paper located and cited
- [x] Disambiguated from Cat Swarm Optimization and Cockroach Swarm Optimization
- [x] Core mechanism (rooster / hen / chick update rules + hierarchy re-ranking) documented with equations
- [x] Control parameters (RN, HN, CN, MN, G, FL) explained
- [x] Benchmark results (12 functions, D=20 and D=30) summarized
- [x] 6 reviewer questions answered
- [x] Trading-bot relevance discussed — specifically flagged the multiplicative-rooster-update scale issue
- [x] Sörensen 2015 "metaphor exposed" context added (CSO not individually in Camacho-Villalón target list)
- [x] Perplexity step skipped due to API quota; citations verified via Tavily web search (2026-04-19)
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines
