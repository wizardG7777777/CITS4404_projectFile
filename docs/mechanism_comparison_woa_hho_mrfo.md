# WOA / HHO / MRFO 机制深度对比 — 为 Conclusions 章节准备的素材

> **用途**：为 Deliverable 1 的 Conclusions (1–2 页对比章节) 预留数学层面的对比证据，避免 Conclusions 沦为"三个比喻并列"的叙事。
> **范围**：只覆盖 WOA(2016)、HHO(2019)、MRFO(2020) 三个一档候选；PSO 作为隐式基线（三者都与它有可测的数学距离）。
> **方法**：将三个算法的核心更新规则写在同一套符号下，用五个机制轴对齐差异。

---

## 1. 统一符号

所有三个算法都可以写成如下骨架：

$$
\mathbf{x}_i(t+1) = \mathbf{A}(t,\,\mathbf{x}_\star,\,\text{context}) + \mathbf{V}(t,\,\mathbf{x}_i(t),\,\mathbf{x}_\star,\,\xi)
$$

- $\mathbf{A}(\cdot)$：**吸引点**（attractor）——可能是 $\mathbf{x}_\star$（当前最优）、某随机个体 $\mathbf{x}_{\text{rand}}$、群体质心 $\mathbf{x}_m$、或前一只个体 $\mathbf{x}_{i-1}$。
- $\mathbf{V}(\cdot)$：**位移项**——可能是线性收缩、对数螺旋、Lévy 重尾、或反射。
- $\xi$：**该步引入的随机源**（以 `U(0,1)`、`N(0,1)`、Lévy 分布等形式入场）。

在这套骨架下，三个算法的差异**可以完全归结到四个问题**：
1. 吸引点 $\mathbf{A}$ 有几种选择，何时切换？
2. 位移 $\mathbf{V}$ 的几何形状是什么？
3. "探索 vs 开发" 的切换机制是什么？
4. 每次迭代的随机源有多少个，代价多大？

---

## 2. 更新规则分解（同一符号下并列）

### 2.1 WOA — 两模式 + 50/50 抛硬币

| 模式 | 触发条件 | 吸引点 $\mathbf{A}$ | 位移 $\mathbf{V}$ |
|:---|:---|:---|:---|
| **收缩包围** | $p<0.5$, $\|A\|<1$ | $\mathbf{x}_\star(t)$ | $-A\cdot\|C\,\mathbf{x}_\star - \mathbf{x}\|$ |
| **随机搜索** | $p<0.5$, $\|A\|\ge 1$ | $\mathbf{x}_{\text{rand}}(t)$ | $-A\cdot\|C\,\mathbf{x}_{\text{rand}} - \mathbf{x}\|$ |
| **对数螺旋** | $p\ge 0.5$ | $\mathbf{x}_\star(t)$ | $\|\mathbf{x}_\star-\mathbf{x}\|\cdot e^{bl}\cos(2\pi l)$ |

系数：$A = 2a\,r - a$，$a: 2\to 0$（线性）；$C = 2r$；$l\sim U(-1,1)$；$p\sim U(0,1)$。

**机制本质**：**单一连续退火参数 $a$** 把 $|A|$ 从宽带（探索）压到窄带（开发），但是否走收缩还是螺旋由**无记忆的 50/50 抛币**决定。

### 2.2 HHO — 两阶段 × 多模式 + Lévy 跳跃 + 贪心接受

$$
E(t) = 2\,E_0\left(1-\frac{t}{T}\right),\quad E_0\sim U(-1,1)
$$

| 模式 | 触发条件 | 吸引点 $\mathbf{A}$ | 位移 $\mathbf{V}$ |
|:---|:---|:---|:---|
| **探索 a** | $\|E\|\ge 1$, $q\ge 0.5$ | $\mathbf{x}_{\text{rand}}$ | $-r_1\|\mathbf{x}_{\text{rand}}-2r_2\mathbf{x}\|$ |
| **探索 b** | $\|E\|\ge 1$, $q<0.5$ | $\mathbf{x}_\star - \mathbf{x}_m$ | $-r_3(\text{lb}+r_4(\text{ub}-\text{lb}))$ |
| **软包围** | $\|E\|\ge 0.5$, $r\ge 0.5$ | $\Delta\mathbf{x}=\mathbf{x}_\star-\mathbf{x}$ | $-E\|J\,\mathbf{x}_\star-\mathbf{x}\|$ |
| **硬包围** | $\|E\|<0.5$, $r\ge 0.5$ | $\mathbf{x}_\star$ | $-E\|\Delta\mathbf{x}\|$ |
| **软俯冲** | $\|E\|\ge 0.5$, $r<0.5$ | 先试 $Y$，再试 $Z=Y+S\cdot\mathrm{LF}(D)$ | 贪心取 $f$ 更小者，否则不动 |
| **硬俯冲** | $\|E\|<0.5$, $r<0.5$ | 同上但 $Y$ 中用 $\mathbf{x}_m$ 替代 $\mathbf{x}$ | 同上 |

系数：$J = 2(1-r_5)$ 是"捕食者跳跃强度"；$\mathrm{LF}(D)$ 用 Mantegna 算法（$\beta=1.5$）抽 Lévy 步长。

**机制本质**：**两层门控** —— $|E|$ 决定探索 vs 开发（并且因 $E_0$ 的符号随机使得 $E$ 在衰减包络内**符号振荡**，允许晚期再探索）；在开发阶段 $r$ 又决定"besiege vs dive"。俯冲模式的 $Y/Z$ 贪心接受是三个算法里**唯一**带显式 local-improvement filter 的设计。

### 2.3 MRFO — 三算子 + 链式顺序 + 后置 somersault

$$
\alpha = 2r\sqrt{|\log r|},\quad \beta = 2\exp\!\left(r_1\,\frac{T-t+1}{T}\right)\sin(2\pi r_1)
$$

| 模式 | 触发条件 | 吸引点 $\mathbf{A}$ | 位移 $\mathbf{V}$ |
|:---|:---|:---|:---|
| **链式觅食** | $\mathrm{Rand}<0.5$ | $\mathbf{x}_{i-1}$ + $\mathbf{x}_\star$ | $r(\mathbf{x}_{i-1}-\mathbf{x}_i) + \alpha(\mathbf{x}_\star-\mathbf{x}_i)$ |
| **开发旋涡** | $\mathrm{Rand}\ge 0.5$, $t/T>\mathrm{Rand}$ | $\mathbf{x}_\star$（紧缩） | $r(\mathbf{x}_{i-1}-\mathbf{x}_i) + \beta(\mathbf{x}_\star-\mathbf{x}_i)$ |
| **探索旋涡** | $\mathrm{Rand}\ge 0.5$, $t/T\le\mathrm{Rand}$ | **$\mathbf{x}_{\text{rand}}$（随机中心）** | $r(\mathbf{x}_{i-1}-\mathbf{x}_i) + \beta(\mathbf{x}_{\text{rand}}-\mathbf{x}_i)$ |
| **翻跟斗（后置）** | 每代强制执行 | $\mathbf{x}_\star$ | $S(r_2\mathbf{x}_\star - r_3\mathbf{x}_i)$，$S=2$ |

**机制本质**：**主算子的概率切换**（chain vs cyclone）+ **cyclone 内部的时间进度切换**（$t/T$ vs $\mathrm{Rand}$）。最独特的一点是**探索旋涡围绕随机参考点**，而非像 WOA/MFO 那样围绕 $\mathbf{x}_\star$——这让同一个螺旋算子兼做探索和开发。somersault 作为**后置算子**每代对每个个体追加一次独立 fitness 评估，相当于 $2\times$ FE 代价换每代 diversity top-up。

---

## 3. 五个差异轴（一页对比表）

| 机制轴 | WOA | HHO | MRFO |
|:---|:---|:---|:---|
| **更新模式数** | 2（收缩 / 螺旋；$\|A\|$ 内部再分 2 子模式，合计 3） | **6**（2 探索 + 4 开发） | **3 + 后置**（链 / 两种旋涡 + somersault） |
| **吸引点种类** | $\{\mathbf{x}_\star,\,\mathbf{x}_{\text{rand}}\}$ | $\{\mathbf{x}_\star,\,\mathbf{x}_{\text{rand}},\,\mathbf{x}_m,\,\text{边界}\}$ | $\{\mathbf{x}_\star,\,\mathbf{x}_{\text{rand}},\,\mathbf{x}_{i-1}\}$ |
| **位移几何** | 线性 + 对数螺旋 | 线性 + Lévy 重尾（模式 c/d） | 线性 + 正弦指数螺旋 + 反射 |
| **探索-开发切换** | $\|A\| = \|2ar-a\|$ 对 1 的比较，$a$ 单调退火 | $\|E\|$ 包络 + **符号振荡** + $r$ 门控 | 概率 $\mathrm{Rand}$ + 时间进度 $t/T$ |
| **后期再探索** | ✗ $\|A\|\to 0$ 必然收窄 | ✓ $E_0\sim U(-1,1)$ 使 $E$ 在衰减包络内振荡换符号 | ✓ 探索旋涡的激活概率 $(1-t/T)$ 非零 |
| **Heavy-tail 跳跃** | ✗ | ✓ Lévy（$\beta=1.5$）在软/硬俯冲中 | ✗（但 somersault 提供短程反射跳） |
| **Local-improvement filter** | ✗ 每步直接替换 | ✓ $Y/Z$ 贪心接受 | ✓ somersault 后贪心接受 |
| **每代 FE/个体** | 1 | 1（besiege）或 2（dive：测 $Y$ 和 $Z$） | **2**（主算子 + somersault） |
| **独立随机源数** | 3（$r$, $l$, $p$） | 5–6（$q, r_1..r_5, E_0, J$, Lévy） | 5（$\mathrm{Rand}, r, r_1, r_2, r_3$） |
| **可调超参**（除 $N,T$） | $a$ schedule, $b=1$ | 几乎无（阈值硬编码 0.5, 1.0；$\beta_{\text{Lévy}}=1.5$） | $S=2$ 固定 |
| **记忆 / 状态** | 仅 $\mathbf{x}_\star$ | $\mathbf{x}_\star$ + 质心 $\mathbf{x}_m$ | $\mathbf{x}_\star$ + 位置序（index chain） |

---

## 4. 三个"真正有意义的结构差异"（Conclusions 叙事线）

结合上面的轴，三者并不只是"2 种 / 4 种 / 3 种模式"这种数量差别——有**三个结构上的本质差异**，建议在 Conclusions 的对比段落中按以下顺序阐述：

### 4.1 **切换机制**：单退火 vs 符号振荡 vs 双概率门

- **WOA 的切换是单调退火的**。$a: 2\to 0$ 保证 $|A|$ 期望单调下降，所以 WOA 的搜索轨迹在几何上是一个**单调收窄的过程**——早期广撒网，晚期必然收窄到 $\mathbf{x}_\star$ 邻域。
- **HHO 的切换是带符号振荡的退火**。$E = 2E_0(1-t/T)$ 中 $E_0$ 每次迭代都重抽，所以 $E$ 在一个单调衰减的"包络"内**换符号**，意味着即使到了晚期 $|E|$ 也可能偶尔超过 1，触发全局探索阶段。对我们的交易机器人而言，这是**最契合"市场制度突变"语义的机制**——当一个盈利参数区在某个制度下失效时，符号振荡允许种群跳出已收敛的局部。
- **MRFO 的切换是双概率门**。主切换 $\mathrm{Rand}<0.5$ 与模式内的 $t/T\lessgtr\mathrm{Rand}$ 没有耦合，本质是**两个独立的随机决策叠加**。这让 MRFO 的搜索模式更像"三面骰子每代掷一次"，晚期探索概率为 $\Pr[t/T\le\mathrm{Rand}]=1-t/T$，线性递减但永不为零。

### 4.2 **吸引点结构**：单点 vs 多源

WOA 每步只看 $\mathbf{x}_\star$ 或 $\mathbf{x}_{\text{rand}}$。HHO 在探索-b 模式把 $\mathbf{x}_\star$ 和群体质心 $\mathbf{x}_m$ 做差，使得搜索方向包含"种群当前平均形态 vs 最优形态"的信息——这是一种隐性的**群体统计反馈**。MRFO 则用链索引 $\mathbf{x}_{i-1}$，形式上引入了种群顺序结构——但注意 Zhao et al. 2020 自己也承认"链索引是纯索引的，不是基于相似性的"，这点在 `mrfo_synopsis_draft.md` §6 被诚实标记（Li et al. 2022 的高维实验也反映这是一个弱点）。

### 4.3 **Heavy-tail 和 local filter**：直接替换 vs 贪心接受

WOA 每步**无条件替换**旧位置——这是经典群智能的标准做法，但意味着随机扰动可能把一个好解推回差区域。HHO 的俯冲模式对 $Y$ 和 $Z$ 做**显式 greedy acceptance**，把搜索效率从"尝试"升级为"尝试+过滤"。MRFO 的 somersault 同样是贪心的，但是每代**强制**执行一次，相当于把 local filter 做成种群级常规操作。

对我们的优化目标（回测 fitness 是 noisy、单次评估昂贵）而言，这个差异意味着：
- WOA 简单但可能浪费 FE
- HHO 的贪心接受降低 FE 浪费，但在 noisy 目标下可能把伪改进锁死（synopsis 草稿 §6 已标记这个风险）
- MRFO 每代 2× FE 的代价换到了每代 1 次额外 local filter，**预算换质量的取舍最显式**

---

## 5. 与 PSO 的距离（给 Conclusions 用的反批判防御）

Conclusions 最好能正面回应 Camacho-Villalón 2023 对 WOA 的批判（指 WOA 螺旋-收缩可写成 PSO + 调度）。三个算法对 PSO 的"数学距离"可以这样排序：

| 算法 | 与 PSO 的核心差异 | 是否被 Camacho-Villalón 2023 点名 |
|:---|:---|:---:|
| **WOA** | 引入对数螺旋 + 线性退火 $a$，但吸引仍是单点 $\mathbf{x}_\star$；没有动量项 | 家族隶属（六算法之一的变体立场） |
| **HHO** | 吸引点扩展到 $\{\mathbf{x}_\star, \mathbf{x}_{\text{rand}}, \mathbf{x}_m\}$；位移含 Lévy + 贪心过滤；$|E|$ 的符号振荡没有 PSO 对应物 | **未被点名** |
| **MRFO** | 吸引点引入链顺序 $\mathbf{x}_{i-1}$；cyclone 围绕随机参考点是真正新的探索机制；somersault 是后置算子 | **未被点名** |

也就是说，**HHO 和 MRFO 在"是否仅是 PSO 的重新叙事"这个检验上都通过了** —— 它们的机制能在不借助比喻的情况下用上面四个维度（吸引点、位移几何、切换机制、后置算子）与 PSO 区分开。WOA 的独特性主要在对数螺旋的几何形状，但这单点差异在代数上等价于"PSO + 一个特殊调度的位移采样"，这也是 Camacho-Villalón 把它归入家族批判的原因。

**对 Conclusions 的实际意义**：如果我们团队最终选择的是 PSO + WOA + HHO + MRFO，那么 Conclusions 可以这样叙事——

> 我们的四个算法覆盖了从"群智能奠基期的极简单点吸引"（PSO）→"Mirjalili-era 引入单调退火 + 对数螺旋的家族模板"（WOA）→"后批判时代引入多源吸引 + 符号振荡 + 贪心过滤"（HHO）→"后批判时代进一步引入概率门控 + 后置算子"（MRFO）这一条**结构复杂度递增的线**。Camacho-Villalón 2023 的批判在前两者有效（WOA 被家族归类，但 PSO 作为 baseline 本身不受批评），在后两者无效——这正好构成我们 Conclusions 的辨识度。

---

## 6. 实验设计上的三条预测（Part II 可能会观测到）

基于机制差异，可以给 Part II 的实验结果预埋一些可验证的假设：

1. **在稳定趋势段（单一制度）**，三者收敛速度应该接近；WOA 因结构最简可能略快。
2. **在制度切换段**（如 2018 年末熊市突变点），**HHO 的符号振荡应带来比 WOA 更好的再探索能力**——如果观测到 WOA 在制度切换处的 final cash 显著低于 HHO，这是 $|E|$ 符号振荡机制有效的直接证据。
3. **在给定相同 FE 预算下**，MRFO 因 $2\times$ FE 会在"代数"上只跑一半——如果观测到 MRFO 在公平预算下不及 HHO，则是 somersault 代价的直接证据；如果反过来 MRFO 胜，则说明每代 local filter 价值高于代数。

这三条假设可以为 Part II 的 Conclusions 提供**超出 synthetic benchmark 的独立证据**——这正是项目规范 Q5 强调的"how are results validated"。

---

## 7. 小结：两个可融入 Conclusions 的结论

对比得出两个可以直接搬进 Deliverable 1 Conclusions 的判断：

1. **"三个算法不是同一主题的变体"**：它们在吸引点结构、切换机制、后置算子三个轴上都有**结构性**（非参数级）差异。Camacho-Villalón 2023 的批判线明确点名 WOA 隶属家族变体，但在 HHO、MRFO 上不成立——这是机制对比的直接证据，不是信念。
2. **"后批判时代算法为晚期再探索提供了显式机制"**：HHO 的符号振荡 $E$ 和 MRFO 的时间进度概率门都让晚期 diversity 不为零，而 WOA 的 $|A|\to 0$ 保证晚期收窄。对我们这种非平稳的交易环境，这是**三者中最可观测的差异**。

---

## 文档状态

- [x] 统一符号定义
- [x] 三算法更新规则按统一骨架分解
- [x] 五差异轴对比表
- [x] 三条结构差异叙事线（切换 / 吸引点 / local filter）
- [x] 与 PSO 的数学距离分析（反批判防御）
- [x] Part II 实验三条可验证预测
- [ ] 合并进 Deliverable 1 Conclusions（待最终报告整合时裁剪到 1–2 页所需篇幅）
