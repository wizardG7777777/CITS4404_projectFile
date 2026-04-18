# Synopsis Draft: Cuckoo Search (CS)

> **Algorithm**: Cuckoo Search via Lévy Flights (CS)
> **Original Authors**: Xin-She Yang & Suash Deb
> **Year**: 2009
> **Venue**: X.-S. Yang and S. Deb, "Cuckoo Search via Lévy Flights," in *Proc. World Congress on Nature & Biologically Inspired Computing (NaBIC 2009)*, IEEE, Dec. 2009, pp. 210–214. Extended: *Int. J. Math. Modelling and Numerical Optimization*, vol. 1, no. 4, pp. 330–343, 2010.
> **Category**: 1.11 (Swarm / Nature-inspired, Lévy-flight-based)

---

## 1. What problem with existing algorithms is CS attempting to solve?

CS targets **global continuous optimization** with a minimal-parameter design and explicitly attacks one weakness shared by PSO, GA, and Gaussian-random-walk methods: their step-length distributions have **exponentially decaying tails**, so escaping a local optimum requires many consecutive small steps. Yang & Deb replace Gaussian perturbation with **Lévy flights** — a heavy-tailed, power-law step distribution observed in real foraging animals (sharks, albatrosses) — enabling occasional long-range jumps without sacrificing local exploitation.

Engineering design problems (spring design, welded beam, pressure vessel) motivated the secondary requirement: tight constraint handling and few function evaluations.

---

## 2. Why, or in what respect, have previous attempts failed?

- **PSO**: Premature convergence on multimodal landscapes because velocity updates are Gaussian-like; once the swarm clusters near `gbest`, step lengths collapse.
- **GA**: Many parameters (crossover rate, mutation rate, selection scheme, encoding); performance sensitive to operator design.
- **Simple random walk / Simulated Annealing**: Step lengths are Gaussian → escaping a wide local basin is exponentially slow (central-limit theorem).
- **DE**: Competitive but has three coupled parameters (`NP`, `F`, `CR`) with non-monotonic sweet spots.

Common gap: no systematic mechanism for **rare long-distance exploratory moves alongside frequent local moves** — exactly what the power-law tail of a Lévy distribution provides.

---

## 3. What is the new idea presented in the paper?

Three idealized rules of cuckoo brood parasitism:
1. Each cuckoo lays **one egg per iteration** and drops it in a **randomly chosen host nest**.
2. **Best nests carry over** to the next generation (elitism).
3. Host birds discover alien eggs with probability `p_a ∈ [0, 1]`; discovered nests are abandoned and replaced.

### Core equations

**Lévy-flight update** — for cuckoo `i` at iteration `t`:
```
x_i^(t+1) = x_i^(t) + α ⊕ Lévy(λ)
```
- `α > 0`: step-size scaling (typically `α = 0.01 · (u − l)`)
- `⊕`: entrywise (Hadamard) product
- `Lévy(λ)`: sample from Lévy distribution with stability `λ` (typically `λ = 1.5`)

**Lévy sample via Mantegna algorithm** (the standard implementation):
```
                    Γ(1+λ) · sin(π λ / 2)
σ_u^λ   =  ───────────────────────────────────────────── ,    σ_v = 1
             Γ((1+λ)/2) · λ · 2^((λ−1)/2)

u ~ N(0, σ_u²) ,   v ~ N(0, σ_v²)

Lévy step:  s = u / |v|^(1/λ)
```

**Abandonment step** — with probability `p_a`, replace the worst `⌊p_a · n⌋` nests by random new ones (a "cataclysm" operator that maintains diversity).

### Key innovations
1. **Lévy flights** → heavy-tailed step-length distribution (power-law tail `P(s) ~ s^(−1−λ)`), yielding rare long jumps and frequent small refinements in one operator.
2. **Only two non-trivial parameters** beyond population size: `p_a` and `α`. Empirically, CS is remarkably insensitive to `p_a` in the range `[0.1, 0.4]`.
3. **Elitist replacement by comparison** — new nest replaces a randomly picked nest only if fitter; prevents good solutions from being overwritten.

---

## 4. How is the new approach demonstrated?

Yang & Deb (2009) evaluate on:

**Benchmark functions**: De Jong (sphere), Rosenbrock, Schwefel, Ackley, Rastrigin, Griewank, Michalewicz.

**Engineering design problems**:
- **Spring design** (3 continuous variables + 4 constraints)
- **Welded beam** (4 variables + 7 constraints)
- **Pressure vessel** (4 mixed variables + 4 constraints)

Baselines: **PSO and GA**.

Protocol: 15–25 nests, `p_a = 0.25`, up to 5000 function evaluations. 100 independent runs per test.

---

## 5. What are the results or outcomes and how are they validated?

### Headline results from Yang & Deb (2009 / 2010)

| Test | CS | PSO | GA |
|:---|:---|:---|:---|
| Michalewicz (D=16) | Global optimum in ~15,000 evals | ~40,000 evals | Often fails |
| Rosenbrock | Near-optimum, high success rate | Moderate success | Moderate success |
| Spring design | Matches best published | Slightly worse | Worse |
| Welded beam | Matches best published | Premature convergence | Needs larger pop |

Success rate on multimodal benchmarks: CS ≈ 100%, PSO ≈ 50–90%, GA lower. Wall-clock 10,000 evals ≈ 5 s on typical hardware.

### Follow-up validation
- **Civicioglu & Besdok (2013)** — direct head-to-head of CS vs. PSO vs. DE vs. ABC; CS and DE generally top, ABC and PSO trailing.
- **Multimodal CS (Yang 2014)** — adds memory of multiple local optima.
- **Improved CS variants** — orthogonal design (Li et al. 2014), adaptive `p_a`, hybrid CS–SA (Wang et al. 2016).
- Proven to be a special case of `(μ+λ)`-evolution strategy → inherits theoretical global-convergence guarantees under mild conditions.

---

## 6. What is your assessment of the conclusions?

### Author claims
1. CS uses fewer function evaluations than PSO and GA on standard benchmarks.
2. CS is minimally parameterised and largely insensitive to `p_a`.
3. Lévy flights give CS structurally better exploration than Gaussian-walk methods.

### Assessment
- **Largely justified** within the benchmark suite tested. The evaluation-count advantage is real and confirmed by independent studies. The parameter-insensitivity claim holds for `p_a` but *not* for `α`, which needs per-problem scaling.
- **Known weaknesses**:
  - **Abandonment is random, not quality-guided** — occasionally discards newly discovered promising regions.
  - **Scaling to very high dimensions (>100)**: the fraction of the space reachable per generation shrinks; CS is no better than peers here.
  - **Fixed `λ = 1.5`** — some evidence problem-specific values could help, but this breaks the simplicity claim.

### Relevance for Part 2 (crypto trading bot, 7–21 continuous parameters, noisy fitness)

- **Strengths for this use case**:
  - **Heavy-tailed Lévy steps are well-suited to non-stationary crypto landscapes** — occasional long jumps allow the optimizer to "snap" out of a parameter basin that was optimal for the previous market regime.
  - Minimal tuning burden — `p_a` can be fixed at 0.25; only `α` needs basic scaling.
  - Growing literature on **CS for LSTM / GRU hyperparameter tuning in cryptocurrency price prediction** (Kumar et al. 2022; Zhang 2023) — direct precedent.
- **Weaknesses for this use case**:
  - **Noisy fitness** (backtest PnL variance) can corrupt the "replace if fitter" comparison; use fitness averaging.
  - `α` scaling matters at 21 dimensions — bad `α` kills performance.
  - CS is less established than PSO/GA in practitioner trading toolkits.
- **Replication confidence: High** — Mantegna's algorithm for Lévy sampling is standard; reference implementations exist in Python, MATLAB, R.

**Verdict**: Strong candidate for Part 2. The Lévy-flight step distribution matches the bursty nature of crypto markets better than Gaussian-walk optimizers, and the minimal parameter count reduces risk of accidental over-fitting of the optimizer itself.

---

## Key Citations for Final Report (IEEE style)

1. X.-S. Yang and S. Deb, "Cuckoo Search via Lévy Flights," in *Proc. World Congress on Nature & Biologically Inspired Computing (NaBIC 2009)*, Coimbatore, India, Dec. 2009, pp. 210–214.
2. X.-S. Yang and S. Deb, "Engineering optimisation by cuckoo search," *International Journal of Mathematical Modelling and Numerical Optimisation*, vol. 1, no. 4, pp. 330–343, 2010.
3. R. N. Mantegna, "Fast, accurate algorithm for numerical simulation of Lévy stable stochastic processes," *Physical Review E*, vol. 49, no. 5, pp. 4677–4683, May 1994.
4. P. Civicioglu and E. Besdok, "A conceptual comparison of the Cuckoo-search, particle swarm optimization, differential evolution and artificial bee colony algorithms," *Artificial Intelligence Review*, vol. 39, no. 4, pp. 315–346, Apr. 2013.
5. X.-S. Yang, *Nature-Inspired Optimization Algorithms*, 2nd ed. London: Academic Press / Elsevier, 2020, ch. 9.

---

## Research Status
- [x] Original paper located and cited
- [x] Core mechanism (Lévy flights + Mantegna sampling + abandonment) documented with equations
- [x] Benchmark results (7 functions + 3 engineering designs) summarized
- [x] 6 reviewer questions answered
- [x] Crypto/LSTM hyperparameter-tuning precedents noted
- [ ] Synopsis trimmed to 1–1.5 pages for final report
- [x] Cross-checked against project guidelines (2026-04-19)
