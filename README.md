# CITS4404 Team Project — Building AI Trading Bots

**Team 20**: Qiurong Chen (24558583) and Yanchen Yu (24256987)

This repository contains the implementation accompanying both Deliverable 1
(literature review) and Deliverable 2 (trading-bot experiment) of the
CITS4404 team project.

The primary submission artefact for Deliverable 2 is the notebook
[`notebooks/final_report.ipynb`](notebooks/final_report.ipynb), which can be
opened directly with all figures embedded — no need to re-run the experiment.

---

## Deliverable 2 — Trading-Bot Experiment

### Layout

```
tradebot/
├── data/load.py          PDF §3 Data — Kaggle BTC loader, < 2020 / >= 2020 split
├── bot/
│   ├── wma.py            PDF §2.1 SMA / LMA / EMA (1-D convolution + flip-pad)
│   ├── signals.py        PDF §2.2 / §2.3 / Eq.(6) — crossover edge detection
│   ├── bots.py           B1 (2-D dual-SMA) + B2 (~14-D PDF §3 Eq.(7) compound)
│   └── backtest.py       PDF §3 Evaluation — $1000, 3% fee, final liquidation
├── optim/
│   ├── base.py           Optimizer abstract + Objective FE-budget accountant
│   ├── random_search.py  PDF §3 single-state baseline
│   ├── pso.py            D1 Synopsis 1 — Kennedy & Eberhart 1995 + Shi 1998
│   └── hho.py            D1 Synopsis 2 — Heidari et al. 2019, 6-rule
└── experiments/
    ├── config.py         5 seeds × 3 algos × 2 bots, 5000 FE budget each
    ├── run_matrix.py     Experiment driver (~1 min total wall time)
    ├── analyze.py        Aggregate + Mann-Whitney U two-sided p-values
    ├── test_eval.py      Cold-deploy each best-x on the ≥ 2020 test split
    ├── behavior.py       PDF §3 explicit prompt — B2 weight allocation analysis
    └── figures.py        Generate every report figure into results/figures/

tests/                    214 pytest cases pinning every PDF clause we touch
notebooks/final_report.ipynb   Submission notebook (see below)
docs/d2_requirement_alignment.md   PDF clause → code/test cross-reference
results/                  summary.csv, stats.json, test_results.csv, behavior.json,
                          per-run traces, and the figures referenced by the report
data/raw/                 Kaggle CSVs (gitignored — see data/README.md)
data/processed/           train/test parquets (gitignored, regenerated on demand)
```

### Setup

```bash
uv sync                                 # Python 3.12 + numpy/pandas/matplotlib/pyarrow
uv run pytest tests/                    # 214 passed
```

### Reproducing the experiment (~1 min)

```bash
uv run python -m tradebot.data.load                    # build processed parquets
uv run python -m tradebot.experiments.run_matrix       # 30 runs (~1 min)
uv run python -m tradebot.experiments.analyze          # stats.json + p-values
uv run python -m tradebot.experiments.test_eval        # test-set retest
uv run python -m tradebot.experiments.behavior         # B2 weight analysis
uv run python -m tradebot.experiments.figures          # 9 PNGs to results/figures/
uv run python -m tools.build_notebook                  # regenerate notebook
```

The notebook is pre-executed and ships with all figures embedded, so a
reviewer who only wants to *read* the output never needs to run any of the
above.

### Required dataset

PDF §3 *Data* specifies Kaggle's
[**Bitcoin Historical Dataset**](https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd)
(daily ≈ 2 652 rows from 2014-11-28 to 2022-03-01). Download `BTC-Daily.csv`
into `data/raw/` and run `tradebot.data.load`. Full instructions in
[`data/README.md`](data/README.md).

### Compliance summary (PDF §3 *Rules of Engagement*)

| Rule | How we comply |
|---|---|
| No external bot code | Every file under `tradebot/bot/` is hand-written from the PDF equations. |
| No general optim libraries | Every file under `tradebot/optim/` is hand-written; only numpy/pandas/matplotlib for compute/plots. |
| Acknowledge algorithm sources | Module headers cite Kennedy & Eberhart 1995, Shi & Eberhart 1998, Heidari et al. 2019; the same references appear in the report and will appear in the video. |

### Submission contents

| Artefact | Location | PDF §4 requirement |
|---|---|---|
| Code (`.ipynb`) | `notebooks/final_report.ipynb` | "submit a .ipynb file that includes all your implementation" |
| README | `README.md` (this file) | "Brief instructions for running the code" |
| Report (PDF, ≤ 3000 words, IEEE) | (Task #15) | "complement your video" |
| Video (≤ 25 min, MP4/link) | (Task #16) | six content sections listed in §4 *Presentation* |

---

## Deliverable 1 — Auxiliary toolkit

The `toolkit/` package is the literature-review helper used during Deliverable 1
(CSV / PDF / DOCX inspection + structural checks for the synopsis Markdown
drafts). It is independent of the Deliverable 2 implementation and remains in
the repo for reference. See its CLI surface:

```bash
uv run python -m toolkit --help
```

Detailed usage was the subject of the Deliverable 1 submission and is not
repeated here; the canonical reference for Deliverable 1 is `1951.pdf`.
