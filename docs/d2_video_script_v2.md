# Deliverable 2 — Video Script v2 (PPT-aligned, ≤25 min)

**Team 20**: Qiurong Chen (24558583) · Yanchen Yu (24256987)

**Revision note (v2 vs v1)**: This script is rewritten to match the 21-slide
`CITS4404_Team20_Presentation.pptx` exactly. Four algorithm animations from
`results/animations/` are kept as full-screen B-roll between PPT Slide 9 and
Slide 10. Segment §6 is compressed (270 → 135 words) by dropping the
counted-objective framework / BudgetExhausted technical detail that PPT
Slide 11 doesn't visualise — that detail stays in the report §3. Segments
§5b, §7, §10 are trimmed slightly. All numerical claims are identical to
v1, the PPT, and `d2_report_draft.md`. Total narration ≈ 2 559 words, ≈
19–21 min depending on TTS pace — well under the 25:00 cap.

Speaker tags:

- **Q** = Qiurong (D1 PSO author; reads PSO / Random Search / training-results sections)
- **Y** = Yanchen (D1 HHO author; reads HHO / GWO / behaviour / generalisation sections)
- **Both** = joint reading (title, closing)

Pacing target: 115–120 wpm (slightly slow for technical narration).
Total narration ≈ 2 559 words → ≈ 21:20 at 120 wpm, ≈ 18:57 at 135 wpm.
Either pace lands comfortably under the 25:00 hard cap.

Visual cues:
- **`[PPT N]`** = advance to PowerPoint slide N
- **`[ANIMATION: file.mp4 — full screen B-roll]`** = cut from PPT to the
  animation video, full screen, while narration continues

---

## Segment 0 — Title (0:00 – 0:20, 45 w)

**[PPT 1]**

**Both**:
> Good afternoon. We are Team 20 — Qiurong Chen and Yanchen Yu. This presentation reports our work for CITS4404 Deliverable 2: optimising a Bitcoin trading bot with four nature-inspired and stochastic algorithms.

---

## Segment 1 — Introduction (0:20 – 1:22, 140 w)

**[PPT 2]**

**Q**:
> Algorithmic trading already drives an estimated 70 to 80 per cent of digital-asset volume. Our project asks a narrower question: given the moving-average building blocks defined in the project specification, can a nature-inspired optimiser find parameter settings that yield a profitable Bitcoin trading bot — and if so, do the optimisers differ from each other in any way that matters?

**Y**:
> Part 1 of this project compared Particle Swarm Optimization, or PSO, from 1995, with Harris Hawks Optimization, or HHO, from 2019 — two ends of a swarm-intelligence design arc. We carry both into Part 2, add Random Search as the specification's single-state baseline, and add Grey Wolf Optimizer as a third population-based algorithm — for reasons we will come back to.

---

## Segment 2 — Part 1 algorithms (1:22 – 4:22, 400 w)

### §2a — PSO design motivation & velocity update (1:22 – 2:20, 130 w)

**[PPT 3]**

**Q**:
> Particle Swarm Optimization, by Kennedy and Eberhart in 1995, was a deliberate reaction against Genetic Algorithms. Genetic Algorithms discarded weak individuals — losing knowledge through competitive selection. Gradient methods used a single solution that got trapped in local basins. PSO kept all particles, but pulled each one toward two attractors — its own personal best and the swarm's global best.

**Q**:
> In 1998, Shi and Eberhart added the inertia-weight extension, which scales the previous velocity by a constant w. That extension is the standard formulation, and we use it: w equals 0.7, c-one and c-two both equal 2.0, with a swarm of 30 particles.

### §2b — HHO energy gate & six update modes (2:20 – 3:21, 140 w)

**[PPT 4]**

**Y**:
> Harris Hawks Optimization, by Heidari and colleagues in 2019, is a deliberately structural response to the problem flagged in PSO and its descendants: single-update-rule swarms contract once the global best stabilises, and once they contract they cannot escape local optima.

**Y**:
> HHO replaces the single update rule with six. At each iteration every hawk draws an escape energy E equal to 2 times E-naught times one minus t over T, where E-naught is uniform in negative one to one. When the magnitude of E is at least one, the hawk explores via one of two perch rules. When it is less than one, the hawk exploits via one of four rules — including two that end with a heavy-tailed Lévy-flight dive, committed only on strict improvement.

### §2c — PSO vs HHO structural comparison (3:21 – 4:22, 130 w)

**[PPT 5]**

**Y**:
> This table summarises the structural difference. PSO uses one velocity update rule, one attractor, velocity as memory, and no heavy-tailed jumps. HHO uses six energy-gated modes, no velocity memory, and Lévy-flight dives in the exploitation phase. PSO has fixed inertia weight; HHO has linearly decaying escape energy.

**Y**:
> Our Part 1 prediction was that PSO would converge faster but might overfit, while HHO would explore more broadly but converge more slowly. The comparison is worth running empirically because the two algorithms make genuinely different structural choices — and Deliverable 2 lets us put those choices to the test.

---

## Segment 3 — Bot design (4:22 – 7:22, 400 w)

### §3a — WMA building blocks (4:22 – 5:42, 180 w)

**[PPT 6]**

**Q**:
> Every bot is built from three weighted moving averages — Simple, Linear, and Exponential — applied to the closing price via one-dimensional convolution, exactly the equation shown on screen.

**Q**:
> The Simple Moving Average uses a flat kernel — equal weights across the window. It is the slowest to react and the most smoothing. The Linear MA uses a triangular kernel that decays linearly to zero — medium responsiveness. The Exponential MA uses a geometric decay with a smoothing factor alpha — the fastest response to recent prices.

**Q**:
> Together the three filters give us a hierarchy of recency-bias. That hierarchy lets the optimiser blend them rather than us having to guess which one to use. We use flip-padding to handle the edge case at time zero, so the warm-up region produces no spurious signals.

### §3b — Two hypothesis spaces B1 and B2 (5:42 – 7:22, 220 w)

**[PPT 7]**

**Y**:
> We designed two hypothesis spaces.

**Y**:
> Bot B1 is the simplest setup the specification supports: two Simple Moving Averages of different durations, and a buy or sell signal on every crossover. The parameter vector is just two integers, each between 2 and 300 days. B1 is our "is the optimisation worth doing at all" reference point.

**Y**:
> Bot B2 implements equation 7 from the specification. The fast indicator is a weighted normalised sum of an SMA, an LMA, and an EMA, each with its own window. The slow indicator has the same structure. Together that gives a 14-dimensional vector: six weights, six windows, two alphas. Both blocks share the same bounds — the optimiser is free to discover that the fast indicator should use shorter windows than the slow indicator, rather than us hard-coding it.

**Q**:
> We stopped at 14 dimensions rather than extending to the 21-dimensional MACD-style variant the specification also describes. Two hypothesis spaces — one minimal, one mid-sized — are enough to expose the trade-off between expressiveness and search difficulty.

---

## Segment 4 — Algorithm selection (7:22 – 10:22, 400 w)

### §4a — Four-algorithm structural spectrum (7:22 – 8:30, 150 w)

**[PPT 8]**

**Q**:
> Four algorithms, chosen to span a structural spectrum. Random Search has no attractor — it just samples uniformly from the box. PSO has one attractor, the global best, with velocity as memory. GWO has three attractors — the top-three ranked wolves, alpha, beta, and delta — and moves the population to their averaged candidate. HHO has one attractor, the rabbit, but six energy-gated update modes including Lévy-flight dives.

**Q**:
> The first two carry over from Part 1. Random Search satisfies the specification's explicit invitation to compare against a single-state stochastic baseline. GWO is the only structural addition for D2. All four run under exactly 5 000 fitness evaluations per run — every comparison is apples-to-apples.

### §4b — Why add GWO? The Camacho-Villalon claim (8:30 – 10:22, 250 w)

**[PPT 9]**

**Y**:
> Grey Wolf Optimizer, by Mirjalili and colleagues in 2014, ranks the population each iteration and labels the top three wolves alpha, beta, and delta. Every non-leader wolf computes three candidate positions — one per leader — and moves to their average. There is no velocity memory, no Lévy flight, no probabilistic mode switching. The only annealing signal is a linearly decaying coefficient a that goes from two to zero.

**Y**:
> We added GWO for a specific reason. In 2023, Camacho-Villalon, Dorigo, and Stützle published a peer-reviewed critique in International Transactions in Operational Research, arguing that GWO can be algebraically reduced to an inertia-weight PSO variant — meaning its wolf-hierarchy biological framing is misleading and its updates are not genuinely new. Dorigo is the inventor of Ant Colony Optimization, which gives the critique unusual weight in the metaheuristics community. Their claim is theoretical. Our Deliverable 2 experiment lets us put it to an empirical test on a non-stationary financial landscape.

**Q**:
> So our four algorithms span the structural spectrum: no attractor, one attractor, three attractors, and one attractor with multi-mode gating. That spectrum is what we will compare under exactly 5 000 fitness evaluations per run.

---

## Segment 5 — Algorithm walkthrough with animations (10:22 – 15:22, ≈ 690 w)

Each sub-segment plays one of the four pre-rendered animations from
`results/animations/` while the narrator speaks over it. **Cut away from
PPT Slide 9 to full-screen animation video; cut back to PPT Slide 10 for
§5e.** Animations show the algorithms running on a deliberately simple
2-D toy fitness landscape so the search behaviour is visible; the actual
experiment uses the full 14-D BTC back-test.

---

### §5a — Random Search (10:22 – 10:52, 90 w)

**[ANIMATION: results/animations/rs.mp4 — full screen B-roll, ~30 s]**

**Q**:
> Random Search has no inner logic. Every step draws an independent uniform sample from the parameter box and evaluates it. Watch the red dots scatter across the landscape — there is no memory, no neighbourhood, no learning. The yellow star tracks the running maximum, jumping each time a fresh draw beats the previous best. Random Search exists as the reference line the swarm algorithms must beat to justify their inductive bias.

---

### §5b — PSO (10:52 – 11:50, 130 w — compressed from 175)

**[ANIMATION: results/animations/pso.mp4 — full screen B-roll, ~30 s, may loop]**

**Q**:
> PSO maintains thirty particles, each with a position and a velocity. The velocity update has three terms: inertia preserving momentum, a cognitive term pulling toward personal best, and a social term pulling toward global best.

**Q**:
> In the animation, white dots are the particles and the cyan star marks the global best. Notice how within five or six iterations every particle is pulled into a single basin — the cognitive-plus-social attractor is strong. Once converged, the swarm has no mechanism to escape if the basin is wrong. That single-attractor concentration directly explains the high variance PSO shows on the 14-D B2 problem in a moment.

---

### §5c — GWO (11:50 – 13:08, 175 w)

**[ANIMATION: results/animations/gwo.mp4 — full screen B-roll, ~30 s, may loop]**

**Y**:
> GWO ranks the population each iteration. The top three wolves — alpha in red, beta in orange, delta in yellow — become temporary attractors. Every non-leader wolf computes three candidate positions, one per leader, and moves to the average. The annealing factor a decays linearly from two to zero, gradually tightening exploitation.

**Y**:
> Visually, GWO converges differently from PSO. There is no single g-best to be pulled toward; instead the population follows a moving centroid of the top three. That averaging smooths the trajectory and suppresses jackpot-or-nothing behaviour — and it is exactly the property the Camacho-Villalon critique claims reduces algebraically to an inertia-weight PSO variant. We will see empirical evidence of that algebraic equivalence on the next slides.

---

### §5d — HHO (13:08 – 14:50, 230 w)

**[ANIMATION: results/animations/hho.mp4 — full screen B-roll, ~30 s, may loop]**

**Y**:
> HHO is the most structurally complex of the four. Every hawk draws an escape energy E equal to two times E-naught times one minus t over T, with E-naught uniform in negative one to one. When the magnitude of E is at least one, the hawk explores — see the blue dots leaving the attractor to wander the landscape. When the magnitude is less than one, the hawk exploits via one of four behaviours: soft besiege in green, hard besiege in red, and two dive variants in purple and orange.

**Y**:
> The dive modes generate two candidate positions Y and Z, with Z being Y perturbed by a heavy-tailed Lévy flight. Both are evaluated, and neither is committed unless it strictly improves on the current hawk — otherwise the hawk stays put. That strict greedy acceptance is the mechanism Part 1 flagged as both HHO's strength on smooth benchmarks and its weakness on noisy fitness surfaces. We will see this behaviour manifest twice in our experiments: HHO under-performs on training fitness, but it over-fits less than the other three on the test set.

---

### §5e — Compliance recap (14:50 – 15:22, 65 w)

**[PPT 10]** — cut back to PowerPoint deck.

**Q**:
> All four algorithms are hand-written, as shown in these condensed pseudocode blocks. We did not use scipy.optimize, mealpy, pyswarm, or any other general optimisation library. The Rules of Engagement in section three of the specification allow adapting code from research papers, and we acknowledge those sources in the references.

---

## Segment 6 — Experiment setup (15:22 – 16:34, 150 w — compressed from 270)

**[PPT 11]**

**Y**:
> Every algorithm runs under a strictly equal evaluation budget — exactly 5 000 fitness evaluations per run, enforced at the framework level rather than by trust. The matrix is four algorithms by two bot configurations by five random seeds — forty runs total, consuming 200 000 back-tests on an 1860-day price series. On a single laptop core, that completes in about ninety seconds.

**[PPT 12]**

**Q**:
> Per the specification, we optimise on data prior to 2020 and hold out 2020 onwards for the final test. That gives us 1 860 training days from late 2014 to the end of 2019, and 791 test days through early 2022. The training period is dominated by a multi-year bull market with eighteen-times price appreciation. The test period contains the 2020 COVID crash, the dual peaks of 2021, and the 2022 retracement.

---

## Segment 7 — Training results (16:34 – 19:18, 370 w — trimmed from 400)

### §7a — Training fitness boxplot (16:34 – 17:18, 100 w)

**[PPT 13]**

**Q**:
> Across forty training runs, fitness spans 41 802 to 77 897 US dollars, starting from a thousand. The closed-form buy-and-hold baseline on the training split is 17 925 dollars. Every optimised bot beats buy-and-hold by a factor of 2.3 to 4.4 on training. So far the picture is positive — the optimisers are clearly extracting signal from the price series during the 2014 to 2019 bull run.

### §7b — Training results table & key statistics (17:18 – 18:38, 180 w)

**[PPT 14]**

**Y**:
> Three patterns deserve comment.

**Y**:
> First — and this is the headline empirical finding — GWO and PSO are statistically indistinguishable on B1. Identical mean, standard deviation, minimum, and maximum. Mann-Whitney U two-sided p-value: 1.0. We cannot detect any difference between them. This is exactly the prediction of Camacho-Villalon, Dorigo, and Stützle.

**Y**:
> Second, on the 14-dimensional B2 space GWO pulls ahead. Significantly better than Random Search and HHO with p-values of 0.009 each. Mean higher than PSO's, standard deviation roughly half. GWO is the most consistent optimiser of the four.

**Y**:
> Third, HHO has the lowest mean on both bots, with the worst-case B1 run dropping below Random Search's minimum.

### §7c — Convergence curves (18:38 – 19:18, 90 w)

**[PPT 15]**

**Q**:
> The convergence trace shows why HHO under-performs. GWO in green tracks PSO in blue almost perfectly on B1, and edges ahead on B2 — empirical evidence of the algebraic equivalence Camacho-Villalon claimed. HHO keeps the swarm broadly exploring through the first two thousand evaluations, which leaves less budget for exploitation than the others. That extended exploration is what the Part 1 synopsis flagged as a potential weakness — and it costs HHO training fitness.

---

## Segment 8 — Generalisation (19:18 – 21:48, 340 w)

### §8a — All 40 bots underperform on test (19:18 – 20:18, 120 w)

**[PPT 16]**

**Q**:
> The held-out test split tells a less flattering story. The buy-and-hold baseline on the test period is 5 660 dollars — substantially less than on training, but positive, because BTC ended the test period at six times its 2020-01 level.

**Q**:
> Every single one of our forty bots underperforms this baseline. The best run is HHO on B1, seed 1, at 3 623 dollars — still 36 per cent below buy-and-hold. The worst is PSO on B2, seed 0, at 537 dollars. The optimisers have found patterns specific to the 2014 to 2019 bull run that do not transfer to the 2020 to 2022 regime.

### §8b — Training champion → test failure (20:18 – 21:18, 120 w)

**[PPT 17]**

**Q**:
> The clearest example is PSO on B2, seed 4 — the run that turned a thousand dollars into nearly 78 thousand on training. On the test split, the same parameter vector emits exactly one buy in late 2021 and one sell in early 2022, ending at 992 dollars. The training-period strategy that catches multi-year up-trends has no signal value during the 2020 COVID crash, the 2021 dual peaks, or the 2022 retracement. The training champion is a test loser.

### §8c — Generalisation table (21:18 – 21:48, 100 w)

**[PPT 18]**

**Y**:
> The pattern holds across the matrix. GWO and PSO have the two best training means on B2 and the two worst test means. HHO has the worst training means on both bots and the best test means on both. The unproductive late-run re-exploration we flagged in Part 1 as a weakness of HHO behaves as implicit regularisation on a non-stationary financial landscape. The Part 1 weakness is a Part 2 feature.

---

## Segment 9 — Behavioural analysis (21:48 – 23:18, 200 w)

**[PPT 19]**

**Y**:
> The specification poses an explicit question for the 14-dimensional bots: do the optimisers consistently favour one of the three filters, or continue to draw from all three?

**Y**:
> The answer is consistent across all four algorithms. Every optimised bot uses all three filters. The Herfindahl-Hirschman concentration index ranges from 0.37 — almost perfectly uniform — to 0.52, well below single-filter dominance. The fast indicator favours the recency-biased filters: SMA gets only 16 to 24 per cent of the fast-band weight, while LMA and EMA together take 60 to 84 per cent. The optimisers re-discovered the conventional wisdom that fast indicators should weight recent samples more heavily.

**Y**:
> The slow indicator prefers SMA, which takes 28 to 46 per cent of the weight. GWO is the most decisive of the four — in four of its five seeds, SMA wins the slow band outright and EMA's share collapses to roughly ten per cent. That decisiveness matches GWO's lower run-to-run variance reported earlier.

---

## Segment 10 — Conclusions (23:18 – 24:11, 120 w — compressed from 150)

**[PPT 20]**

**Q**:
> Four take-aways.

**Q**:
> One — engineering fairness is non-trivial. A counted-objective framework made every comparison apples-to-apples under exactly 5 000 evaluations.

**Y**:
> Two — the Camacho-Villalon claim survives. GWO and PSO are statistically indistinguishable on both bots, p equals 1.0 on B1 and 0.46 on B2 — empirical support for the algebraic argument.

**Q**:
> Three — higher dimensionality amplifies the gap. On 2-D all four algorithms clustered; on 14-D the gap opened and HHO under-performed.

**Y**:
> Four — over-fitting is severe, and exploration acts as implicit regularisation. The most concentrated training search produced the worst out-of-sample performance. Algorithm choice changes how you over-fit, not whether you do.

---

## Segment 11 — Closing (24:11 – 24:38, 70 w)

**[PPT 21]**

**Both**:
> Our submission contains the pre-executed notebook, the report, and this video. All forty per-run traces, all figures, and the full reproduction pipeline are in the repository. The narration in this video was assisted by text-to-speech; all data, code, and analysis were produced by Team 20.

**Both**:
> Thank you.

---

## Time budget check (actual word counts)

| Segment | Narration words | Time @ 135 wpm | Time @ 120 wpm |
|---|---:|---:|---:|
| §0 Title | 32 | 0:14 | 0:16 |
| §1 Introduction | 121 | 0:54 | 1:01 |
| §2 Part 1 algorithms (§2a + §2b + §2c) | 325 | 2:24 | 2:43 |
| §3 Bot design (§3a + §3b) | 303 | 2:15 | 2:32 |
| §4 Algorithm selection (§4a + §4b) | 307 | 2:16 | 2:34 |
| §5a Random Search animation | 71 | 0:32 | 0:36 |
| §5b PSO animation | 104 | 0:46 | 0:52 |
| §5c GWO animation | 118 | 0:52 | 0:59 |
| §5d HHO animation | 182 | 1:21 | 1:31 |
| §5e Compliance recap | 49 | 0:22 | 0:25 |
| §6 Experiment setup | 135 | 1:00 | 1:08 |
| §7 Training results (§7a + §7b + §7c) | 249 | 1:51 | 2:05 |
| §8 Generalisation (§8a + §8b + §8c) | 254 | 1:53 | 2:07 |
| §9 Behavioural HHI | 159 | 1:11 | 1:20 |
| §10 Conclusions | 103 | 0:46 | 0:52 |
| §11 Closing + AI disclosure | 47 | 0:21 | 0:24 |
| **Total** | **2 559** | **≈ 18:57** | **≈ 21:20** |

**The v2 script is comfortably under the 25:00 hard cap with ≈ 4–6 minutes of headroom.**

This means you can — and probably should — slow the TTS pacing from
135 wpm down to 115–120 wpm. Clear, slightly slow narration is easier
to follow when the slides contain dense numerical content (training
tables, p-values, HHI numbers). At 120 wpm the final video lands
around 21:20, leaving ~3.5 min for inter-slide transitions, fades,
and animation lead-ins/outs. At 115 wpm it lands around 22:15.

If the recorded pace ends up faster than expected, add 1–2 seconds
of silence between segments rather than re-recording.

---

## Production notes (for the team)

1. **TTS voices** — recommend ElevenLabs "Daniel" (UK male) for Q and
   "Sarah" (UK female) for Y, or any two well-matched voices. Keep the
   same two voices for the full deck.

2. **Pacing checks** — record one test segment first. If 135 wpm sounds
   rushed, the densest paragraphs (§4b Camacho-Villalon, §5d HHO,
   §7b results table) are the candidates to trim further. Aim for
   24:00-24:30 in the final cut.

3. **Slide transitions** — every `[PPT N]` cue marks a slide advance.
   The deck has 21 slides plus 4 animation B-rolls = 25 visual units,
   averaging ~60 s on screen.

4. **Animation B-roll editing** — in the video editor, place the four
   mp4 files from `results/animations/` on a layer above the slide
   capture. When the cue fires, fade or cut to the animation full-screen
   for the duration of the §5a–d narration, then cut back to PPT Slide 10
   when §5e begins. Each animation is ~30 s; if the narration runs longer
   than the animation, loop the mp4.

5. **AI assistance disclosure** — segment 11 includes the TTS disclosure.
   PPT Slide 21 also carries the same line in small text — both audio
   and visual disclosure satisfy CITS transparency expectations.

6. **Time budget** — final cut must be ≤ 25:00 per PDF §4. Current
   narration is 2 559 words → ~19 min at fast TTS pace (135 wpm) or
   ~21 min at slower technical pace (120 wpm). Both land safely under
   the cap with ≥ 4 min headroom; choose the slower pace.

7. **Submission link** — upload to YouTube (Unlisted) or Google Drive;
   set "Anyone with the link can view"; paste the URL into the report's
   title-page metadata block and into PPT Slide 21's "Video" field.
