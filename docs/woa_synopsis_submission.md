# Synopsis: Whale Optimization Algorithm (WOA)

> **Algorithm**: Whale Optimization Algorithm (WOA)
> **Authors**: Seyedali Mirjalili & Andrew Lewis
> **Year**: 2016
> **Venue**: *Advances in Engineering Software*, Vol. 95, pp. 51–67. DOI: 10.1016/j.advengsoft.2016.01.008

---

## 1. Problem Being Solved

By 2016, hundreds of meta-heuristic optimizers existed, yet persistent challenges remained: premature convergence to local optima, poor exploration-exploitation balance, and sensitivity to algorithm-specific parameters. Mirjalili and Lewis sought an algorithm that would naturally integrate broad exploration in early iterations with fine-grained exploitation near the optimum — without manual phase switching. Their inspiration was the bubble-net hunting strategy of humpback whales, a behavior not previously modeled in optimization literature, offering a novel and biologically distinct alternative to bird-flock (PSO) or wolf-hierarchy (GWO) metaphors.

---

## 2. Previous Failures

PSO suffered from premature convergence on multimodal problems — particles cluster too quickly around a local best, and the velocity update provides no explicit mechanism for encircling and attacking a moving optimum. Physics-based algorithms (e.g., GSA) required pairwise force calculations that increased per-iteration cost and lacked adaptive behavioral switching. Evolutionary algorithms (GA, DE) depended on genetic operators (crossover, mutation, selection) that added complexity and whose "natural evolution" metaphor had been exhaustively explored, offering diminishing returns in fresh algorithmic insight.

---

## 3. New Idea + Core Equation

WOA models three phases of humpback whale hunting. In the **encircling phase** (exploitation), whales converge toward the best-known solution. In the **bubble-net attack phase** (exploitation), a whale swims along a logarithmic spiral toward prey. In the **search phase** (exploration), whales move toward a randomly chosen agent when `|A| >= 1`. A single linearly decreasing parameter `a` (from 2 to 0) drives the adaptive transition between exploration and exploitation without manual tuning.

**Spiral update (core equation):**
```
X(t+1) = D' * exp(b*l) * cos(2*pi*l) + X*(t)
```
Where `D'` is the distance between the current whale and the best solution `X*`, `b` defines the logarithmic spiral shape, and `l` is a random number in [-1, 1]. The algorithm randomly selects between shrinking encirclement and spiral updating with 50% probability each iteration.

---

## 4. How Demonstrated

WOA was benchmarked on **29 mathematical test functions** (F1–F7 unimodal, F8–F23 multimodal, F24–F29 fixed-dimension) and **6 structural engineering design problems** (welded beam, pressure vessel, tension/compression spring, and others). Baselines included PSO, GSA, DE, FEP, and CMA-ES. Results were reported as mean and standard deviation over **30 independent runs**, and convergence curves were provided. Source code was made publicly available.

---

## 5. Results

| Benchmark | WOA Performance | Best Baseline |
| :--- | :--- | :--- |
| Unimodal F1–F7 | Best or second-best on most functions | PSO / CMA-ES |
| Multimodal F8–F23 | Best or second-best on majority | DE / CMA-ES |
| Welded beam design | Avg. 1.7320 (9,900 evals) | PSO: 1.7422 (13,770 evals) |

WOA outperformed PSO and GSA on the welded beam problem in both solution quality and computational cost, and remained competitive with CMA-ES across the mathematical benchmark suite.

---

## 6. Assessment and Part 2 Relevance

**Strengths:** The empirical foundation is robust — 29 benchmark functions plus 6 engineering problems, 30 independent runs with mean/std reporting, and public source code. WOA's adaptive `a` parameter elegantly automates the exploration-to-exploitation transition. Structural engineering results provide a credible bridge from synthetic benchmarks to practical applications.

**Weaknesses:** WOA can still exhibit premature convergence on very high-dimensional or complex landscapes. Convergence precision degrades on extremely multimodal problems in later iterations. The original formulation addresses only single-objective continuous optimization; binary and multi-objective extensions require separate variants. As with most meta-heuristic papers, benchmark functions are standard test sets, so generalization to truly novel problem types is not guaranteed.

**Trading-bot relevance:** WOA is a strong candidate for optimizing trading-bot parameters (WMA weights, window sizes, trigger thresholds). Its adaptive balance of exploration and exploitation suits the multimodal, moderately high-dimensional parameter space typical of such bots. Because the original WOA paper explicitly benchmarks against PSO, using both algorithms in Part 2 provides a natural, literature-backed experimental comparison. Replication confidence is **very high** — the paper provides full pseudocode, equations, and publicly available MATLAB/Python source.

---

## References

[1] S. Mirjalili and A. Lewis, "The Whale Optimization Algorithm," *Advances in Engineering Software*, vol. 95, pp. 51–67, 2016. DOI: 10.1016/j.advengsoft.2016.01.008

[2] S. Mirjalili, S. M. Mirjalili, and A. Lewis, "Grey Wolf Optimizer," *Advances in Engineering Software*, vol. 69, pp. 46–61, 2014.

[3] J. Kennedy and R. C. Eberhart, "Particle swarm optimization," in *Proc. ICNN'95 — Int. Conf. Neural Networks*, Perth, Australia, 1995, vol. IV, pp. 1942–1948, IEEE.

[4] E. Rashedi, H. Nezamabadi-Pour, and S. Saryazdi, "GSA: A gravitational search algorithm," *Information Sciences*, vol. 179, no. 13, pp. 2232–2248, 2009.
