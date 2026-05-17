# Deliverable 2 — PPT × 视频脚本 契合度审查 & 修改方案

**审查日期**: 2026-05-17
**对象**: `CITS4404_Team20_Presentation.pptx` (21 张) vs `docs/d2_video_script.md` (11 段, ~25 min) vs `docs/d2_report_draft.md` (Part 2 交付报告)
**结论**: **整体契合度高（约 85%）**, 内容、数字、结构性论点三方完全一致, 但存在 **1 个重大缺口 + 3 个次要不一致**, 必须在最终视频前修正。

---

## 1. 一句话结论

PPT 与脚本和 Part 2 报告在**叙事主线、所有定量结论、所有图表、所有引用**上完全对齐, 无需大改。最大问题在于脚本写了 5 分钟的「四算法动画走查」（§5a–§5d, 占总时长 20%）, 而 PPT 完全没有对应的动画幻灯片——直接从「为什么加 GWO」（Slide 9）跳到「四算法伪代码」（Slide 10）再到「实验矩阵」（Slide 11）。其余三处仅为细节修补。

---

## 2. 推荐方案: **以 PPT 为视觉基线 + 保留脚本动画段**

理由:

1. PPT 已是当前最成熟的可交付物, 21 张结构干净、信息层级清晰、与 Part 2 报告小节一一对应。重新做幻灯片成本高。
2. 但脚本 §5 的动画段是整段视频里**最有视觉冲击力**的 5 分钟, `results/animations/{rs,pso,gwo,hho}.mp4` 4 段动画已经渲染好。直接抛弃会让 10:30–15:30 这段叙事干瘪（全程对着伪代码读 5 分钟）。
3. 把动画作为 **B-roll 插入到 PPT 第 9 张和第 10 张之间**, 不需要改 PPT 文件本身——只需要在视频剪辑时让动画 mp4 全屏覆盖 PPT 画面, 旁白照读。

净效果: 最终视频会有约 **21 张 PPT + 4 段动画 ≈ 25 个视觉单元**, 整体时长 ~24 分钟, 既满足 ≤25 min 硬性要求, 也保留了脚本设计的最佳呈现节奏。

---

## 3. PPT ↔ 脚本 ↔ 报告 三方对齐表

| PPT # | PPT 标题 | 对应脚本段 | 对应报告小节 | 状态 |
|---|---|---|---|---|
| 1 | Title (Team 20) | §0 Title | 标题页 | ✅ |
| 2 | Introduction / Why nature-inspired | §1 Introduction | §1 | ✅ |
| 3 | PSO (1995) | §2 Part 1 (pso_velocity) | §3 | ✅ |
| 4 | HHO (2019) | §2 Part 1 (hho_energy_gate) | §3 | ✅ |
| 5 | D1 PSO vs HHO 对照表 | §2 Part 1 (part1_comparison_table) | §3 | ✅ |
| 6 | WMA 三核 SMA/LMA/EMA | §3 Bot design (wma_kernels) | §2 Fig.1 | ✅ |
| 7 | B1 + B2 假设空间 | §3 Bot design (b1_b2 + eq7) | §2 | ✅ |
| 8 | 四算法结构光谱表 | §4 Algorithm selection | §3 表 | ✅ |
| 9 | Why GWO + Camacho-Villalon | §4 (gwo_three_leaders + camacho_villalon_paper) | §3 | ✅ |
| **缺** | **动画 RS** | §5a Random Search (~90 w) | — | ⚠️ **缺 PPT** |
| **缺** | **动画 PSO** | §5b PSO (~175 w) | — | ⚠️ **缺 PPT** |
| **缺** | **动画 GWO** | §5c GWO (~175 w) | — | ⚠️ **缺 PPT** |
| **缺** | **动画 HHO** | §5d HHO (~230 w) | — | ⚠️ **缺 PPT** |
| 10 | 四算法伪代码 + Rules of Engagement | §5e Compliance recap (~65 w) | §3 | ✅ |
| 11 | 实验矩阵 + 数据切分 | §6 (objective_framework + experiment_matrix) | §4 | ⚠️ **2 段合 1 张** |
| 12 | BTC 价格 log scale | §6 (btc_split, Fig. 2) | §4 Fig.2 | ✅ |
| 13 | 训练 fitness boxplot | §7 (boxplot, Fig. 3) | §5 Fig.3 | ✅ |
| 14 | 训练结果表 + 主要发现 | §7 (stats_table) | §5 表 1 | ✅ |
| 15 | 收敛曲线 | §7 (convergence_curves, Fig. 4) | §5 Fig.4 | ✅ |
| 16 | 测试: 全 40 跑落败 buy-and-hold | §8 (train_test_scatter, Fig. 5) | §6 Fig.5 | ✅ |
| 17 | 训练冠军→测试输家 | §8 (best_bot_trades, Fig. 7) | §6 Fig.7 | ✅ |
| 18 | 泛化对照表 | §8 (generalisation_table) | §6 表 2 | ✅ |
| 19 | B2 权重份额 + HHI | §9 (b2_weight_shares, Fig. 8) | §7 Fig.8 / 表 3 | ✅ |
| 20 | 四点结论 | §10 Conclusions (takeaways) | §8 | ✅ |
| 21 | Thank You + 引用 | §11 Closing (links_qrcode) | 引用列表 | ⚠️ **缺 AI 声明** |

数字交叉核对全部通过: $77,897 / $5,660 / $3,623 / $537 / p = 1.0 / p = 0.009 / HHI 0.37–0.52——PPT、脚本、报告三方完全一致, 无任何事实冲突。

---

## 4. 四处需要修正的问题

### 4.1 重大问题: 动画段 (§5a–§5d) 在 PPT 中完全缺失 ⚠️

**症状**: 脚本 10:30–15:30 这 5 分钟（约 700 词, 约占总时长 20%）安排了 4 段算法动画作为视觉支撑, 旁白完全围绕「看屏幕里粒子怎么动」展开（"watch the red dots scatter", "the cyan star marks the global best", "see the blue dots leaving the attractor"）。PPT 第 9 张直接跳到第 10 张（伪代码), 这段旁白会**无视觉可指**。

**事实**: 4 段动画已在 `results/animations/` 渲染完成（rs.mp4 124 KB, pso.mp4 208 KB, gwo.mp4 168 KB, hho.mp4 179 KB）, 总长约 2 分钟。

**修复方案 (推荐): 视频剪辑时插入 B-roll**

在视频剪辑层（不修改 PPT 文件本身）执行:

1. PPT Slide 9 结束后, 切到 `rs.mp4` 全屏 → Q 读 §5a 旁白 (30 s)
2. 切到 `pso.mp4` 全屏 → Q 读 §5b 旁白 (75 s)
3. 切到 `gwo.mp4` 全屏 → Y 读 §5c 旁白 (75 s)
4. 切到 `hho.mp4` 全屏 → Y 读 §5d 旁白 (90 s)
5. 回到 PPT Slide 10 → Q 读 §5e 合规声明 (30 s)

**收益**: 视觉单元数从 21 提升到 25, 平均每张 60 秒, 与脚本「~50 s/张」的节奏假设接近。

**替代方案 (不推荐, 仅作备选)**: 直接砍掉 §5a–§5d, 把 §5e 扩写到 200 词覆盖 4 个算法的伪代码（对应 PPT Slide 10）。损失: 整段视频缺少最直观的「算法实际运行起来是什么样子」, 评委只能听抽象描述。视频时长会缩短到 ~20 min。

---

### 4.2 次要问题: §6 两张幻灯片被合并为 PPT Slide 11

**症状**: 脚本 §6 写了两张:
- `[SLIDE: objective_framework]` — 讲 `BudgetExhausted` 异常、counted wrapper, 解释「公平性是怎么在代码层强制的」
- `[SLIDE: experiment_matrix]` — 讲 4×2×5=40 跑 / 5000 FE / ~90 s wall time

PPT Slide 11 把两者合成一张, 标题是「Experiment Matrix & Data Split」, 但页脚只用一行小字写「5,000 FE per run · 200,000 backtests total · ~90 sec wall time」带过了「counted wrapper」的核心机制。Y 的旁白讲到「we enforce that requirement at the framework level...raises a BudgetExhausted exception on the five-thousand-and-first invocation」时, 屏幕上找不到对应内容。

**修复方案 (推荐, 选其一)**:

**方案 A — 调整旁白以匹配 PPT (推荐)**: 把 §6 的 270 词压到 ~150 词, 删掉 BudgetExhausted 的技术细节, 简化为「每个算法都在严格相同的 5000 次评估预算下运行——这是公平比较的基础。matrix 是 4 算法 × 2 bot × 5 seed = 40 跑」。技术细节留在报告 §3 里, 视频不展开。

**方案 B — 给 PPT 加一张「公平性」幻灯片**: 在现有 Slide 11 前插入一张, 标题「Counted-Objective Framework」, 内容是 3 行代码片段（counted wrapper + BudgetExhausted）+ 一句「Every algorithm sees exactly 5,000 evaluations — enforced at the framework level, not by trust」。

如果时间紧, **选 A**。

---

### 4.3 次要问题: PPT Slide 21 缺 AI 辅助声明

**症状**: 脚本 §11 的最后一句"The narration in this video was assisted by text-to-speech; all data, code, and analysis were produced by Team 20." 被标注为 **非可选 (non-optional)**——CITS 课程要求 AI 使用透明度声明。PPT Slide 21 只有 "Submission Contents"、"Key References"、"Team 20 · ..." 三块, 没有这段声明。

**修复方案**: 直接在 PPT Slide 21 的「Submission Contents」块下方加一行小字:

> *Narration assisted by text-to-speech; all data, code, and analysis produced by Team 20.*

字号小一些（10–12 pt）即可, 不破坏页面布局。

---

### 4.4 微小问题 (无需修改, 仅记录)

- **PPT Slide 5 表格**「Design era」行重复了列头里的 "PSO (1995)" / "HHO (2019)"——纯美观问题, 不影响内容, 可不改。
- **PPT Slide 21** 列出的 6 篇引用脚本旁白完全没读——这是正确的（视频里读引用很奇怪）, PPT 上列出来供截图存档即可。

---

## 5. 修改后视频时间预算（推荐方案）

| 段 | 内容 | 词数 | 时长 (135 wpm) | 累计 |
|---|---|---|---|---|
| §0 | Title | 45 | 0:20 | 0:20 |
| §1 | Introduction | 160 | 1:10 | 1:30 |
| §2 | Part 1 review (PSO/HHO/对照) | 400 | 3:00 | 4:30 |
| §3 | Bot design (WMA + B1/B2) | 400 | 3:00 | 7:30 |
| §4 | Algorithm selection + Camacho-Villalon | 400 | 3:00 | 10:30 |
| §5a–d | **动画 B-roll × 4** | 670 | 5:00 | 15:30 |
| §5e | Compliance recap (PPT Slide 10) | 65 | 0:30 | 16:00 |
| §6 | Setup (压缩到 150 w, 对应 PPT Slide 11+12) | 150 | 1:10 | 17:10 |
| §7 | Training results (Slides 13–15) | 400 | 3:00 | 20:10 |
| §8 | Generalisation (Slides 16–18) | 340 | 2:30 | 22:40 |
| §9 | Behavioural HHI (Slide 19) | 200 | 1:30 | 24:10 |
| §10 | Conclusions (Slide 20) | 150 | 1:10 | 25:20 |
| §11 | Closing + AI disclosure (Slide 21) | 70 | 0:30 | **25:50** ⚠️ |

**警告**: 加上动画段后总时长 25:50, 超出 25 min 硬性上限 50 秒。

**收紧建议** (按优先级):
1. §6 进一步压到 100 词 (省 25 s)
2. §5b PSO 旁白从 175 → 130 词 (省 20 s)
3. §10 Conclusions 从 150 → 120 词 (省 15 s)

执行这 3 项可压回 ~24:50, 留 10 s 安全余量。

---

## 6. 行动清单 (建议执行顺序)

1. **[剪辑层]** 在 Slide 9 后插入 4 段动画 mp4 作为 B-roll, 全屏覆盖, 按脚本 §5a–§5d 旁白配音。
2. **[PPT 层]** 在 Slide 21 「Submission Contents」下方加一行 AI 辅助声明。
3. **[脚本层]** 把 §6 旁白从 270 词 → 150 词, 删掉 `BudgetExhausted` / counted wrapper 技术细节, 让旁白和 PPT Slide 11 内容对齐。
4. **[脚本层]** 按时间预算表收紧 §5b / §10, 总时长压到 24:50。
5. **[最终核对]** 用 TTS 跑一遍全段, 实测时长, 必要时再微调。

完成以上 5 步后, PPT 与脚本对齐度可达 100%, 与 Part 2 报告的所有数字、结论、引用三方一致, 满足 ≤25 min 的硬性要求。
