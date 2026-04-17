# Synopsis Draft: Particle Swarm Optimization (PSO)

> **Algorithm**: Particle Swarm Optimization (PSO)  
> **Original Authors**: James Kennedy & Russell C. Eberhart  
> **Year**: 1995  
> **Venue**: Proceedings of the IEEE International Conference on Neural Networks (ICNN'95), Perth, Australia, Vol. IV, pp. 1942–1948.  
> **Precursor Paper**: Eberhart, R.C. & Kennedy, J. (1995). "A new optimizer using particle swarm theory." Proc. 6th Int. Symposium on Micro Machine and Human Science, Nagoya, Japan, pp. 39–43.  

---

## 1. What problem with existing algorithms is PSO attempting to solve?

PSO was introduced to fill a conceptual and practical gap between two extremes of computational optimization:

- **Evolutionary Algorithms (e.g., Genetic Algorithms)**: Operate on an evolutionary timescale (eons), requiring complex operators such as selection, crossover, and mutation.
- **Neural Networks / Gradient Descent**: Operate on a millisecond timescale, but are prone to getting stuck in local optima and require differentiable objective functions.

Kennedy and Eberhart sought an optimization method that operates on the **timescale of ordinary experience** — social interaction. They aimed to create an algorithm that was:
- **Computationally inexpensive** (minimal memory, few primitive mathematical operators)
- **Structurally simple** (implementable in a few lines of code)
- **Biologically/socially plausible** (based on swarm behavior like bird flocking and fish schooling)
- **Effective on continuous nonlinear functions** without requiring gradient information

In essence, PSO attempts to solve the problem of **overly complex, slow, or gradient-dependent optimizers** by leveraging social information sharing among a population of simple agents.

---

## 2. Why, or in what respect, have previous attempts failed?

**Genetic Algorithms (GAs)** had several perceived deficiencies that motivated PSO:
- **Complexity**: GAs require multiple genetic operators (selection, crossover, mutation), parameter tuning, and encoding schemes.
- **Speed**: The evolutionary metaphor implies slow adaptation over generations.
- **Competition vs. Cooperation**: GAs rely on competitive selection and the "survival of the fittest," discarding potentially useful information from less-fit individuals.

**Gradient-based methods** (e.g., backpropagation) failed in different respects:
- They require the objective function to be differentiable.
- They are highly susceptible to local optima, especially on discontinuous or highly nonlinear surfaces.
- They do not maintain a population of candidate solutions, so they lack the robustness of population-based search.

Kennedy and Eberhart argued that **social sharing of information** — rather than genetic competition — could be a more efficient and elegant route to optimization.

---

## 3. What is the new idea presented in this paper?

The core novelty of PSO is the concept of **optimizing nonlinear functions through particle swarm methodology**, where each candidate solution is a "particle" flying through the search space. The algorithm mimics the social behavior of bird flocking and fish schooling.

### The Original Update Equations (1995):

**Velocity update:**
```
v_id = v_id + c1 * rand() * (p_id - x_id) + c2 * Rand() * (p_gd - x_id)
```

**Position update:**
```
x_id = x_id + v_id
```

Where:
- `x_id`: Current position of particle *i* in dimension *d*
- `v_id`: Velocity of particle *i* in dimension *d*
- `p_id`: Personal best position found so far by particle *i* (cognitive component)
- `p_gd`: Global best position found so far by the entire swarm (social component)
- `c1, c2`: Positive acceleration constants
- `rand(), Rand()`: Random numbers uniformly distributed in [0, 1]

### Key Innovations:
1. **No evolutionary operators**: Unlike GAs, there is no selection, crossover, or mutation. The swarm evolves purely through velocity adjustments.
2. **Social intelligence**: Particles share the global best position directly, allowing the entire swarm to be attracted toward promising regions simultaneously.
3. **Memory**: Each particle remembers its own best experience (`p_id`) and the swarm's best experience (`p_gd`).
4. **Simplicity**: The algorithm requires only primitive arithmetic and can be implemented in a few lines of code.

---

## 4. How is the new approach demonstrated?

The authors demonstrated PSO through **implementation and benchmark testing** on two primary tasks:

### Task 1: Nonlinear Function Optimization
The main benchmark was **Schaffer's f6 function**, an extremely nonlinear, highly discontinuous function with many local optima — a standard genetic algorithm benchmark from Davis (1991).

**Result**: The particle swarm paradigm **found the global optimum in every run** and approximated the performance of elementary genetic algorithms in terms of the number of evaluations required.

### Task 2: Neural Network Training
PSO was applied to training a feedforward neural network for classifying **EEG (electroencephalogram) spike waveforms and false positives**.

**Result**:
- Backpropagation (gradient descent) achieved **89%** correct on the test data.
- PSO achieved **92%** correct on the test data.
- Additionally, the weights found by PSO generalized better from training set to test set.

### Methodological Rigor Assessment:
- The paper provides **enough detail to replicate** the basic algorithm (equations are explicit).
- However, the 1995 paper is more of a **proof-of-concept** than an exhaustive empirical study. It uses only one GA benchmark function and one neural network dataset.
- There is no formal statistical hypothesis testing or large-scale benchmark suite (e.g., CEC functions), which came in later years.

---

## 5. What are the results or outcomes and how are they validated?

### Results from the Original Paper:

| Benchmark | PSO Result | Baseline | Comparison |
| :--- | :--- | :--- | :--- |
| **Schaffer's f6** | Found global optimum **every run** | Davis GA benchmark | Matched or approximated GA performance in evaluations |
| **EEG Classification** | **92%** test accuracy | Backpropagation (89%) | Outperformed gradient descent in accuracy and generalization |

### Validation Method:
- **Repeated runs** on Schaffer's f6 to show consistency (global optimum every run).
- **Train-test split** on the EEG dataset to demonstrate generalization.
- Comparisons were made against **genetic algorithms** (on f6) and **backpropagation** (on NN training).

### Subsequent Validation (from later literature):
- Over the next 25+ years, PSO was benchmarked against hundreds of algorithms (GAs, DE, ABC, GWO, WOA, etc.) on thousands of test functions.
- It became one of the **most cited optimization algorithms** in history, spawning hundreds of variants (inertia weight PSO, constriction factor PSO, fully informed PSO, etc.).
- A 2020 systematic review noted that while PSO is easy to implement and often faster than evolutionary algorithms, it needed enhancements in **archiving, convergence handling, and diversity preservation** — precisely the issues that later variants addressed.

---

## 6. What is your assessment of the conclusions?

### Author Claims (1995):
1. PSO is an "extremely simple algorithm that seems to be effective for optimizing a wide range of functions."
2. It is computationally inexpensive in terms of memory and speed.
3. It has ties to both artificial life (bird flocking) and evolutionary computation.

### Assessment:
- **Largely justified**: The 1995 claims have held up remarkably well over three decades. PSO is indeed simple, fast, and widely applicable.
- **Proof-of-concept level**: The original evidence was limited to one benchmark function and one neural network task. The authors did not claim superiority over all algorithms, only that PSO was "effective" and "promising" — a modest and reasonable claim given the data.
- **Negative result awareness**: The authors were cautious. They did not oversell; they presented PSO as a new paradigm worthy of further investigation.

### Relevance for Part 2 (Trading Bot):
- **Strong candidate**: PSO is well-understood, easy to implement, and has been applied to financial optimization problems (portfolio optimization, trading strategy parameter tuning).
- **Known limitations**: PSO can suffer from **premature convergence** on high-dimensional or multimodal problems. For a trading bot with many parameters (e.g., 7-21 dimensions), a modern variant (e.g., inertia weight PSO or fully informed PSO) might be more appropriate than the 1995 original.
- **Replication confidence**: **High**. The original paper provides explicit equations, and the algorithm is so widely implemented that replication is straightforward.

---

## Key Citations for Final Report

1. **Kennedy, J., & Eberhart, R. C. (1995).** Particle swarm optimization. *Proceedings of ICNN'95—International Conference on Neural Networks*, Perth, Australia, Vol. IV, pp. 1942–1948. IEEE Service Center.
2. **Eberhart, R. C., & Kennedy, J. (1995).** A new optimizer using particle swarm theory. *Proceedings of the Sixth International Symposium on Micro Machine and Human Science*, Nagoya, Japan, pp. 39–43. IEEE Service Center.
3. **Shi, Y., & Eberhart, R. C. (1998).** A modified particle swarm optimizer. *IEEE International Conference on Evolutionary Computation*, pp. 69–73. (For inertia weight variant, if needed for Part 2)

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism documented
- [x] Benchmark results summarized
- [x] 6 reviewer questions answered
- [ ] Synopsis formatted to 1-1.5 pages (needs trimming)
- [ ] Cross-checked against project guidelines
