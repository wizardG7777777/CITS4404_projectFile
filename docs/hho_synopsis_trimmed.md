# HHO Synopsis — Trimmed Version (Balanced path, target ≈1.8 pages)

Target per-section word budget and actual:

| Section | Before | After | Delta |
|---------|--------|-------|-------|
| Q1 Problem | 178 | 107 | −71 |
| Q2 Previous Failures | 145 | 96 | −49 |
| Q3 New Idea (prose) | 239 | 165 | −74 |
| Q4 How Demonstrated | 194 | 119 | −75 |
| Q5 Results (prose) | 225 | 121 | −104 |
| Q6 Assessment (3 paras) | 373 | 230 | −143 |
| **Body total** | 1354 | **838** | **−516** |
| + headings + banner | 1412 | 902 | −510 |

Projected whole-doc total: **2621 → ~2111 words** (≈30% buffer under 3000).

---

## Synopsis 2: Harris Hawks Optimization (HHO)

> Algorithm: Harris Hawks Optimization (HHO)
> Authors: Ali Asghar Heidari, Seyedali Mirjalili, Hossam Faris, Ibrahim Aljarah, Majdi Mafarja, Huiling Chen
> Year: 2019
> Venue: Future Generation Computer Systems, vol. 97, pp. 849–872, Aug. 2019.

### 1. Problem Being Solved

HHO is presented as a general-purpose global optimiser for continuous, unconstrained problems [5], but its design targets a narrower issue: the premature convergence of PSO-family swarm algorithms on multimodal landscapes. The authors flag two coupled failure modes in prior methods. The exploration-to-exploitation transition is typically governed by a monotonic decay schedule that is blind to actual search state, and late-stage exploitation offers little structural branching — a single blended update rule draws agents toward the best-so-far point, so the swarm contracts and cannot escape local basins. The authors frame this in predator–prey terms and use it to warrant a multi-phase architecture with explicit mode switching.

### 2. Previous Failures

PSO [1] uses a single velocity update that contracts once gbest stabilises, a source of premature convergence on multimodal landscapes. GWO [6] enriches the attractor with three leaders but keeps a linear combination without behavioural branching. WOA [7] offers two exploitation modes (shrinking encircle, logarithmic spiral), but chooses between them by a coin flip rather than a target-state signal. DE, CS, and FA similarly lack mode switching conditioned on the prey's state. None encode the joint energy-plus-escape-chance switching that the HHO authors argue is needed to preserve diversity while exploiting.

### 3. New Idea + Core Equation

The novelty is a search process structured around the cooperative surprise-pounce behaviour of Harris's hawks [8], encoded through an escape-energy gate plus six update rules. At each iteration, each hawk draws:

```
E = 2 · E_0 · (1 − t/T),   E_0 ∈ U(−1, 1)
```

If |E| ≥ 1, the hawk enters one of two exploration rules (perch relative to family/rabbit, or random perch). If |E| < 1, it enters one of four exploitation rules gated jointly by |E| and a fresh escape chance r ∈ U(0,1): soft besiege, hard besiege, and the same two paired with progressive Lévy dives. Dive modes generate Y and a Lévy-perturbed Z = Y + S·LF(D), committing only if fitness strictly improves. Three aspects are novel: (i) because E_0 ∈ U(−1, 1), escape energy E oscillates in sign within a decaying envelope, producing transient re-exploration bursts late in the run; (ii) exploitation is four genuinely distinct behaviours, not one blended rule; and (iii) heavy-tailed Lévy steps are gated behind a strict greedy filter. Together, these make HHO algorithmic rather than merely zoological, a distinction that matters for Q6.

### 4. How Demonstrated

HHO is demonstrated by implementation and large-scale numerical experiment. The benchmark suite comprises 29 mathematical test functions (F1–F23 across unimodal, high-dimensional multimodal, and fixed-dimension multimodal groups, plus F24–F29 IEEE CEC 2005 composites) and 6 real engineering design problems. Baselines cover 11 peer algorithms spanning evolutionary (GA, DE, BBO), swarm (PSO, GWO, MFO, CS, BA, FA, FPA), and teaching-inspired (TLBO) approaches. The protocol uses 30 agents, 500 iterations, and 30 independent runs, with the Wilcoxon rank-sum test at α = 0.05. MATLAB source code and pseudocode are released, and the algorithm has since been re-implemented in multiple Python libraries. A notable gap: no component-level ablation is reported, so the evidence speaks to HHO as a package rather than validating individual design choices.

### 5. Results

The Wilcoxon rank-sum test (α = 0.05) returned p < 0.05 versus each peer on the majority of functions. Gains are substantive on unimodal, high-dimensional multimodal (F9–F11 Rastrigin/Ackley/Griewank near-optimal where PSO, GWO, and WOA stagnate), and CEC 2005 composite groups (top-ranked on all six rotated, hybridised F24–F29 functions — exactly the regime the four-mode design targets). The fixed-dimension multimodal set (F14–F23, D ≤ 6) is the weaker part of the case, where behavioural branching offers little marginal benefit and HHO's advantage shrinks. On the six engineering problems, HHO matches or improves the best previously published designs. The emerging pattern — HHO's advantage is concentrated in larger, irregular search spaces, not small benchmark landscapes — signals the regime where it is most likely to outperform.

### 6. Assessment

Within the paper's deterministic benchmark setting, the authors' positive claims are largely justified. The multi-mode exploitation design is a genuine structural change, and the Wilcoxon p < 0.05 result on the majority of the 29 benchmarks supports the claim that the four-mode structure is functional. The principal qualification is that without a component-level ablation, the contributions of energy gating, the four modes, and the Lévy dives are not isolated — the evidence supports HHO as a package rather than validating any single design choice.

Key limitations. The E_0 ∈ U(−1,1) draw is not phase-locked to swarm state and can produce unproductive re-exploration late in the run; the Lévy step uses a fixed β = 1.5, inheriting CS's limitation; and the thresholds on |E| and r are hard rather than smoothly gated. Most consequentially, the greedy Y/Z acceptance assumes a deterministic objective — under noisy fitness, single-evaluation comparisons can lock in spurious improvements, which interacts badly with stochastic evaluation regimes.

Bearing on Part II. HHO's effective regime (7–30 D, multimodal, irregular) matches the trading-bot parameter vector (7 D single HIGH, up to 21 D full MACD), and its state-conditioned switching plausibly suits regime-shifting price data. Unlike several contemporaries including WOA, HHO is not named in Camacho-Villalón, Dorigo and Stützle's 2023 critique [9], so it carries no structural-legitimacy concerns. The caveat is noise-sensitivity: backtest fitness is noisy, and HHO's greedy acceptance interacts badly with noisy objectives — mitigable via K-seed averaging, but must be made explicit in the fair-comparison protocol.
