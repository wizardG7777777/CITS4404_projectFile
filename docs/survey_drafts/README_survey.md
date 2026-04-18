# Survey Drafts — Deliverable 1 素材库说明

> 本文件为 `docs/survey_drafts/` 目录的使用说明。
> 与项目根目录的 `README.md`（工具包说明）、`docs/research_plan.md`（团队研究计划）区分。

---

## 目录定位

`docs/survey_drafts/` 存放的是 **Deliverable 1 综述素材库** —— 即 `partOne_guidline.md` 第三节流水线中要求生成的标准化 Markdown 档案卡片，用于支撑 Conclusions 部分的跨算法对比分析。

**本目录 ≠ 最终交付物**。
正式的 Deliverable 1 提交材料（PSO / WOA synopsis + 双算法对比）仍位于 `docs/` 根目录。

---

## 文件分工

### A. 单算法 synopsis 卡片（9 份，覆盖 Member 1 经典清单除 PSO 外的全部算法）

每份遵循统一模板：元数据、Q1–Q6 六问、核心更新方程、与交易机器人场景的针对性评估、IEEE 引用、Research Status 检查清单。

| 文件 | 算法 | 年份 |
|:---|:---|:---|
| `aco_synopsis_draft.md` | Ant Colony Optimization | 1992 |
| `abc_synopsis_draft.md` | Artificial Bee Colony | 2007 |
| `bbo_synopsis_draft.md` | Biogeography-based Optimization | 2008 |
| `cs_synopsis_draft.md` | Cuckoo Search | 2009 |
| `fa_synopsis_draft.md` | Firefly Algorithm | 2009 |
| `ba_synopsis_draft.md` | Bat Algorithm | 2010 |
| `ffo_synopsis_draft.md` | Fruit Fly Optimization | 2011 |
| `kh_synopsis_draft.md` | Krill Herd | 2012 |
| `smo_synopsis_draft.md` | Spider Monkey Optimization | 2014 |

> PSO 的 synopsis 在根目录 `docs/pso_synopsis_draft.md`（预存），作为该模板的基准参照。

### B. 跨算法横向对比

- `classic_list_comparison.md` — 11 算法（10 经典 + WOA 参照）的时间线、分类、机制、参数、探索-开发范式、应用适配度综合分析，**含 6 项调研关键发现**（FFO 原点偏倚、BA 新颖性质疑、SMO 多制度契合、FA O(n²) 瓶颈、ACO 原生离散、metaphor inflation 现象）。

---

## 与其他文档的关系

```
docs/
├── research_plan.md           ← 团队计划 (路径引用仅指向根目录 PSO/WOA)
├── comparison_summary.md      ← Deliverable 1 交付物: PSO vs WOA 双算法对比
├── pso_synopsis_draft.md      ← Deliverable 1 交付物: Member 1 synopsis
├── woa_synopsis_draft.md      ← Deliverable 1 交付物: Member 2 synopsis
└── survey_drafts/             ← (本目录) Conclusions 素材库
    ├── README_survey.md       ← 本文件
    ├── {9 个 synopsis}
    └── classic_list_comparison.md
```

---

## 使用约定

1. **不要**将 `survey_drafts/` 下的文件直接提交为 Deliverable 1 答卷——它们是 800–1500 字的素材卡片，不是 1–1.5 页的正式 synopsis。
2. 撰写 Conclusions 时，**优先从 `classic_list_comparison.md` 取结构**，从各单算法卡片取细节和引用。
3. 每份卡片末尾的 Research Status 清单标注了仍需完成的工作（通常是最终裁剪步骤）。
4. 新增算法调研：沿用相同模板，文件命名为 `<abbr>_synopsis_draft.md`，并在本 README 的文件表中登记。

---

## 生成来源

本批素材由 AI 辅助流水线生成（2026-04-18）：
- Step 1 — 本地 `toolkit` CLI 读取 CSV 种子元数据
- Step 2 — Perplexity MCP (`perplexity_research`) 提取每个算法的 Q1–Q6 结构化答案与引用
- Step 3 — 按 PSO synopsis 模板格式化并写入本目录

流水线细节见 `docs/research_plan.md` 与 `partOne_guidline.md`。
