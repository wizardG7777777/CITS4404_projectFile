# Synopsis: Particle Swarm Optimization (PSO)

> **Algorithm**: Particle Swarm Optimization (PSO)
> **Authors**: James Kennedy & Russell C. Eberhart
> **Year**: 1995
> **Venue**: *Proc. ICNN'95 — IEEE Int. Conf. on Neural Networks*, Perth, Australia, Vol. IV, pp. 1942–1948.

---

## 1. Problem Being Solved

Optimization in the 1990s was dominated by two extremes: evolutionary algorithms (e.g., Genetic Algorithms) that were powerful but structurally complex, and gradient-based methods (e.g., backpropagation) that were fast but required differentiable objectives and were prone to local optima. Kennedy and Eberhart sought a third path — an algorithm that was computationally inexpensive, structurally simple, and effective on continuous nonlinear functions without gradient information. Their solution drew from the social behavior of bird flocks and fish schools, where collective intelligence emerges from simple individual rules.

---

## 2. Previous Failures

Genetic Algorithms required multiple operators (selection, crossover, mutation), encoding schemes, and careful parameter tuning. Their competitive selection model discarded information from less-fit individuals. Gradient-based methods failed on non-differentiable or discontinuous surfaces and maintained only a single candidate solution, making them fragile on multimodal landscapes. Neither approach modeled the cooperative information-sharing observed in natural swarms, where individuals benefit from the group's collective memory of promising regions.

---

## 3. New Idea + Core Equation

PSO represents each candidate solution as a "particle" moving through the search space. Every particle adjusts its velocity based on two memories: its own best-known position (cognitive component) and the swarm's global best-known position (social component). The algorithm requires only primitive arithmetic and can be implemented in fewer than twenty lines of code.

**Velocity update (core equation):**
```
v_id = v_id + c1*rand()*(p_id - x_id) + c2*Rand()*(p_gd - x_id)
x_id = x_id + v_id
```
Where `x_id` is current position, `v_id` is velocity, `p_id` is the particle's personal best, `p_gd` is the swarm's global best, `c1`/`c2` are acceleration constants, and `rand()`/`Rand()` are independent uniform random draws in [0, 1]. There are no selection, crossover, or mutation operators — the swarm evolves solely through velocity updates.

---

## 4. How Demonstrated

The authors tested PSO on two tasks: (1) **Schaffer's f6 function**, a highly discontinuous multimodal benchmark drawn from the GA literature (Davis, 1991); and (2) **EEG spike classification**, a neural network training task. Baselines were an elementary Genetic Algorithm (f6) and backpropagation (EEG). No large-scale benchmark suite (e.g., CEC functions) was used; the 1995 paper is a proof-of-concept study.

---

## 5. Results

| Benchmark | PSO Result | Baseline | Outcome |
| :--- | :--- | :--- | :--- |
| Schaffer's f6 | Global optimum every run | Davis GA | Matched GA in function evaluations |
| EEG Classification | **92%** test accuracy | Backprop (89%) | Outperformed gradient descent |

PSO found the global optimum on every run of f6, demonstrating robustness. On EEG classification it also generalized better from training to test set than backpropagation.

---

## 6. Assessment and Part 2 Relevance

**Strengths:** The 1995 claims have held up over three decades. PSO is genuinely simple, fast, and gradient-free. The explicit equations make replication trivial, and the algorithm has spawned hundreds of validated variants (inertia-weight PSO, constriction-factor PSO, fully informed PSO).

**Weaknesses:** The original evidence base is thin — one benchmark function and one dataset. The 1995 formulation has no mechanism for preventing premature convergence; particles can cluster around a local best on high-dimensional or strongly multimodal surfaces. No statistical hypothesis testing was performed.

**Trading-bot relevance:** PSO is a strong candidate for optimizing trading-bot parameters (WMA window sizes, trigger thresholds, weighting coefficients). Its simplicity and low computational cost suit iterative strategy evaluation. For problems with 7–21 dimensions, a modern variant with an inertia weight (Shi & Eberhart, 1998) is preferable to the 1995 original. Replication confidence is **high** — equations are explicit and the algorithm is universally implemented.

---

## References

[1] J. Kennedy and R. C. Eberhart, "Particle swarm optimization," in *Proc. ICNN'95 — Int. Conf. Neural Networks*, Perth, Australia, 1995, vol. IV, pp. 1942–1948, IEEE.

[2] R. C. Eberhart and J. Kennedy, "A new optimizer using particle swarm theory," in *Proc. 6th Int. Symp. Micro Machine and Human Science*, Nagoya, Japan, 1995, pp. 39–43, IEEE.

[3] Y. Shi and R. C. Eberhart, "A modified particle swarm optimizer," in *Proc. IEEE Int. Conf. Evolutionary Computation*, 1998, pp. 69–73.

[4] L. Davis, Ed., *Handbook of Genetic Algorithms*. New York: Van Nostrand Reinhold, 1991.
