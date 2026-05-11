"""Unit tests for `tradebot.bot.signals`."""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.bot.signals import crossover_signals, edge_filter


# --------------------------------------------------------------------------- #
# edge_filter — PDF Eq.(6)
# --------------------------------------------------------------------------- #


def test_edge_filter_matches_pdf_eq6():
    np.testing.assert_array_equal(edge_filter(), np.array([0.5, -0.5]))


# --------------------------------------------------------------------------- #
# crossover_signals — pipeline tests
# --------------------------------------------------------------------------- #


def test_crossover_no_crosses_returns_all_zero():
    """When high is always strictly above low, no crossings occur."""
    high = np.array([2.0, 3.0, 4.0, 5.0])
    low = np.array([1.0, 2.0, 3.0, 4.0])
    out = crossover_signals(high, low)
    np.testing.assert_array_equal(out, np.zeros(4))


def test_crossover_single_golden_cross_emits_positive_signal():
    """Sign series goes from -1 to +1 at index 2 → buy at index 2."""
    high = np.array([1.0, 1.0, 3.0, 3.0])
    low = np.array([2.0, 2.0, 2.0, 2.0])
    # sign(high-low) = [-1, -1, +1, +1]
    out = crossover_signals(high, low)
    assert out[0] == 0.0
    assert out[1] == 0.0
    assert out[2] > 0  # buy at the cross
    assert out[3] == 0.0


def test_crossover_single_death_cross_emits_negative_signal():
    """Sign series goes from +1 to -1 at index 2 → sell at index 2."""
    high = np.array([3.0, 3.0, 1.0, 1.0])
    low = np.array([2.0, 2.0, 2.0, 2.0])
    # sign(high-low) = [+1, +1, -1, -1]
    out = crossover_signals(high, low)
    assert out[0] == 0.0
    assert out[1] == 0.0
    assert out[2] < 0  # sell at the cross
    assert out[3] == 0.0


def test_crossover_alternating_pattern():
    """Sign series [-1, +1, -1, +1, -1] should emit alternating signals."""
    high = np.array([0.0, 2.0, 0.0, 2.0, 0.0])
    low = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    # sign(high-low) = [-1, +1, -1, +1, -1]
    out = crossover_signals(high, low)
    assert out[0] == 0.0
    assert out[1] > 0
    assert out[2] < 0
    assert out[3] > 0
    assert out[4] < 0


def test_crossover_first_sample_is_always_zero():
    """The first sample never has a prior to compare → output[0] == 0."""
    rng = np.random.default_rng(42)
    high = rng.uniform(0, 10, size=50)
    low = rng.uniform(0, 10, size=50)
    out = crossover_signals(high, low)
    assert out[0] == 0.0


def test_crossover_output_length_equals_input_length():
    for n in (1, 2, 5, 100):
        out = crossover_signals(np.ones(n), np.zeros(n))
        assert out.shape == (n,)


def test_crossover_mismatched_shapes_raises():
    with pytest.raises(ValueError, match="same shape"):
        crossover_signals(np.array([1.0, 2.0]), np.array([1.0]))


def test_crossover_higher_dimensional_raises():
    with pytest.raises(ValueError, match="1-D"):
        crossover_signals(np.array([[1.0, 2.0]]), np.array([[1.0, 2.0]]))


def test_crossover_empty_raises():
    with pytest.raises(ValueError, match="non-empty"):
        crossover_signals(np.array([]), np.array([]))


def test_crossover_signs_compatible_with_backtest():
    """The convention is: positive=buy, negative=sell. Check that a sequence
    of crosses maps to a sensible buy/sell trace through the back-test."""
    from tradebot.bot.backtest import backtest_detailed

    # High > Low for steps 1-2 (buy at 1), then Low > High (sell at 3).
    high = np.array([0.0, 2.0, 2.0, 0.0, 0.0])
    low = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    sigs = crossover_signals(high, low)
    prices = np.array([100.0, 100.0, 100.0, 100.0, 100.0])
    res = backtest_detailed(prices, sigs)
    actions = [t.action for t in res.trades]
    # Expect one buy + one sell (the second cross happens before the final
    # sample so no forced liquidation is needed).
    assert actions == ["buy", "sell"]
