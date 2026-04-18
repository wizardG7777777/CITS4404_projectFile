# Conclusions

## Scope of This Survey

This survey examined twenty nature-inspired optimisation algorithms spanning 1992 to 2020, ranging from the foundational works of Dorigo et al. (ACO, 1992) [1] and Kennedy & Eberhart (PSO, 1995) [2] through to Heidari et al. (HHO, 2019) [3] and Zhao et al. (MRFO, 2020) [4]. The primary deliverable for Part 1 is a pair of deep-dive synopses for PSO and the Whale Optimization Algorithm (WOA); the remaining eighteen algorithms serve as comparative context, grounding the two synopses in a broader picture of how swarm intelligence has evolved in design philosophy, methodological rigour, and applicability to continuous optimisation.

---

## Finding 1: Peer-Reviewed Evidence of Metaphor Inflation Implicates Four to Six of the Twenty Algorithms

The most consequential evidence to emerge from this survey is the 2023 paper by Camacho-Villalón, Dorigo, and Stützle, published in the *International Transactions in Operational Research* [5]. This is not a blog post or preprint; it is a journal article co-authored by Dorigo—the originator of ACO—and constitutes a structurally rigorous algebraic critique. The authors demonstrate that Grey Wolf Optimizer (GWO), Moth-Flame Optimization (MFO), WOA, Firefly Algorithm (FA), and Bat Algorithm (BA) can each be reduced, through algebraic manipulation, to variants of PSO with a monotone decreasing inertia schedule. In GWO, the three-leader weighted average `X(t+1) = (X1+X2+X3)/3` is equivalent to a PSO update with `a: 2→0` matching Shi & Eberhart's (1998) inertia-weight extension. In WOA, the spiral-and-shrink mechanism collapses to the same structure. The paper further documents that bugs and ambiguities in the original MATLAB implementations have been copied verbatim into thousands of subsequent studies.

When the independent critique by Castelli et al. (2022) [6]—which shows that the SSA follower rule converges to an exponential-smoothing low-pass filter of the leader trajectory—is combined with the Camacho-Villalón analysis, and Sörensen's (2015) earlier broadside against metaphor-driven metaheuristics [7] is added as a third independent line, the cumulative picture is clear: **four to six of the twenty algorithms surveyed carry documented novelty disputes in the peer-reviewed literature**. This is the methodological baseline against which any algorithm selection for Part 2 must be justified.

---

## Finding 2: A Four-Stage Design-Philosophy Arc Structures the 1992–2020 Period

The twenty algorithms do not constitute a uniform field; they map onto a coherent chronological arc with four identifiable stages.

**Stage 1 (1992–1995): Foundational paradigms.** ACO established stigmergic discrete search; PSO established continuous velocity-based flocking. Both have withstood nearly three decades of independent replication.

**Stage 2 (2007–2014): Early derivatives and genuine operator innovation.** Cuckoo Search (CS, 2009) introduced Lévy-flight heavy-tailed steps; Biogeography-based Optimization (BBO, 2008) contributed a rank-proportional migration operator; Spider Monkey Optimization (SMO, 2014) introduced fission-fusion topology as a genuinely variable population structure. Firefly Algorithm added distance-decay multi-modal attraction, though at an O(n²) pairwise evaluation cost that limits practical scalability.

**Stage 3 (2014–2017): The Mirjalili surge and novelty dilution.** Six of the nine algorithms in this window—GWO, MFO, WOA, Dragonfly Algorithm (DA), SSA, and GOA—originate from Mirjalili's authorship network. Each follows the same template: a novel animal metaphor encoded as a difference-weighted shrink equation, a single monotone schedule parameter (`a: 2→0` or `c: c_max→c_min`), and benchmark comparisons against untuned PSO on unshifted functions. This template, identified by Camacho-Villalón et al. as the structural basis of the critique, inflated the apparent diversity of the field without a commensurate increase in algorithmic innovation.

**Stage 4 (2019–2020): Post-critique multi-operator designs.** HHO and MRFO are the only two algorithms in the survey that postdate the main wave of methodological criticism and that employ multiple structurally distinct operators with ablation validation.

---

## Finding 3: HHO as the Exemplar of the Post-Critique Era; MRFO as Structurally Distinct

Harris Hawks Optimization (HHO, 2019) [3] satisfies three criteria that distinguish it from the Mirjalili-era majority. First, it does not appear on the Camacho-Villalón (2023) target list. Second, its four exploitation modes—soft besiege, hard besiege, soft besiege with progressive rapid dives, and hard besiege with progressive rapid dives—are gated jointly by `|E|` and a random variable `r`, and ablation studies (independently confirmed by Lei et al., 2022, *Applied Soft Computing*) show that removing any single mode measurably degrades multi-modal performance. Third, peer-reviewed financial precedents exist: Essam et al. (2021) applied an HHO-LSTM hybrid to cryptocurrency price prediction, and Moayedi et al. (2020) applied HHO to time-series forecasting.

MRFO (2020) [4] offers a complementary form of structural novelty. Its three operators—chain foraging, cyclone foraging, and somersault—are independently ablatable. Critically, the cyclone operator spirals around a **random reference point** rather than the global best, which is a genuine departure from WOA's and MFO's "orbit around `x_best`" design. This distinction matters for non-stationary landscapes where `x_best` is an unreliable anchor. The practical trade-off is that MRFO performs two function evaluations per iteration (primary plus somersault), doubling the evaluation budget relative to single-pass algorithms.

---

## Taxonomy Synthesis: Four Exploration–Exploitation Paradigms

Mapping all twenty algorithms against their exploration–exploitation balance mechanisms produces four design paradigms. **Paradigm A (explicit schedule)** uses a single parameter that decreases monotonically over iterations, as in PSO's inertia weight `ω`, WOA's `a: 2→0`, GWO's identical `a` schedule, and HHO's energy envelope `E`. This paradigm accounts for nine of the twenty algorithms and dominates the Mirjalili era. **Paradigm B (stagnation trigger)** resets or restructures the population upon detecting search stagnation, as in ABC's scout abandonment and SMO's fission-fusion. **Paradigm C (probabilistic branching)** selects exploration or exploitation mode each iteration via a random gate, as in CS's abandonment probability `p_a`, HHO's four-mode `|E|`/`r` logic, and MRFO's chain/cyclone switch. **Paradigm D (spatial or role differentiation)** achieves balance through heterogeneous subpopulations or roles, as in FA's distance-decay multi-modal clustering, CSO's rooster/hen/chick hierarchy, and MRFO's chain-index positional ordering.

PSO sits firmly in Paradigm A; WOA also sits in Paradigm A, which is one reason Camacho-Villalón's equivalence argument is structurally plausible. Algorithms in Paradigms B, C, and D offer more adaptive responses to non-stationary landscapes, which is directly relevant to the multi-regime nature of cryptocurrency markets.

---

## Implication for Part 2: Defensible Choices and Algorithms to Flag

The Part 2 trading-bot optimisation task involves a continuous parameter space of 7–21 dimensions, expensive noisy fitness evaluations (backtests), and a non-stationary multi-regime environment. Against these requirements, the twenty algorithms divide clearly.

**Defensible choices.** PSO remains the appropriate baseline: low parameter count, extensive literature, and straightforward implementation. WOA is the second deep-dive algorithm and is defensible as a compact modern comparator, but any report using WOA must explicitly acknowledge the Camacho-Villalón (2023) critique and justify why the structural similarity to PSO does not invalidate the comparison. HHO is the strongest supplementary candidate: multi-regime via four modes, Lévy-flight diversity maintenance, and a direct cryptocurrency LSTM precedent. CS and SMO are credible alternatives if additional algorithms are needed—CS for its heavy-tailed step distribution (matching market jump dynamics) and SMO for its topology-restructuring fission-fusion (matching regime shifts).

**Algorithms to flag or avoid.** FFO should not be used: the origin-bias in `S_i = 1/sqrt(X_i²+Y_i²)` is a structural flaw documented in 2014 [8] and cannot be resolved by parameter tuning. DA carries a reproducibility gap due to an ambiguous enemy term in the original paper that different implementations resolve in contradictory ways without public acknowledgement. EHO's separating operator introduces a midpoint-of-bounding-box bias analogous to FFO's. GWO, MFO, SSA, and GOA may be included as comparison points, but their structural equivalence to PSO variants should be acknowledged explicitly rather than treated as independent evidence.

---

## Closing

This survey has established a structured methodological baseline for algorithm selection in Part 2: three independent lines of peer-reviewed criticism (Sörensen 2015 [7], Camacho-Villalón et al. 2023 [5], Castelli et al. 2022 [6]) converge on the same diagnosis of the 2014–2017 surge, and the post-2019 algorithms HHO and MRFO represent the most defensible candidates from the modern era. What this survey has not settled is empirical performance on the specific backtest landscape of the chosen trading strategy—that question can only be resolved by the experiments in Part 2.

---

## References

[1] M. Dorigo, V. Maniezzo, and A. Colorni, "Ant System: optimization by a colony of cooperating agents," *IEEE Trans. Systems, Man, and Cybernetics, Part B*, vol. 26, no. 1, pp. 29–41, Feb. 1996.

[2] J. Kennedy and R. Eberhart, "Particle swarm optimization," in *Proc. IEEE ICNN*, vol. 4, 1995, pp. 1942–1948.

[3] A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and H. Chen, "Harris hawks optimization: Algorithm and applications," *Future Generation Computer Systems*, vol. 97, pp. 849–872, Aug. 2019.

[4] W. Zhao, Z. Zhang, and L. Wang, "Manta ray foraging optimization: An effective bio-inspired optimizer for engineering applications," *Engineering Applications of Artificial Intelligence*, vol. 87, art. 103300, Jan. 2020.

[5] C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, Nov. 2023.

[6] M. Castelli, L. Manzoni, L. Mariot, M. S. Nobile, and A. Tangherloni, "Salp Swarm Optimization: A critical review," *Expert Systems with Applications*, vol. 189, art. 116029, Mar. 2022.

[7] K. Sörensen, "Metaheuristics—the metaphor exposed," *International Transactions in Operational Research*, vol. 22, no. 1, pp. 3–18, Jan. 2015.

[8] H. Iscan and Ş. Gülcü, "Disadvantages of fruit fly optimization algorithm," *Proc. Int. Conf. Engineering Applications of Neural Networks*, 2014.

[9] S. Mirjalili and A. Lewis, "The whale optimization algorithm," *Advances in Engineering Software*, vol. 95, pp. 51–67, May 2016.

[10] S. Mirjalili, S. M. Mirjalili, and A. Lewis, "Grey Wolf Optimizer," *Advances in Engineering Software*, vol. 69, pp. 46–61, Mar. 2014.
