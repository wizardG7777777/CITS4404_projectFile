# Deliverable 1 (Part One) 研究指南与算法清单

本文档旨在为所有后续参与 CITS4404 交易机器人项目 Deliverable 1（算法概要与文献综述）研究的 Agent 或团队成员提供明确的行动指南和算法调查清单。

---

## 一、 核心研究目标

根据项目指南（`project_guidelines.txt`）及评分标准（`Deliverable_1_Rubric.md`），第一阶段的核心任务是：
1.  **独立算法概要 (Algorithm Synopses)**：深入调查选定的自然启发式优化算法，每种算法撰写 1-1.5 页的概要，**必须回答 6 个核心问题**。
2.  **综合对比分析 (Comparative Analysis)**：在报告结论部分（1-2 页），从分类学、时间演进及机制等维度对所选算法进行深度横向对比。

---

## 二、 预计调查的算法清单 (Algorithm Roster - 20个候选池)

在前期广泛调查阶段，团队成员（共2人）需各自认领 10 个算法进行初步调研。为了保证最终对比分析的质量，以下从数据库中精选了 20 个具有代表性的群体智能（及高度相关）算法，涵盖了从 1992 到 2020 年的发展脉络：

### 成员 1 负责清单 (重点：经典奠基与早期衍生)
1. **Ant Colony Optimization (ACO, 1992)** - 蚁群优化（离散优化经典，路径规划）
2. **Particle Swarm Optimization (PSO, 1995)** - 粒子群优化（连续优化基准，速度-位置模型）
3. **Artificial Bee Colony (ABC, 2007)** - 人工蜂群（模拟采蜜，全局搜索能力强）
4. **Biogeography-based Optimization (BBO, 2008)** - 生物地理学优化（栖息地迁移机制）
5. **Cuckoo Search (CS, 2009)** - 布谷鸟搜索（引入莱维飞行 Lévy flights）
6. **Firefly Algorithm (FA, 2009)** - 萤火虫算法（模拟荧光吸引，适合多峰优化）
7. **Bat Algorithm (BA, 2010)** - 蝙蝠算法（回声定位，频率与脉冲率自动调优）
8. **Fruit Fly Optimization (FFO, 2011)** - 果蝇优化（嗅觉与视觉搜索，极简实现）
9. **Krill Herd (KH, 2012)** - 磷虾群算法（模拟南极磷虾，多目标优化潜力）
10. **Spider Monkey Optimization (SMO, 2014)** - 蜘蛛猴优化（裂变-融合 Fission-Fusion 策略）

### 成员 2 负责清单 (重点：现代自适应与复杂机制)
11. **Grey Wolf Optimizer (GWO, 2014)** - 灰狼优化（严格的社会等级与包围策略）
12. **Chicken Swarm Optimization (CSO, 2014)** - 鸡群优化（公鸡、母鸡和小鸡的等级行为）
13. **Moth-Flame Optimization (MFO, 2015)** - 飞蛾扑火优化（横向取向导航，非线性收敛）
14. **Elephant Herding Optimization (EHO, 2015)** - 象群优化（氏族更新与分离算子）
15. **Whale Optimization Algorithm (WOA, 2016)** - 鲸鱼优化（气泡网捕食，自适应平衡机制）
16. **Dragonfly Algorithm (DA, 2016)** - 蜻蜓算法（静态与动态集群行为对比）
17. **Salp Swarm Algorithm (SSA, 2017)** - 樽海鞘群算法（模拟链式运动，简单的数学结构）
18. **Grasshopper Optimization (GOA, 2017)** - 蝗虫优化（模拟幼体与成体的社会交互）
19. **Harris Hawks Optimization (HHO, 2019)** - 哈里斯鹰优化（多阶段围捕，现代高性能代表）
20. **Manta Ray Foraging Optimization (MRFO, 2020)** - 蝠鲼觅食优化（链式、螺旋式及随机翻滚觅食）

---

## 三、 AI 辅助高效调研流水线 (AI-Assisted Survey Pipeline)

面对 20 个算法的庞大阅读量，必须借助 AI（如当前 Agent）建立标准化的流水线作业。团队成员应指挥 Agent 按照以下 3 个步骤执行：

### Step 1: 自动化信息提取 (Automated Extraction)
*   **输入**：向 Agent 提供目标算法的原始 PDF 论文（或要求 Agent 联网检索原始文献）。
*   **指令 (Prompt)**：要求 Agent 严格按照 `Deliverable_1_Rubric.md` 的要求，一次性提取出 **6 个必答问题 (Q1-Q6)** 的答案。
    > *参考 Prompt: "阅读 [算法名称] 的原始论文，并提取以下 6 个信息：1. 解决什么问题？ 2. 前人方法的局限？ 3. 核心创新机制？ 4. 作者如何验证？ 5. 实验具体结果数据？ 6. 该算法在交易机器人参数优化中的潜在优缺点？"*

### Step 2: 机制数学建模分析 (Mathematical Mechanism Check)
*   **目标**：理解算法是如何在“探索（全局搜索）”和“开发（局部收敛）”之间取得平衡的。
*   **指令**：让 Agent 提取论文中的核心更新公式（如 PSO 的速度公式，WOA 的螺旋公式），并用通俗的语言解释公式中各个参数（如惯性权重、收敛因子）的物理意义。

### Step 3: 生成标准化 Markdown 卡片 (Standardized Output)
*   每完成一个算法的调研，要求 Agent 立即输出一份 500-800 字左右的标准化 Markdown 档案卡片（存入 `docs/survey_drafts/` 目录）。
*   这些卡片将作为最终撰写 Deliverable 1（挑选其中最优的算法进行详写）和 Conclusions（进行 20 个算法的演进分类对比）的直接素材库。

---

## 四、 最终交付撰写指南 (Final Writing Guidelines)

任何接手后续文献调研的 Agent，在阅读上述算法的原始论文或相关文献时，**必须**严格按照以下结构提取信息并撰写 Markdown 格式的草稿：

### 核心任务 1：提取 6 个必答问题 (Q1-Q6)
在阅读每种算法的文献时，请务必寻找并总结以下 6 个维度的答案（缺一不可）：
1.  **Problem (解决什么问题)**：原算法旨在解决的特定优化问题或应用场景是什么？
2.  **Previous failures (前人的局限)**：在它提出之前，现有的优化方法（如传统数学方法或其他早期启发式算法）存在哪些不足？
3.  **Novelty (核心创新)**：该算法引入了什么新思想或独特的仿生学机制？
4.  **Demonstration (验证方法)**：作者是如何证明该算法有效的？（例如：使用了哪些标准基准测试函数或工程问题？）
5.  **Results (实验结果)**：原作者得出了什么结论？（需要具体的数据/指标支撑，证明其优越性）。
6.  **Assessment (主观评价)**：该算法的优缺点是什么？它在本项目（加密货币交易机器人的参数优化）中具有怎样的应用潜力？

### 核心任务 2：为综合对比收集素材 (Comparison Prep)
在独立分析的同时，请随时记录可用于对比分析的素材：
*   **机制对比**：PSO 的“速度-位置”更新与 WOA 的“气泡网螺旋”更新在数学本质上有何异同？
*   **平衡策略**：两者在处理“探索（全局搜索）”与“开发（局部收敛）”的平衡时，策略有何不同？
*   **演进脉络**：从 1995 年的 PSO 到 2016 年的 WOA，群体智能算法在设计哲学上发生了怎样的演变？

### 核心任务 3：格式与合规性约束
*   **引用规范**：所有引用的文献、数据和图表，必须在草稿末尾以严格的 **IEEE 格式** 列出参考文献。
*   **工具使用**：如果需要从 PDF 中提取文本或从 CSV 中查找数据，**必须优先使用项目提供的 `toolkit` CLI 工具**（例如 `uv run python -m toolkit pdf find-keyword ...`），避免编写一次性的处理脚本。
*   **交付格式**：所有输出均采用 **Markdown** 格式（代替 PDF 和 `.ipynb`），并确保字数精炼。
