# Data

> 本目录用于存放 BTC 历史价格数据。**所有原始文件 + 派生大文件均不入仓**（见根目录 `.gitignore`）。

## 数据源（按 PDF §3 *Data* 原文）

> "we will use as the base case a dataset from the kaggle repository (you may add to this if you wish). **The Bitcoin Historical Dataset** provides historical data between (variously) 2014 and 2022 daily, hourly and by the minute. It ranges from sequences of **2652 data points for daily data** to around 600,000 data points for each yearly set of minute data."

要点：

- **来源**：Kaggle 上名为 "Bitcoin Historical Dataset" 的数据集
- **覆盖**：2014–2022（不同时间粒度起止时间略有差异）
- **粒度**：daily / hourly / minute
- **校验数字**：daily ≈ **2652 个数据点**（用这个数核对你下载的版本是否对版）

## 训练/测试切分（PDF §3 *Data* 硬约束）

> "**You should optimise your agent on data prior to 2020, and preserve the data from 2020 onwards for final testing of your optimised bot.** ... we'll act as if it is the start of 2020."

- **训练集**：`< 2020-01-01` 的所有数据
- **测试集**：`>= 2020-01-01` 的所有数据
- 测试集**只在最终评估时**触碰一次，期间任何调参都不能用它

## 目录约定

```
data/
├── raw/         # Kaggle 原始 CSV（.gitignore，自己下载）
│   └── btc_daily.csv      # 日线 OHLCV
└── processed/   # 切分后的 train/test 文件（.gitignore，由 src/data 脚本生成）
    ├── btc_daily_train.parquet   # < 2020-01-01
    └── btc_daily_test.parquet    # >= 2020-01-01
```

## 下载步骤（团队成员手动执行一次）

1. 登录 Kaggle 账号
2. 搜索 "Bitcoin Historical Dataset"，找到 daily 数据点数 ≈ 2652 的版本
3. 下载 daily 粒度的 CSV，重命名为 `btc_daily.csv`，放到 `data/raw/`
4. 运行 `tradebot.data.split` 切分（脚本待写，Task #6）

## 可选扩展

PDF 允许自行添加数据：

> "you may add to this if you wish"

如需小时线/分钟线，按相同方式放到 `data/raw/btc_hourly.csv` / `data/raw/btc_1min.csv`。但**默认实验只跑日线**——分钟线评估代价 ×1440，会拖垮算法对比。

## 红线提示

- **不要** commit 任何数据文件（即使是几 MB 的 CSV）。所有 `data/raw/`、`data/processed/` 都被 `.gitignore` 排除。
- **不要** 用未来数据训练（e.g. 用 2021 的数据调超参再跑 train < 2020）——这等于偷看测试集。
