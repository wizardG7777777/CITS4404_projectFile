# Synopsis: Harris Hawks Optimization (HHO)

> **Algorithm**: Harris Hawks Optimization (HHO)
> **Authors**: A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, H. Chen
> **Year**: 2019
> **Venue**: *Future Generation Computer Systems*, Vol. 97, pp. 849–872. DOI: 10.1016/j.future.2019.02.028

---

## 1. What problem with existing algorithms is the new algorithm attempting to solve?

The paper presents HHO as a **general-purpose global optimiser** for continuous, unconstrained problems [1]. Read from its design, however, HHO's practical advantage is narrower than that positioning suggests: it targets a specific pathology of PSO-family swarm algorithms on multimodal landscapes — premature convergence coupled with rigid late-stage exploitation. The authors flag two coupled failure modes in prior methods. First, the exploration-to-exploitation transition is typically governed by a fixed, monotonic decay schedule (e.g., linearly shrinking inertia or step size) that is blind to the swarm's actual search state and so tends not to re-explore once stagnation occurs. Second, late-stage exploitation offers little structural branching: a single blended update rule draws agents toward the best-so-far point, so the swarm contracts into a Gaussian cloud and has limited room to escape a local basin through coordinated diversion. The authors frame this diagnosis in biological terms — real predator–prey encounters combine steady approach, tight encirclement, and rapid dives depending on the prey's residual energy and escape attempts — and use the framing as the warrant for a multi-phase architecture with explicit mode switching.

## 2. Why, or in what respect, have previous attempts failed?

PSO [3] uses a single velocity update whose search behaviour contracts once `gbest` stabilises, which the HHO authors flag as a source of premature convergence on multimodal landscapes. GWO [4] enriches the attractor with three leaders (α, β, δ), but the update remains a linear combination without behavioural branching. WOA [2] offers two exploitation modes (shrinking encircle and logarithmic spiral), but the mode choice is a coin flip rather than being gated on a target-state signal. DE foregrounds exploration without a matched exploitation structure; CS and FA rely on heavy-tailed or attraction-only moves without mode switching. Relative to HHO, these methods offer less explicit **state-conditioned behavioural branching** during the exploration-to-exploitation transition — their limitation under this framing is not that they are ineffective in general, but that they do not encode the joint energy-plus-escape-chance switching the HHO authors argue is needed to preserve diversity while exploiting.

## 3. What is the new idea presented in this paper?

The novelty is a search process structured around the cooperative surprise-pounce behaviour of Harris's hawks [5], encoded through an escape-energy gate plus six update rules. At each iteration, each hawk draws

```
E = 2 · E_0 · (1 − t/T),        E_0 ∈ U(−1, 1)
```

If `|E| ≥ 1`, the hawk follows one of two **exploration** rules (with equal probability `q`): when `q < 0.5`, perching based on the positions of other family members and the rabbit; when `q ≥ 0.5`, perching on a random location within the group's home range. If `|E| < 1`, it follows one of four **exploitation** rules selected jointly by `|E|` and a fresh escape chance `r ∈ U(0,1)`: *soft besiege*, *hard besiege*, *soft besiege with progressive Lévy dives*, and *hard besiege with progressive Lévy dives*. The two dive modes generate a candidate `Y` followed by a Lévy-perturbed candidate `Z = Y + S·LF(D)`, then commit only if fitness strictly improves. Three aspects are novel relative to prior swarm methods: (i) because `E_0` is uniform on `[−1, 1]`, the escape energy `E` **oscillates in sign** within a decaying envelope, producing transient re-exploration bursts late in the run; (ii) exploitation is **four genuinely distinct behaviours**, not one blended rule; and (iii) heavy-tailed Lévy steps are gated behind a strict greedy filter. Taken together, these features make HHO structurally distinct from algorithms whose updates remain variants of a single attraction rule — the novelty is **algorithmic rather than merely zoological**, a distinction that will matter when assessing the paper's legitimacy in Q6.

## 4. How is the new approach demonstrated?

HHO is demonstrated by implementation and large-scale numerical experiment. The benchmark suite comprises **29 mathematical test functions** (F1–F7 unimodal, F8–F13 high-dimensional multimodal, F14–F23 fixed-dimension multimodal, and F24–F29 composite functions from **IEEE CEC 2005**) and **6 real engineering design problems** (tension/compression spring, pressure vessel, welded beam, three-bar truss, rolling-element bearing, multi-plate disc clutch brake). Baselines cover **11 peer algorithms** spanning evolutionary (GA, DE, BBO), swarm-inspired (PSO, GWO, MFO, CS, BA, FA, FPA), and teaching-inspired (TLBO) approaches. The protocol uses 30 agents, up to 500 iterations, and **30 independent runs**, reporting best, mean, and standard deviation, with the Wilcoxon rank-sum significance test at α = 0.05. Reference MATLAB source code and pseudocode are released with the paper, and the algorithm has since been re-implemented in multiple Python libraries, so replication by downstream users is well supported. The protocol's emphasis is on **breadth** — many benchmarks, many peers, many seeds — rather than depth: it does not include a component-level ablation isolating the contributions of energy gating, the four exploitation modes, or the Lévy dives, so the demonstration speaks to *whether* HHO works as a package, not to *which* design choices drive the gains.

## 5. What are the results or outcomes and how are they validated?

Validation proceeds by statistical comparison against the 11 baselines across every benchmark group. Headline outcomes:

| Benchmark group | HHO vs 11 peers |
| :--- | :--- |
| Unimodal F1–F7 | Top-ranked on 6 of 7 |
| High-dim multimodal F8–F13 | Top-ranked on 5 of 6 |
| Composite F24–F29 (CEC 2005) | Top-ranked on 6 of 6 |
| Engineering (6 problems) | Matches or improves best published designs |

The Wilcoxon rank-sum test (α = 0.05) returned `p < 0.05` versus each peer on the majority of functions. The improvements are substantive on the unimodal, high-dimensional multimodal, and CEC 2005 composite groups; differences on fixed-dimension (F14–F23) functions are smaller and not always significant.

Zooming in on representative anchors: the **strongest evidence** comes from the CEC 2005 composite group (F24–F29), where HHO is top-ranked on all six — these are rotated, hybridised multi-modal functions that stress both exploration-exploitation balance and scale invariance, exactly the regime the four-mode design targets. On **F9–F11 (Rastrigin / Ackley / Griewank)** HHO reaches near-optimal values where PSO, GWO and WOA stagnate at orders-of-magnitude worse means. By contrast, the **weaker part of the case** is the fixed-dimension multimodal set (F14–F23): these are low-dimensional (D ≤ 6) landscapes where behavioural branching offers little marginal benefit over simpler updates, and HHO's advantage shrinks accordingly. Across the **six engineering problems**, HHO matches or improves the best previously published designs on both cost and constraint feasibility. The emerging pattern — HHO's advantage is concentrated in **larger, more irregular search spaces**, not in small benchmark landscapes — matters for downstream use, because it signals the regime in which HHO is most likely to outperform, rather than treating its gains as uniform across settings.

## 6. What is your assessment of the conclusions?

**Within the paper's own deterministic benchmark setting, the authors' positive claims are largely justified.** The multi-mode exploitation design is a genuine structural change rather than a cosmetic re-parameterisation, and the accompanying statistical evidence (Wilcoxon `p < 0.05` versus each peer on the majority of the 29 benchmarks) supports the claim that the four-mode structure is functional. The principal qualification is that, because no component-level ablation is reported, the relative contribution of energy gating, the four exploitation modes, and the Lévy dives is not isolated — the evidence supports HHO as a **package** rather than individually validating any of its three design choices.

**Key limitations and boundaries.** The paper's shortcomings are mostly of the kind a reviewer would flag for downstream practitioners. The `E_0 ∈ U(−1,1)` draw is pseudo-random and not phase-locked to swarm state, occasionally producing unproductive re-exploration late in the run; the Lévy step uses a fixed shape parameter `β = 1.5`, inheriting CS's limitation; and the thresholds on `|E|` and `r` are hard rather than smoothly gated. The most consequential limitation is that the greedy `Y/Z` acceptance assumes a *deterministic* objective — under **noisy fitness**, single-evaluation comparisons can lock in spurious improvements, which interacts badly with stochastic evaluation regimes.

**Bearing on Part II.** For the trading-bot experiments, the balance of evidence supports including HHO as a candidate optimiser, subject to a fair-comparison caveat. Three factors support inclusion: HHO's effective regime (7–30 D, multimodal, irregular) matches the trading-bot parameter vector (7 D for a single HIGH component, scaling to 21 D for full MACD under the Part II specification); its state-conditioned behavioural switching plausibly suits regime-shifting price data; and HHO is **not** named in Camacho-Villalón, Dorigo and Stützle's 2023 critique of six bestial-metaphor algorithms [6] — in contrast to several of its contemporaries, including WOA — so engaging with it does not carry the structural-legitimacy concerns that some other swarm algorithms do. The main caution concerns the evaluation regime: backtest-based fitness is noise-sensitive, and HHO's greedy `Y/Z` acceptance interacts badly with noisy objectives. This is mitigable without modifying HHO itself — e.g., wrapping the objective with K-seed fitness averaging — but should be made explicit in any fair-comparison protocol so the noise-sensitivity does not silently bias the comparison between HHO and its peers.

---

## References

[1] A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and H. Chen, "Harris hawks optimization: Algorithm and applications," *Future Generation Computer Systems*, vol. 97, pp. 849–872, 2019.

[2] S. Mirjalili and A. Lewis, "The Whale Optimization Algorithm," *Advances in Engineering Software*, vol. 95, pp. 51–67, 2016.

[3] J. Kennedy and R. C. Eberhart, "Particle swarm optimization," in *Proc. ICNN'95*, Perth, Australia, 1995, pp. 1942–1948.

[4] S. Mirjalili, S. M. Mirjalili, and A. Lewis, "Grey Wolf Optimizer," *Advances in Engineering Software*, vol. 69, pp. 46–61, 2014.

[5] J. C. Bednarz, "Cooperative hunting in Harris' hawks (*Parabuteo unicinctus*)," *Science*, vol. 239, no. 4847, pp. 1525–1527, 1988.

[6] C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, 2023. DOI: 10.1111/itor.13176
