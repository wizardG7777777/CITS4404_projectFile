# Notebooks

探索性 / 中间 notebook 都放这里。**最终交付的单 `.ipynb`** 会从这里凝缩出来（PDF §4 *Code* 要求一个 notebook 含全部实现）。

## 命名约定

- `01_data_explore.ipynb` — 数据 EDA、价格序列可视化
- `02_wma_sanity.ipynb` — WMA 卷积模块的可视化验证（对照 PDF Figure 3/4/5）
- `03_bot_b1_b2.ipynb` — bot 行为 trace、买卖点叠图
- `04_optim_smoke.ipynb` — 三个优化算法在低维玩具问题上的收敛 smoke test
- `05_experiments.ipynb` — 完整实验矩阵（5×3×2）+ 收敛曲线 + 统计检验
- `06_test_set.ipynb` — 测试集回测 + 行为分析（哪种 WMA 权重大？）
- `final_report.ipynb` — **交付用**，把 01–06 的关键代码 + 结果凝缩成一个

## 运行约定

所有 notebook 的导入路径默认从仓库根目录开始，请用 `uv run jupyter lab` 或 `uv run jupyter notebook` 启动，确保 `tradebot.*` 可以 import。
