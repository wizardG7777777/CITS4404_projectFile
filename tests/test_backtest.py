"""Unit tests for `tradebot.bot.backtest`.

Each test references the PDF §3 *Evaluation of Bots* rule it verifies.
"""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.bot.backtest import (
    FEE_RATE,
    INITIAL_CASH,
    BacktestResult,
    Trade,
    backtest_detailed,
    backtest_fitness,
)


# --------------------------------------------------------------------------- #
# Constants pinned to PDF §3.
# --------------------------------------------------------------------------- #


def test_constants_match_pdf_specification():
    assert INITIAL_CASH == 1000.0
    assert FEE_RATE == 0.03


# --------------------------------------------------------------------------- #
# Trading behaviour (PDF rules 1-5).
# --------------------------------------------------------------------------- #


def test_no_signals_preserve_initial_cash():
    """No trades → fitness == initial cash (PDF rule 1)."""
    prices = np.array([100.0, 200.0, 150.0])
    signals = np.array([0, 0, 0])
    assert backtest_fitness(prices, signals) == INITIAL_CASH


def test_sell_without_holding_btc_is_noop():
    """Sell signals before any buy do nothing (PDF rule 3 only fires when
    'holding bitcoin')."""
    prices = np.array([100.0, 200.0])
    signals = np.array([-1, -1])
    assert backtest_fitness(prices, signals) == INITIAL_CASH


def test_buy_then_liquidate_at_higher_price():
    """Buy at 100, hold, liquidate at 200. Two fees applied (PDF rules 2+5)."""
    prices = np.array([100.0, 200.0])
    signals = np.array([1, 0])
    # After buy: btc = 1000 * 0.97 / 100 = 9.7, cash = 0.
    # Final liquidation @ 200: cash = 9.7 * 200 * 0.97 = 1881.8.
    assert backtest_fitness(prices, signals) == pytest.approx(1881.8)


def test_buy_then_sell_no_final_liquidation():
    """Buy at 100, sell at 200. No BTC at end → no rule-5 liquidation."""
    prices = np.array([100.0, 200.0])
    signals = np.array([1, -1])
    assert backtest_fitness(prices, signals) == pytest.approx(1881.8)


def test_second_buy_while_holding_btc_is_noop():
    """PDF rule 2 only fires when 'holding cash'."""
    prices = np.array([100.0, 50.0, 100.0])
    signals = np.array([1, 1, 0])  # second buy should be ignored
    # First buy: btc = 9.7. Second buy: noop. Liquidate @ 100: 9.7 * 100 * 0.97
    assert backtest_fitness(prices, signals) == pytest.approx(9.7 * 100 * 0.97)


def test_second_sell_while_holding_cash_is_noop():
    """PDF rule 3 only fires when 'holding bitcoin'."""
    prices = np.array([100.0, 100.0, 100.0])
    signals = np.array([1, -1, -1])  # second sell should be ignored
    # Round-trip at price 100: 1000 * 0.97 * 0.97 = 940.9
    assert backtest_fitness(prices, signals) == pytest.approx(1000.0 * 0.97**2)


def test_3pct_fee_round_trip_at_same_price():
    """Buy then sell at the same price loses exactly 1 - 0.97^2 = 5.91%."""
    prices = np.array([100.0, 100.0])
    signals = np.array([1, -1])
    assert backtest_fitness(prices, signals) == pytest.approx(1000.0 * 0.97**2)


def test_final_liquidation_pays_fee():
    """End-of-sequence liquidation is a transaction (PDF rule 4 applies)."""
    prices = np.array([100.0, 100.0])
    signals = np.array([1, 0])
    # Buy + forced liquidation @ same price = 1000 * 0.97^2
    assert backtest_fitness(prices, signals) == pytest.approx(1000.0 * 0.97**2)


def test_same_day_buy_and_sell_keeps_buy_only():
    """If both rules are triggerable on the same day, buy fires first; the
    'elif' guard prevents a same-day sell from immediately reversing it."""
    prices = np.array([100.0, 100.0])
    signals = np.array([2, 0])  # positive => buy
    # After buy: btc = 9.7. Liquidate @ 100: 940.9.
    assert backtest_fitness(prices, signals) == pytest.approx(1000.0 * 0.97**2)


def test_fractional_signals_treated_by_sign():
    """Signal threshold is just sign, not magnitude (consistent with PDF
    §2.3 Eq.(6) which can emit fractional values)."""
    prices = np.array([100.0, 200.0])
    signals_unit = np.array([1, -1])
    signals_frac = np.array([0.5, -0.5])
    assert backtest_fitness(prices, signals_unit) == pytest.approx(
        backtest_fitness(prices, signals_frac)
    )


# --------------------------------------------------------------------------- #
# Custom initial cash and fee rate (for sensitivity analysis).
# --------------------------------------------------------------------------- #


def test_custom_initial_cash_scales_linearly():
    """Doubling initial cash should double final fitness (linear back-test)."""
    prices = np.array([100.0, 200.0])
    signals = np.array([1, -1])
    a = backtest_fitness(prices, signals, initial_cash=1000.0)
    b = backtest_fitness(prices, signals, initial_cash=2000.0)
    assert b == pytest.approx(2 * a)


def test_zero_fee_round_trip_breaks_even_at_same_price():
    prices = np.array([100.0, 100.0])
    signals = np.array([1, -1])
    assert backtest_fitness(prices, signals, fee_rate=0.0) == pytest.approx(1000.0)


# --------------------------------------------------------------------------- #
# Input validation.
# --------------------------------------------------------------------------- #


def test_length_mismatch_raises():
    with pytest.raises(ValueError, match="same length"):
        backtest_fitness(np.array([100.0, 200.0]), np.array([0]))


def test_empty_inputs_raise():
    with pytest.raises(ValueError, match="non-empty"):
        backtest_fitness(np.array([]), np.array([]))


def test_nonfinite_prices_raise():
    with pytest.raises(ValueError, match="finite"):
        backtest_fitness(np.array([100.0, np.nan]), np.array([0, 0]))


def test_nonpositive_prices_raise():
    with pytest.raises(ValueError, match="strictly positive"):
        backtest_fitness(np.array([100.0, 0.0]), np.array([0, 0]))
    with pytest.raises(ValueError, match="strictly positive"):
        backtest_fitness(np.array([100.0, -1.0]), np.array([0, 0]))


def test_higher_dimensional_prices_raise():
    with pytest.raises(ValueError, match="1-D"):
        backtest_fitness(np.array([[100.0]]), np.array([[0]]))


# --------------------------------------------------------------------------- #
# `backtest_detailed`: trade-log audit.
# --------------------------------------------------------------------------- #


def test_detailed_returns_backtest_result_with_metadata():
    res = backtest_detailed(np.array([100.0, 200.0]), np.array([1, -1]))
    assert isinstance(res, BacktestResult)
    assert res.fitness == pytest.approx(1881.8)
    assert res.initial_cash == INITIAL_CASH
    assert res.fee_rate == FEE_RATE


def test_detailed_trade_log_buy_then_sell():
    prices = np.array([100.0, 200.0])
    signals = np.array([1, -1])
    res = backtest_detailed(prices, signals)
    assert res.n_trades == 2

    buy, sell = res.trades
    assert isinstance(buy, Trade)
    assert buy.action == "buy"
    assert buy.index == 0
    assert buy.price == 100.0
    assert buy.cash_before == 1000.0
    assert buy.cash_after == 0.0
    assert buy.btc_after == pytest.approx(9.7)
    assert buy.fee_paid == pytest.approx(30.0)  # 1000 * 0.03

    assert sell.action == "sell"
    assert sell.index == 1
    assert sell.price == 200.0
    assert sell.btc_before == pytest.approx(9.7)
    assert sell.btc_after == 0.0
    assert sell.cash_after == pytest.approx(1881.8)
    assert sell.fee_paid == pytest.approx(9.7 * 200.0 * 0.03)


def test_detailed_records_liquidation_when_btc_held_at_end():
    prices = np.array([100.0, 200.0])
    signals = np.array([1, 0])
    res = backtest_detailed(prices, signals)
    assert res.n_trades == 2

    buy, liq = res.trades
    assert buy.action == "buy"
    assert liq.action == "liquidate"
    assert liq.index == 1  # final day
    assert liq.price == 200.0


def test_detailed_no_trades_when_no_signals():
    res = backtest_detailed(np.array([100.0, 200.0]), np.array([0, 0]))
    assert res.n_trades == 0
    assert res.fitness == INITIAL_CASH


def test_detailed_fitness_matches_fast_path_random():
    """`backtest_fitness` and `backtest_detailed` must return identical fitness."""
    rng = np.random.default_rng(20260510)
    prices = rng.uniform(50.0, 200.0, size=500)
    signals = rng.choice([-1, 0, 1], size=500, p=[0.2, 0.6, 0.2])
    fast = backtest_fitness(prices, signals)
    detailed = backtest_detailed(prices, signals).fitness
    assert fast == pytest.approx(detailed)


# --------------------------------------------------------------------------- #
# Smoke test on real BTC training data.
# --------------------------------------------------------------------------- #


def test_buy_and_hold_on_real_btc_train_data():
    """Buy-and-hold baseline: buy on day 0, liquidate at end. Should at
    minimum produce a positive fitness on the 2014-2019 BTC bull market."""
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present; run tradebot.data.load")

    signals = np.zeros(prices.size, dtype=np.int8)
    signals[0] = 1  # one buy on day 0; the rest is liquidate-at-end
    fitness = backtest_fitness(prices, signals)

    # Manual closed form: 1000 * 0.97 / p[0] * p[-1] * 0.97
    expected = 1000.0 * 0.97 / prices[0] * prices[-1] * 0.97
    assert fitness == pytest.approx(expected)
    assert fitness > INITIAL_CASH  # BTC ended 2019 well above its 2014 price
