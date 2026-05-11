"""Unit tests for `tradebot.bot.bots`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.bot.backtest import INITIAL_CASH, backtest_fitness
from tradebot.bot.bots import Bot, BotB1, BotB2


# --------------------------------------------------------------------------- #
# Shared interface
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("cls", [BotB1, BotB2])
def test_bot_class_exposes_required_attributes(cls):
    assert issubclass(cls, Bot)
    assert isinstance(cls.NAME, str) and cls.NAME != ""
    assert isinstance(cls.N_PARAMS, int) and cls.N_PARAMS > 0
    assert cls.LOWER.shape == (cls.N_PARAMS,)
    assert cls.UPPER.shape == (cls.N_PARAMS,)
    assert np.all(cls.LOWER < cls.UPPER)


@pytest.mark.parametrize("cls", [BotB1, BotB2])
def test_bot_bounds_returns_copies(cls):
    lo, hi = cls.bounds()
    lo[:] = -999
    hi[:] = +999
    # Original LOWER/UPPER must be unchanged.
    assert not np.allclose(cls.LOWER, -999)
    assert not np.allclose(cls.UPPER, +999)


@pytest.mark.parametrize("cls", [BotB1, BotB2])
def test_bot_random_params_within_bounds(cls):
    rng = np.random.default_rng(0)
    for _ in range(20):
        p = cls.random_params(rng)
        assert p.shape == (cls.N_PARAMS,)
        assert np.all(p >= cls.LOWER)
        assert np.all(p <= cls.UPPER)


# --------------------------------------------------------------------------- #
# B1: 2-D dual-SMA crossover
# --------------------------------------------------------------------------- #


def test_b1_wrong_param_shape_raises():
    with pytest.raises(ValueError, match=r"shape=\(2,\)"):
        BotB1.signals(np.arange(50, dtype=float), np.array([10.0]))


def test_b1_signals_have_same_length_as_prices():
    prices = np.arange(1, 101, dtype=float)
    sigs = BotB1.signals(prices, np.array([5.0, 20.0]))
    assert sigs.shape == (100,)


def test_b1_equal_windows_degenerate_to_no_trades():
    prices = np.arange(1, 101, dtype=float)
    sigs = BotB1.signals(prices, np.array([10.0, 10.0]))
    np.testing.assert_array_equal(sigs, np.zeros(100))


def test_b1_swapped_window_order_yields_same_signals():
    """B1 internally orders the two windows, so [10, 30] and [30, 10] must
    produce identical signal vectors."""
    rng = np.random.default_rng(1)
    prices = rng.uniform(50, 150, size=300)
    a = BotB1.signals(prices, np.array([10.0, 30.0]))
    b = BotB1.signals(prices, np.array([30.0, 10.0]))
    np.testing.assert_allclose(a, b)


def test_b1_window_too_long_for_prices_returns_zeros():
    prices = np.arange(1, 21, dtype=float)  # 20 days
    sigs = BotB1.signals(prices, np.array([5.0, 100.0]))
    np.testing.assert_array_equal(sigs, np.zeros(20))


def test_b1_warmup_region_is_zero():
    """No trades may be emitted inside the longest window's warm-up."""
    prices = np.arange(1, 201, dtype=float)
    N_long = 30
    sigs = BotB1.signals(prices, np.array([5.0, float(N_long)]))
    np.testing.assert_array_equal(sigs[: N_long - 1], np.zeros(N_long - 1))


def test_b1_emits_at_least_one_signal_on_noisy_data():
    """A sinusoidal-with-noise series should produce at least one crossover."""
    rng = np.random.default_rng(7)
    t = np.arange(500)
    prices = 100 + 20 * np.sin(2 * np.pi * t / 80) + rng.normal(scale=2.0, size=500)
    sigs = BotB1.signals(prices, np.array([5.0, 30.0]))
    assert np.any(sigs != 0)


# --------------------------------------------------------------------------- #
# B2: 14-D compound
# --------------------------------------------------------------------------- #


def test_b2_wrong_param_shape_raises():
    with pytest.raises(ValueError, match=r"shape=\(14,\)"):
        BotB2.signals(np.arange(50, dtype=float), np.zeros(7))


def test_b2_signals_have_same_length_as_prices():
    prices = np.arange(1, 301, dtype=float)
    params = (BotB2.LOWER + BotB2.UPPER) / 2  # midpoint of bounds
    sigs = BotB2.signals(prices, params)
    assert sigs.shape == (300,)


def test_b2_all_zero_weights_in_high_component_returns_zeros():
    """Degenerate weights → bot emits no trades."""
    prices = np.arange(1, 301, dtype=float)
    params = (BotB2.LOWER + BotB2.UPPER) / 2
    params[0:3] = 0.0  # HIGH weights all zero
    sigs = BotB2.signals(prices, params)
    np.testing.assert_array_equal(sigs, np.zeros(300))


def test_b2_all_zero_weights_in_low_component_returns_zeros():
    prices = np.arange(1, 301, dtype=float)
    params = (BotB2.LOWER + BotB2.UPPER) / 2
    params[7:10] = 0.0  # LOW weights all zero
    sigs = BotB2.signals(prices, params)
    np.testing.assert_array_equal(sigs, np.zeros(300))


def test_b2_clips_out_of_range_params():
    """Optimiser may propose out-of-range values — they should be clipped
    rather than crash."""
    prices = np.arange(1, 301, dtype=float)
    bad = np.array(
        [
            -5.0, 2.0, 0.5,        # HIGH weights (out of [0,1])
            -1.0, 5.0, 999.0,      # HIGH windows (out of [2,200])
            5.0,                   # HIGH alpha (out of (0,1])
            0.5, 0.5, 0.5,
            10.0, 20.0, 30.0,
            0.3,
        ]
    )
    # Should not raise.
    sigs = BotB2.signals(prices, bad)
    assert sigs.shape == (300,)


def test_b2_collapses_to_b1_like_when_only_sma_weights_active():
    """Setting w2=w3=0 on both components reduces B2 to a pure SMA-vs-SMA
    crossover — should at least produce non-zero signals on noisy data."""
    rng = np.random.default_rng(3)
    t = np.arange(400)
    prices = 100 + 10 * np.sin(2 * np.pi * t / 60) + rng.normal(scale=1.0, size=400)
    params = np.array(
        [
            1.0, 0.0, 0.0,         # HIGH: SMA only
            5.0, 5.0, 5.0,         # windows
            0.3,                   # alpha (unused)
            1.0, 0.0, 0.0,         # LOW: SMA only
            30.0, 30.0, 30.0,
            0.3,
        ]
    )
    sigs = BotB2.signals(prices, params)
    assert np.any(sigs != 0)


def test_b2_warmup_region_is_zero():
    """No trades inside the longest of all six windows."""
    prices = np.arange(1, 301, dtype=float)
    params = np.array(
        [
            0.5, 0.5, 0.5,
            5.0, 5.0, 5.0,
            0.3,
            0.5, 0.5, 0.5,
            10.0, 50.0, 80.0,  # max = 80
            0.3,
        ]
    )
    sigs = BotB2.signals(prices, params)
    max_n = 80
    np.testing.assert_array_equal(sigs[: max_n - 1], np.zeros(max_n - 1))


# --------------------------------------------------------------------------- #
# Integration with the back-test engine
# --------------------------------------------------------------------------- #


def test_b1_plus_backtest_no_trades_recovers_initial_cash():
    """A degenerate B1 (equal windows) trades nothing → fitness == 1000."""
    prices = np.arange(1, 101, dtype=float)
    sigs = BotB1.signals(prices, np.array([10.0, 10.0]))
    assert backtest_fitness(prices, sigs) == INITIAL_CASH


def test_b1_plus_backtest_finite_and_positive_on_real_data():
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")
    sigs = BotB1.signals(prices, np.array([10.0, 50.0]))
    fitness = backtest_fitness(prices, sigs)
    assert np.isfinite(fitness)
    assert fitness > 0


def test_b2_plus_backtest_finite_and_positive_on_real_data():
    pytest.importorskip("pyarrow")
    try:
        from tradebot.data.load import load_close
        prices = load_close("train")
    except FileNotFoundError:
        pytest.skip("Processed train parquet not present.")
    rng = np.random.default_rng(42)
    params = BotB2.random_params(rng)
    sigs = BotB2.signals(prices, params)
    fitness = backtest_fitness(prices, sigs)
    assert np.isfinite(fitness)
    assert fitness > 0
