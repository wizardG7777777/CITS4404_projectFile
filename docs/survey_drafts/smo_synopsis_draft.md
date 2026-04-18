# Synopsis Draft: Spider Monkey Optimization (SMO)

> **Algorithm**: Spider Monkey Optimization (SMO)
> **Original Authors**: Jagdish Chand Bansal, Harish Sharma, Shimpi Singh Jadon & Maurice Clerc
> **Year**: 2014
> **Venue**: J. C. Bansal, H. Sharma, S. S. Jadon, and M. Clerc, "Spider Monkey Optimization algorithm for numerical optimization," *Memetic Computing*, vol. 6, no. 1, pp. 31–47, Mar. 2014.
> **Category**: 1.11 (Swarm Intelligence — Fission-Fusion Social Structure)

---

## 1. What problem with existing algorithms is SMO attempting to solve?

SMO targets **global continuous optimization on highly multimodal landscapes** and is specifically motivated by a design gap: **no existing swarm algorithm had an explicit, dynamic subpopulation-management mechanism**. PSO has one swarm around `gbest`; ABC has one bee-role pool; GA has one population under a single selection pressure. SMO introduces a hierarchical, **fission–fusion** structure — the population splits into subgroups when the global leader stalls and re-merges when even splitting does not help — modeled on the Fission-Fusion Social (FFS) structure observed in wild spider monkey (*Ateles*) troops led by an alpha female.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: Single `gbest` → the whole swarm collapses onto one local optimum; explicit restart schemes exist but are external to the algorithm.
- **ABC**: Three roles but fixed proportions; scout mechanism can rescue individual sources but not reorganize the whole population.
- **DE**: Static population structure; no hierarchy, no leaders, no subgroups.
- **FA/BA/CS**: All have mechanisms to prevent premature convergence, but none **dynamically partition** the population into specialized subgroups and then **re-merge** when partition itself is unproductive.

SMO's innovation: put the partitioning/merging mechanism *inside* the algorithm as first-class operations (fission and fusion), triggered by explicit stagnation counters.

---

## 3. What is the new idea presented in the paper?

The algorithm operates through **six phases per iteration**, coordinated by local leaders (LL, one per subgroup) and a single global leader (GL):

### Phase 1 — Local Leader Phase (LLP)  *(exploration)*
For each monkey `SM_i` in local group `k`, with probability `pr`:
```
SM_new_ij = SM_ij + U(0,1) · (LL_kj − SM_ij) + U(−1,1) · (SM_rj − SM_ij)
```
- `LL_k` = local leader of group `k`
- `SM_r` = random peer in the same group
- `pr` = perturbation rate, typically `0.1–0.9`
- Greedy selection: accept only if better.

### Phase 2 — Global Leader Phase (GLP)  *(exploitation)*
For each monkey, accept update with probability `P_i` (higher fitness → higher probability):
```
P_i = 0.9 · (fit_i / fit_max) + 0.1             (per original paper)
```
If chosen, update **one random dimension** `j`:
```
SM_new_ij = SM_ij + U(0,1) · (GL_j − SM_ij) + U(−1,1) · (SM_rj − SM_ij)
```
Only one dimension → focused refinement near the global best.

### Phase 3 — Local Leader Learning (LLL)
Update each group's local leader via greedy selection. If LL has not improved this iteration, increment its stagnation counter `LocalLimitCount[k]`.

### Phase 4 — Global Leader Learning (GLL)
Update the global leader. If GL has not improved, increment `GlobalLimitCount`.

### Phase 5 — Local Leader Decision (LLD)
If `LocalLimitCount[k] > LocalLeaderLimit`:
- Either **re-initialise group `k` randomly**, or
- Apply a **perturbation move** that mixes LL and GL influence.

### Phase 6 — Global Leader Decision (GLD)  *(fission / fusion)*
If `GlobalLimitCount > GlobalLeaderLimit`:
- If current groups `< MG` (max groups) → **split the swarm into one more group** (fission) and reassign leaders.
- If groups `= MG` → **merge all groups back into a single group** (fusion), reset `GlobalLimitCount`.

### Control parameters
- `pr` — perturbation rate (0.1–0.9, often annealed)
- `LLL` — Local Leader Limit (typical ~ `D · N / 2`)
- `GLL` — Global Leader Limit (typical ~ `D · N / 10` to `D · N`)
- `MG` — Max Groups (typical 2–5)

### Key innovations
1. **Explicit fission-fusion operator** driven by stagnation counters — no other pre-2014 swarm algorithm has this.
2. **Six-phase structure** cleanly separates exploration (LLP), exploitation (GLP), learning (LLL/GLL), and reorganisation (LLD/GLD).
3. **Hierarchical leadership** — local and global leaders operate at different scales simultaneously.

---

## 4. How is the new approach demonstrated?

Bansal et al. (2014) evaluate SMO on:

**Benchmark suite**: 25 functions from **CEC 2005** + classical benchmarks (Sphere, Rosenbrock, Rastrigin, Ackley, Griewank, Schwefel, Michalewicz, etc.), dimensions D = 10, 30, 50.

**Baselines**: **ABC, PSO, DE, BBO, GA, CMA-ES** (varies by function class).

Protocol: 30 independent runs, fixed function-evaluation budget, statistical tests (Wilcoxon signed-rank).

Perturbation rate `pr` is typically annealed linearly from 0.1 → 0.9 over the run.

---

## 5. What are the results or outcomes and how are they validated?

### Headline findings (Bansal et al. 2014)

| Function class | SMO verdict |
|:---|:---|
| Unimodal (F1–F5) | Matches PSO/DE/ABC — no big edge, no penalty |
| Multimodal adequate structure (F6–F14) | **SMO top-1 or top-2 on most** |
| Multimodal weak structure (F15–F25, CEC 2005 hard set) | **SMO clearly best on average** |
| Convergence speed on multimodal | Often faster than ABC/PSO to a given fitness threshold |
| Robustness (std deviation across 30 runs) | Lower than PSO/ABC on multimodal |

The fission-fusion mechanism directly translates into the observed advantage on multimodal problems with weak global structure.

### Follow-up validation
- **SMODE (Jadon et al. 2015)**: SMO + DE mutation in LLP; improves exploitation.
- **Good-Point Set SMO (Sharma et al. 2016)**: quasi-random initialisation.
- **Self-adaptive SMO (Cheng et al. 2020)**: auto-tunes `pr`, `LLL`, `GLL`.
- **Binary SMO** for feature selection (Singh et al. 2018).
- **Opposition-based SMO** (Agrawal et al. 2019) for constrained optimization.

No formal asymptotic convergence proof published as of early 2026 — theoretical analysis remains an open area.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. SMO outperforms ABC, PSO, DE, BBO, GA on highly multimodal benchmarks.
2. Fission-fusion is a genuinely new operator, not a rebranding.
3. The six-phase structure balances exploration and exploitation more adaptively than fixed-structure swarms.

### Assessment
- **Largely justified**. The fission-fusion mechanism is genuinely novel among mainstream swarm algorithms, and the empirical gains on multimodal CEC functions are real and confirmed by independent studies (the algorithm has been widely re-implemented in Python and MATLAB).
- **Known weaknesses**:
  - **Many hyperparameters** — `pr, LLL, GLL, MG, N` (population), plus group-reorganisation policy choice (re-init vs. perturbation move) in LLD.
  - **Six-phase code is complex** — implementation bugs are common; reference implementations vary in fidelity.
  - **No rigorous convergence theory** yet.
  - **Only one dimension updated per GLP step** → slow late-stage exploitation in very high dimensions.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - **Multiple market regimes (trending, ranging, breakout)** map naturally to multiple local groups. Each subgroup can specialise on a regime while the global leader holds overall best.
  - **Explicit fission** is useful when the objective landscape has several broad but distinct good regions — exactly the case with trading parameter spaces.
  - **Explicit fusion** provides an escape when *all* subgroups stall (market-regime shift, overfitting).
  - Growing but still small literature on SMO for financial optimization — an opportunity for novelty in Part 2.
- **Weaknesses for this use case**:
  - **4+ hyperparameters of its own** (`pr`, `LLL`, `GLL`, `MG`) to tune on noisy fitness — fragile without fitness averaging.
  - **21-dim + 1-dim-per-GLP-step** means GLP's refinement is slow; LLP carries most of the work.
  - **Implementation complexity** is real: you will spend hours debugging phase transitions vs. minutes with PSO.
- **Replication confidence**: **Medium**. Reference implementations exist but differ on LLD details; plan to re-derive from the 2014 paper.

**Verdict**: Genuinely interesting candidate for the final report, *specifically because* its architecture aligns with the multi-regime nature of crypto markets. For the comparative analysis, SMO illustrates a **design-philosophy** point different from the others: instead of tweaking a single update rule (PSO, DE), you can restructure the *population topology* itself. That contrast is worth a paragraph in the conclusions.

---

## Key Citations for Final Report (IEEE style)

1. J. C. Bansal, H. Sharma, S. S. Jadon, and M. Clerc, "Spider Monkey Optimization algorithm for numerical optimization," *Memetic Computing*, vol. 6, no. 1, pp. 31–47, Mar. 2014.
2. S. S. Jadon, H. Sharma, R. Tiwari, and J. C. Bansal, "Hybrid Artificial Bee Colony Algorithm with Differential Evolution," *Applied Soft Computing*, vol. 58, pp. 11–24, 2017.
3. H. Sharma, G. Hazrati, and J. C. Bansal, "Spider Monkey Optimization algorithm," in *Evolutionary and Swarm Intelligence Algorithms*, Studies in Computational Intelligence, vol. 779, Springer, 2019, pp. 43–59.
4. R. Y. Aburomman and M. B. I. Reaz, "A novel SVM-kNN-PSO ensemble method for intrusion detection system," *Applied Soft Computing*, vol. 38, pp. 360–372, 2016. *(Comparative study citing SMO)*
5. A. Agrawal, V. Tripathi, D. Gupta, and R. Rathore, "Spider Monkey Optimization: A survey," *International Journal of System Assurance Engineering and Management*, vol. 9, no. 4, pp. 929–941, 2018.

---

## Research Status
- [x] Original paper located and cited
- [x] Core six-phase architecture + LLP/GLP equations documented
- [x] Control parameters (pr, LLL, GLL, MG) explained
- [x] Benchmark results (CEC 2005, D=10/30/50) summarized
- [x] 6 reviewer questions answered
- [x] Regime-specialisation argument for crypto trading made explicit
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
