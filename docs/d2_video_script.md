# Deliverable 2 — Video Script (≤25 min)

**Team 20**: Qiurong Chen (24558583) · Yanchen Yu (24256987)

Speaker tags:

- **Q** = Qiurong (D1 PSO author; reads PSO / RandomSearch / training-results sections)
- **Y** = Yanchen (D1 HHO author; reads HHO / GWO / behaviour / generalisation sections)
- **Both** = joint reading (title, closing)

Pacing assumption: ~135 wpm (clear, slightly slow for technical narration). Total script ≈ 3 300 words → ≈ 24:30.

Visual cues `[SLIDE: name]` mark where to advance the deck. All figures live in `results/figures/`.

---

## Segment 0 — Title (0:00 – 0:20, ≈ 45 w)

**[SLIDE: title]**

**Both**:
> Good afternoon. We are Team 20 — Qiurong Chen and Yanchen Yu. This presentation reports our work for CITS4404 Deliverable 2: optimising a Bitcoin trading bot with four nature-inspired and stochastic algorithms.

---

## Segment 1 — Introduction (0:20 – 1:30, ≈ 160 w)

**[SLIDE: btc_animation]** (B-roll: BTC candlestick chart)

**Q**:
> Algorithmic trading already drives an estimated 70 to 80 per cent of digital-asset volume. Our project asks a narrower question: given the moving-average building blocks defined in the project specification, can a nature-inspired optimiser find parameter settings that yield a profitable Bitcoin trading bot — and if so, do the optimisers differ from each other in any way that matters?

**Y**:
> We continue from our Part 1 literature review, which compared Particle Swarm Optimization, or PSO, from 1995, with Harris Hawks Optimization, or HHO, from 2019. Those two algorithms anchor two ends of a swarm-intelligence design arc: PSO is one velocity update rule with a single attractor; HHO uses six update rules gated by an escape-energy variable. We carry both into Part 2, add Random Search as the specification's single-state baseline, and add Grey Wolf Optimizer as a third population-based algorithm — for reasons we will come back to.

---

## Segment 2 — Algorithms examined in Part 1 (1:30 – 4:30, ≈ 400 w)

**[SLIDE: part1_arc]**

**Q**:
> Particle Swarm Optimization, by Kennedy and Eberhart in 1995, was a deliberate reaction against Genetic Algorithms. Genetic Algorithms threw away weak individuals through competitive selection; gradient methods used a single solution that got trapped in local basins. PSO held both: every particle persists, but the swarm pulls each one toward two attractors — its own personal best and the swarm's global best. The original 1995 paper used twenty particles and acceleration constants c1 and c2 both equal to two.

**[SLIDE: pso_velocity]**

**Q**:
> In 1998, Shi and Eberhart added the inertia-weight extension, which scales the previous velocity by a constant w. That extension is now the standard formulation, and we use it: w equals 0.7, c1 and c2 both equal 2.0.

**Y**:
> Harris Hawks Optimization, by Heidari and colleagues in 2019, is a deliberately structural response to a problem flagged in PSO and its descendants — premature convergence on multimodal landscapes. Their critique is that single-update-rule swarms contract once the global best stabilises. Once they contract, they cannot escape.

**[SLIDE: hho_energy_gate]**

**Y**:
> HHO replaces the single update rule with six. At each iteration every hawk draws an escape energy E equal to 2·E₀·(1 − t/T), where E₀ is uniformly distributed in negative one to one. When the absolute value of E is at least one, the hawk explores via one of two perch rules. When it is less than one, the hawk exploits via one of four rules gated jointly by the magnitude of E and a fresh escape chance r. Two of those four end with a Lévy-flight dive that is committed only on strict fitness improvement.

**[SLIDE: part1_comparison_table]**

**Y**:
> Our Part 1 conclusion was that the comparison between PSO and HHO is worth running because the two algorithms make genuinely different structural choices. The 1995 paper has one update rule applied uniformly. The 2019 paper has six update rules selected at run time by the state of the search. Whether that complexity pays off on a real problem is precisely what Deliverable 2 lets us test.

---

## Segment 3 — Bot design and hypothesis space (4:30 – 7:30, ≈ 400 w)

**[SLIDE: wma_kernels]** (Fig. 1 from report — SMA / LMA / EMA)

**Q**:
> Every bot is built from three weighted moving averages — Simple, Linear, and Exponential — applied to the closing price via one-dimensional convolution. The Simple Moving Average uses a flat kernel of equal weights. The Linear MA uses a triangular kernel that decays to zero. The Exponential MA uses a geometric decay with a smoothing factor alpha.

**Q**:
> These three filters give us a hierarchy of recency-bias. SMA is the slowest to react. EMA responds fastest. LMA sits between them. That hierarchy lets the optimiser blend them rather than us having to guess which to use.

**[SLIDE: b1_b2_diagram]**

**Y**:
> We designed two hypothesis spaces.

**Y**:
> Bot B1 is the simplest setup the specification supports: two Simple Moving Averages of different durations, and a buy or sell signal on every crossover. The parameter vector is just two integers, each between 2 and 300 days. B1 is our "is the optimisation worth doing at all" reference point.

**[SLIDE: eq7_compound]**

**Y**:
> Bot B2 implements equation 7 from the specification. The fast indicator is a weighted normalised sum of an SMA, an LMA, and an EMA, each with its own window. The slow indicator has the same structure. Together that gives a 14-dimensional vector: six weights, six windows, two alphas. Both blocks share the same bounds, so the optimiser is free to discover that the fast indicator should use shorter windows — we don't hard-code that.

**Q**:
> We deliberately stopped at 14 dimensions rather than extending to the 21-dimensional MACD-style variant the specification also describes. Two hypothesis spaces — one minimal, one mid-sized — are enough to expose the trade-off between expressiveness and search difficulty. Going to 21 dimensions would have given us more room for over-fitting without changing the qualitative conclusions.

---

## Segment 4 — Algorithm selection (7:30 – 10:30, ≈ 400 w)

**[SLIDE: algo_spectrum_table]**

**Q**:
> Four algorithms. The first two carry over from Part 1 — PSO and HHO. Random Search satisfies the specification's explicit invitation to compare against a single-state stochastic algorithm under a fixed evaluation budget. The fourth, Grey Wolf Optimizer, is the only addition that wasn't in our Part 1 synopses.

**[SLIDE: gwo_three_leaders]**

**Y**:
> Grey Wolf Optimizer, by Mirjalili and colleagues in 2014, ranks the population each iteration and labels the top three wolves alpha, beta, and delta. Every non-leader wolf computes three candidate positions — one per leader — and moves to their average. There's no velocity memory. There's no Lévy flight. There's no probabilistic mode switching. The only annealing signal is a linearly decaying coefficient a that goes from 2 to 0.

**[SLIDE: camacho_villalon_paper]**

**Y**:
> We added GWO for a specific reason. A 2023 peer-reviewed critique by Camacho-Villalon, Dorigo, and Stützle argued that GWO can be algebraically reduced to an inertia-weight PSO variant — meaning, in their view, its biological framing is misleading and its updates are not genuinely new. Dorigo is the author of Ant Colony Optimization, which gives the critique unusual weight. Their claim is theoretical. Our experiment lets us put it to an empirical test.

**Q**:
> So our four algorithms span a structural spectrum: no attractor, one attractor, three attractors, and one attractor with multi-mode gating. That spectrum is what we will compare under exactly five thousand fitness evaluations per run.

---

## Segment 5 — Algorithm walkthrough (10:30 – 14:30, ≈ 540 w)

**[SLIDE: rs_pseudocode]**

**Q**:
> Random Search has no inner logic to speak of. Every step draws an independent uniform sample from the parameter box and evaluates it. No memory, no exploitation, no neighbourhood. The running maximum is tracked by the fairness framework, not by the algorithm itself. Its role is the reference line — the swarm algorithms must beat Random Search to justify their inductive bias.

**[SLIDE: pso_pseudocode]**

**Q**:
> PSO maintains thirty particles, each with a position and a velocity. At every step the velocity is updated using three terms: an inertia term that preserves momentum, a cognitive term pulling the particle toward its own best position so far, and a social term pulling it toward the swarm's global best. Positions are clipped to the bounds box.

**[SLIDE: gwo_pseudocode]**

**Y**:
> GWO ranks the population each iteration. For each non-leader wolf, three candidate positions are computed — one each from alpha, beta, and delta — using two random factors A and C. The wolf moves to the average of those three candidates. The annealing factor a decays linearly from two to zero over the iteration horizon, which gradually tightens the exploitation pressure.

**[SLIDE: hho_pseudocode]**

**Y**:
> HHO is the most structurally complex. Every hawk draws an escape energy E. When the magnitude of E is at least one, the hawk explores by perching relative to a random family member or to the swarm mean. When the magnitude of E is less than one, the hawk exploits, choosing between four behaviours: soft besiege, hard besiege, soft besiege with rapid dives, hard besiege with rapid dives. The "dive" modes generate two candidate positions Y and Z, with Z being Y plus a heavy-tailed Lévy step. Both are evaluated and committed only on strict improvement; otherwise the hawk stays put.

**[SLIDE: rules_of_engagement]**

**Q**:
> All four algorithms are hand-written. We did not use scipy.optimize, mealpy, pyswarm, or any other general optimisation library. The specification's Rules of Engagement allow adapting code provided in conjunction with the original research papers, and we acknowledge those sources here: Kennedy and Eberhart 1995, Shi and Eberhart 1998, Mirjalili and colleagues 2014, and Heidari and colleagues 2019.

---

## Segment 6 — Evaluation regime (14:30 – 16:30, ≈ 270 w)

**[SLIDE: objective_framework]**

**Y**:
> The Project specification asks us to compare algorithms on a fixed number of fitness evaluations, not on a fixed number of generations. We enforce that requirement at the framework level. Every algorithm — Random Search, PSO, GWO, and HHO — receives the fitness function only through a counted wrapper. That wrapper records every call, tracks the running maximum, and raises a BudgetExhausted exception on the five-thousand-and-first invocation. No algorithm can spend more or fewer evaluations than its peers, regardless of how it apportions generations or how many candidates it considers per iteration.

**[SLIDE: experiment_matrix]**

**Q**:
> The matrix is four algorithms by two bot configurations by five random seeds — forty runs total, each consuming five thousand fitness evaluations. Two hundred thousand back-tests on an 1860-day price series. On a single laptop core, that completes in roughly ninety seconds.

**[SLIDE: btc_split]** (Fig. 2 — train/test split)

**Q**:
> Per the specification, we optimise on data prior to 2020 and hold out the data from 2020 onwards for the final test. That gives us 1860 training days from late 2014 to the end of 2019, and 791 test days through early 2022. The training period is dominated by a multi-year bull market; the test period contains the 2020 COVID crash, the dual peaks of 2021, and the early 2022 retracement.

---

## Segment 7 — Training results (16:30 – 19:30, ≈ 400 w)

**[SLIDE: boxplot]** (Fig. 3)

**Q**:
> Across forty training runs the fitness spans 41 802 to 77 897 US dollars, starting from a thousand. Every optimised bot beats the closed-form buy-and-hold baseline of 17 925 dollars by a factor of 2.3 to 4.4 on the training split. So far the picture is positive.

**[SLIDE: stats_table]**

**Y**:
> Three patterns deserve comment.

**Y**:
> First — and this is the headline empirical finding — GWO and PSO are statistically indistinguishable on B1. Identical mean, standard deviation, minimum, and maximum. Mann-Whitney U two-sided p-value: 1.0. We cannot detect any difference between them. This is exactly the prediction of Camacho-Villalon, Dorigo, and Stützle. On a two-dimensional landscape with a wide basin, both algorithms walk the same trajectory toward the same attractor.

**[SLIDE: convergence_curves]** (Fig. 4)

**Y**:
> Second, on the 14-dimensional B2 space GWO pulls ahead. Significantly better than Random Search and HHO with p-values of 0.009 each. The mean is higher than PSO's, and the standard deviation is half. Averaging three leader-candidates damps the cognitive-plus-social attractor pull that gives PSO its high-variance "jackpot or nothing" behaviour. GWO is the most consistent optimiser of the four.

**Q**:
> Third, HHO has the lowest mean on both bots, with the worst-case B1 run dropping to 41 802 dollars — below Random Search's minimum. The convergence trace shows why: HHO keeps the swarm broadly exploring through the first two thousand evaluations, which leaves less budget for exploitation than the others.

---

## Segment 8 — Generalisation (19:30 – 22:00, ≈ 340 w)

**[SLIDE: train_test_scatter]** (Fig. 5)

**Q**:
> The held-out test split tells a less flattering story. The buy-and-hold baseline on the test period is 5 660 dollars. Every single one of our forty bots underperforms this baseline. The best run is HHO on B1, seed 1, at 3 623 dollars — still 36 per cent below buy-and-hold. The worst is PSO on B2, seed 0, at 537 dollars.

**[SLIDE: best_bot_trades]** (Fig. 7)

**Q**:
> The bot that converted a thousand dollars to nearly 78 thousand on training — PSO on B2, seed 4 — emits exactly one buy in late 2021 and one sell in early 2022 on the test split, ending at 992 dollars. The training-period strategy that catches multi-year up-trends has no signal value during the 2020 COVID crash, the 2021 dual peaks, or the 2022 retracement.

**[SLIDE: generalisation_table]**

**Y**:
> The training champions are the test losers. GWO and PSO have the two best training means on B2 and the two worst test means. HHO has the worst training means on both bots and the best test means on both. The unproductive late-run re-exploration that we flagged in Part 1 as a weakness of HHO behaves as implicit regularisation on a non-stationary financial landscape. The "weakness" is a feature here.

**Y**:
> This is the project specification's caveat realised in numbers — and we quote: "success on past sequences of data does not guarantee a strategy will be successful on future sequences."

---

## Segment 9 — Behavioural analysis (22:00 – 23:30, ≈ 200 w)

**[SLIDE: b2_weight_shares]** (Fig. 8)

**Y**:
> The specification poses an explicit question for the 14-dimensional bots: do the optimisers consistently favour one of the three filters, or continue to draw from all three?

**Y**:
> The answer is consistent across all four algorithms. Every optimised bot uses all three filters. The Herfindahl-Hirschman concentration index ranges from 0.37 — almost perfectly uniform — to 0.52, well below single-filter dominance. The fast indicator favours the recency-biased filters: SMA gets only 16 to 24 per cent of the fast-band weight, while LMA and EMA together take 60 to 84 per cent. The optimisers re-discovered the conventional wisdom that fast indicators should weight recent samples more heavily.

**Y**:
> GWO is the most decisive of the four — in four of its five seeds, SMA wins the slow band outright and EMA's share collapses to roughly ten per cent. That decisiveness matches GWO's lower run-to-run variance reported earlier.

---

## Segment 10 — Conclusions (23:30 – 24:30, ≈ 150 w)

**[SLIDE: takeaways]**

**Q**:
> Four take-aways.

**Q**:
> One — engineering fairness is non-trivial. A counted-objective framework was the technical lever that made every comparison apples-to-apples.

**Y**:
> Two — the Camacho-Villalon claim survives. GWO and PSO are statistically indistinguishable on both bots, supporting the algebraic argument that GWO reduces to an inertia-weight PSO variant.

**Q**:
> Three — higher dimensionality amplifies the algorithm gap. On 2-D all four clustered at the same plateau; on 14-D the gap opened, and HHO under-performed.

**Y**:
> Four — over-fitting is severe, and exploration acts as implicit regularisation. The most concentrated training search produced the worst out-of-sample performance. Algorithm choice changes how you over-fit, not whether you do.

---

## Segment 11 — Closing (24:30 – 25:00, ≈ 70 w)

**[SLIDE: links_qrcode]**

**Both**:
> Code, the notebook, the report, and all 30 per-run traces are in our repository, with a README that reproduces the experiment from scratch in about two minutes. The narration in this video was assisted by text-to-speech; all data, code, and analysis were produced by Team 20.

**Both**:
> Thank you.

---

## Production notes (for the team)

1. **TTS voices** — recommend ElevenLabs "Daniel" (UK male) for Q and "Sarah" (UK female) for Y, or any two well-matched voices in your TTS tool. Keep the same two voices for the full deck; do not mix per-segment.

2. **Pacing checks** — record one test segment first. If 135 wpm sounds rushed, drop to 125 wpm and target ≈ 23:30 by trimming the longest paragraphs (segments 2, 5, and 7 are the densest).

3. **Slide cues** — every `[SLIDE: name]` marks a slide transition. Aim for ~30 slides total; 1 slide per ~50 s on average.

4. **Figure file paths** — the actual figure files live in `results/figures/0X_*.png`. Drag them into your slides verbatim — they are the same images that appear in the report.

5. **Required closing element** — the AI-assistance disclosure in segment 11 is non-optional. CITS courses expect transparency about AI tooling.

6. **Time budget alarm** — final cut must be ≤ 25:00 per PDF §4. Aim for 24:00-24:30 in case of last-minute edits.

7. **Submission link** — upload to YouTube (Unlisted) or Google Drive; set "Anyone with the link can view"; paste the URL into the report's title-page metadata block.
