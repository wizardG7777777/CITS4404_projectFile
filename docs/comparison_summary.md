# 算法对比总结：PSO vs WOA

> **项目**: CITS4404 Team Project — Building AI Trading Bots  
> **对比对象**: Particle Swarm Optimization (PSO) vs Whale Optimization Algorithm (WOA)  

---

## 1. 选择理由 (Why These Two Algorithms?)

本团队选择 **PSO (1995)** 和 **WOA (2016)** 作为研究对象，基于以下考量：

1. **时间跨度清晰**：相隔 21 年，直接展示群体智能算法从经典到现代的演进脉络。
2. **文献基础扎实**：PSO 是历史上引用量最高的优化算法之一；WOA 是 2016 年后最成功的新兴算法之一（原始论文自带 29 个数学 benchmark + 6 个工程问题）。
3. **实现复杂度相近**：两者都只需少量代码即可实现，适合 Part 2 的交易机器人参数优化。
4. **已有直接对比**：WOA 原始论文中已将 PSO 作为主要 benchmark 之一，这为 Part 2 的实验设计提供了天然的文献依据。
5. **同属 population-based**：完全满足项目对“至少一个（建议全部）为 population-based”的约束。

---

## 2. 核心差异一览

| 维度 | PSO (1995) | WOA (2016) |
| :--- | :--- | :--- |
| **自然隐喻** | 鸟群飞行 / 鱼群游动 | 座头鲸气泡网捕食 |
| **核心机制** | 粒子速度更新 = 惯性 + 个体历史最佳 + 全局最佳 | 收缩 encircling + 对数螺旋攻击 + 随机搜索 |
| **信息传递方式** | 所有粒子共享全局最佳位置 `g_best` | 鲸鱼围绕当前最佳解 `X*` 进行螺旋/收缩运动 |
| **探索-开发切换** | 依赖速度惯性，无显式阶段切换 | 通过参数 `a` 从 2→0 自适应控制 `\|A\|` 的大小，实现显式切换 |
| **参数数量** | 惯性权重 `w` + 学习因子 `c1, c2`（原始版为 `c1, c2` 两个常数） | 主要参数 `a`（线性递减）+ 螺旋常数 `b` |
| **数学优雅性** | 简单线性速度/位置更新 | 创新性地引入对数螺旋 `e^(bl) · cos(2πl)` |
| **原始 benchmark 规模** | 1 个 GA 测试函数 + 1 个神经网络任务 | 29 个数学函数 + 6 个工程设计问题 |
| **源代码公开** | 广泛传播但非作者官方首发 | 作者主动公开 MATLAB/Python 源码 |

---

## 3. 它们属于同一主题变体，还是不同本质？

**结论：同一“ swarm intelligence ”大主题下的深度变体，而非简单 patch。**

从分类学 (taxonomy) 角度看：
- 两者都属于 **Swarm-based / Swarm Intelligence** 算法（与自然进化算法、物理启发算法并列）。
- 它们都维护一个候选解种群，并通过种群成员之间的信息共享来引导搜索。

但从机制本质上看，差异显著：
- **PSO 是“速度驱动”的**：粒子靠速度向量在搜索空间中飞行，最佳解通过速度调整间接吸引粒子。
- **WOA 是“位置驱动”的**：鲸鱼直接根据与最佳解的距离，通过几何变换（收缩圆 + 对数螺旋）更新位置。

打个比方：
- PSO 像一群鸟通过调整飞行速度和方向，逐渐向食物源靠拢。
- WOA 像一群猎手通过包围圈和螺旋冲锋，直接向猎物发起攻击。

这种差异不是参数微调，而是**搜索动力学 (search dynamics)** 的根本不同：
- PSO 的收敛是渐进的、基于动量的。
- WOA 的收敛是阶段性的（早期大范围搜索 → 后期螺旋收紧），且螺旋路径允许非线性的局部探索。

---

## 4. 对交易机器人优化的启示

在 CITS4404 项目中，交易机器人是一个**多维连续优化问题**（例如：SMA/LMA/EMA 权重、窗口长度、触发阈值等）。两个算法在此场景下的适用性对比如下：

| 评估维度 | PSO | WOA | 备注 |
| :--- | :--- | :--- | :--- |
| **实现速度** | ★★★★★ | ★★★★★ | 两者都可在 <30 行代码内实现 |
| **高维适应性** | ★★★★☆ | ★★★★☆ | PSO 有大量高维变体；WOA 原始版在高维上可能收敛偏慢 |
| **局部最优规避** | ★★★☆☆ | ★★★★☆ | WOA 的螺旋机制和随机搜索有助于跳出局部最优 |
| **收敛稳定性** | ★★★★☆ | ★★★★☆ | PSO 经典但易早熟；WOA 后期收敛加速但精度有争议 |
| **文献对比依据** | ★★★★★ | ★★★★★ | WOA 原始论文已直接对比 PSO，方便 Part 2 引用 |

**Part 2 实验设计建议**：
- **主实验**：分别用 PSO 和 WOA 优化同一组交易机器人参数。
- **对照组**：可加入 Simulated Annealing (SA) 作为 single-state baseline。
- **公平比较**：固定评估函数（back-testing fitness）和最大迭代次数/评估次数，比较最终收益、收敛曲线、以及参数稳定性。

---

## 5. 相关时间线与分类图 (Taxonomy)

### 时间线视角

```
1992  ACO (蚁群) ──┐
1995  PSO (粒子群) ─┤── 经典 Swarm Intelligence 奠基期
2007  ABC (人工蜂群)─┘
2009  GSA (引力搜索) ── Physics-based 兴起
2014  GWO (灰狼) ──┐
2015  MFO (飞蛾)   ─┤── 现代 Bio-swarm 爆发期
2016  WOA (鲸鱼)   ─┘
2017  SSA (樽海鞘)
2019  HHO (哈里斯鹰)
```

### Taxonomy 简图

```
Nature-Inspired Optimization Algorithms
├── Evolution-based (GA, DE)
├── Physics-based (GSA, MVO, SCA, SA)
└── Swarm-based (Population-based)  ← 本团队选择此分支
    ├── Foraging (ACO, ABC, BFO)
    ├── Flocking/Schooling (PSO, FSS)
    └── Hunting (GWO, WOA, HHO)
        ├── Wolf pack hunting → GWO
        └── Bubble-net hunting → WOA
```

PSO 和 WOA 都处于 **Swarm-based → Hunting/Flocking** 这一分支，但 WOA 的“气泡网攻击”是狩猎行为的一个独特子类，这是它区别于 PSO 的本质特征。

---

## 6. 最终结论

PSO 和 WOA 代表了群体智能算法在 **21 年间**的两个重要节点：

- **PSO** 证明了：极其简单的社会信息共享规则（速度更新）就可以产生强大的优化能力。它是“简洁即力量”的典范。
- **WOA** 证明了：引入更精细的生物隐喻（螺旋攻击、自适应包围）可以在保持简单性的同时，提升探索-开发的平衡，并在现代 benchmark 上超越经典方法。

对于本项目的交易机器人优化任务，两者都是**可行且文献充分的 candidate**。最终选择哪一个在 Part 2 中实现，可以取决于实验结果；但从文献综述角度，这一对算法构成了一个**逻辑清晰、对比鲜明、且具有时间纵深的优秀研究组合**。

---

## 文档状态
- [x] 选择理由完成
- [x] 核心差异对比完成
- [x] Taxonomy 与时间线完成
- [x] Part 2 实验设计建议完成
- [x] 附录 A：独立第三方 PSO vs WOA 对比
- [x] 格式与引用统一检查完成（2026-04-20）

---

## 附录 A: 独立第三方 PSO vs WOA 对比研究

为避免完全依赖 Mirjalili 2016 原始论文的自我评估，以下列出独立第三方在不同问题域对 PSO 与 WOA 的经验对比。完整引用信息见文末 **References** 一节。

### A.1 文献条目

**[1] 机械臂路径规划（KUKA KR4 R600）.** Elgohr et al. [1] 在 KUKA KR4 R600 六自由度机械臂的路径规划问题上并列对比 PSO 与 WOA，使用相同的适应度函数（路径长度 + 关节平滑度）与相同的评估预算。结果显示 WOA 在最终路径代价上略优于 PSO，但 PSO 收敛更快、方差更小；两者在避障可行性上表现相当。该研究采用了**独立于 Mirjalili 2016 的工程 benchmark**（真实机械臂而非合成 CEC 函数），因此在方法论继承性上偏见较小，是较为公允的第三方对比。

**[2] WOA 系统综述.** Nadimi-Shahraki 等 [2] 汇总了 2016–2022 年间百余篇 WOA 相关文献中 PSO 作为 baseline 的对比实验。综述指出：在 Mirjalili 原始 29 函数套件上 WOA 多数情况下优于标准 PSO，但在**高维（D≥100）单峰函数**与 **CEC2017 shifted/rotated** 测试中，WOA 精度明显下滑，而经过惯性权重调度的 PSO 变体可反超。作者明确指出 WOA 在静态参数、早熟收敛上的缺陷。该综述仍大量引用 Mirjalili 2016 的 benchmark，因此存在**方法论继承偏见**。

**[3] 电力系统最优潮流（OPF）.** 在 IEEE-30 节点电力系统的 OPF 问题上 [3] 对比 PSO 与 WOA。目标函数为总发电燃料成本最小化。作者报告 WOA 在最终成本上以约 1.2–2% 优于 PSO，并且约束违反次数更少。基准完全来自电力系统文献（非 Mirjalili 合成函数），属于**独立工程 benchmark**。但 IJERT 属会议级别期刊，审稿深度有限，结果的稳健性需保留判断。

### A.2 综合判断

独立文献**部分支持**但并未完全确认 Mirjalili 2016 "WOA ≥ PSO on most problems" 的论断。观察到的模式是：
- **WOA 在工程设计/OPF/路径规划等低-中维约束问题**上略胜一筹，这与其螺旋-收缩机制利于快速收敛到可行域有关；
- **PSO 在高维、多峰、shifted benchmarks** 上仍具竞争力，尤其配合线性递减惯性权重；
- 大量比较沿用了 Mirjalili 原始 benchmark 套件，存在**方法论继承偏见**，限制了结论的外推性。

关键上下文：Camacho-Villalón 等 [4] 通过组件级分析指出，WOA 实质上是 PSO 的弱变体，其"气泡网攻击"的数学形式与带权速度更新等价。这意味着实证上的微弱优势很可能源于**参数调度差异**而非本质的算法新颖性——符合 No-Free-Lunch 定理的预期。因此 Part 2 实验应强调**公平参数调优**，避免把调参红利当作算法差异。

---

## References

[1] A. T. Elgohr, M. A. Elazab, M. S. Elhadidy *et al.*, "Particle swarm optimization vs. whale optimization algorithm for robotic arm path planning: A controlled study on the KUKA KR4 R600," *Results in Engineering*, 2025. (Tavily-verified 2026-04-20 via ResearchGate/OiPub; pagination pending library confirmation.)

[2] M. H. Nadimi-Shahraki, H. Zamani, Z. Asghari Varzaneh, and S. Mirjalili, "A systematic review of the whale optimization algorithm: Theoretical foundation, improvements, and hybridizations," *Archives of Computational Methods in Engineering*, 2023. DOI: 10.1007/s11831-023-09928-7

[3] M. Sultan, "Comparison of particle swarm and whale optimization algorithms for optimal power flow solution," *Int. J. Eng. Res. & Technology (IJERT)*, vol. 11, no. 12, Dec. 2022. (Tavily-verified 2026-04-20 via ijert.org.)

[4] C. L. Camacho-Villalón, M. Dorigo, and T. Stützle, "Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms for what they are," *Swarm Intelligence*, 2023.

[5] J. Kennedy and R. C. Eberhart, "Particle swarm optimization," in *Proc. ICNN'95 — Int. Conf. Neural Networks*, Perth, Australia, 1995, vol. IV, pp. 1942–1948, IEEE.

[6] S. Mirjalili and A. Lewis, "The whale optimization algorithm," *Advances in Engineering Software*, vol. 95, pp. 51–67, 2016. DOI: 10.1016/j.advengsoft.2016.01.008

> 说明：[1]–[6] 均已在 `docs/citation_verified.csv` 中标记为 `verified`；[1] 与 [3] 的部分次要字段（[1] 分册/页码、[3] 页码）仍待图书馆数据库最终核验，不影响书目主干的可追溯性。
