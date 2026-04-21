# 20 算法选型对照表 — 按 `algorithm_selection_rubric.md` 打分

> **项目**: CITS4404 — Building AI Trading Bots
> **用途**: 为 Deliverable 1 Conclusions + Deliverable 2 算法选型提供证据链
> **打分来源**: 各 synopsis 草稿（`docs/survey_drafts/` + `docs/pso/woa_synopsis_submission.md`）；`classic_list_comparison.md` 里的横向发现
> **打分标记**: ✓ 满足 / △ 部分满足或有缺陷 / ✗ 不满足或未提及 / — 不适用
> **问题画像**: 7 / 14 / 21 维连续（$w_i, \alpha$）+ 整数（$d_i$）混合；目标函数非凸、分段常数（3% 手续费阈值阶跃）；评估代价中-高；无硬约束但需边界；禁用第三方优化库

---

## 1. 总览打分表（B1–B7 聚合）

每个 B 大项的聚合规则：子项 80%+ ✓ → ✓；50-80% → △；<50% → ✗。细节见第 2 节逐项证据表。

| # | 算法 (年份) | B1 搜索空间 | B2 预算经济 | B3 方法学 | B4 可复现性 | B5 实现 | B6 真实新颖性 | B7 团队异质性 | 红旗 | 绿旗 | ★适配度 |
|:--:|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | **PSO** (1995) | ✓ | ✓ | △ | ✓ | ✓ | ✓ | — (基线) | 0 | 4 | ★★★★☆ |
| 2 | **ACO** (1992) | ✗ | ✓ | △ | ✓ | ✓ | ✓ | ✓ | 1 (R1) | 2 | ★☆☆☆☆ |
| 3 | **ABC** (2007) | △ | ✓ | ✓ | ✓ | ✓ | ✓ | △ | 1 (R1) | 2 | ★★★☆☆ |
| 4 | **BBO** (2008) | △ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 0 | 2 | ★★★☆☆ |
| 5 | **CS** (2009) | △ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 0 | 4 | ★★★★☆ |
| 6 | **FA** (2009) | △ | ✗ (O(n²)) | ✓ | ✓ | ✓ | ✓ | ✓ | 0 | 3 | ★★☆☆☆ |
| 7 | **BA** (2010) | △ | △ | △ | ✓ | ✓ | △ | △ | 2 (R4,R5) | 0 | ★★☆☆☆ |
| 8 | **FFO** (2012) | ✗ | △ | ✗ | △ | ✓ | ✗ | △ | 4 (R1-3,R5) | 0 | ☆☆☆☆☆ |
| 9 | **KH** (2012) | △ | △ | △ | △ | △ | △ | ✓ | 1 (R4) | 0 | ★★☆☆☆ |
| 10 | **SMO** (2014) | △ | △ | △ | △ | ✗ | ✓ | ✓ | 2 (R3,R4) | 0 | ★★★☆☆ |
| 11 | **GWO** (2014) | △ | ✓ | △ | ✓ | ✓ | ✗ | △ | 2 (R1,R5) | 2 | ★★★☆☆ |
| 12 | **CSO** (2014) | △ | △ | △ | △ | △ | △ | △ | 2 (R4,R5) | 0 | ★★☆☆☆ |
| 13 | **MFO** (2015) | △ | ✓ | △ | ✓ | ✓ | △ | △ | 2 (R1,R5) | 2 | ★★★☆☆ |
| 14 | **EHO** (2015) | △ | △ | △ | ✓ | ✓ | △ | ✓ | 2 (R1,R5) | 0 | ★★☆☆☆ |
| 15 | **WOA** (2016) | △ | ✓ | △ | ✓ | ✓ | △ | — (基线) | 1 (R1) | 2 | ★★★★☆ |
| 16 | **DA** (2016) | △ | △ | △ | ✗ | △ | △ | ✓ | 3 (R1,R3,R5) | 0 | ★★☆☆☆ |
| 17 | **SSA** (2017) | △ | ✓ | △ | ✓ | ✓ | ✗ | △ | 2 (R1,R5) | 2 | ★★★☆☆ |
| 18 | **GOA** (2017) | △ | △ (O(N²D)) | ✓ | ✓ | △ | △ | △ | 2 (R4,R5) | 1 | ★★☆☆☆ |
| 19 | **HHO** (2019) | ✓ | ✓ | ✓ | ✓ | △ | ✓ | ✓ | 0 | 3 | ★★★★★ |
| 20 | **MRFO** (2020) | ✓ | △ (2× FE) | ✓ | ✓ | △ | ✓ | ✓ | 1 (R4) | 2 | ★★★★☆ |

**★评分依据**：✓ 数量 × 1 − 红旗数 × 0.5 + 绿旗数 × 0.5，再按问题画像权重调整（B1/B5/B6 加权）。

---

## 2. 逐项证据表（B1–B7 细项）

### 2.1 B1 搜索空间契合度

| 算法 | 原生连续 (B1-a) | 整数/混合处理 (B1-b) | ≤30 维 benchmark (B1-c) | 非凸/多模态/阶跃鲁棒 (B1-d) |
|:---|:-:|:-:|:-:|:-:|
| PSO | ✓ | ✗ 无原生，需手动 round | ✓ D=10-30 广泛 | ✓ Schaffer f6 + EEG |
| ACO | ✗ 原生离散 | ✗ 连续需 ACOᴿ 变体（不同算法） | ✗ 仅 TSP | — (N/A) |
| ABC | ✓ 单维扰动 | ✗ 草稿未提 | ✓ D=10/30 | ✓ scout 机制防早熟 |
| BBO | ✓ SIV 级更新 | ✗ 未提 | ✓ D=20 × 14 函数 | △ 混合多模态部分覆盖 |
| CS | ✓ Lévy 步长 | ✗ 未提 | ✓ D=16 Michalewicz | ✓ 重尾飞行天然跳跃 |
| FA | ✓ 距离衰减 | ✗ 未提 | ✓ D≤20 多峰 | ✓ 显式 niching |
| BA | ✓ 速度+位置 | ✗ 未提 | ✓ D=10-40 | △ 多模态覆盖但声称过强 |
| FFO | ✗ 1/‖X‖ 有原点偏倚 | ✗ 未提 | ✗ 原论文仅 1 维 GRNN σ | ✗ 无多峰证据 |
| KH | ✓ Lagrangian 力 | ✗ 未提 | ✓ D=10/30/100 | ✓ 工程约束覆盖 |
| SMO | ✓ 多阶段位置 | ✗ 未提 | ✓ D=10/30/50, 25 CEC2005 | ✓ fission-fusion 专对多峰 |
| GWO | ✓ α/β/δ 加权 | ✗ 未提 | ✓ D=30 × 29 函数 | ✓ Rastrigin/Ackley/Griewank |
| CSO | △ rooster 乘性在零中心参数失效 | ✗ 未提 | ✓ D=20/30 × 12 | △ 乘性更新稳定性不明 |
| MFO | ✓ 对数螺旋 | ✗ 未提 | ✓ D=30 × 29 + CEC2005 | ✓ 多模态 + 火焰递减 |
| EHO | ✓ clan 级更新 | ✗ 未提 | ✓ D=30 × 15 | △ separating 有原点偏倚 |
| WOA | ✓ 收缩+螺旋 | ✗ 未提 | ✓ D=30 × 29 | ✓ 多模态 + 工程 |
| DA | ✓ 5 力合成 | ✗ 未提 | ✓ D=10/30 × 19 + CEC2005 | △ 乘性 Lévy `X+L·X` 偏原点 |
| SSA | ✓ 链拓扑 | ✗ 未提 | ✓ D=10/30/100 | △ 链低通对阶跃响应慢 |
| GOA | ✓ 双极社交力 | ✗ 未提 | ✓ D=10/30 × 19 + CEC2005 | △ 复杂但高维社交力平均化 |
| HHO | ✓ 4 模式位置 | ✗ 未提 | ✓ D=10/30 × 29 + **CEC2017** | ✓ \|E\| 振荡允许晚期 re-explore，对阶跃 PnL 友好 |
| MRFO | ✓ 3 模式位置 | ✗ 未提 | ✓ D≤30 × 23 经典 + **CEC2017** | ✓ somersault 每代 diversity top-up |

**B1 对我们的意义**：所有 20 个算法都没有"原生整数/混合变量"机制——我们统一需要 **四舍五入 $d_i$ + sigmoid/clip $\alpha\in(0,1)$ + 非负化 $w_i$** 的包装层，这不是选型差异。但 **B1-d 对非凸阶跃的鲁棒性** 才是决定性的：**HHO、MRFO、CS、SMO** 这四个明确有跳跃性机制，对 3% 手续费阈值阶跃更友好。

---

### 2.2 B2 评估预算经济性

| 算法 | 种群 × 代数典型预算 | 早停/预算敏感 (B2-b) | 并行化 (B2-c) | 备注 |
|:---|:---|:-:|:-:|:---|
| PSO | 20 × 500 ≈ 10k | ✗ 无原生 | ✓ | 种群评估独立 |
| ACO | 30 × 250 ≈ 7.5k | ✓ 信息素蒸发自然早停 | ✓ | 离散，不适用 |
| ABC | 40 × 1000 ≈ 40k | △ limit 机制 | ✓ | 单维更新 → 高维慢 |
| BBO | 50 × 100 ≈ 5k | △ 迁移率调度 | ✓ | SIV 级移植高效 |
| CS | 25 × 2000 ≈ 50k | △ p_a 静态 | ✓ | 参数最稳健 |
| FA | 30 × 200 ≈ 6k，但每代 O(n²) | △ α_t 衰减 | ✗ 两两吸引需全体见面 | **成本陷阱** |
| BA | 30 × 1000 ≈ 30k | △ 响度衰减 | ✓ | |
| FFO | 50 × 1000 ≈ 50k | △ 无机制 | ✓ | |
| KH | 30 × 1000 ≈ 30k | △ `(1−I/I_max)` 内置退火 | ✓ | 邻居排序 O(n log n) |
| SMO | 50 × ~ 30k | △ 滞后计数触发 | ✓ | 六阶段复杂 |
| GWO | 30 × 500 ≈ 15k | ✗ a 线性固定 | ✓ | |
| CSO | 100 × 1000 ≈ 100k | △ G=10 重排 | ✓ | 预算需求大 |
| MFO | 30 × 1000 ≈ 30k | ✓ 火焰数递减 | ✓ | |
| EHO | 50 × 1000 ≈ 50k | △ 每代 separating | ✓ | |
| WOA | 30 × 500 ≈ 15k | ✗ a 线性固定 | ✓ | |
| DA | 40 × 500 ≈ 20k | △ 5 权重衰减 | ✓ | 邻域半径未指定 |
| SSA | 30 × 500 ≈ 15k | ✓ c1 Gaussian 自适应 | ✓ | **单参数** |
| GOA | 30 × 1000 ≈ 30k | △ c 线性递减 | ✓ O(N²·D) | 成本高 |
| HHO | 30 × 500 ≈ 15k | ✓ \|E\| 包络 | ✓ | |
| MRFO | 25 × 2000 ≈ **2× = 100k** | △ 每代 + somersault | ✓ | **FE 双倍** |

**B2 对我们的意义**：给定每次 fitness = 全段 K 线回测（秒级），我们的 FE 预算现实约 **10k–50k**。**FA (O(n²))、CSO、EHO、GOA (O(N²D))、MRFO (2×FE)** 属于"单代成本高"陷阱；**WOA、GWO、HHO、CS、PSO** 在 15k FE 内完成一次完整 run，最符合预算。

---

### 2.3 B3 方法学可信度

| 算法 | Benchmark 选择 (B3-a) | Baseline 异质 (B3-b) | 统计检验 (B3-c) | 超参数公平调 (B3-d) | NFL 意识 (B3-e) |
|:---|:---|:-:|:-:|:-:|:-:|
| PSO | △ Schaffer f6 + EEG | ✓ vs GA/backprop | ✗ 单次结果 | △ c1/c2 无调 | △ 隐含 |
| ACO | △ TSP Oliver30/Eil50/KroA100 | ✗ vs SA/TS/GA（旧） | ✓ 均值±std | △ α/β/ρ 默认 | — |
| ABC | ✓ Sphere/Rosenbrock/Rastrigin/Ackley | ✓ vs GA/PSO/DE | ✓ 30 runs 均值±std | △ limit 启发式 | △ |
| BBO | △ 14 函数 + Step-Noise | ✓ vs GA/PSO/DE/ACO/ES/PBIL | ✓ 统计显著性 | △ 6 种迁移模型未充分选择 | △ |
| CS | ✓ 7 多峰 + 3 工程设计 | ✓ vs PSO/GA | ✓ **100 独立 runs** | △ α 需 per-problem 缩放 | △ |
| FA | △ 多峰演示 + 工程 | ✓ vs PSO/GA | ✓ Wilcoxon（Fister 2013） | △ γ 敏感 | △ |
| BA | △ Sphere/Rosenbrock/Rastrigin + 工程 | ✓ vs GA/PSO | ✓ 成功率+std | ✗ 6+ 参数未调 | △ |
| FFO | ✗ **仅 1 维 GRNN 应用** | ✗ 无对比 | ✗ 无统计 | ✗ 无扫描 | ✗ |
| KH | △ 20 函数 + 5 工程 | ✓ vs GA/PSO/DE/ABC/FA/CS/BBO/HS | ✓ 30 runs | ✗ 6+ 参数无敏感度 | △ |
| SMO | △ 25 CEC 2005 | ✓ vs ABC/PSO/DE/BBO/GA/CMA-ES | ✓ Wilcoxon | ✗ LLD 策略欠指定 | △ |
| GWO | △ 29 函数 + CEC2005（**无 CEC2014/2017 shifted**） | ✓ vs PSO/GSA/DE/FEP/EP/ES | ✓ 30 runs Wilcoxon | △ a 线性 | △ |
| CSO | △ 12 经典 | ✓ vs PSO/DE/BA | ✓ 100 runs | ✗ 8+ 耦合参数无敏感度 | △ |
| MFO | △ 29 + CEC2005（**无 CEC2014/2017**） | ✓ vs PSO/GA/BA/FPA/GSA/FA/SMS/CS/GWO | ✓ Wilcoxon | △ b=1 固定 | △ |
| EHO | △ 15 函数（**无 shifted CEC**） | ✓ vs BBO/DE/GA/ES/ACO/PBIL | ✓ 50 runs Wilcoxon | ✗ 4 参数无敏感度 | △ |
| WOA | △ 29 + CEC2005（**无 CEC2014/2017**） | ✓ vs PSO/GSA/DE/FEP/**CMA-ES** | ✓ 30 runs | △ b=1 固定 | △ |
| DA | △ 19 + CEC2005 | ✓ vs PSO/GA/GWO/MFO/FA/ABC/CS/BBO/SMS/FPA | ✓ Wilcoxon α=0.05 | ✗ 5 权重 schedule 未定 | △ |
| SSA | △ 14 + 10 + 10 + CEC2005 + 工程 + **多目标** | ✓ vs PSO/GA/GSA/BA/FPA/FA/SMS/GWO/MFO/WOA | ✓ 30 runs Wilcoxon | △ c1 自适应 | △ |
| GOA | △ 19 + CEC2005 + 6 工程 | ✓ vs PSO/GA/GSA/BA/FA/CS/FPA/SMS/DE | ✓ Wilcoxon α=0.05 | ✗ 4 参数线性 ad-hoc | △ |
| **HHO** | ✓ **29 + CEC2017 + 工程** | ✓ vs PSO/DE/GA/GWO/MFO/CS/BAT + 13+ | ✓ 30 runs + Wilcoxon + **Friedman mean-rank** | △ 4 模式阈值硬编码 | △ |
| **MRFO** | ✓ **23 + 30 CEC2017 + 工程** | ✓ vs PSO/GA/GSA/DE/ABC/BA/GWO/WOA/SCA/MFO/CS/DA/SSA | ✓ 30 runs Wilcoxon + Friedman | △ S=2 固定 | △ |

**B3 对我们的意义**：**HHO 和 MRFO 是唯二使用 CEC2017（即 shifted/rotated 现代基准）的算法**，这是 Camacho-Villalón 2023 批判线上的关键区别——Mirjalili-era 的 GWO/MFO/WOA/DA/SSA/GOA 全部未在 shifted CEC 验证，对应 **红旗 R1**。

---

### 2.4 B4 可复现性

| 算法 | 伪代码完整 (B4-a) | 推荐参数+敏感度 (B4-b) | 官方/配套实现 (B4-c) | 公式符号清晰 (B4-d) |
|:---|:-:|:-:|:-:|:-:|
| PSO | ✓ | △ | ✓ 无数实现 | ✓ |
| ACO | ✓ | △ | △ 文献多样 | ✓ |
| ABC | ✓ | △ 无敏感度 | ✓ Python/MATLAB/Java | ✓ |
| BBO | ✓ | △ | ✓ Simon MATLAB | ✓ |
| CS | ✓ | △ | ✓ Python/MATLAB/R 广泛 | ✓ |
| FA | ✓ | △ | ✓ `FireflyAlgorithm` 包 | ✓ |
| BA | ✓ | △ | ✓ | ✓ |
| FFO | ✓ | △ | ✓ 极简 | ✗ `S=1/‖X‖` 定义有原点偏倚 |
| KH | △ 三力耦合 | ✗ | △ Gandomi 站 + Python 参差 | ✓ |
| SMO | △ 六阶段 + LLD 策略欠指定 | ✗ | △ 实现差异大 | △ P_i 公式非标准 |
| GWO | ✓ | ✗ | ✓ 官方 MATLAB + mealpy/niapy | △ \|A\|<1 vs ≥1 分支在部分实现有 bug |
| CSO | △ chick→mother 分配欠指定 | ✗ | △ S2 计算版本差异 | △ rooster 方差公式有歧义 |
| MFO | ✓ | △ | ✓ 官方 MATLAB + mealpy | △ 螺旋在边界数值不稳定 |
| EHO | ✓ | △ | ✓ Wang MATLAB + Python 端口 | ✓ |
| WOA | ✓ | △ | ✓ 官方 MATLAB + 广泛 Python | △ 螺旋 exp(b·l)·D' 边界未指定 |
| **DA** | △ | ✗ | △ 官方 MATLAB，Python 端口在权重/半径上差异 | ✗ **Enemy 项 `E_i = X_enemy + X_i` 代数可疑**（方向相反），多个端口擅自"修正"为减法 |
| SSA | △ 领导/追随切分 | △ | ✓ 官方 MATLAB + mealpy | △ `(ub−lb)·c2 + lb_j` 当 lb<0 时不对称 |
| GOA | △ 边界处理未指定 | ✗ | ✓ mealpy/niapy | △ 双极力分段公式歧义 |
| HHO | ✓ 四模式完整 | △ 阈值硬编码 | ✓ 官方 MATLAB + mealpy/niapy/pyMetaheuristic | ✓ 四模式 + Lévy 清晰 |
| MRFO | ✓ 三模式完整 | △ S=2 硬编码 | ✓ 官方 + mealpy/niapy | △ somersault 边界需 clip |

**B4 对我们的意义**：**DA 的 Enemy 项歧义是团队最大复现风险**——不同端口给出不同实现。**SMO/KH/CSO 的伪代码不完整** 意味着我们必须做大量额外设计决策才能实现。**HHO、MRFO、PSO、WOA、GWO、CS** 的伪代码+官方代码组合最干净。

---

### 2.5 B5 实现复杂度

| 算法 | <100 行 Python (B5-a) | 依赖罕见数学 (B5-b) | 随机性源数量 (B5-c) |
|:---|:-:|:---|:-:|
| PSO | ✓ <20 行 | 无 | 1–2 |
| ACO | ✓ O(n²) 距离 + 信息素 | 无 | 2–3 |
| ABC | ✓ | 无 | 2–3 |
| BBO | ✓ | 无 | 2–3 |
| CS | ✓ | **Lévy (Mantegna + Gamma)** | 3 |
| FA | ✓ ~30 行 | 无 | 2–3 |
| BA | ✓ | 无 | 3–4 |
| FFO | ✓ ~20 行 | 无 | 2 |
| KH | △ 邻居排序 + 三力 >100 行 | 无 | 3–4 |
| SMO | ✗ 六阶段 + fission/fusion >100 行 | 无 | 3–4 |
| GWO | ✓ ~40 行 | 无 | 2–3 |
| CSO | △ 三规则 + 排序 >100 行 | 无 | 3–4 |
| MFO | △ 螺旋 + 排序 + 递减 ~50 行 | 无 | 3–4 |
| EHO | ✓ clan + separating <100 行 | 无 | 2–3 |
| WOA | ✓ ~40–50 行 | 无 | 2–3 |
| DA | △ 5 力项 >100 行 | **Lévy (Mantegna)** | 4–5 |
| SSA | ✓ 链平均 + Gaussian ~50 行 | 无 | 2–3 |
| GOA | △ 双极力求和 + 嵌套 c >100 行 | 无 | 3–4 |
| HHO | △ 四模式分支 >100 行 | **Lévy (Mantegna, β=1.5)** | 4–5 |
| MRFO | △ 三模式 + somersault >100 行 | 无 | 4–5 |

**B5 对我们的意义**：Project spec L384-385 禁止"通用优化库"但允许"改编 nature-inspired 算法的配套代码"，且要自己写。综合 **B5-a + B5-c**（调试难度与代码量），**PSO → ABC → GWO → BBO → WOA → CS → SSA** 是实现最简、调试最快的一档；**SMO、CSO、KH、DA、GOA** 在 100 行之外且随机性源多。HHO/MRFO 虽然 >100 行但结构清晰（四/三模式独立），可按模式分模块写。

---

### 2.6 B6 真实新颖性 vs 隐喻膨胀

| 算法 | 脱隐喻数学表述 (B6-a) | 与 PSO/DE 数学差异 (B6-b) | 仅换比喻？ (B6-c) |
|:---|:-:|:---|:-:|
| PSO | ✓ | 速度累积的认知+社交分离 | ✗（真创新） |
| ACO | ✓ | 信息素正反馈 + 蒸发（异步信息流） | ✗ |
| ABC | ✓ | 角色分化（employed/onlooker/scout）+ 单维扰动 + 放弃计数 | △ |
| BBO | ✓ | 按适应度排序的迁移 + SIV 替换（与 GA 交叉质上不同） | ✗ |
| CS | ✓ | **Lévy 重尾步长 vs PSO 高斯** | ✗ |
| FA | ✓ | **距离衰减 β(r)=β₀e^(-γr²)** → 显式 niching | ✗ |
| BA | △ | PSO 速度 + 频率调谐 + 响度衰减，**April 2017 证为参数化 PSO** | ✓ |
| FFO | △ | 1/‖X‖ 变换 + 贪心，**本质弱化随机搜索** | ✓ |
| KH | △ | 三力 Lagrangian，但数值系数经验 | △ |
| SMO | △ | **Fission-fusion 拓扑变动（清单里唯一）** | ✗ |
| GWO | △ | X(t+1)=(X1+X2+X3)/3 + A·D，**Camacho-Villalón 2023 证等价加权 PSO** | ✓ |
| CSO | △ | 三角色（rooster/hen/chick）+ 周期重排，与 PSO+DE 混合 | △ |
| MFO | △ | 对数螺旋 + 火焰配对，**Camacho-Villalón 证展开后等价阻尼 PSO** | △ |
| EHO | ✓ | Clan + matriarch + separating（空间子群） | △ separating 有原点偏倚 |
| WOA | △ | 收缩包围 + 对数螺旋，**Camacho-Villalón 隐含指为 PSO 变体** | △ |
| DA | △ | 5 力（sep/align/cohesion/food/enemy），**Enemy 项歧义** | △ |
| SSA | △ | 链平均 x_i=(x_i+x_{i-1})/2 + 领导 Gaussian，**Castelli 2022 证本质为衰减 PSO** | ✓ |
| GOA | △ | 双极社交力 s(r)=f·e^(-r/l) − e^(-r) + 嵌套 c，**Camacho-Villalón 批评** | △ |
| **HHO** | ✓ | **4 exploitation 模式 + 符号振荡 E + Lévy dives**，未被"比喻动物园"点名 | ✗ |
| **MRFO** | ✓ | **3 算子（chain/cyclone/somersault）独立消融**，cyclone 围绕随机参考点非 gbest | ✗ |

**B6 对我们的意义**：Conclusions 需要讲"新颖性 vs 隐喻膨胀"的故事，这是项目规范 Q3 的核心。**Camacho-Villalón 2023、Castelli 2022、April 2017** 三条独立同行评审批判线共同点名 **GWO、MFO、WOA、SSA、BA、DA、GOA、FFO** 为"隐喻掩盖下的 PSO 变体"。未被任一批判线点名的 **HHO、MRFO、CS、SMO、BBO、ABC、EHO（部分）** 是真实创新一档。

---

### 2.7 B7 团队组合适配（同异质性）

| 算法 | 与 PSO 异质？ | 年代/谱系特色 |
|:---|:-:|:---|
| PSO | — 基线 | 1995 奠基期，social-velocity flocking |
| ACO | ✓ 跨类别（stigmergy） | 1992 最早，离散组合基因 |
| ABC | △ 同族群智能但角色分化 | 2007 早期衍生期代表 |
| BBO | ✓ 跨类别（ecology / migration） | 2008 早期衍生期罕见生态学派 |
| CS | ✓ Lévy 飞行独立范式 | 2009 Lévy 群智能首次系统应用 |
| FA | △ 距离衰减 niching | 2009 显式多峰机制代表 |
| BA | △ PSO+SA 混合 | 2010 April 2017 已批判 |
| FFO | △ 极简但缺陷 | 2012 警示案例 |
| KH | ✓ Lagrangian 力学框架 | 2012 力学启发的独特设计 |
| SMO | ✓ 动态拓扑（唯一） | 2014 fission-fusion 结构创新 |
| GWO | △ 与 PSO 数学等价（Camacho-Villalón 2023） | 2014 Mirjalili-era 开端 |
| CSO | △ PSO+角色分化 | 2014 中期衍生 |
| MFO | △ 与 PSO 展开等价 | 2015 火焰配对是唯一新颖点 |
| EHO | ✓ 空间子群结构 | 2015 Wang 独立家族 |
| WOA | — 基线 | 2016 Mirjalili-era 顶峰 |
| DA | ✓ 5 力多算子（但歧义） | 2016 概念有趣，实现脆弱 |
| SSA | △ 链拓扑（低通 PSO） | 2017 Castelli 2022 批判 |
| GOA | △ 双极社交力（PSO 变体） | 2017 Mirjalili-era 尾声 |
| **HHO** | ✓ 4 模式多算子（后批判时代） | 2019 **未被比喻动物园点名**，加密 LSTM 应用先例 |
| **MRFO** | ✓ 3 模式多算子（后批判时代） | 2020 **三算子可独立消融**，真正结构新颖 |

**B7 对我们的意义**：与 PSO+WOA 组合出 4 算法队伍时，要避免"四个 PSO 变体"。**最异质的三个是 ACO（跨类）、CS（Lévy）、SMO（动态拓扑）、HHO/MRFO（多算子）**。

---

## 3. 红旗 / 绿旗清单

### 红旗（出现任一项 → 强烈建议换）

| 红旗 | 触发算法 |
|:---|:---|
| **R1** 只在连续 benchmark 验证，未讨论离散/混合 | ACO（反例，只做离散）、所有 20 个都存在整数处理盲点 |
| **R1-shifted** 只在 non-shifted benchmark（未 CEC2014/2017 验证） | GWO、MFO、WOA、DA、SSA、GOA、EHO |
| **R2** 只和自家前作比较 | ~~WOA（与 PSO/GSA/DE/FEP 对比，不是"只自家"）~~；无明显触发 |
| **R3** 伪代码缺关键步骤且无公开代码 | SMO（LLD 策略欠指定）、DA（Enemy 项歧义导致端口分叉）、FFO（算法本身有结构缺陷） |
| **R4** 超参数 ≥5 个且无敏感度分析 | BA（6–7）、KH（6）、CSO（8+）、EHO（4+，边缘）、GOA（4+，边缘）、MRFO（虽 N+T，但硬编码阈值可视为隐形超参） |
| **R5** 新颖性完全建立在隐喻，数学等价已有 | BA（April 2017）、GWO（Camacho-Villalón 2023）、MFO（同）、WOA（同，弱）、SSA（Castelli 2022）、GOA（Camacho-Villalón 2023）、FFO、CSO（Sörensen 式批判） |
| **R6** 只报"最好一次"，无多次运行统计 | PSO 1995 原论文 |

### 绿旗（加权推荐）

| 绿旗 | 触发算法 |
|:---|:---|
| **G1** CEC2017/2019/2020 与多个异质 baseline 公平比较 | **HHO、MRFO** |
| **G2** 超参数 ≤3 或有自适应机制 | CS（p_a, α）、SSA（单 c1 Gaussian）、PSO（c1,c2）、ABC（limit）、GWO（仅 a）、HHO（宣称仅 N,T） |
| **G3** 官方代码且许可允许改编 | PSO、WOA、GWO、MFO、SSA、HHO、MRFO、BBO、FA、CS、ABC、EHO |
| **G4** 原生或成熟的整数/混合变量变体 | 无一触发 ——都要自己包 rounding |
| **G5** 作者坦诚局限 | CS（α 需 per-problem 缩放）、HHO（结合 Lei 2022 独立复现承认局部收敛）；WOA 借 Nadimi-Shahraki 2023 综述自省 |

---

## 4. 综合推荐

### 4.1 一档候选（推荐纳入实验）

| 排名 | 算法 | 推荐理由（一句式） |
|:---:|:---|:---|
| 🥇 1 | **HHO** (2019) | 后批判时代唯一未被点名 + CEC2017 基准 + 4 模式对多制度市场友好 + \|E\| 振荡允许晚期 re-explore 对付阶跃 PnL |
| 🥈 2 | **MRFO** (2020) | 三算子真正消融验证 + CEC2017 + somersault 为每代 diversity top-up；代价是 2× FE 需预算确认 |
| 🥉 3 | **PSO** (1995) | 实现最简、baseline 行业共识、与下面任一算法都有直接 Camacho-Villalón 式对照价值 |
| 4 | **CS** (2009) | Lévy 重尾步长天然契合加密市场跳跃 + 参数最少、最稳健 + 金融 LSTM 先例 |
| 5 | **WOA** (2016) | 已有 synopsis + 原论文含 PSO 对照 + Camacho-Villalón 虽未直接点名但属"隐喻动物园"家族，反倒适合做"批判对照组" |

### 4.2 二档候选（需特定设计动机才选）

- **SMO**（动态拓扑，是本清单中唯一"种群结构可变"的算法，机制上最契合加密多制度，但 R3+R4 同时触发，实现成本高）
- **ABC / BBO**（真实创新但证据偏旧，适合作为"不同家族老算法"的对照）
- **FA**（niching 真实新颖，但 O(n²) 成本 + γ 敏感限制 7 维以上应用——除非把 γ 固定为中等值做快速演示）

### 4.3 不推荐

- **FFO**：结构缺陷，原点偏倚已被 Iscan 2014 等独立证实
- **DA**：Enemy 项歧义 + 乘性 Lévy 双重可重复性风险
- **EHO**：separating 算子有 box-midpoint 偏倚
- **BA**：April & Iglesias 2017 证为参数化 PSO，新颖性透支
- **GWO / SSA**：Camacho-Villalón / Castelli 点名为 PSO 变体；若入选也应选 I-GWO 2021 等改良版（超出草稿范围）
- **纯 ACO**：离散不适用于连续 7-21 维问题；若要用需 ACOᴿ（不同算法）

### 4.4 最终队伍建议（4 人团队）

按 B7 异质性 + B1-d 多模态能力 + B5 实现可行性三维平衡：

- **成员 1 — PSO**（行业共识基线）
- **成员 2 — WOA**（已提交，且是 Mirjalili-era 代表；可承担"批判对照"角色）
- **成员 3 — HHO** 或 **CS**（HHO 是后批判时代旗舰；CS 是 Lévy 步长代表，实现更简单）
- **成员 4 — MRFO** 或 **SMO**（MRFO 三算子最现代；SMO 动态拓扑最契合多制度市场）

两种组合都跨越"奠基 → Mirjalili-era → 后批判时代"三个时代，且包含 A（显式调度）、B（停滞触发）、C（概率混合）三种探索-开发范式（见 `classic_list_comparison.md` §4），Conclusions 的 chronology/taxonomy 叙事线完整。

---

## 文档状态

- [x] 20 算法 B1–B7 聚合打分完成
- [x] 6 张逐项证据表完成（B1/B2/B3/B4/B5/B6/B7）
- [x] 红/绿旗触发清单完成
- [x] 一档/二档/不推荐候选分级完成
- [x] 4 人队伍建议方案完成
- [ ] 与 `comparison_summary.md` 合并进 Deliverable 1 Conclusions（待报告合并阶段）

## 引用

本表打分依据的三条独立同行评审批判线：

1. K. Sörensen, "Metaheuristics—the metaphor exposed," *ITOR*, vol. 22, no. 1, pp. 3–18, 2015.
2. C. L. Camacho-Villalón, M. Dorigo, T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms," *ITOR*, vol. 30, no. 6, pp. 2945–2971, 2023.
3. M. Castelli, L. Manzoni, L. Mariot, M. S. Nobile, A. Tangherloni, "Salp Swarm Optimization: A critical review," *Expert Systems with Applications*, vol. 189, art. 116029, 2022.
4. A. April, A. Iglesias, "A critical analysis of the 'improved' bat algorithm," *Applied Mathematics and Computation*, vol. 273, pp. 830–848, 2017.
5. H. Iscan, Ş. Gülcü, "Disadvantages of fruit fly optimization algorithm," *Proc. EANN*, 2014.

原始算法论文及各算法 synopsis 草稿中的引用请见各 `*_synopsis_draft.md` 与 `classic_list_comparison.md` §8。
