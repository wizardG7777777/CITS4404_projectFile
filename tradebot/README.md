# tradebot — Deliverable 2 实现包

CITS4404 Team 20 的 D2 主代码包。每个子模块对齐 PDF 一节：

| 子模块 | 对应 PDF 章节 | 内容 |
|---|---|---|
| `data/` | §3 *Data* | 加载 Kaggle Bitcoin Historical Dataset、切分 < 2020 / >= 2020 |
| `bot/wma` | §2.1 *WMA* | SMA / LMA / EMA + flip-padding + 1-D 卷积 |
| `bot/signals` | §2.2 / §2.3 | 交叉点、sign-change 边沿滤波（Eq.6） |
| `bot/bot` | §2.3 + §3 Eq.(7) | B1（2D 双 SMA） / B2（≈14D 复合）bot 类 |
| `bot/backtest` | §3 *Evaluation of Bots* | $1000 起始、3% 手续费、期末清仓 |
| `optim/base` | — | Optimizer 抽象基类 |
| `optim/random_search` | §3 单态对照 | Random Search baseline |
| `optim/pso` | D1 Synopsis 1 | Kennedy & Eberhart 1995 + inertia weight |
| `optim/hho` | D1 Synopsis 2 | Heidari et al. 2019 |
| `experiments/` | §3 *Choosing Algorithms* | 实验矩阵 driver、固定 FE 预算 |

## 合规红线（PDF §3 *Rules of Engagement*）

1. 所有 bot/评估代码自己写，**不抄外部 bot**
2. **不用通用优化库**（`scipy.optimize` / `pyswarm` / `mealpy` 等禁止）
3. 引用论文代码要在文件头注释 + 报告 + 视频三处署源

## 运行

```bash
uv sync
uv run pytest tests/  # 单元测试
uv run jupyter lab    # 启动 notebook
```
