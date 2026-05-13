"""Generate every figure referenced by the report and the final notebook.

Outputs to ``results/figures/`` (.png, dpi=150). The notebook re-runs this
module so figures and notebook are guaranteed to match.

Usage:

    uv run python -m tradebot.experiments.figures
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tradebot.bot.backtest import INITIAL_CASH, backtest_detailed
from tradebot.bot.bots import BotB1, BotB2
from tradebot.bot.wma import ema_filter, lma_filter, sma_filter, wma
from tradebot.data.load import load_close, load_ohlcv
from tradebot.experiments.test_eval import buy_and_hold


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "results" / "runs"
FIGS_DIR = REPO_ROOT / "results" / "figures"
SUMMARY_CSV = REPO_ROOT / "results" / "summary.csv"
TEST_RESULTS_CSV = REPO_ROOT / "results" / "test_results.csv"
BEHAVIOR_JSON = REPO_ROOT / "results" / "behavior.json"


plt.rcParams.update(
    {
        "figure.dpi": 100,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.grid": True,
        "grid.alpha": 0.3,
    }
)

ALGOS_ORDER = ["RandomSearch", "PSO", "GWO", "HHO"]
ALGO_COLOURS = {
    "RandomSearch": "tab:gray",
    "PSO": "tab:blue",
    "GWO": "tab:green",
    "HHO": "tab:red",
}


# --------------------------------------------------------------------------- #
# Figures 1-3: Data and WMA building blocks (for §Design)
# --------------------------------------------------------------------------- #


def fig_01_data_split() -> Path:
    """Train / test price split (PDF §3 *Data*)."""
    train = load_ohlcv("train")
    test = load_ohlcv("test")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(train["date"], train["close"], label=f"Train ({len(train)} d)", color="tab:blue", lw=1.0)
    ax.plot(test["date"], test["close"], label=f"Test ({len(test)} d)", color="tab:orange", lw=1.0)
    ax.axvline(pd.Timestamp("2020-01-01"), color="black", lw=0.7, ls="--")
    ax.set_yscale("log")
    ax.set_xlabel("Date")
    ax.set_ylabel("BTC/USD (log)")
    ax.set_title("Bitcoin Historical Dataset: train (pre-2020) vs test (>= 2020)")
    ax.legend(loc="upper left")
    out = FIGS_DIR / "01_price_train_test.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def fig_02_wma_demo() -> Path:
    """Reproduce PDF Figure 3: price + two SMAs of different windows."""
    prices = load_close("train")[-365:]
    x = np.arange(len(prices))
    sma_10 = wma(prices, 10, sma_filter(10))
    sma_40 = wma(prices, 40, sma_filter(40))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(x, prices, label="Close", color="black", alpha=0.5, lw=0.8)
    ax.plot(x, sma_10, label="SMA(10)", color="tab:blue", lw=1.5)
    ax.plot(x, sma_40, label="SMA(40)", color="tab:orange", lw=1.5)
    ax.set_xlabel("Day (last year of training)")
    ax.set_ylabel("Price (USD)")
    ax.set_title("PDF Figure 3 reproduction: 10- and 40-day SMA on BTC close")
    ax.legend()
    out = FIGS_DIR / "02_wma_sma_two_windows.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def fig_03_wma_comparison() -> Path:
    """Reproduce PDF Figure 5: SMA vs LMA vs EMA at the same N."""
    prices = load_close("train")[-200:]
    x = np.arange(len(prices))
    N = 20
    sma = wma(prices, N, sma_filter(N))
    lma = wma(prices, N, lma_filter(N))
    ema = wma(prices, N, ema_filter(N, 0.3))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(x, prices, label="Close", color="black", alpha=0.5, lw=0.8)
    ax.plot(x, sma, label=f"SMA({N})", color="tab:blue", lw=1.5)
    ax.plot(x, lma, label=f"LMA({N})", color="tab:orange", lw=1.5)
    ax.plot(x, ema, label=f"EMA({N}, alpha=0.3)", color="tab:green", lw=1.5)
    ax.set_xlabel("Day (last 200 days of training)")
    ax.set_ylabel("Price (USD)")
    ax.set_title("PDF Figure 5 reproduction: SMA / LMA / EMA at the same window N=20")
    ax.legend()
    out = FIGS_DIR / "03_wma_three_kernels.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Figures 4-5: Training results (for §Results)
# --------------------------------------------------------------------------- #


def fig_04_train_fitness_boxplot() -> Path:
    """Box plot of train fitness over 5 seeds, faceted by bot."""
    summary = pd.read_csv(SUMMARY_CSV)
    bots = sorted(summary["bot"].unique())
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    for ax, bot in zip(axes, bots):
        bot_data = summary[summary["bot"] == bot]
        data = [
            bot_data[bot_data["algorithm"] == a]["best_fitness"].values
            for a in ALGOS_ORDER
        ]
        bp = ax.boxplot(data, tick_labels=ALGOS_ORDER, patch_artist=True, showmeans=True)
        for patch, algo in zip(bp["boxes"], ALGOS_ORDER):
            patch.set_facecolor(ALGO_COLOURS[algo])
            patch.set_alpha(0.4)
        # Baseline reference: $1000 starting cash (the no-trade fallback).
        ax.axhline(INITIAL_CASH, color="black", ls=":", lw=0.8, alpha=0.6)
        ax.set_title(bot)
        ax.set_ylabel("Train fitness (USD)" if ax is axes[0] else "")
    fig.suptitle("Training fitness over 5 seeds, 5000 FE budget each", y=1.02)
    out = FIGS_DIR / "04_train_fitness_boxplot.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def fig_05_convergence_curves() -> Path:
    """Median best-fitness-so-far across 5 seeds, ± IQR shaded."""
    bots = ["B1_dual_sma", "B2_compound"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, bot in zip(axes, bots):
        for algo in ALGOS_ORDER:
            traces = []
            for seed in range(5):
                trace = pd.read_parquet(
                    RUNS_DIR / f"{algo}_{bot}_seed{seed}" / "trace.parquet"
                )
                traces.append(trace["best_so_far"].to_numpy())
            arr = np.stack(traces)
            median = np.median(arr, axis=0)
            p25 = np.percentile(arr, 25, axis=0)
            p75 = np.percentile(arr, 75, axis=0)
            x = np.arange(arr.shape[1])
            ax.plot(x, median, label=algo, color=ALGO_COLOURS[algo], lw=1.8)
            ax.fill_between(x, p25, p75, color=ALGO_COLOURS[algo], alpha=0.15)
        ax.set_title(bot)
        ax.set_xlabel("Fitness evaluations")
        ax.set_ylabel("Best fitness so far (USD)" if ax is axes[0] else "")
        ax.legend(loc="lower right")
    fig.suptitle(
        "Convergence: best-so-far fitness (median solid, IQR shaded), 5 seeds",
        y=1.02,
    )
    out = FIGS_DIR / "05_convergence_curves.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Figures 6-7: Generalisation (for §Results / §Discussion)
# --------------------------------------------------------------------------- #


def fig_06_train_test_scatter() -> Path:
    """Train vs test fitness scatter — visualises the generalisation gap."""
    test_results = pd.read_csv(TEST_RESULTS_CSV)
    test_prices = load_close("test")
    bh = buy_and_hold(test_prices)

    bots = ["B1_dual_sma", "B2_compound"]
    markers = {"RandomSearch": "s", "PSO": "o", "GWO": "D", "HHO": "^"}

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, bot in zip(axes, bots):
        bot_data = test_results[test_results["bot"] == bot]
        for algo in ALGOS_ORDER:
            d = bot_data[bot_data["algorithm"] == algo]
            ax.scatter(
                d["train_fitness"],
                d["test_fitness"],
                marker=markers[algo],
                c=ALGO_COLOURS[algo],
                label=algo,
                s=80,
                edgecolors="black",
                alpha=0.75,
            )
        ax.axhline(bh, color="green", ls="--", lw=1, label=f"Buy-and-hold = ${bh:.0f}")
        ax.axhline(
            INITIAL_CASH, color="orange", ls=":", lw=1, label=f"$1000 (no trades)"
        )
        ax.set_xlabel("Train fitness (USD)")
        ax.set_ylabel("Test fitness (USD)" if ax is axes[0] else "")
        ax.set_title(bot)
        ax.legend(loc="best", fontsize=8)
    fig.suptitle("Generalisation: train fitness vs test fitness (5 seeds × 3 algos)", y=1.02)
    out = FIGS_DIR / "06_train_test_scatter.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def fig_07_test_fitness_bar() -> Path:
    """Bar chart of mean test fitness per (algo, bot) vs buy-and-hold."""
    test_results = pd.read_csv(TEST_RESULTS_CSV)
    test_prices = load_close("test")
    bh = buy_and_hold(test_prices)

    agg = test_results.groupby(["bot", "algorithm"])["test_fitness"].agg(["mean", "std"])
    bots = ["B1_dual_sma", "B2_compound"]
    x = np.arange(len(ALGOS_ORDER))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for i, bot in enumerate(bots):
        means = [agg.loc[(bot, a), "mean"] for a in ALGOS_ORDER]
        stds = [agg.loc[(bot, a), "std"] for a in ALGOS_ORDER]
        ax.bar(
            x + (i - 0.5) * width,
            means,
            width=width,
            yerr=stds,
            label=bot,
            alpha=0.8,
            capsize=4,
        )
    ax.axhline(bh, color="green", ls="--", lw=1, label=f"Buy-and-hold = ${bh:.0f}")
    ax.axhline(INITIAL_CASH, color="orange", ls=":", lw=1, label="$1000 baseline")
    ax.set_xticks(x, ALGOS_ORDER)
    ax.set_ylabel("Test fitness (USD)")
    ax.set_title("Mean test-set fitness (± std over 5 seeds)")
    ax.legend()
    out = FIGS_DIR / "07_test_fitness_bar.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Figure 8: B2 weight breakdown (for §Behaviour analysis)
# --------------------------------------------------------------------------- #


def fig_08_b2_weight_shares() -> Path:
    """Stacked bar: mean SMA/LMA/EMA share per algo, HIGH and LOW components."""
    beh = json.loads(BEHAVIOR_JSON.read_text())
    wma_colours = {"SMA": "tab:blue", "LMA": "tab:orange", "EMA": "tab:green"}

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, side in zip(axes, ["HIGH", "LOW"]):
        key = f"{side.lower()}_mean_shares"
        sma = [beh["per_algorithm"][a][key]["SMA"] for a in ALGOS_ORDER]
        lma = [beh["per_algorithm"][a][key]["LMA"] for a in ALGOS_ORDER]
        ema = [beh["per_algorithm"][a][key]["EMA"] for a in ALGOS_ORDER]
        x = np.arange(len(ALGOS_ORDER))
        ax.bar(x, sma, label="SMA", color=wma_colours["SMA"])
        ax.bar(x, lma, bottom=sma, label="LMA", color=wma_colours["LMA"])
        ax.bar(
            x,
            ema,
            bottom=np.array(sma) + np.array(lma),
            label="EMA",
            color=wma_colours["EMA"],
        )
        hhi_key = f"{side.lower()}_mean_hhi"
        for i, a in enumerate(ALGOS_ORDER):
            hhi_v = beh["per_algorithm"][a][hhi_key]
            ax.text(i, 1.02, f"HHI={hhi_v:.2f}", ha="center", fontsize=9)
        ax.axhline(1 / 3, color="black", lw=0.6, ls="--", alpha=0.6)
        ax.set_xticks(x, ALGOS_ORDER)
        ax.set_ylim(0, 1.12)
        ax.set_ylabel("Mean weight share" if ax is axes[0] else "")
        ax.set_title(f"{side}-frequency component")
        ax.legend(loc="upper right", fontsize=8)
    fig.suptitle("B2: how does each optimiser balance SMA / LMA / EMA?", y=1.02)
    out = FIGS_DIR / "08_b2_weight_shares.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Figure 9: Best bot trade overlay (for §Results / "show, don't tell")
# --------------------------------------------------------------------------- #


def fig_09_best_bot_trades() -> Path:
    """Plot best-train-fitness bot's buy/sell points on train and test prices."""
    summary = pd.read_csv(SUMMARY_CSV)
    best_row = summary.loc[summary["best_fitness"].idxmax()]
    algo = best_row["algorithm"]
    bot_name = best_row["bot"]
    seed = int(best_row["seed"])

    meta = json.loads(
        (RUNS_DIR / f"{algo}_{bot_name}_seed{seed}" / "final.json").read_text()
    )
    best_x = np.array(meta["best_x"])
    BotCls = BotB1 if bot_name == "B1_dual_sma" else BotB2

    train_ohlcv = load_ohlcv("train")
    test_ohlcv = load_ohlcv("test")
    fig, axes = plt.subplots(2, 1, figsize=(11, 7))
    for ax, ohlcv, label in (
        (axes[0], train_ohlcv, "Train"),
        (axes[1], test_ohlcv, "Test"),
    ):
        prices = ohlcv["close"].to_numpy()
        dates = ohlcv["date"].to_numpy()
        signals = BotCls.signals(prices, best_x)
        res = backtest_detailed(prices, signals)
        ax.plot(dates, prices, color="black", alpha=0.6, lw=0.8, label="BTC close")
        buys = [t for t in res.trades if t.action == "buy"]
        sells = [t for t in res.trades if t.action == "sell"]
        liqs = [t for t in res.trades if t.action == "liquidate"]
        if buys:
            ax.scatter(
                [dates[t.index] for t in buys],
                [t.price for t in buys],
                marker="^",
                c="green",
                s=70,
                label=f"Buy ({len(buys)})",
                zorder=5,
                edgecolors="black",
            )
        if sells:
            ax.scatter(
                [dates[t.index] for t in sells],
                [t.price for t in sells],
                marker="v",
                c="red",
                s=70,
                label=f"Sell ({len(sells)})",
                zorder=5,
                edgecolors="black",
            )
        if liqs:
            ax.scatter(
                [dates[t.index] for t in liqs],
                [t.price for t in liqs],
                marker="x",
                c="purple",
                s=100,
                label="Final liquidate",
                zorder=5,
            )
        ax.set_yscale("log")
        ax.set_ylabel("Price (USD, log)")
        ax.set_title(f"{label}: fitness = ${res.fitness:.0f}")
        ax.legend(loc="upper left", fontsize=8)
    fig.suptitle(
        f"Best train-fitness bot: {algo} on {bot_name}, seed={seed}",
        y=1.00,
    )
    out = FIGS_DIR / "09_best_bot_trades.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #


ALL_FIGURE_FUNCS = [
    fig_01_data_split,
    fig_02_wma_demo,
    fig_03_wma_comparison,
    fig_04_train_fitness_boxplot,
    fig_05_convergence_curves,
    fig_06_train_test_scatter,
    fig_07_test_fitness_bar,
    fig_08_b2_weight_shares,
    fig_09_best_bot_trades,
]


def make_all() -> list[Path]:
    FIGS_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for func in ALL_FIGURE_FUNCS:
        path = func()
        paths.append(path)
        print(f"  ✓ {path.name}")
    return paths


def main() -> None:
    print(f"Generating figures into {FIGS_DIR.relative_to(REPO_ROOT)} ...")
    paths = make_all()
    print(f"\n{len(paths)} figures written.")


if __name__ == "__main__":
    main()
