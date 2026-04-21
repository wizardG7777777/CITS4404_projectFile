# HHO Synopsis 核查报告 #1

**日期**: 2026-04-21  
**核查人**: Tavily 代理（网络核实）+ 本地 Toolkit 静态检查  
**核查对象**: `docs/hho_synopsis_submission.md`（Harris Hawks Optimization Synopsis）  
**数据来源**: Heidari et al. 2019 原论文 PDF（*Future Generation Computer Systems*, Vol. 97, pp. 849–872, DOI: 10.1016/j.future.2019.02.028）

---

## 一、核查方法

1. **本地静态检查**：使用项目 `toolkit` 运行 `check structure`, `check equations`, `check comparison`, `check format`, `check citations` 五项检查。
2. **网络搜索核实**：使用 `tvly` 搜索工具对 9 条待查断言进行交叉验证。
3. **原论文 PDF 提取**：通过公开渠道获取 HHO 原论文 PDF（24 页），使用 `pdfplumber` 提取全文文本，直接定位到表格、公式、引言和参考文献的原文。

---

## 二、Toolkit 本地检查结果速览

| 检查项 | 状态 | 说明 |
|--------|------|------|
| `structure` | ✅ 通过 | Q1–Q6 六个必答章节齐全 |
| `equations` | ✅ 通过 | 检测到 1 个公式代码块 |
| `comparison` | ⚠️ 8 warnings | ACO/ABC/FFO/KH/CSO/EHO/GOA/MRFO 未提及（synopsis 为单算法分析，可接受） |
| `format` | ❌ 1 error | **Team Statement heading 缺失** |
| `citations` | ⚠️ 1 warning | Reference [5] 不在 `citation_verified.csv` 中 |

> **独立发现**：Reference [5] 作者名错误（`J. L. Bednarz` → 应为 `J. C. Bednarz`），DOI 10.1126/science.239.4847.1525、卷号页码均正确。

---

## 三、逐条核查详情

### ① 第 5 节表格："Unimodal F1–F7 | Top-ranked on 6 of 7"

**待验证断言**：原论文 Table 3 中，HHO 在 7 个单模态函数里有 6 个取得最佳均值。

**原论文依据**（Section 4.2, Table 3）
> "As per result in Table 3, the HHO can obtain the best results compared to other competitors on **F1–F5, F7**"

**判定**：✅ **正确**。原论文明确列出 HHO 在 F1、F2、F3、F4、F5、F7 上取得最佳均值，即 **6 of 7**。

**建议改文**：无需修改。

---

### ② 第 5 节表格："High-dim multimodal F8–F13 | Top-ranked on 5 of 6"

**待验证断言**：原论文 Table 4（实为 Table 3 的延续）中，HHO 在 6 个高维多模态函数里有 5 个取得最佳均值。

**原论文依据**（同上 Table 3）
> "and **F9–F13**"

**判定**：✅ **正确**。F9、F10、F11、F12、F13 共 5 个函数，即 **5 of 6**。

**建议改文**：无需修改。

---

### ③ 第 5 节表格："Composite F24–F29 (CEC 2005) | Top-ranked on majority"

**待验证断言**：F24–F29 上 HHO 在多数函数上排名靠前。

**原论文依据**（Section 4.4, Table 8）

原论文 Table 8 的 AVG 数据（30 维，HHO 为第 1 列）：

| Function | HHO | 次优 |
|---------|-----|------|
| F24 | 396.83 | 412.46 (CS) |
| F25 | 910.00 | 910.10 (HHO 自身 std≈0) |
| F26 | 910.00 | 910.13 (HHO 自身) |
| F27 | 910.00 | 910.12 (HHO 自身) |
| F28 | 860.89 | 1016.39 (CS) |
| F29 | 558.97 | 1882.97 (GWO) |

**判定**：✅ **正确，且可强化为精确数字**。HHO 在 **全部 6 个** F24–F29 函数上均为最佳均值。

**建议改文**：将 "top-ranked on majority" 强化为 **"top-ranked on all 6"** 或 **"top-ranked on 6 of 6"**，以反映原论文的实际数据。

---

### ④ 第 5 节："Friedman placed HHO first overall across the 29 benchmarks"

**待验证断言**：原论文的 Friedman mean-rank 测试确实是在 29 个函数的整体排名上报告 HHO 第一。

**原论文依据**：PDF 全文搜索 `"Friedman"` = **0 命中**。原论文只使用了 **Wilcoxon rank-sum test**（5% 显著性水平）。

> "the non-parametric Wilcoxon statistical test with 5% degree of significance is also performed"

**判定**：🔴 **错误，需修正**。原论文**没有 Friedman 测试**。

**建议改文**：

删除或替换该句。可改为：

> "The Wilcoxon rank-sum test returned `p < 0.05` versus each peer on the majority of functions, and HHO achieved the best mean results on **22 of 29** benchmarks (F1–F5, F7, F9–F13, F14–F23, F24–F29)."

---

### ⑤ 第 3 节：Lévy flight β = 1.5 和 Mantegna 引用

**待验证断言**：(a) HHO 原论文的 Lévy flight 公式中 β 确实固定为 1.5；(b) 原论文使用 Mantegna 1994 引用。

**原论文依据**（Section 3.3, Eq. 8–9）
> "β is a default constant set to **1.5**"

公式 (9) 的引用标记为 **[49]**。参考文献 [49] 内容为：
> "[49] X.-S. Yang, *Nature-inspired Metaheuristic Algorithms*, Luniverpress, 2010."

PDF 全文搜索 `"Mantegna"` = **0 命中**。

**判定**：
- (a) β = 1.5：✅ **正确**
- (b) Mantegna 引用：🔴 **错误**。原论文**没有引用 Mantegna 1994**，公式 (9) 引用的是 **Yang 2010**。

**建议改文**：
- 删除文中将 Mantegna 1994 与 HHO 原论文直接绑定的表述。
- 若要在 synopsis 中保留对 Lévy flight 技术路线的批评，可改为：
  > "The Lévy step uses a fixed shape parameter β = 1.5 [1], with the simulation formula following the standard Mantegna-style implementation."
- **注意**：是否需要在 references 中新增 Mantegna 1994 取决于你是否想保留对该技术细节的批评。如果保留，可新增 `[7] R. N. Mantegna, "Fast, accurate algorithm for numerical simulation of Lévy stable stochastic processes," Physical Review E, vol. 49, no. 5, pp. 4677–4683, 1994.` 作为背景引用，但**不能**把它说成是 HHO 原论文的引用。

---

### ⑥ 第 4 节：6 个工程设计问题的精确清单

**待验证断言**：原论文使用的 6 个工程设计问题确实是：tension/compression spring, pressure vessel, welded beam, three-bar truss, rolling-element bearing, multi-plate disc clutch brake。

**原论文依据**（Section 4.6, Table 9）

| No. | Name | D | CV | DV | NC | Objective |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | Three-bar truss | 2 | 2 | 0 | 3 | Minimize weight |
| 2 | Tension/compression spring | 3 | 3 | 0 | 4 | Minimize weight |
| 3 | Pressure vessel | 4 | 2 | 2 | 4 | Minimize cost |
| 4 | Welded beam | 4 | 4 | 0 | 7 | Minimize cost |
| 5 | Multi-plate disc clutch brake | 5 | 0 | 5 | 8 | Minimize weight |
| 6 | Rolling element bearing | 10 | 9 | 1 | 9 | Maximize dynamic load |

**判定**：✅ **完全正确**。清单与 synopsis 逐字一致。

**建议改文**：无需修改。

---

### ⑦ 第 3 节：HHO 探索阶段的两条规则措辞

**待验证断言**：Synopsis 中 "(random perching on a peer, or centroid-plus-random offset)" 是否与原论文 Eq. (1) 的实际含义一致。

**原论文依据**（Section 3.1, Eq. 1）
> "we consider an equal chance q for each perching strategy, they perch based on the positions of other family members (to be close enough to them when attacking) and the rabbit, which is modeled in Eq. (1) for the condition of **q < 0.5**, or perch on random tall trees (random locations inside the group's home range), which is modeled in Eq. (1) for condition of **q ≥ 0.5**."

公式 (1) 的具体形式：
- **q ≥ 0.5**: `X(t+1) = X_rabbit(t) − r1|X_rabbit(t) − 2r2 X(t)|`
- **q < 0.5**: `X(t+1) = X_rand(t) − r3|X_rand(t) − 2r4 X(t)| − r4(LB + r3(UB−LB))`

**判定**：⚠️ **部分正确，但措辞是简化解读而非原论文说法**。Synopsis 的 "centroid-plus-random offset" 是对 q < 0.5 分支的数学行为推断（该式包含群体平均位置 + 随机缩放），但原论文的原始描述是生物学语言：
- q < 0.5: 基于其他家族成员和兔子的位置（为攻击时足够接近）
- q ≥ 0.5: 栖息在随机高树上（群体活动范围内的随机位置）

**建议改文**：

> 原文："random perching on a peer, or centroid-plus-random offset"

> 改为："perching based on other family members and the rabbit's position when **q < 0.5**, or perching on random tall trees inside the group's home range when **q ≥ 0.5**"

或保持简洁但贴近原文：

> "perching near the prey and other hawks, or perching on random locations inside the group's home range"

---

### ⑧ 第 1 节：HHO 论文的自述动机

**待验证断言**：HHO 原论文是否确实把自己定位为 "alternative to the single update rule plus monotonic decay template"。

**原论文依据**（Section 1 Introduction + Section 2 Background 全文）

原论文的引言主要完成两件事：
1. 介绍优化算法的通用背景（连续/离散/约束问题、传统数学规划的局限、四大元启发式类别）。
2. 介绍 Harris's hawk 的生物学合作狩猎行为（引用 Bednarz 1988）。

PDF 全文搜索 `"single update"`、`"monotonic decay"`、`"fixed decay"` = **0 命中**。作者**没有**使用这种对比框架来自我定位。

**判定**：🔴 **不正确**。这是 synopsis 作者合理的机制推断，但不是 HHO 原论文的自述。

**建议改文**：

> 原文："The motivation is framed in biological terms: ... and Heidari et al. [1] argue that a faithful algorithmic translation of this structure produces a more robust optimiser than the then-dominant 'single update rule plus monotonic decay' template."

> 改为："The motivation is framed in biological terms: real predator–prey interactions combine steady approach, tight encirclement, and rapid dives depending on the prey's residual energy and escape attempts. The resulting algorithm implements a **multi-phase structure with explicit switching** between exploration and exploitation, in contrast to algorithms that rely on a single blended update rule."

---

### ⑨ 原 [6] Lei 2022 相关的独立复现 / 消融研究

**待验证断言**：截至 2026-04，是否存在任何真实发表、同行评审的、专门针对 HHO 四模式结构做消融或独立复现的研究。

**搜索方法**：tvly 多次搜索 `"HHO ablation"`、`"HHO component analysis"`、`"HHO replication study"`、`"four mode structure HHO"`、`"independent evaluation HHO"`，并交叉检查 2022–2025 年 *Applied Soft Computing*、*Swarm Intelligence*、*Engineering Applications of AI* 等期刊。

**搜索结果**：未发现任何**专门针对 HHO 四模式结构**做系统性消融（如 "What if we remove the Lévy dives?" 或 "Is the four-mode structure necessary?"）的同行评审研究。现有文献类型包括：
- HHO 变体/混合算法（MHHO、DEHHO、CCHHO、ERHHO 等）
- HHO 在特定应用领域的应用（工程优化、特征选择、电力系统等）
- HHO 的正式分析综述（Khurma et al. 2021, *SciTePress*）

**判定**：✅ **现状准确**。第 6 节的 "the absence of an independent peer-reviewed ablation study, however, remains a caveat" 是**可辩护的**。

**建议改文**：保留现状，无需修改。

---

## 四、汇总修改清单

| # | 待查项 | 状态 | 修改建议 |
|---|--------|------|---------|
| ① | F1–F7 "6 of 7" | ✅ 正确 | 无需修改 |
| ② | F8–F13 "5 of 6" | ✅ 正确 | 无需修改 |
| ③ | F24–F29 "majority" | ✅ 正确，可强化 | "majority" → **"all 6"** 或 **"6 of 6"** |
| ④ | Friedman "first overall" | 🔴 错误 | **删除 Friedman 句**；改为 Wilcoxon + 精确计数（22 of 29） |
| ⑤(a) | β = 1.5 | ✅ 正确 | 无需修改 |
| ⑤(b) | Mantegna 引用 | 🔴 错误 | **删除 Mantegna 作为 HHO 原引用的表述**；可选新增为背景引用 |
| ⑥ | 6 个工程问题 | ✅ 正确 | 无需修改 |
| ⑦ | 探索规则措辞 | ⚠️ 简化过度 | 改为原论文的生物学描述 |
| ⑧ | 自我定位动机 | 🔴 推断贴嘴 | **软化**，避免把解读写成作者自述 |
| ⑨ | 独立消融研究 | ✅ 现状正确 | 保留 |

---

## 五、附录：数据来源与引用

### A. 原论文信息
- **Title**: Harris hawks optimization: Algorithm and applications
- **Authors**: A. A. Heidari, S. Mirjalili, H. Faris, I. Aljarah, M. Mafarja, H. Chen
- **Journal**: *Future Generation Computer Systems*
- **Volume/Pages**: Vol. 97, pp. 849–872
- **Year**: 2019
- **DOI**: 10.1016/j.future.2019.02.028
- **PDF 来源**: 公开镜像（24 页完整版）

### B. 关键页码/章节索引
| 核查项 | 原论文位置 |
|--------|-----------|
| Table 3 (F1–F13) | Section 4.2, pp. 855–856 |
| Table 8 (F14–F29) | Section 4.4, pp. 858–859 |
| Table 9 (工程问题清单) | Section 4.6, p. 862 |
| Eq. (1) 探索阶段 | Section 3.1, p. 852 |
| Eq. (8)–(9) Lévy flight | Section 3.3, p. 854 |
| β = 1.5 | Eq. (9) 下方注释 |
| Wilcoxon 测试说明 | Section 4.2, p. 855 |
| Reference [49] | 参考文献列表末页 |
| Introduction 动机 | Section 1, pp. 849–850 |
| Background 生物学 | Section 2, pp. 850–851 |

### C. 独立发现（非待查项）
1. **Reference [5] 作者名错误**：`J. L. Bednarz` → `J. C. Bednarz`（PubMed PMID 17772751 确认）。
2. **Team Statement 缺失**：`toolkit check format` 报 error，需在文件开头/结尾添加 Team Statement 标题。
3. **Reference [5] 不在 verified-db**：建议将 Bednarz 1988 加入 `docs/citation_verified.csv`。

---

*报告结束*
