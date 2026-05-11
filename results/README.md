# Results

实验产出（pickle / json / parquet / png）都落到这里。**大文件不入仓**（见 `.gitignore`），只 commit 小的汇总：

- `summary.csv` — 每个 (algo × bot × seed) 一行：best fitness、收敛迭代、wall time
- `figures/` — 报告/视频用的最终图（png/pdf）

## 目录约定

```
results/
├── runs/                    # 单次 run 的详细输出（.gitignore）
│   └── {algo}_{bot}_seed{N}/
│       ├── trace.parquet    # 每代 best fitness
│       └── final.json       # 最终最优解 + 元数据
├── summary.csv              # 跨所有 run 的汇总（commit）
└── figures/                 # 报告/视频图（commit）
```
