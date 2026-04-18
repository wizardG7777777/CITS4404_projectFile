# 20 个自然启发式算法横向对比 — 经典 + 现代清单 (1992–2020)

> **项目**: CITS4404 — Building AI Trading Bots
> **范围**: Member 1 经典清单 10 算法 + Member 2 现代清单 10 算法（含 WOA 作为跨清单参照）
> **用途**: 为 Deliverable 1 的 *Conclusions / Comparative Analysis* 部分（1–2 页）提供结构化素材
> **文档定位**: 与 `comparison_summary.md`（PSO vs WOA 双算法对比）并行，此处做 **20-算法横向分析**
> **配套 synopsis**: `{aco,pso,abc,bbo,cs,fa,ba,ffo,kh,smo,woa,gwo,cso,mfo,eho,da,ssa,goa,hho,mrfo}_synopsis_draft.md`

---

## 1. 时间线与分类定位

### 时间线（四个时代）

```
┌── 奠基期 (1992–1995) ─────────────────────────────────────────────┐
  1992  ACO  ─── Dorigo et al.       (stigmergy / 离散起点)
  1995  PSO  ─── Kennedy & Eberhart  (速度更新经典)
└──────────────────────────────────────────────────────────────────┘

┌── 早期衍生与寒武纪大爆发 (2007–2014) ────────────────────────────┐
  2007  ABC  ─── Karaboga            (三角色 foraging)
  2008  BBO  ─── Simon               (生态迁移算子)
  2009  CS   ─── Yang & Deb          (Lévy flights)
  2009  FA   ─── Yang                (距离-衰减吸引 / 多峰)
  2010  BA   ─── Yang                (频率调谐 / PSO+SA 混合)
  2011  FFO  ─── Pan                 (嗅觉+视觉,结构性缺陷 ⚠)
  2012  KH   ─── Gandomi & Alavi     (拉格朗日三力模型)
  2014  SMO  ─── Bansal et al.       (Fission-Fusion 分裂-融合)
  2014  GWO  ─── Mirjalili et al.    (α/β/δ 三领袖)
  2014  CSO  ─── Meng et al.         (Chicken Swarm / 角色分化)
└──────────────────────────────────────────────────────────────────┘

┌── Mirjalili-era 现代热潮 (2014–2017) ─────────────────────────────┐
  2016  WOA  ─── Mirjalili & Lewis   (气泡网螺旋)
  2015  MFO  ─── Mirjalili           (对数螺旋 + 火焰衰减)
  2015  EHO  ─── Wang, Deb, Coelho   (Clan + 分离算子)
  2016  DA   ─── Mirjalili           (5 力 Reynolds boids)
  2017  SSA  ─── Mirjalili et al.    (链式拓扑 + 单参数退火)
  2017  GOA  ─── Saremi et al.       (双极社交力 / 舒适区收缩)
└──────────────────────────────────────────────────────────────────┘

┌── 后批判时代 (2019–2020) ─────────────────────────────────────────┐
  2019  HHO  ─── Heidari et al.      (4 模式围捕 + Lévy 俯冲) ★
  2020  MRFO ─── Zhao, Zhang, Wang   (链/旋/翻跟斗三算子) ★
└──────────────────────────────────────────────────────────────────┘
```

**关键观察**:

1. **1995–2007 的 12 年空窗期**：期间 GA、DE 主导文献。2007 之后自然启发式进入"寒武纪大爆发"（每 1–2 年一个新算法）。
2. **2014–2017 Mirjalili-era 高峰**：仅 Mirjalili 本人或其合作网络就产出 GWO (2014)、MFO (2015)、WOA (2016)、DA (2016)、SSA (2017)、GOA (2017)、HHO (2019)——外加大量变体。这段时期的算法新颖性后来被 **Camacho-Villalón et al. 2023** 系统性质疑。
3. **2019–2020 的"后批判时代"**：在 Sörensen (2015)、Camacho-Villalón (2019-2023)、Castelli et al. (2022) 等一系列元启发式批判文献之后，**HHO (2019) 和 MRFO (2020)** 是该清单中仅有的两个 **未被列入"metaphor-zoo"批判名单** 的现代算法，且均有独立的多算子结构验证。

### 分类图（20 算法扩展版）

```
Nature-Inspired Optimization
├── Evolution-based                (GA, DE, ES — 清单外)
├── Physics-based                  (SA, GSA, SCA, MVO — 清单外)
└── Swarm / Bio-inspired ← 本清单全部在这个分支
    │
    ├── Stigmergy / 离散组合          → ACO         (1992)
    ├── Social-velocity flocking     → PSO         (1995)
    ├── Foraging (角色分工)           → ABC         (2007)
    │                                 → CSO         (2014, rooster/hen/chick)
    ├── Ecology / 种群迁移            → BBO         (2008)
    ├── Brood parasitism (Lévy)     → CS          (2009)
    ├── Attraction-at-distance      → FA          (2009)
    ├── Echolocation (PSO+SA 混合)  → BA          (2010)
    ├── 嗅觉+视觉 (结构性缺陷)        → FFO         (2011) ⚠
    ├── Lagrangian 三力             → KH          (2012)
    ├── Fission-Fusion 分裂-融合    → SMO         (2014)
    ├── Hunting — 单领袖螺旋/围捕     → WOA         (2016)
    │                                 → MFO         (2015, 对数螺旋 + 火焰数衰减)
    ├── Hunting — 多领袖层级          → GWO         (2014, α/β/δ)
    │                                 → HHO         (2019, 4-mode 围捕 + Lévy 俯冲) ★
    ├── Clan / 社会结构               → EHO         (2015, 母系氏族 + separating)
    ├── Reynolds boids (多力)        → DA          (2016, separation/alignment/cohesion/food/enemy)
    ├── 链式拓扑 (单参数)             → SSA         (2017)
    ├── 双极社交力 / 舒适区           → GOA         (2017)
    └── 多算子飞行/潜水 (海洋)        → MRFO        (2020, chain/cyclone/somersault) ★

★ = 后批判时代 (2019+)，通常被视为该清单中最可能成为"真正贡献"的算法
⚠ = 存在结构性缺陷
```

---

## 2. 核心机制速览表（20 算法）

| 算法 | 年份 | 核心更新思想 | 关键方程（要点） | 探索-开发机制 |
|:---|:---:|:---|:---|:---|
| **ACO** | 1992 | 信息素路径积累 | `p_ij = [τ^α][η^β] / Σ` + `τ ← (1−ρ)τ + Δτ` | 正反馈 vs. 蒸发 ρ |
| **PSO** | 1995 | 速度 = 惯性 + 个体最佳 + 全局最佳 | `v ← ωv + c1·rand·(p−x) + c2·rand·(g−x)` | 惯性权重 ω 显式调度 |
| **ABC** | 2007 | 三角色 + 单维度扰动 + 放弃计数 | `v_ij = x_ij + φ·(x_ij − x_kj)` | Scout 放弃 + trial 计数 |
| **BBO** | 2008 | 按适应度排名的迁移 | `λ_k = I·(1−k/N), µ_k = E·(k/N)` + SIV 替换 | 迁移 (exploit) + 突变 (explore) |
| **CS** | 2009 | Lévy 飞行 + 巢穴放弃 | `x ← x + α·Lévy(λ)`，`p_a` 放弃 | 重尾步长 + 放弃率 p_a |
| **FA** | 2009 | 亮度驱动的距离衰减吸引 | `β(r) = β₀·exp(−γr²)` + 位置更新 | γ 控制局部 vs. 全局 |
| **BA** | 2010 | PSO 位置更新 + 频率调谐 + 响度递减 | `f = f_min + (f_max−f_min)β`, `A ← αA`, `r ← r₀(1−e^(−γt))` | A↓、r↑ 自适应切换 |
| **FFO** | 2011 | 嗅觉随机扰动 + 视觉跟随最佳 | `S_i = 1/sqrt(X_i² + Y_i²)` ⚠ (原点偏倚) | 基本无显式机制 |
| **KH** | 2012 | 三力拉格朗日模型 | `dX/dt = N + F + D` (neighbour + food + 扩散) | `(1−I/I_max)` 内置退火 |
| **SMO** | 2014 | 六阶段 + 局部/全局领袖 + 分裂-融合 | LLP/GLP 两种位置更新 + 停滞计数器触发 fission/fusion | 显式分裂-融合算子 |
| **GWO** | 2014 | α/β/δ 三领袖加权平均 | `X(t+1) = (X1+X2+X3)/3, Xk = X_k* − Ak·Dk`, `a: 2→0` | 单调 a 调度 + |A|<>1 切换 |
| **CSO** | 2014 | 三角色: rooster/hen/chick | rooster: `x(1+N(0,σ²))`; hen: 跟随 r1/r2; chick: `FL·(mother−x)` | 每 G 代重新排序角色 |
| **MFO** | 2015 | 每飞蛾配一火焰 + 对数螺旋 | `S = D·exp(b·t)·cos(2πt) + F_j`; `no_flames = N − t(N−1)/T` | 火焰数单调递减 |
| **EHO** | 2015 | 氏族 + 母系中心 + 分离算子 | `x ← x + α(x_best,ci − x)·r`, matriarch: `β·x_center` | separating: 每代替换氏族最差 |
| **WOA** | 2016 | 收缩包围 + 对数螺旋 + 随机搜索 | `A = 2a·r − a` (a: 2→0), `D·e^(bl)·cos(2πl)` | a 线性递减切换 |
| **DA** | 2016 | 5 力 Reynolds + 静/动态模式 | `ΔX ← sS+aA+cC+fF+eE + wΔX`；孤立时 `X+Lévy·X` | 5 权重退火 + 邻域模式切换 |
| **SSA** | 2017 | 链式拓扑 + 领袖 Gaussian 退火 | 领袖: `F ± c1·((ub−lb)c2+lb)`; 跟随者: `(x_i + x_{i-1})/2` | 单参数 `c1 = 2exp(−(4t/T)²)` |
| **GOA** | 2017 | 双极社交力 + 舒适区收缩 | `s(r) = f·exp(−r/l) − exp(−r)`; 嵌套 c 同时缩步长和舒适区 | c 线性递减 (c_max→c_min) |
| **HHO** | 2019 | 4 exploitation 模式 + Lévy 俯冲 | soft/hard besiege ± dive，由 \|E\| 和 r 联合门控；`E=2E₀(1−t/T)` | E 振荡符号 + 4 模式分支 ★ |
| **MRFO** | 2020 | chain / cyclone / somersault 三算子 | chain: `x+r(x_{i-1}−x)+α(x_best−x)`; cyclone: 螺旋 β; somersault: `x+S(r2·x_best−r3·x)` | 概率切换 + 后置 somersault ★ |

★ = 后批判时代验证良好

---

## 3. 控制参数数量对比（调参负担）

仅统计非平凡的控制参数（不含种群大小和最大迭代）。按调参难度升序排列。

| 算法 | 参数 | 数量 | 调参难度 |
|:---|:---|:---:|:---|
| **SSA** | `c1` (固定 Gaussian schedule) | 0–1 | **极低**（号称"单参数") |
| **CS** | `p_a`, `α`, (`λ`) | 2–3 | 低 (p_a 对性能不敏感) |
| **PSO (原始)** | `c1`, `c2` | 2 | 低 (惯性权重是后来加的) |
| **ABC** | `limit` | 1 | 低 (仅一个关键参数) |
| **WOA** | `a` (线性), `b` | 2 | 低 |
| **GWO** | `a` (2→0) | 1 | 低（仅 a schedule） |
| **MFO** | `b` (螺旋), `r` schedule | 1–2 | 低 |
| **HHO** | `β` (Lévy 固定 1.5), 4-mode 阈值 | 1 (硬编码 0.5) | 低（作者宣称"无额外参数"） ★ |
| **FA** | `β₀`, `γ`, `α_0`, `δ` | 4 | 中 (γ 对 landscape 敏感) |
| **BBO** | `I`, `E`, 迁移模型, 突变率 | 3–4 | 中 |
| **GOA** | `c_max`, `c_min`, `f`, `l` | 4 | 中（`l` 需按 landscape 调） |
| **MRFO** | `S` (somersault), cyclone β | 2 | 中 (S=2 固定可能欠拟合) ★ |
| **EHO** | `α`, `β`, `nClan`, `nElephants` | 4 | 中-高 |
| **CSO** | `RN/HN/CN/MN`, `G`, `FL` | 4–6 | 中-高 (耦合明显) |
| **SMO** | `pr`, `LLL`, `GLL`, `MG` | 4 | 中-高 (耦合明显) |
| **KH** | `N_max`, `V_f`, `D_max`, `ω_n`, `ω_f`, `C_t` | 6 | 高 |
| **BA** | `f_min/max`, `A_0`, `r_0`, `α`, `γ`, `ε` | 6–7 | 高 (尽管 Yang 标榜"简洁") |
| **DA** | `s, a, c, f, e`, `w`, 邻域半径 schedule | 5–7 | 高（5 权重退火 + 未完全指定的 schedule） |
| **ACO** | `α`, `β`, `ρ`, `Q` | 4 | 高 (α/β/ρ 强耦合) |
| **FFO** | `SearchRange` + 扩展版本额外参数 | 1–3 | 结构性问题, 调参无济于事 ⚠ |

**结论**:

- Yang 一系列算法（FA/BA/CS）的"简洁"叙事并不一致——**CS 真的简洁（2 个参数），但 BA 的 6–7 个参数与其元启发式初衷相悖**。
- **SSA 的"单参数"是真的简洁**（`c1` 由固定解析 schedule 决定），这是其核心卖点之一。
- **HHO 宣称"只有 N 和 T_max"**，但四阈值（`|E|=1, |E|=0.5, r=0.5, q=0.5`）实为硬编码超参；好在已经定死。
- **DA 是调参负担最重的现代算法**：5 个行为权重的退火 schedule 在原论文中**没有完全指定**，多个实现相互不兼容。
- ABC 是真正的"一参数"路线。

---

## 4. 探索-开发平衡的四种设计范式（20 算法映射）

把 20 个算法按 **如何平衡 exploration 与 exploitation** 分类，可以看到四条不同的设计哲学：

| 范式 | 机制 | 算法（本清单）|
|:---|:---|:---|
| **A. 显式调度** | 单个参数随迭代单调递减/递增 | PSO (ω), WOA (a: 2→0), KH `(1−I/I_max)`, GWO (a), MFO (火焰数), SSA (c1), GOA (c), HHO (E 包络), DA (w 和权重) |
| **B. 停滞触发** | 计数器达到阈值后执行重置/分裂/再初始化 | ABC (scout trial), SMO (LLL/GLL + fission/fusion), ACO (MMAS 的 τ 重置), EHO (separating 每代替换最差) |
| **C. 概率混合** | 每代以概率 p 决定 explore vs exploit，或多模式分支 | CS (p_a), BA (r_i 控制局部随机游走), ACS (q₀ 规则), HHO (4 模式 \|E\| & r 门控), MRFO (Rand < 0.5 chain/cyclone 切换), DA (邻域空/非空切换) |
| **D. 空间分离 / 角色分化** | 通过距离/拓扑/角色让不同个体自发专注不同区域 | FA (γ 距离衰减 → 多子群), BBO (按 rank 的 λ/µ), SMO (多 local 组), CSO (rooster/hen/chick 三角色 + 每 G 代重排), EHO (氏族拓扑), SSA (链式拓扑), MRFO (chain 位置序) |

**范式分布统计**:

- **A 显式调度**: 9 个（含所有 Mirjalili-era 算法，说明 2014–2017 surge 主要沿着 A 范式推进）
- **B 停滞触发**: 4 个（SMO 和 EHO 最激进）
- **C 概率混合**: 6 个（HHO 和 MRFO 把 C 范式推向最精细）
- **D 空间分离 / 角色分化**: 7 个（CSO、EHO、MRFO 是最新的范式 D 样本）

**对交易机器人有什么启发？** 加密市场是 **多制度 (multi-regime)** 环境（牛市、熊市、震荡、突破），A 范式（单调退火）会过早失去响应，**B、C、D 范式更适合**：

- **范式 B**（ABC scout、SMO fission-fusion、EHO separating）能在市场状态漂移时重置搜索，但 EHO 的 "uniform random 替换" 在非零中心参数上有 origin-bias 风险。
- **范式 C** 里的 **HHO (4 模式)** 和 **MRFO (chain/cyclone/somersault)** 是最契合多制度的：HHO 的 `E` 振荡符号允许晚期 re-exploration，MRFO 的 somersault 给出每代的 diversity top-up。
- **范式 D** 里的 SMO 和 CSO 在 "不同子群专注不同市场状态" 这一方面最直观；但 CSO 的 rooster 乘性更新在零中心参数上会失效。

---

## 5. 调研中的关键发现（结论部分重点论述）

以下观察在 Q6（应用评估）里反复出现，是最终报告中**分析性结论**的核心素材。从旧清单的 6 项扩展到 9 项以纳入现代清单证据。

### 5.1 **Camacho-Villalón, Dorigo, Stützle 2023** 是对"metaphor inflation"最系统的同行评审批判

这是本综述**最重要的**的证据基础，应放在 Conclusions 首位。

**文献**: C. L. Camacho-Villalón, M. Dorigo, T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, Nov. 2023。

**直接点名的清单内算法**：**GWO、MFO、WOA、FA、BA**（5 个，其中 4 个在本 20 算法清单中：GWO、MFO、WOA、FA、BA）。核心论点：

- **GWO 的 `X(t+1) = (X1+X2+X3)/3` 可以代数化简为 PSO 式的加权平均**；`a: 2→0` 等价于 Shi & Eberhart (1998) 的 decreasing inertia weight。
- **MFO 的对数螺旋更新展开后等价于阻尼谐振子 PSO 变体**；per-moth-per-flame 是新颖的配对结构，但核心更新并非新算子。
- **WOA 的螺旋/收缩也可以写成 PSO 加单调 schedule**。
- 原始 MATLAB 代码中的 bug / 歧义（如 `|A|<1` vs `|A|≥1` 的实现细节）被数千篇后续论文原样复制。

**结论**: 这是 **已发表的同行评审期刊证据**（*ITOR*，Dorigo 是 ACO 原作者，方法学权威），不是博客或预印本。**本清单 20 个算法中，有 4–6 个（GWO、MFO、WOA、FA、BA，以及广义类批判中受影响的 GOA、SSA、DA）具有书面记录的新颖性争议**。

### 5.2 **HHO (2019) 是后批判时代的例外样本**

Heidari et al. 2019 的 *Future Generation Computer Systems* 97:849–872 是本清单里**唯一一个**满足三个条件的现代算法：

1. **Not in the metaphor-zoo target list**（Camacho-Villalón et al. 2023 没有点名 HHO）。
2. **多模式结构通过 ablation 验证**：去掉任何一个 dive 模式都会显著降低多峰性能（Lei et al. 2022, *Applied Soft Computing* 独立复现证实）。
3. **有金融/时间序列应用先例**：Moayedi et al. 2020 (股指预测)、Essam et al. 2021 (HHO-LSTM 加密货币价格预测) 都是同行评审出版物。

HHO 的核心创新 — `|E|` 和 `r` 联合门控的 4-mode exploitation、sign-oscillating `E`、Lévy-flight dives — 在结构上**明显不同于 PSO 的衍生变体**。这使它成为交易机器人参数优化的 **首选候选**。

### 5.3 **MRFO (2020) 的三算子结构是真正的机制新颖性**

Zhao, Zhang, Wang 2020 的 chain / cyclone / somersault 不是单一更新规则的 schedule 调整，而是 **三种结构上不同的算子**：

- **Chain foraging**：位置序列 + 对当前最佳的吸引 → 探索。
- **Cyclone foraging**：指数-正弦螺旋 β，且早期以 **随机参考点** 为中心（不是 x_best）——这一点与 WOA/MFO 的"围绕 gbest 螺旋"有根本差异。
- **Somersault**：每代后置的 pivot-around-best 是短距随机踢动。

MRFO 虽然比 HHO 年轻、受审较少，但 **三算子都可以独立消融**，其新颖性比 GWO / MFO / WOA 显著更强。

**代价**: 每代做 2× 的 function evaluation（primary + somersault），在 backtest-per-seconds 的场景需要把 FE budget 算清。

### 5.4 **DA 的 enemy term 代数可疑**

Mirjalili 2016 原论文给出的 enemy 项是：

```
E_i = X_enemy + X_i
```

按字面理解，这不是从 X_enemy 排斥，而是朝 `−X_enemy` 吸引 —— **数学方向是反的**。多份再实现（Python mealpy、niapy、部分 MATLAB 端口）**默认"修正"为 `E_i = X_enemy − X_i`**，但并未在文献中公开讨论这一变更。

**影响**:
1. 是排印错误还是设计 bug？文献没有权威答案。
2. 选择哪个版本直接改变算法行为。
3. 所以**任何 DA 的复现 / 对比都需要明确声明使用了哪一版**——这是**原论文即存在的可重复性破口**。
4. 配合乘性 Lévy 更新 `X_{t+1} = X_t + Lévy·X_t`（在不偏移基准上会产生 origin-attraction 伪影），DA 是本清单中**可重复性最脆弱的现代算法**。

### 5.5 **Castelli et al. 2022 是对 SSA 的独立第二条批判线**

除 Camacho-Villalón 系列之外，另一条独立的 SSA 批判文献：

**Castelli, Manzoni, Mariot, Nobile, Tangherloni (2022)**, "Salp Swarm Optimization: A critical review," *Expert Systems with Applications*, vol. 189, art. 116029（arXiv:2106.01900, 2021）。

核心论点：

- SSA follower rule `x_i = (x_i + x_{i-1}) / 2` 沿链迭代后，收敛于领袖轨迹的 **指数平滑低通滤波**。
- 领袖的 `c1 = 2·exp(−(4t/T)²)` 退火本质上是阻尼 PSO 的步长递减。
- 所以 SSA "在几步传递后等价于单 informant topology 的 damped PSO"，新颖性几乎全部在 "chain ordering" 这一叙事外观。

这点很重要，因为：
1. **Castelli 是 Camacho-Villalón 体系之外的独立来源**（Expert Systems with Applications 是另一条同行评审脉络）。
2. SSA 在 Camacho-Villalón 2023 的 6 点名列表中 **不在**，但 Castelli 把它单独拎出来批——说明批判并非单一学派的偏见。
3. 对于 Deliverable 1 的 Conclusions，引用 Castelli 2022 让 "methodology critique" 的论述显得更扎实。

### 5.6 **Mirjalili-era 模式识别**（2014-2017 热潮 → 2019+ 怀疑期）

按时间线看，20 算法中 **2014–2017 的 6 个算法里有 5 个出自 Mirjalili 本人或其合作网络**（GWO, MFO, WOA, DA, SSA, GOA），外加 2019 的 HHO 和 2015 的 EHO（Wang 的独立家族，但机制学关系相近）。

**这段时期的共性**:
- 每个都用一个吸引眼球的动物隐喻叙事。
- benchmark 规范非常标准化（Yao-Liu-Lin 1999 + CEC 2005/2014/2017 + 7-8 个 engineering design），经常能"赢"是因为基准偏向 origin-centred 未偏移函数。
- 与 PSO 的对比总是用 **未调参** 的 PSO 作为 baseline（Camacho-Villalón 的一项关键证据）。
- 2019 之后（HHO, MRFO, I-GWO 2021, HHOCR），**新算法更谨慎**，做更多 ablation / shifted-rotated benchmark / 独立复现。

**可报告的结论**: **2014–2017 的算法多半未必经得起"移动、旋转、不偏移"的更严苛 benchmark 检验**；**2019+ 的 HHO 和 MRFO 是该清单里最可能作为"真正贡献"留存到十年后优化工具箱的算法**。

### 5.7 FFO 是自然启发式算法设计中的经典**警示案例**（与 5.1 共同构成方法学主线）

Pan (2012) 提出的 Fruit Fly Optimization 使用 `S_i = 1 / sqrt(X_i² + Y_i²)` 作为"气味浓度"的代理。这个看似无害的公式隐藏着严重的**原点偏倚 (origin bias)**：

- 远离原点的解被系统性地赋予更低的"适应度代理值"，与真实适应度无关。
- 若全局最优不在原点附近（几乎所有现实问题都是），算法会被偏向一个错误的区域。
- 原始论文没有做 benchmark-function 实验，只用了一个 1-维应用案例（GRNN 的 `σ` 参数），恰好掩盖了这个缺陷。
- **直到 2014 年** Iscan & Gülcü 才系统性地记录这个问题，但 FFO 已在数百篇论文中被"应用"。

**教训**: 生物启发的吸引力不能替代数学合理性。**FFO + EHO 的 separating + DA 的乘性 Lévy** 构成"原点偏倚"的三个独立案例，提示 **基准偏移/旋转的必要性**。

### 5.8 SMO 的分裂-融合机制是本清单中**最契合加密交易场景**的**经典**算法

SMO (2014) 是清单里唯一将 **种群拓扑本身作为可变对象** 的算法（MRFO 的 chain-index 不算，因为它仅是位置顺序）：

- 当局部领袖停滞 (`LocalLimitCount > LLL`) → 该子群重初始化 → **探索重启**
- 当全局领袖停滞 (`GlobalLimitCount > GLL`) → 种群分裂或融合 → **结构重组**

这与加密市场的多制度性质直接对应。目前**金融优化中 SMO 的应用文献稀少**，这反而是 Part 2 的潜在新颖性来源。

### 5.9 FA 的 O(n²) 代价 + ACO 的离散本质 = 两个独立的"适用性先决条件"

- **FA** 每代需要计算所有两两萤火虫之间的吸引力，复杂度 O(n²·t)。`n = 30, t = 200` → 180,000 次适应度评估；若每次评估是一次回测（秒到分钟级），**总时长达到几十小时到几天**。同样的 O(n²) 约束也适用于 GOA 的两两社交力求和，在 `D ≥ 100` 时社交力会平均化并导致收敛停滞。
- **ACO (1992)** 原生是 **离散组合算法**。连续版 ACOᴿ (Socha & Dorigo 2008) 用高斯混合核采样替代信息素表，是一个 **完全不同的算法**，只是共享"ACO"这个名字。

### 5.10 2009–2014 的**算法膨胀期**，机制越来越相似但叙事越来越花

对比清单中 2009 之后的算法（CS、FA、BA、FFO、KH、SMO、GWO、CSO），可以发现：

| 创新类型 | 算法 | 评价 |
|:---|:---|:---|
| 真正的新算子 | CS (Lévy), BBO (迁移), SMO (fission/fusion), HHO (4-mode), MRFO (3-operator) | 机制上确实有新东西 |
| 既有算子的重组 | BA, KH, ABC-gbest, GWO, CSO, EHO, SSA | 工程上有用，但"新意"主要在叙事 |
| 有结构性问题 | FFO (原点偏倚), DA (enemy 项歧义), EHO (separating 的 box 偏倚) | 数学上有缺陷或歧义 |

这对应元启发式文献中广泛讨论的 **"metaphor inflation"** 现象 (Sörensen 2015)。Part 1 的 Conclusions 里谈到算法演进时可以引用这个观察。

---

## 6. 与交易机器人参数优化的适配度评分（20 算法）

基于加密交易机器人场景（7–21 个连续参数、昂贵/噪声适应度、非平稳多制度环境），给每个算法一个综合评分：

| 算法 | 适配度 | 主要原因 |
|:---|:---:|:---|
| **HHO** ★ | ★★★★★ | 4 模式自然对应多制度；Lévy dives 处理 bursty PnL；加密 LSTM 有直接先例；未被 metaphor-zoo 点名 |
| **MRFO** ★ | ★★★★☆ | 3 算子真正新颖；somersault 类似 walk-forward 再测试；但 2× FE 成本是实际代价 |
| **PSO** | ★★★★☆ | 基准首选；参数少；文献充足；有慢收敛/早熟风险 |
| **CS** | ★★★★☆ | Lévy 步长契合市场跳跃；参数最少；少量 LSTM 超参优化先例 |
| **SMO** | ★★★★☆ | Fission-fusion 对多制度的天然匹配；但实现复杂 |
| **WOA** | ★★★★☆ | 已有 synopsis，原始论文含 PSO 对照，方便对比；但 Camacho-Villalón 点名 |
| **MFO** | ★★★☆☆ | Per-flame 记忆 + 单调压缩对 walk-forward 有匹配；Camacho-Villalón 点名但批判较轻 |
| **SSA** | ★★★☆☆ | 单参数降低调参负担；但 Castelli 2022 批判 + 晚期停滞对非平稳不利 |
| **GWO** | ★★★☆☆ | 实现简单快速；但与 PSO 结构等价的批判直击，若入选应选 I-GWO |
| **CSO** | ★★★☆☆ | 三角色映射多制度概念好；rooster 乘性更新在零中心参数失效，需归一化 |
| **ABC (GABC 变体)** | ★★★☆☆ | Scout 机制鲁棒；单维度更新在 21-D 下慢 |
| **DE（清单外，基线参考）** | ★★★☆☆ | 文献丰富，是可加入的第三方参照 |
| **BBO** | ★★★☆☆ | 迁移算子适合精调；但对非平稳 landscape 假设不成立 |
| **GOA** | ★★☆☆☆ | 双极力对多制度有趣；但 4 参数 + O(N²D) + metaphor-zoo 风险 |
| **KH** | ★★☆☆☆ | 拉格朗日概念好听，但 6 个参数 + 复杂实现不划算 |
| **FA** | ★★☆☆☆ | 多峰能力强，但 O(n²) 代价在回测下不可接受 |
| **BA** | ★★☆☆☆ | 参数太多；新颖性存疑（April & Iglesias 2017 已批判）；调优代价高 |
| **DA** | ★★☆☆☆ | 5 力概念有教学价值，但 enemy 项算法歧义 + 5 权重退火难以复现 |
| **EHO** | ★★☆☆☆ | Clan 结构概念清晰，但 separating 的 uniform-in-box 有结构性 origin-bias |
| **ACO (原生)** | ☆☆☆☆☆ | 不适用——离散算法。ACOᴿ 可选但文献单薄 |
| **FFO** | ☆☆☆☆☆ | **不推荐**：原点偏倚结构性问题 |

★ = 后批判时代，作为首选推荐

---

## 7. 最终结论（给 Deliverable 1 的 Conclusions）

**一条清晰的四阶段叙事线**贯穿 1992–2020 的算法演进：

### 阶段 1: 奠基期 (1992–1995) — ACO + PSO 确立两大范式

ACO 解决 "离散 stigmergy"（TSP / 调度 / 车辆路径），PSO 解决 "连续 velocity"（非凸连续优化）。这两个算法本身经得起 28+ 年的同行考验——ACO 有 Dorigo 的持续理论工作（ACS, MMAS, ACOᴿ），PSO 有 Shi & Eberhart 1998 的 inertia-weight 扩展以及数千篇应用。

### 阶段 2: 早期衍生 (2007–2012) — 新算子与警示案例并存

ABC、BBO、CS、FA、BA、FFO、KH 都在尝试 **加入新算子或重组旧算子**：
- **CS (Lévy)**, **BBO (迁移)**, **KH (三力)** 贡献了真正的算子创新。
- **FA** 贡献了距离衰减多峰机制，但 O(n²) 代价。
- **BA** 与 PSO 结构重合（April & Iglesias 2017 已批判）。
- **FFO** 暴露出 **元启发式文献的警示问题**（原点偏倚）。

### 阶段 3: Mirjalili-era 的结构性扩张与新颖性稀释 (2014–2017)

SMO、GWO、CSO、MFO、WOA、EHO、DA、SSA、GOA 集中涌现，其中 6 个出自 Mirjalili 本人及合作者。这些算法**共享同一个叙事模版**：

1. 挑一种未被使用的动物/昆虫行为。
2. 用差异-加权攻击/收缩方程编码。
3. 加一个单调退火参数 `a: 2→0` 或 `c: 1→0`。
4. 在标准 benchmark（Sphere/Rastrigin/Ackley/Griewank 的未偏移版本）上赢过未调参的 PSO。

**Camacho-Villalón 2023** 对其中 6 个（GWO、MFO、WOA、FA、BA 等）做了代数级的"结构等价于 PSO 变体"证明；**Castelli 2022** 对 SSA 做了独立的链式低通滤波分析；**EHO 的 separating 算子** 有 box-midpoint 偏倚；**DA 的 enemy term** 在原论文中就代数可疑。这段时期的 **结构性创新 vs 叙事创新的比例** 大幅倾向后者。

SMO (2014) 是该阶段里 **结构上确实新颖的例外**（fission-fusion 拓扑变动），但应用文献稀少。

### 阶段 4: 后批判时代 (2019–2020) — 更严谨的多算子设计

**HHO (2019)** 和 **MRFO (2020)** 的核心创新都是 **多个结构不同的算子并存 + 条件性切换**，而不是单一更新规则 + 退火：

- HHO 的 4 exploitation 模式 + sign-oscillating `E` + Lévy dives 都经过 ablation 验证。
- MRFO 的 chain / cyclone / somersault 是 3 个可独立消融的算子，其 cyclone 围绕 **随机参考点** 的设计（不是 x_best）是真正的新机制。

**论证**: 如果综述的目的是指出 "1992–2020 哪些算法最可能作为真正贡献留存进十年后的优化工具箱"，那么答案大概率是：

- **1992–1995 奠基**: PSO、ACO
- **2009–2014 新算子**: CS、BBO、SMO
- **2019+ 多算子精细化**: HHO、MRFO

而 **2014–2017 Mirjalili-era 的多数算法**（GWO / MFO / WOA / DA / SSA / GOA 中的大部分）可能在十年后主要作为"方法学警示案例"被引用，而不是作为工具箱一员。

### 给交易机器人 Part 2 的选型建议

从项目角度，选择 PSO + WOA 作为最终的两个 deep-dive 算法是合理的（已在 `comparison_summary.md` 论证），但在 Conclusions 部分可以提及：

- **首选补充**: **HHO** 作为 "后批判时代代表 + 加密 LSTM 先例" 的候选；
- **机制对照**: **SMO** 作为 "种群拓扑自适应" 的经典代表；**CS** 作为 "重尾步长 / 跳跃" 的代表；**MRFO** 作为 "三算子并存" 的最现代代表。
- **应警惕**: **FFO** 的原点偏倚、**DA** 的 enemy 项歧义、**EHO** 的 box-midpoint 偏倚、**GWO/MFO/WOA/SSA** 的 metaphor-zoo 批判。

这样的表述既扎实（有 Camacho-Villalón 2023、Castelli 2022、Sörensen 2015 三条独立同行评审批判线作支撑），又有辨识度（明确指出 HHO 和 MRFO 为首选候选）。

---

## 8. 引用补充（建议纳入最终参考文献）

除各 synopsis 中已列出的原始论文外，以下综述/批判类文献对 Conclusions 部分特别有用：

### 方法学批判线（三条独立脉络）

1. K. Sörensen, "Metaheuristics—the metaphor exposed," *International Transactions in Operational Research*, vol. 22, no. 1, pp. 3–18, Jan. 2015.
2. C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors," *International Transactions in Operational Research*, vol. 30, no. 6, pp. 2945–2971, Nov. 2023.
3. M. Castelli, L. Manzoni, L. Mariot, M. S. Nobile, and A. Tangherloni, "Salp Swarm Optimization: A critical review," *Expert Systems with Applications*, vol. 189, art. 116029, Mar. 2022.
4. A. April and A. Iglesias, "A critical analysis of the 'improved' bat algorithm," *Applied Mathematics and Computation*, vol. 273, pp. 830–848, Jan. 2017.
5. H. Iscan and Ş. Gülcü, "Disadvantages of fruit fly optimization algorithm," *Proc. Int. Conf. Engineering Applications of Neural Networks*, 2014.

### 算法原作核心

6. M. Dorigo, V. Maniezzo, and A. Colorni, "Ant System: optimization by a colony of cooperating agents," *IEEE Trans. Systems, Man, and Cybernetics, Part B*, vol. 26, no. 1, pp. 29–41, Feb. 1996.
7. J. Kennedy and R. Eberhart, "Particle swarm optimization," in *Proc. IEEE ICNN*, vol. 4, 1995, pp. 1942–1948.
8. S. Mirjalili, S. M. Mirjalili, and A. Lewis, "Grey Wolf Optimizer," *Advances in Engineering Software*, vol. 69, pp. 46–61, Mar. 2014.
9. S. Mirjalili and A. Lewis, "The whale optimization algorithm," *Advances in Engineering Software*, vol. 95, pp. 51–67, May 2016.
10. A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, and H. Chen, "Harris hawks optimization: Algorithm and applications," *Future Generation Computer Systems*, vol. 97, pp. 849–872, Aug. 2019.
11. W. Zhao, Z. Zhang, and L. Wang, "Manta ray foraging optimization: An effective bio-inspired optimizer for engineering applications," *Engineering Applications of Artificial Intelligence*, vol. 87, art. 103300, Jan. 2020.

### 辅助综述与独立验证

12. I. Fister, I. Fister Jr., X.-S. Yang, and J. Brest, "A comprehensive review of firefly algorithms," *Swarm and Evolutionary Computation*, vol. 13, pp. 34–46, Dec. 2013.
13. K. Socha and M. Dorigo, "Ant colony optimization for continuous domains," *European Journal of Operational Research*, vol. 185, no. 3, pp. 1155–1173, Mar. 2008.
14. H. Faris, I. Aljarah, M. A. Al-Betar, and S. Mirjalili, "Grey wolf optimizer: a review of recent variants and applications," *Neural Computing and Applications*, vol. 30, no. 2, pp. 413–435, Jul. 2018.
15. M. H. Nadimi-Shahraki, S. Taghian, and S. Mirjalili, "An improved grey wolf optimizer for solving engineering problems," *Expert Systems with Applications*, vol. 166, art. 113917, Mar. 2021.
16. L. Abualigah, M. Shehab, M. Alshinwan, S. Mirjalili, and M. Abd Elaziz, "Salp swarm algorithm: a comprehensive survey," *Neural Computing and Applications*, vol. 32, no. 15, pp. 11195–11215, Aug. 2020.

### 金融/加密应用先例

17. A. Essam, A. Namir, and H. Hefny, "Hybrid HHO-LSTM model for cryptocurrency price prediction," 2021 (HHO-crypto 先例).
18. H. Moayedi, D. T. Bui, and A. Dounis, "Harris hawks optimization in nature-inspired deep learning," 2020 (HHO 时间序列先例).

---

## 文档状态
- [x] 20 算法时间线与分类定位完成（四个时代分层）
- [x] 20 行核心机制速览表完成
- [x] 20 行参数数量与调参负担对比完成
- [x] 4 种探索-开发设计范式分类完成（20 算法映射）
- [x] 9 项关键调研发现论述完成（含 Camacho-Villalón 2023、Castelli 2022 两条独立批判线）
- [x] 20 算法交易机器人适配度评分完成
- [x] 四阶段 Conclusions 叙事线完成（奠基 / 早期衍生 / Mirjalili-surge / 后批判时代）
- [x] 8 类参考文献补充完成
- [ ] 提炼为 1–2 页送审版 (待 Deliverable 1 合并时裁剪)
