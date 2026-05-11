"""Concrete bot implementations.

Two hypothesis spaces per the scope frozen in `docs/d2_requirement_alignment.md`:

- `BotB1` — 2-D baseline (two SMAs + crossover, PDF §2.3 Figure 6 example).
- `BotB2` — ~14-D compound (high/low components each as a weighted sum of
            SMA/LMA/EMA per PDF §3 Eq.(7), then a crossover between them).

The 21-D MACD-style variant (PDF §3) is intentionally out of scope.

Shared interface (each class exposes):
  NAME       — short identifier for logs / result tables.
  N_PARAMS   — dimensionality of the parameter vector.
  LOWER, UPPER — lower / upper bounds for each parameter (np.ndarray of
                 length N_PARAMS).
  bounds()   — convenience returning (LOWER.copy(), UPPER.copy()).
  signals(prices, params) → np.ndarray  same-length signal with the
                 convention used by tradebot.bot.backtest:
                   > 0  -> buy   < 0  -> sell   == 0 -> hold.

For invalid / degenerate parameter configurations (e.g. equal windows,
all-zero weights, windows exceeding price length) the bots return an
all-zero signal vector → the back-test simulates "no trades", producing
fitness == INITIAL_CASH. This gives the optimiser a finite, well-defined
fitness for every point in the search space (no NaN, no exceptions
escaping the hot loop).

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np

from .signals import crossover_signals
from .wma import ema_filter, lma_filter, sma_filter, wma


__all__ = ["Bot", "BotB1", "BotB2"]


# --------------------------------------------------------------------------- #
# Shared base
# --------------------------------------------------------------------------- #


class Bot:
    """Base class defining the shared bot interface.

    Subclasses set the NAME / N_PARAMS / LOWER / UPPER attributes and override
    `signals`.
    """

    NAME: str = ""
    N_PARAMS: int = 0
    LOWER: np.ndarray = np.array([])
    UPPER: np.ndarray = np.array([])

    @classmethod
    def bounds(cls) -> tuple[np.ndarray, np.ndarray]:
        """Return (lower, upper) copies of the bounds arrays."""
        return cls.LOWER.copy(), cls.UPPER.copy()

    @classmethod
    def random_params(cls, rng: np.random.Generator) -> np.ndarray:
        """Sample one parameter vector uniformly inside the bounds box."""
        return rng.uniform(cls.LOWER, cls.UPPER)

    @staticmethod
    def signals(prices: np.ndarray, params: np.ndarray) -> np.ndarray:
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# B1: 2-D baseline (PDF §2.3 example)
# --------------------------------------------------------------------------- #


class BotB1(Bot):
    """Two-SMA crossover bot (PDF §2.3 Figure 6).

    Parameter vector (2-D, continuous → rounded to int):
        params[0]  window A
        params[1]  window B

    The smaller of the two is treated as the high-frequency (fast) SMA and
    the larger as the low-frequency (slow) SMA, so the optimiser is free to
    output them in either order.
    """

    NAME = "B1_dual_sma"
    N_PARAMS = 2
    LOWER = np.array([2.0, 2.0])
    UPPER = np.array([300.0, 300.0])

    @staticmethod
    def signals(prices: np.ndarray, params: np.ndarray) -> np.ndarray:
        prices = np.asarray(prices, dtype=np.float64)
        params = np.asarray(params, dtype=np.float64)
        if params.shape != (BotB1.N_PARAMS,):
            raise ValueError(
                f"BotB1 expects shape=({BotB1.N_PARAMS},); got shape={params.shape}"
            )
        # Clip defensively (optimiser may overshoot bounds during search).
        p = np.clip(params, BotB1.LOWER, BotB1.UPPER)
        N1 = max(1, int(round(p[0])))
        N2 = max(1, int(round(p[1])))
        N_short, N_long = min(N1, N2), max(N1, N2)

        # Degenerate cases — emit no trades.
        if N_short == N_long or N_long >= prices.size:
            return np.zeros(prices.size, dtype=np.float64)

        sma_short = wma(prices, N_short, sma_filter(N_short))
        sma_long = wma(prices, N_long, sma_filter(N_long))
        sigs = crossover_signals(sma_short, sma_long)
        # Suppress trades inside the longest WMA's warm-up region.
        sigs[: N_long - 1] = 0.0
        return sigs


# --------------------------------------------------------------------------- #
# B2: ~14-D compound bot (PDF §3 Eq.(7))
# --------------------------------------------------------------------------- #


class BotB2(Bot):
    """Compound mixture-of-WMAs bot (PDF §3 Eq.(7) extended to both bands).

    Parameter vector (14-D), two 7-element blocks for HIGH and LOW components:
        HIGH-frequency block:
          params[0]  w1_h   SMA weight    (in [0, 1])
          params[1]  w2_h   LMA weight    (in [0, 1])
          params[2]  w3_h   EMA weight    (in [0, 1])
          params[3]  d1_h   SMA window    (rounded to int, in [2, 200])
          params[4]  d2_h   LMA window
          params[5]  d3_h   EMA window
          params[6]  α_h    EMA decay     (in (0, 1])
        LOW-frequency block (same layout):
          params[7..13]: w1_l, w2_l, w3_l, d1_l, d2_l, d3_l, α_l

    Each component computes
        component = (w1·SMA(d1) + w2·LMA(d2) + w3·EMA(d3, α)) / Σ w_i
    (PDF §3 Eq.(7)). The HIGH-vs-LOW crossover then produces the buy/sell
    signal.

    The bounds are intentionally symmetric for HIGH and LOW — the optimiser
    is free to discover that one should be smaller than the other.
    """

    NAME = "B2_compound"
    N_PARAMS = 14
    LOWER = np.array(
        [
            0.0, 0.0, 0.0,           # HIGH weights
            2.0, 2.0, 2.0,           # HIGH windows
            0.01,                    # HIGH alpha
            0.0, 0.0, 0.0,           # LOW weights
            2.0, 2.0, 2.0,           # LOW windows
            0.01,                    # LOW alpha
        ]
    )
    UPPER = np.array(
        [
            1.0, 1.0, 1.0,
            200.0, 200.0, 200.0,
            1.0,
            1.0, 1.0, 1.0,
            200.0, 200.0, 200.0,
            1.0,
        ]
    )

    @staticmethod
    def signals(prices: np.ndarray, params: np.ndarray) -> np.ndarray:
        prices = np.asarray(prices, dtype=np.float64)
        params = np.asarray(params, dtype=np.float64)
        if params.shape != (BotB2.N_PARAMS,):
            raise ValueError(
                f"BotB2 expects shape=({BotB2.N_PARAMS},); got shape={params.shape}"
            )
        p = np.clip(params, BotB2.LOWER, BotB2.UPPER)

        high = _compound_wma(prices, p[:7])
        low = _compound_wma(prices, p[7:14])
        if high is None or low is None:
            return np.zeros(prices.size, dtype=np.float64)

        sigs = crossover_signals(high, low)
        # Suppress warm-up: longest window across all six WMAs in the bot.
        windows = (
            int(round(p[3])), int(round(p[4])), int(round(p[5])),
            int(round(p[10])), int(round(p[11])), int(round(p[12])),
        )
        max_n = max(windows)
        sigs[: max_n - 1] = 0.0
        return sigs


# --------------------------------------------------------------------------- #
# Internal helper for B2 component evaluation.
# --------------------------------------------------------------------------- #


def _compound_wma(prices: np.ndarray, sub: np.ndarray) -> np.ndarray | None:
    """Compute one PDF §3 Eq.(7) component, or None if parameters are
    degenerate (all weights zero, or any window exceeds the series length)."""
    w1, w2, w3, d1, d2, d3, alpha = sub
    weight_sum = w1 + w2 + w3
    if weight_sum <= 1e-9:
        return None

    N1 = max(1, int(round(d1)))
    N2 = max(1, int(round(d2)))
    N3 = max(1, int(round(d3)))
    if max(N1, N2, N3) >= prices.size:
        return None

    sma = wma(prices, N1, sma_filter(N1))
    lma = wma(prices, N2, lma_filter(N2))
    ema = wma(prices, N3, ema_filter(N3, alpha))
    return (w1 * sma + w2 * lma + w3 * ema) / weight_sum
