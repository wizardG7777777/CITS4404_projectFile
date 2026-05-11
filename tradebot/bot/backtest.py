"""Back-test engine for the trading bot.

Implements the five rules listed in PDF §3 *Evaluation of Bots* verbatim:

  1. "the bot begins with $1000 USD (and zero bitcoin)"
  2. "each time the bot is holding cash and generates a *buy* signal, it
     trades all the cash (minus fees) for bitcoin at the current price"
  3. "each time the bot is holding bitcoin and generates a *sell* signal, it
     trades all its bitcoin for cash (minus fees) at the current price"
  4. "each transaction attracts a fee of 3%"
  5. "at the end of the sequence, the bot sells its remaining bitcoin at the
     final price"

  fitness = "the cash it is holding at the end of the evaluation"

Signal convention (decoupled from any specific bot — Tasks #8/#10/#11/#12):

  signal[i] > 0  -> buy  (only acts if currently holding cash)
  signal[i] < 0  -> sell (only acts if currently holding BTC)
  signal[i] == 0 -> hold

Two entry points:
  `backtest_fitness(prices, signals)`  -> float
      Lean path used inside the optimisation hot loop.
  `backtest_detailed(prices, signals)` -> BacktestResult
      Same simulation but records every trade for analysis / plots.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


# PDF §3 *Evaluation of Bots* constants — kept at module level for visibility.
INITIAL_CASH: float = 1000.0
FEE_RATE: float = 0.03


__all__ = [
    "INITIAL_CASH",
    "FEE_RATE",
    "Trade",
    "BacktestResult",
    "backtest_fitness",
    "backtest_detailed",
]


@dataclass(frozen=True)
class Trade:
    """A single executed transaction.

    `action` is one of {"buy", "sell", "liquidate"} where "liquidate" denotes
    the forced final-day sell prescribed by PDF §3 rule 5.
    """

    index: int
    action: Literal["buy", "sell", "liquidate"]
    price: float
    cash_before: float
    btc_before: float
    cash_after: float
    btc_after: float
    fee_paid: float


@dataclass
class BacktestResult:
    fitness: float
    trades: list[Trade]
    initial_cash: float
    fee_rate: float

    @property
    def n_trades(self) -> int:
        return len(self.trades)


# --------------------------------------------------------------------------- #
# Input validation (shared by both entry points)
# --------------------------------------------------------------------------- #


def _validate(
    prices: np.ndarray, signals: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    prices_arr = np.asarray(prices, dtype=np.float64)
    signals_arr = np.asarray(signals)
    if prices_arr.ndim != 1:
        raise ValueError(
            f"prices must be a 1-D array; got shape={prices_arr.shape}"
        )
    if signals_arr.ndim != 1:
        raise ValueError(
            f"signals must be a 1-D array; got shape={signals_arr.shape}"
        )
    if prices_arr.size != signals_arr.size:
        raise ValueError(
            "prices and signals must have the same length; "
            f"got len(prices)={prices_arr.size}, len(signals)={signals_arr.size}"
        )
    if prices_arr.size == 0:
        raise ValueError("prices and signals must be non-empty")
    if not np.all(np.isfinite(prices_arr)):
        raise ValueError("prices must be finite (no NaN or inf)")
    if np.any(prices_arr <= 0):
        raise ValueError("all prices must be strictly positive")
    return prices_arr, signals_arr


# --------------------------------------------------------------------------- #
# Fitness-only path (hot loop for optimisation)
# --------------------------------------------------------------------------- #


def backtest_fitness(
    prices: np.ndarray,
    signals: np.ndarray,
    *,
    initial_cash: float = INITIAL_CASH,
    fee_rate: float = FEE_RATE,
) -> float:
    """Run the PDF §3 back-test and return ending cash (fitness)."""
    prices_arr, signals_arr = _validate(prices, signals)
    one_minus_fee = 1.0 - float(fee_rate)
    cash = float(initial_cash)
    btc = 0.0
    n = prices_arr.size

    for i in range(n):
        s = signals_arr[i]
        p = prices_arr[i]
        if s > 0 and cash > 0.0:
            # PDF rule 2: trade all cash (minus fees) for BTC at price p.
            btc = (cash * one_minus_fee) / p
            cash = 0.0
        elif s < 0 and btc > 0.0:
            # PDF rule 3: trade all BTC for cash (minus fees) at price p.
            cash = btc * p * one_minus_fee
            btc = 0.0

    # PDF rule 5: sell remaining BTC at the final price. Treated as a
    # transaction → fee applies (rule 4: "each transaction attracts a fee of 3%").
    if btc > 0.0:
        cash = btc * prices_arr[-1] * one_minus_fee

    return cash


# --------------------------------------------------------------------------- #
# Detailed path (analysis / plots / trade-by-trade audit)
# --------------------------------------------------------------------------- #


def backtest_detailed(
    prices: np.ndarray,
    signals: np.ndarray,
    *,
    initial_cash: float = INITIAL_CASH,
    fee_rate: float = FEE_RATE,
) -> BacktestResult:
    """Run the same back-test and return the full trade log."""
    prices_arr, signals_arr = _validate(prices, signals)
    fee = float(fee_rate)
    one_minus_fee = 1.0 - fee
    cash = float(initial_cash)
    btc = 0.0
    trades: list[Trade] = []
    n = prices_arr.size

    for i in range(n):
        s = signals_arr[i]
        p = float(prices_arr[i])
        if s > 0 and cash > 0.0:
            fee_paid = cash * fee
            new_btc = (cash * one_minus_fee) / p
            trades.append(
                Trade(
                    index=i,
                    action="buy",
                    price=p,
                    cash_before=cash,
                    btc_before=btc,
                    cash_after=0.0,
                    btc_after=new_btc,
                    fee_paid=fee_paid,
                )
            )
            cash = 0.0
            btc = new_btc
        elif s < 0 and btc > 0.0:
            gross = btc * p
            fee_paid = gross * fee
            new_cash = gross * one_minus_fee
            trades.append(
                Trade(
                    index=i,
                    action="sell",
                    price=p,
                    cash_before=cash,
                    btc_before=btc,
                    cash_after=new_cash,
                    btc_after=0.0,
                    fee_paid=fee_paid,
                )
            )
            cash = new_cash
            btc = 0.0

    if btc > 0.0:
        final_p = float(prices_arr[-1])
        gross = btc * final_p
        fee_paid = gross * fee
        new_cash = gross * one_minus_fee
        trades.append(
            Trade(
                index=n - 1,
                action="liquidate",
                price=final_p,
                cash_before=cash,
                btc_before=btc,
                cash_after=new_cash,
                btc_after=0.0,
                fee_paid=fee_paid,
            )
        )
        cash = new_cash
        btc = 0.0

    return BacktestResult(
        fitness=cash,
        trades=trades,
        initial_cash=float(initial_cash),
        fee_rate=fee,
    )
