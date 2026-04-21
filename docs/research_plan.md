# CITS4404 团队研究计划与算法分配

> **项目**: Building AI Trading Bots  
> **团队规模**: 2 人  
> **Part 1 截止**: 2025-04-24 (Deliverable 1: 算法综述 Synopses)  
> **Part 2 截止**: 2025-05-24 (Deliverable 2: 视频、报告、代码仓库)  

---

## 1. 项目约束与策略

根据 `project_guidelines.txt` 的要求：

- ** synopsis 数量 = 团队人数 = 2 个算法**
- 所选算法必须是 **optimisation algorithms**
- **至少一个（建议全部）为 population-based**
- 最终需要产出 1-2 页的跨算法对比总结
- 每个 synopsis 必须回答 6 个 reviewer 问题

**本团队策略**：选择 **一经典、一现代** 的跨代际组合，既保证文献充足，又能在对比中讨论群体智能的演进。

---

## 2. 算法分配（按大类分工）

291 个算法按自然现象源头直接二分为两大类：

| 大类 | 来源 Category | 算法数量 |
| :--- | :--- | :--- |
| **群体算法** (Swarm / Bio-behaviour) | 1.x + 2.x | **219** |
| **物理模拟** (Physics-based) | 3.x | **73** |

| 成员 | 负责大类 | 涵盖子类 | Synopsis 算法 |
| :--- | :--- | :--- | :--- |
| **Member 1** | **群体算法** | 1.11, 1.12, 1.13, 2.21, 2.22, 2.23 | 从 219 个中选一个代表性算法撰写 synopsis（推荐 WOA 或 PSO） |
| **Member 2** | **物理模拟** | 3.31, 3.32, 3.33 | 从 73 个中选一个代表性算法撰写 synopsis（推荐 GSA 或 SCA） |

**分工逻辑**：
- Member 1 对“生物行为/社会行为”类算法有整体把握（觅食、狩猎、植物生长、免疫）
- Member 2 对“物理定律”类算法有整体把握（引力、退火、水流、电磁）
- 最终对比总结形成 **"生物启发 vs 物理启发"** 的元分析

---

## 3. 研究顺序 (Investigation Order)

### Phase 1: 独立文献调研 (4月17日 - 4月20日)
按以下顺序逐个完成，确保每个算法都有足够的时间深读原始论文。

```
Step 1 → PSO 原始论文 + benchmark 综述
Step 2 → WOA 原始论文 + benchmark 综述
Step 3 → 交叉阅读：找一篇直接对比 PSO vs WOA 的第三方论文
```

### Phase 2: Synopsis 撰写 (4月21日 - 4月22日)
每人根据以下 6 个问题框架撰写 1-1.5 页 synopsis。

### Phase 3: 对比总结 + 整合 (4月23日)
共同撰写 1-2 页对比分析，讨论：
- 为什么选择这两个算法？
- 它们是“同一主题的变体”还是“不同本质”？
- 是否存在相关的时间线或分类法 (taxonomy) ?

### Phase 4: 提交前检查 (4月24日上午)
- [ ] 字数检查 (max 3000 words 不含图表和引用)
- [ ] 引用格式统一为 IEEE style
- [ ] 包含 word count、团队号、成员姓名学号

---

## 4. Synopsis 六问题框架（每个算法必须回答）

以下内容必须出现在每个 synopsis 中：

1. **What problem with existing algorithms is the new algorithm attempting to solve?**
   - 新算法试图解决现有算法的什么缺陷？

2. **Why, or in what respect, have previous attempts failed?**
   - 前人的尝试在哪些方面失败了？

3. **What is the new idea presented in this paper?**
   - 本文提出的核心新思想是什么？其新颖性体现在哪里？

4. **How is the new approach demonstrated?**
   - 新方法是如何被验证的？（实验、数学证明、案例研究？）
   - 是否有足够信息可以复现？

5. **What are the results or outcomes and how are they validated?**
   - 结果如何？与哪些算法做了 benchmark 对比？
   - 是在所有指标上都更好，还是部分指标更好？

6. **What is your assessment of the conclusions?**
   - 作者的结论是否合理？
   - 这是否会影响你选择在 Part 2 中实现该算法？

---

## 5. 进度追踪 (Status Tracker)

### PSO (Member 1)
- [x] 原始论文已定位并下载
- [x] 阅读完成
- [x] 6 个问题答案已记录
- [x] Synopsis 初稿完成 (`docs/pso_synopsis_draft.md`)
- [x] 校对与润色完成（提交版见 `docs/pso_synopsis_submission.md`；内联引用统一为 IEEE [N] 格式，2026-04-20）

### WOA (Member 2)
- [x] 原始论文已定位并下载
- [x] 阅读完成
- [x] 6 个问题答案已记录
- [x] Synopsis 初稿完成 (`docs/woa_synopsis_draft.md`)
- [x] 校对与润色完成（提交版见 `docs/woa_synopsis_submission.md`；补齐 PSO/GWO/GSA 内联 [N] 标注，2026-04-20）

### 对比总结 (共同)
- [x] 对比表格/分类图完成
- [x] 1-2 页对比文字完成 (`docs/comparison_summary.md`)
- [x] 格式与引用统一检查（新增统一 IEEE References 节；附录内联标注与末尾列表对齐；未核验字段已标注并回指 `citation_verified.csv`，2026-04-20）

---

## 6. 关键文献线索（预检索提示）

| 算法 | 原始论文线索 | 建议检索关键词 |
| :--- | :--- | :--- |
| PSO | Kennedy & Eberhart, 1995, *IEEE International Conference on Neural Networks* | "Particle swarm optimization" Kennedy Eberhart 1995 original paper |
| WOA | Mirjalili & Lewis, 2016, *Advances in Engineering Software* | "Whale Optimization Algorithm" Mirjalili Lewis 2016 |

---

## 7. 后续多代理查验规范

当其他 Agent 读取此文件时，应遵循以下规范：
1. 先确认当前研究的算法是 PSO 还是 WOA。
2. 使用 `tavily_research` 或 `tavily_search` 搜索该算法的原始论文和 benchmark 综述。
3. 将研究发现按“6 个问题框架”整理为结构化文本。
4. 更新本文件中的 **进度追踪 (Status Tracker)** 状态。
5. 不要跳过顺序：先完成 PSO，再完成 WOA，最后做对比总结。
