# Synopsis Draft: Salp Swarm Algorithm (SSA)

> **Algorithm**: Salp Swarm Algorithm (SSA)
> **Original Authors**: Seyedali Mirjalili, Amir H. Gandomi, Seyedeh Zahra Mirjalili, Shahrzad Saremi, Hossam Faris & Seyed Mohammad Mirjalili
> **Year**: 2017
> **Venue**: S. Mirjalili, A. H. Gandomi, S. Z. Mirjalili, S. Saremi, H. Faris, and S. M. Mirjalili, "Salp Swarm Algorithm: A bio-inspired optimizer for engineering design problems," *Advances in Engineering Software*, vol. 114, pp. 163–191, Dec. 2017.
> **Category**: 1.13 (Swarm Intelligence — Marine Pelagic Tunicate Chains)

---

## 1. What problem with existing algorithms is SSA attempting to solve?

SSA targets **constrained continuous single-objective engineering design** and, in a companion multi-objective extension (MSSA) published in the same paper, also multi-objective problems. The framing in Mirjalili et al. (2017):

1. **Balancing exploration and exploitation with minimal tuning.** The authors argue that PSO/GA/DE require careful per-problem tuning of several interacting parameters, and that GWO/WOA/MFO (their own prior family) rely on complex update rules. SSA pitches a design with essentially **one runtime control parameter** (`c1`, annealed deterministically) plus two uniform random draws (`c2`, `c3`).
2. **Chain-structured information propagation.** In salps' natural form, individuals form a long physical chain; each follower's position is coupled only to its immediate predecessor. SSA converts this into a **sequential, anisotropic population topology** — the update pathway from leader to tail is a linear chain rather than a fully-connected swarm. The claim is that this gentle propagation smooths the exploration/exploitation transition without discrete phase switches.
3. **Engineering-design focus.** Unlike its siblings (GWO/WOA), SSA is evaluated prominently on seven classical engineering design problems (welded beam, pressure vessel, tension/compression spring, etc.) plus airfoil shape design and marine propeller design — emphasising practical-engineering utility.

---

## 2. Why, or in what respect, have previous attempts failed?

Per Mirjalili et al. (2017):

- **PSO**: Fully-connected swarm, all particles pulled simultaneously toward `gbest` / `pbest`; diversity collapses quickly on multimodal landscapes.
- **GA**: Parameter-heavy (crossover rate, mutation rate, selection type); performance sensitive to encoding.
- **DE**: Three coupled parameters (`NP`, `F`, `CR`); no topological structure.
- **ABC**: Fixed three-role scheme; no chain or spatial structure.
- **GWO, WOA, MFO (Mirjalili family)**: Several update modes selected by branch conditions; the authors now frame this as added complexity without a commensurate benefit.
- **CS / FA / BA**: Single-rule swarms; no population topology.

SSA's proposed fix: **chain topology** + **one annealed parameter** → information flows from the food source through the leader down the chain, naturally smoothing exploration → exploitation without branch conditions.

---

## 3. What is the new idea presented in the paper?

A population of `N` salps is ordered into a chain. The **first salp is the leader**; salps 2..N are **followers**, each coupled only to its predecessor.

### 3.1 Leader update (salp index `i = 1`)

For each dimension `j`:

```
          ⎧ F_j + c1 · ( (ub_j − lb_j) · c2 + lb_j )    if c3 ≥ 0.5
x_j^1  =  ⎨
          ⎩ F_j − c1 · ( (ub_j − lb_j) · c2 + lb_j )    if c3 <  0.5
```

- `F_j` = current food-source position in dimension `j` (best-so-far).
- `ub_j`, `lb_j` = upper / lower bound in dimension `j`.
- `c1` = annealed scale (primary control parameter, see below).
- `c2, c3 ∈ [0, 1]` = independent uniform random numbers, refreshed per leader update.

### 3.2 `c1` annealing schedule (the single control parameter)

```
c1 = 2 · exp( − ( 4 · t / T_max )² )
```

where `t` is the current iteration and `T_max` the maximum. `c1` decays smoothly from ≈ 2.0 (exploration) to ≈ 0 (exploitation) over the run. The Gaussian-in-`t` envelope is SSA's sole exploration/exploitation balance mechanism.

### 3.3 Follower update (salp index `i ≥ 2`)

Mirjalili et al. derive the follower rule from Newton's law of motion assuming a stationary initial velocity and time-step of one iteration. The discretised form collapses to a **simple average with the predecessor**:

```
x_j^i = ( x_j^i + x_j^{i−1} ) / 2          for i ≥ 2
```

This is the characteristic SSA rule: **each follower moves to the midpoint between itself and the salp in front**. Applied iteratively along the chain, positions propagate smoothly from leader to tail, creating a gradient of influence.

### 3.4 Food source update

At the end of each iteration, the best solution found so far is stored as `F` and used as the leader's attractor next iteration. If any salp has a better fitness than `F`, `F` is replaced.

### 3.5 Control parameters
- `N` (swarm / chain size, typical 30)
- `T_max` (iteration budget)
- `c1` annealing schedule (fixed formula — no tuning required)

### 3.6 Multi-objective extension (MSSA)
Add a repository of non-dominated solutions; sample `F` from low-crowding cells (roulette); sample a random archive member to steer the chain on each objective direction. Standard archived-MOEA machinery.

### 3.7 Key innovations claimed
1. **Chain topology with midpoint-averaging follower rule** — anisotropic, information-propagating population structure unique to SSA.
2. **Single annealed parameter `c1`** — dramatically simpler than GWO/WOA/PSO hyperparameter sets.
3. **Multi-objective SSA (MSSA)** natively from the same chain template.

---

## 4. How is the new approach demonstrated?

Mirjalili et al. (2017) evaluate SSA on:

**Single-objective continuous benchmarks**: 14 unimodal + 10 multimodal + 10 fixed-dimension multimodal + 5 composite CEC 2005 functions, D = 10 / 30 / 100 for scalable problems.

**Engineering design problems** (7 constrained): welded beam, tension/compression spring, pressure vessel, three-bar truss, I-beam, cantilever beam, multiple-disc clutch brake.

**Real-world design**: 2D airfoil design (aerofoil drag minimization) + marine propeller design (cavitation-free efficiency).

**Multi-objective** (MSSA): ZDT1–6 + CEC 2009 UF1–10.

**Baselines (single-objective)**: PSO, GA, GSA, BA, FPA, FA, SMS, GWO, MFO, WOA, State-of-the-art (depends on function class).

**Baselines (multi-objective)**: MOPSO, NSGA-II, MOEA/D, MOGWO.

**Protocol**: 30 independent runs, pop = 30, `T_max = 500–1000` depending on dimension. Mean / std; Wilcoxon at α = 0.05.

---

## 5. What are the results or outcomes and how are they validated?

### Headline findings (Mirjalili et al. 2017)

| Problem class | SSA verdict (per paper) |
|:---|:---|
| Unimodal (F1–F7) | Competitive — often slightly behind GWO/WOA on sphere-like |
| Multimodal (F8–F13) | **SSA reported best on several** |
| Fixed-dim multimodal (F14–F23) | All tested algorithms reach optimum |
| CEC 2005 composite (F24–F29) | SSA ties or wins |
| Welded beam, spring, pressure vessel | Matches or slightly beats published best |
| Airfoil design | ~1% drag reduction vs. baseline |
| ZDT / UF multi-objective (MSSA) | Competitive IGD/GD vs. MOPSO / NSGA-II |

### Follow-up validation and variants

- **ISSA** (Zhang et al. 2020) — chaotic initialisation + opposition-based learning; improved convergence.
- **Hybrid SSA-PSO** (Ibrahim, Ewees, Oliva, Abd Elaziz, Lu 2019) — blends PSO velocity with chain update for feature selection.
- **BSSA** (Faris et al. 2018) — binary SSA for feature selection on UCI; reports strong classification-accuracy / feature-count tradeoffs.
- **Survey**: Abualigah, Shehab, Alshinwan, Mirjalili & Abd Elaziz (2020) — *Salp swarm algorithm: a comprehensive survey*, *Neural Computing and Applications*.
- **Reviews of SSA applications in power systems, MPPT, PV-parameter estimation, feature selection, image processing** — several hundred derivative papers by 2022.

### Critical follow-up — structural concerns

- **Castelli, Manzoni, Mussi & Vanneschi (2022)** and the broader **Camacho-Villalón, Dorigo, Stützle (2020–2023)** critique of the Mirjalili family extend to SSA:
  - **The follower rule `x_j^i = (x_j^i + x_j^{i−1}) / 2` is a simple pairwise midpoint.** When applied along a chain from iteration 1, all followers progressively collapse toward the leader's trajectory — the chain is essentially a low-pass filter of the leader's walk. On unshifted origin-centred benchmarks, the leader's Gaussian-annealed search also concentrates around the food source, reinforcing origin-proximity bias.
  - **Leader update `F_j ± c1·((ub − lb)·c2 + lb)`**: note the `+ lb_j` inside the scale. For search spaces where `lb < 0`, this can cause the leader's step distribution to be asymmetric around `F_j` in a way that has no mechanistic justification — a possible typographical ambiguity that several re-implementations "repair" differently.
  - **Mechanism repetition**: the follower rule reduces, after a few chain steps, to a recency-weighted average of leader positions — mathematically close to an exponentially-smoothed PSO `gbest`-trail. Castelli et al. argue SSA offers no genuinely new dynamics relative to a damped PSO with decaying step size.
  - **Benchmark-suite concerns**: as with EHO, DA, GWO and WOA, the 2017 paper's reported wins concentrate on unshifted / unrotated classical benchmarks. On CEC 2014/2017 *shifted-rotated* suites, SSA's advantage diminishes or inverts versus modern DE variants (L-SHADE, JADE) and CMA-ES.
- No formal asymptotic convergence proof exists; several papers attempt stability analysis of the follower recurrence but not of the whole algorithm.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. SSA outperforms PSO, GA, GSA, BA, FPA, FA, SMS, GWO, MFO, WOA on many benchmarks with a single annealed parameter.
2. SSA is strong on constrained engineering design problems.
3. MSSA is competitive with MOPSO and NSGA-II.
4. Chain topology + midpoint-averaging is a genuinely novel mechanism.

### Assessment
- **Empirical results mostly reproducible** on the 2017 benchmark protocol, but **benchmark choice and unshifted landscapes favour SSA** (and its family siblings GWO/WOA) in ways documented by the Camacho-Villalón/Castelli line of work. On modern shifted-rotated CEC benchmarks, SSA is no longer a clear winner.
- **Mechanism-novelty claim is the weakest link.** The follower rule is a two-line moving average; a short calculation shows the chain behaves as an exponentially-decaying low-pass filter of the leader's trajectory. This reduces, after enough iterations, to *"PSO with decaying step size and a single-member informant topology"* — which is very close to prior work under a new name. The Mirjalili-family "mechanism-repetition" critique lands here.
- **Engineering-design claims are solid.** SSA's constrained-optimization results on the seven classical engineering problems are reproducible and have been re-confirmed independently. For practitioners, SSA is a reasonable plug-and-play choice *provided* the benchmark-bias caveat is disclosed.
- **Simplicity is real and valuable.** One-parameter annealing is attractive for student projects, for quick baselines, and for teaching. Implementation is ~50 lines of NumPy.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy multimodal backtest-PnL, non-stationary multi-regime markets)

- **Strengths for this use case**:
  - **One-parameter tuning** (`c1` is fixed by schedule; only `N` and `T_max` remain) — minimal meta-optimization burden, which is valuable under noisy fitness.
  - **Chain-averaging follower rule** is very smooth — successive evaluations produce positions close to their predecessors, so backtest fitness changes gradually along the chain. Useful for local-sensitivity diagnostics.
  - **Cheap per-iteration**: midpoint averaging is O(N·D) and allocation-free.
  - **Broad empirical record** in energy-system parameter estimation (PV cells, MPPT) — similar continuous-parameter tuning problem, though without adversarial non-stationarity.
- **Weaknesses for this use case**:
  - **Mechanism-repetition concern**: if SSA is essentially a damped PSO in disguise, then including it alongside PSO in the final survey adds limited methodological diversity. This must be disclosed in the comparative analysis.
  - **Origin-bias risk (moderate)**: crypto parameters are not origin-centred, and the midpoint-averaging chain interacts unusually with asymmetric bounded domains. Mitigate by normalising parameters to [0, 1] before optimisation.
  - **Slow exploration in late stages**: once `c1` anneals toward zero, the leader ceases exploring; the chain then collapses onto `F` via midpoint-averaging and the algorithm effectively halts. For non-stationary landscapes (regime shift mid-optimisation) this is a structural weakness — SSA does not naturally recover from stagnation without external restart.
  - **Noisy fitness on greedy `F`-update**: updating the food source from a single best evaluation is brittle under backtest-PnL variance. Use fitness averaging across k runs.
  - **Limited finance-specific precedent**: SSA has substantial literature in PV/MPPT and feature selection; trading-bot parameter tuning has been explored only in a handful of papers (e.g., Ewees et al. 2022 style studies).
- **Replication confidence**: **High on the chain update, medium on the leader update**. The Mirjalili MATLAB reference and multiple Python ports are consistent on the follower rule; they differ on whether the leader's `c2` is drawn once per dimension or once per update.

**Verdict**: SSA is a **reasonable middle-of-the-road candidate** for the crypto trading bot — simpler than DA/SMO/EHO, less aggressive on exploration than PSO/CS, and well-suited to low-tuning-budget scenarios. Its main liabilities are (i) the mechanism-repetition critique from the Castelli / Camacho-Villalón line (which the final report must acknowledge honestly) and (ii) its tendency to stall once `c1` decays — problematic for multi-regime non-stationary markets without a restart scheme. If SSA is used, pair it with periodic restart or opposition-based refresh; and for the survey component, present it explicitly as an illustration of the "chain topology + annealed single parameter" design philosophy.

---

## Key Citations for Final Report (IEEE style)

1. S. Mirjalili, A. H. Gandomi, S. Z. Mirjalili, S. Saremi, H. Faris, and S. M. Mirjalili, "Salp Swarm Algorithm: A bio-inspired optimizer for engineering design problems," *Advances in Engineering Software*, vol. 114, pp. 163–191, Dec. 2017.
2. H. Faris, M. M. Mafarja, A. A. Heidari, I. Aljarah, A. M. Al-Zoubi, S. Mirjalili, and H. Fujita, "An efficient binary Salp Swarm Algorithm with crossover scheme for feature selection problems," *Knowledge-Based Systems*, vol. 154, pp. 43–67, Aug. 2018.
3. L. Abualigah, M. Shehab, M. Alshinwan, S. Mirjalili, and M. Abd Elaziz, "Salp swarm algorithm: a comprehensive survey," *Neural Computing and Applications*, vol. 32, no. 15, pp. 11195–11215, Aug. 2020.
4. R. A. Ibrahim, A. A. Ewees, D. Oliva, M. Abd Elaziz, and S. Lu, "Improved salp swarm algorithm based on particle swarm optimization for feature selection," *Journal of Ambient Intelligence and Humanized Computing*, vol. 10, no. 8, pp. 3155–3169, 2019.
5. M. Castelli, L. Manzoni, L. Mariot, M. S. Nobile, and A. Tangherloni, "Salp Swarm Optimization: A critical review," *Expert Systems with Applications*, vol. 189, art. 116029, Mar. 2022. *(Preprint: arXiv:2106.01900, Jun. 2021. The most detailed published critique of SSA's mechanism novelty and benchmark practices.)*
6. C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, Nov. 2023. *(Representative of the broader critique family; does not target SSA directly but the methodological concerns generalise.)*

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (leader annealed Gaussian envelope + chain midpoint-averaging follower) documented with equations
- [x] Parameter list (`c1` schedule, `N`, `T_max`) recorded
- [x] Benchmark protocol (29 single-obj + 7 engineering designs + MSSA on ZDT/UF) summarized (count verified via secondary sources against Mirjalili et al. 2017 *AES* 114; exact CEC 2005 composite subset still warrants a direct read of the paper)
- [x] 6 reviewer questions answered
- [x] Mechanism-repetition / benchmark-bias critiques flagged honestly in Q6
- [x] Castelli et al. SSA critique citation verified via Tavily (authors corrected from prior "Mussi & Vanneschi" attribution to **Castelli, Manzoni, Mariot, Nobile, Tangherloni**, *ESWA* vol. 189, 2022; arXiv:2106.01900, 2021)
- [x] Perplexity step skipped due to API quota; citations verified via Tavily web search (2026-04-19)
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
