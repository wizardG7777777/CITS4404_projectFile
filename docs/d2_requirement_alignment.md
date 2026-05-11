# Deliverable 2 需求对齐表

> 把每个执行步骤、每件交付物、每条合规红线，逐一对齐到 `CITS4404Projects.pdf` 的章节、公式与原文引文。
> 用途：写报告/录视频/做实验时随时回查"我这块对应原文哪条要求"。
>
> **PDF 出处版本**：CITS4404Projects.pdf（仓库根目录）；本文中 `§n.m` 与 `Eq.(k)` 均指该 PDF。
>
> **DDL**：2026-05-24（周日）23:59 AWST。

---

## 0. 团队与 D1 上游约束

- **团队**：Team 20，2 人（Qiurong Chen 24558583 + Yanchen Yu 24256987）
- **D1 终稿**：2099 字，PSO + HHO 两份 synopsis + Comparative Analysis（见 `1951.pdf` / 上传归档）
- **D1 → D2 的叙事钩子**："HHO 的多模态结构 vs PSO 的单更新规则"——D1 已经把这场比较从 CEC 基准定位到本项目 7–21 维粗糙 fitness 上，D2 直接接住做实证

---

## 1. 三件交付物 → PDF 原文

### 1.1 视频（Presentation）

- **PDF 出处**：§4 *Presentation* + §5 *Submissions*
- **时长上限**：≤25 分钟
- **必须覆盖的 6 段内容**（直接引文）：
  1. "A short overview of the algorithms you examined in Part 1, along with any other optimisation algorithms you tested in your practical work."
  2. "A discussion of the considerations that went into choosing your bot configuration (and hence hypothesis space) and the parameterisation that results from it."
  3. "Your algorithm selection ... Why did you choose to test the algorithms that you did? ... A high level explanation of the optimisation algorithm(s) chosen and how they work. The explanation may make use of diagrams and/ or pseudocode rather than actual code."
  4. "Your evaluation/testing regime."
  5. "Presentations of results. Visual representations are preferred (images, tables, animations, simulations)."
  6. "Conclusions from your work."
- **格式**：MP4 文件 或 YouTube/Google Drive 链接；Drive 必须 "access permissions are set to 'Anyone with the link can view'"；链接放进报告里

### 1.2 报告（Report）

- **PDF 出处**：§4 *Report* + §5 *Submissions*
- **字数**：≤3000 字（**不含图表与参考文献**）
- **封面三件套**：word count + team number + names and student numbers
- **格式**：PDF
- **引用**：IEEE
- **定位（直接引文）**："complement your video, including extra details that could distract from the flow of the presentation. This includes references and links."
- **不需要做的事**：
  - 不重复 PDF 讲义内容："does not need to repeat information from the project specification"
  - 不重复 D1："You may also refer back to the deliverable for Part 1, you do not need to repeat it"
  - 不要塞代码："should not include code, but may refer to code you submitted"

### 1.3 代码（Code）

- **PDF 出处**：§4 *Code*
- **格式**：单 `.ipynb` 文件 + README
- **直接引文**："submit a .ipynb file that includes all your implementation of this project. The code should allow reproduction of the results. Brief instructions for running the code can be included in a README."
- **评分约束**："The coding will not be marked per se, but the results should be repeatable if required."

### 1.4 截止与逾期

- **PDF 出处**：§5 *Deadlines* / *Late Submission*
- DDL：**2026-05-24（周日）23:59 AWST**
- 逾期：48h 内有宽限；第 3 天起每日 -5%；第 7 天后不收

---

## 2. 14 个执行步骤 → PDF 原文逐一对齐

### Task #4 — 冻结 D2 scope

- **PDF 出处**：§3 *Generalisation and Design* / *Choosing Algorithms* / *Data*
- **设计层级**：§3 给出 14 维 / 21 维 / 自由 WMA 三档；Eq.(7) 即 14 维高频复合
- **算法集**：§3 "use one or more algorithms from those you researched. Trying more than one algorithm allows you to make an informed comparison"
- **时间尺度**：§3 "The time scale of your evaluation sequence(s) (for example, minutes, hours, days) is up to you"
- **本项目决定**：PSO + HHO + Random Search baseline；B1（2D 双 SMA） + B2（≈14D Eq.(7)）；日线；2014–2019 训练 / 2020–2022 测试；5 seeds × 5,000 FE

### Task #5 — 建仓库骨架（src/data, src/bot, src/optim, notebooks, results）

- **PDF 出处**：§4 *Code*
- **对齐要点**：最终要凝缩成单 `.ipynb`，目录骨架是为了过程清晰，提交时再合并到 notebook
- **合规**：见第 3 节红线 1 + 2

### Task #6 — 下载并切分 BTC 历史数据

- **PDF 出处**：§3 *Data*
- **直接引文**：
  - "the kaggle repository ... The Bitcoin Historical Dataset provides historical data between (variously) 2014 and 2022 daily, hourly and by the minute"
  - **硬约束**："You should optimise your agent on data prior to 2020, and preserve the data from 2020 onwards for final testing of your optimised bot."
  - "as it's a limited time project, we'll act as if it is the start of 2020"

### Task #7 — 实现 WMA 卷积模块（SMA / LMA / EMA + pad）

- **PDF 出处**：§2.1 *Weighted Moving Averages*
- **逐项对齐**：
  - **SMA**：Eq.(1) 求和形式 + Eq.(2) boxcar 核
  - **LMA**：Eq.(4) 三角核（线性递减权重，归一化系数 2/(N+1)）
  - **EMA**：Eq.(5) 指数核，含 N 与 α 两个超参
  - **Padding**：原文 "we will 'flip' the first part of the sequence over (rotate it 180°)"
  - **卷积形式**：Eq.(3) `SMA = P * K`
- **PDF 给出的代码骨架**（直接照抄即可）：
  ```python
  def pad(P, N):
      padding = -np.flip(P[1:N])
      return np.append(padding, P)
  def sma_filter(N):
      return np.ones(N)/N
  def wma(P, N, kernel):
      return np.convolve(pad(P,N), kernel, 'valid')
  ```

### Task #8 — 实现 bot 类（B1 双 SMA + B2 复合 14 维）

- **PDF 出处**：§2.2 *Crossover* + §2.3 *Building a Bot* + §3 *Generalisation and Design*
- **B1（2D baseline）**：
  - §2.2 "buy when the higher frequency indicator crosses above the lower frequency indicator and sell when the reverse happens"
  - §2.3 给出具体例子（10/20 SMA → 差信号 → sign → Eq.(6) 边沿检测）
- **B2（≈14D，PDF 案例式）**：
  - §3 Eq.(7)：`HIGH = (w₁·SMA(d₁)+w₂·LMA(d₂)+w₃·EMA(d₃,α₃))/Σwᵢ`
  - §3 明文："To optimise our bot in this case we need to optimise a 7-dimensional vector: [w₁,...,w₃, d₁,...,d₃, α₃]"
  - §3 明文："Doing the same for the low-frequency component will give us a 14-dimensional vector to optimise."
- **B3（21D MACD-style）**：§3 提供，**本项目默认不做**，时间富余再加
- **设计哲学要点**：§3 "trade-off between descriptiveness of our language and size of the hypothesis space"——B1 vs B2 的对比正是这个 trade-off 的实证

### Task #9 — 实现回测引擎

- **PDF 出处**：§3 *Evaluation of Bots*
- **五条硬规则**（直接引文，逐条照实现）：
  1. "the bot begins with $1000 USD (and zero bitcoin)"
  2. "each time the bot is holding cash and generates a *buy* signal, it trades all the cash (minus fees) for bitcoin at the current price"
  3. "each time the bot is holding bitcoin and generates a *sell* signal, it trades all its bitcoin for cash (minus fees) at the current price"
  4. "**each transaction attracts a fee of 3%**"
  5. "at the end of the sequence, the bot sells its remaining bitcoin at the final price"
- **fitness 定义**："The *fitness* of the bot is the cash it is holding at the end of the evaluation."
- **可重复性**："Evaluation experiments should be repeatable"

### Task #10 — Optimizer 基类 + Random Search baseline

- **PDF 出处**：§3 *Choosing Algorithms* + *Rules of Engagement*
- **为什么加 baseline**：§3 "A more complete comparison could be achieved by also trying one of the single-state algorithms covered in lectures (eg. direct methods/stochastic/single global optimisation algorithms). In this case you would need to compare the outcome on a fixed number of evaluations (as opposed to, say, generations)."
- **强制自写**：§3 红线 2 "You may not use general optimisation libraries or optimisation code from other sources for this assignment."

### Task #11 — 实现 PSO

- **PDF 出处**：§3 *Choosing Algorithms* + *Rules of Engagement*
- **D1 对齐**：与 Synopsis 1（Kennedy & Eberhart 1995 + Shi & Eberhart 1998 inertia weight 扩展）一致
- **代码引用规则**：§3 "may adapt for your use code provided in conjunction with a specific research paper for a nature-inspired algorithm, providing you acknowledge the code source in both your written and verbal deliverables"
- → 实现里要在文件头注释引用 IEEE 编号；报告/视频也要署源

### Task #12 — 实现 HHO

- **PDF 出处**：同上
- **D1 对齐**：与 Synopsis 2（Heidari et al. 2019）一致——能量门控 E、6 条 update rule（含 Lévy dive）、greedy Y/Z 接收

### Task #13 — 跑训练集完整实验矩阵（5 seeds × 3 algos × 2 bots）

- **PDF 出处**：§3 *Choosing Algorithms* + *Evaluation of Bots*
- **公平对比口径**：§3 "compare the outcome on a fixed number of evaluations (as opposed to, say, generations)" → 用 5,000 FE 而非按代数
- **可重复**：§3 "Evaluation experiments should be repeatable" → 固定 seeds + YAML 配置
- **多算法的目的**：§3 "Trying more than one algorithm allows you to make an informed comparison ... which may help elucidate important differences"

### Task #14 — 测试集回测 + 行为分析

- **PDF 出处**：§3 *Data* + *Generalisation and Design*
- **测试集**：§3 "Typically this testing on unseen data could be used to compare your final bot against bots from other developers"
- **行为分析**：§3 "It will be interesting to look after optimising to see how much weight the bot gives to each component — for example, does it consistently favour one or continue to draw from all three." → 这是 PDF **明文点名**要做的分析
- **泛化警告**：§3 "Of course, success on past sequences of data does not guarantee a strategy will be successful on future sequences!" → 报告/视频要诚实写出 train→test 的退化

### Task #15 — 写报告（≤3000 字，IEEE，PDF）

- **PDF 出处**：§4 *Report* + §5 *Submissions*
- 见 1.2 节
- **额外提醒**：§5 "Text beyond the maximum word count will not be marked"——超字数即被截断不评分

### Task #16 — 录制并剪辑视频（≤25 min）

- **PDF 出处**：§4 *Presentation* + §5
- 见 1.1 节六段 checklist

### Task #17 — 整理 .ipynb + README 提交

- **PDF 出处**：§4 *Code*
- 见 1.3 节

---

## 3. 贯穿全程的合规红线（Rules of Engagement，§3）

| # | 原文（直接引文） | 影响 |
|---|---|---|
| 1 | "You may not use trading bots or code for bots from any other source — all coding for the bot(s) and their evaluation must be written by the team members as an implementation of the building blocks described in this specification." | Task #7 / #8 / #9 — bot 组件全自己写 |
| 2 | "You may not use general optimisation libraries or optimisation code from other sources for this assignment." | Task #10 / #11 / #12 — 不能 `import scipy.optimize`、`pyswarm`、`mealpy` |
| 3 | "You may adapt for your use code provided in conjunction with a specific research paper for a nature-inspired algorithm, providing you acknowledge the code source in both your written and verbal deliverables." | Task #11 / #12 + 报告 + 视频 — PSO（Kennedy & Eberhart）、HHO（Heidari et al.）的引用要在代码注释 + 报告 + 视频中三处署源 |

## 4. 项目本意自查（每周回顾一次）

§3 *Rules of Engagement* 开头列出的"primary purpose"五点，对应到本项目的步骤：

| § 原文目标 | 对应步骤 |
|---|---|
| "Understand the 'pluggable' components as a language for designing bots." | Task #7 + #8 |
| "Use nature-inspired algorithms to generate instances (hypotheses, models) within that language." | Task #11 + #12 |
| "Use the algorithms along with an evaluation function, over real-world data, to adaptively improve those models." | Task #6 + #9 + #13 |
| "Understand and have practical experience with the trade-off between degrees of freedom ... and finding the right balance through experimentation." | B1 vs B2 对比（Task #8 + #13 的实验设计） |
| "Be able to use an experimental design to assess (through fair comparisons) the algorithms." | Task #13 的 5 seeds × 固定 FE 设计 + 统计检验 |

## 5. 提交 checklist（DDL 前最后一遍过）

- [ ] 报告 PDF：≤3000 字，封面有 word count + team number + 姓名 + 学号
- [ ] 报告内含视频链接（若用 Drive，权限是"Anyone with the link"）
- [ ] 视频 ≤25 min，6 段内容齐全
- [ ] 单 `.ipynb` 能从头到尾跑通且复现结果
- [ ] README 写清楚运行步骤
- [ ] 报告内 IEEE 引用：PSO（Kennedy & Eberhart 1995；Shi & Eberhart 1998）、HHO（Heidari et al. 2019）、PDF 提到的 Bitcoin Historical Dataset 来源
- [ ] 代码注释中署源（红线 3）
- [ ] **无** `scipy.optimize` / `pyswarm` / `mealpy` 等通用优化库（红线 2）
- [ ] **无** 任何外部 bot 代码（红线 1）
