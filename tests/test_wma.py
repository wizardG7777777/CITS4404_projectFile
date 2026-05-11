"""Unit tests for `tradebot.bot.wma`.

Each test references the PDF clause it verifies.
"""
from __future__ import annotations

import numpy as np
import pytest

from tradebot.bot.wma import (
    ema_filter,
    lma_filter,
    pad,
    sma_filter,
    wma,
)


# --------------------------------------------------------------------------- #
# pad — PDF §2.1 paragraph after Eq.(3): "flip the first part of the
# sequence over (rotate it 180°)"
# --------------------------------------------------------------------------- #


def test_pad_n1_returns_input_unchanged():
    P = np.array([1.0, 2.0, 3.0])
    out = pad(P, N=1)
    np.testing.assert_array_equal(out, P)


def test_pad_length_equals_len_plus_n_minus_one():
    P = np.arange(10, dtype=float)
    for N in (2, 3, 5, 10):
        assert pad(P, N).shape == (len(P) + N - 1,)


def test_pad_formula_matches_pdf():
    """pad(P, N) prepends `-np.flip(P[1:N])` to P (PDF §2.1 code listing)."""
    P = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    out = pad(P, N=3)
    # P[1:3] = [2, 3];  np.flip(...) = [3, 2];  -np.flip(...) = [-3, -2]
    np.testing.assert_array_equal(out, np.array([-3.0, -2.0, 1.0, 2.0, 3.0, 4.0, 5.0]))


def test_pad_invalid_window_raises():
    with pytest.raises(ValueError, match=r"N must be a positive integer; got N=0"):
        pad(np.array([1.0, 2.0]), N=0)
    with pytest.raises(ValueError, match=r"N must be a positive integer; got N=-1"):
        pad(np.array([1.0, 2.0]), N=-1)


def test_pad_series_shorter_than_window_raises():
    with pytest.raises(ValueError, match=r"len\(P\)=2, N=3"):
        pad(np.array([1.0, 2.0]), N=3)


# --------------------------------------------------------------------------- #
# sma_filter — PDF Eq.(2): boxcar, weights = 1/N
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("N", [1, 2, 3, 5, 10, 50])
def test_sma_filter_length_and_normalisation(N):
    K = sma_filter(N)
    assert K.shape == (N,)
    assert np.isclose(K.sum(), 1.0)
    np.testing.assert_allclose(K, np.full(N, 1.0 / N))


# --------------------------------------------------------------------------- #
# lma_filter — PDF Eq.(4): triangular, weights sum to 1
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("N", [2, 3, 5, 10, 50])
def test_lma_filter_length_and_normalisation(N):
    K = lma_filter(N)
    assert K.shape == (N,)
    assert np.isclose(K.sum(), 1.0)


def test_lma_filter_first_weight_is_2_over_n_plus_one():
    """K[0] (largest weight) == 2 / (N + 1) per Eq.(4) at k=0."""
    for N in (2, 3, 5, 10):
        assert np.isclose(lma_filter(N)[0], 2.0 / (N + 1))


def test_lma_filter_strictly_decreasing():
    """Weights decay linearly to zero; strictly decreasing for N>=2."""
    K = lma_filter(10)
    assert np.all(np.diff(K) < 0)


# --------------------------------------------------------------------------- #
# ema_filter — PDF Eq.(5): K_k = alpha * (1-alpha)^k
# --------------------------------------------------------------------------- #


def test_ema_filter_first_weight_equals_alpha():
    for alpha in (0.1, 0.3, 0.5, 0.9):
        assert np.isclose(ema_filter(N=5, alpha=alpha)[0], alpha)


def test_ema_filter_decay_ratio_is_constant():
    """Adjacent ratio K[k+1]/K[k] == (1-alpha) per Eq.(5)."""
    K = ema_filter(N=10, alpha=0.3)
    ratios = K[1:] / K[:-1]
    np.testing.assert_allclose(ratios, np.full(9, 0.7))


def test_ema_filter_alpha_one_collapses_to_indicator():
    """alpha=1 => kernel = [1, 0, 0, ...]; output equals input."""
    K = ema_filter(N=4, alpha=1.0)
    np.testing.assert_allclose(K, np.array([1.0, 0.0, 0.0, 0.0]))


def test_ema_filter_alpha_out_of_range_raises():
    with pytest.raises(ValueError, match=r"alpha must satisfy 0 < alpha <= 1"):
        ema_filter(N=4, alpha=0.0)
    with pytest.raises(ValueError, match=r"alpha must satisfy 0 < alpha <= 1"):
        ema_filter(N=4, alpha=1.5)


# --------------------------------------------------------------------------- #
# wma — PDF Eq.(3): SMA = P * K (1-D convolution).
# Tests are restricted to indices i >= N-1 to avoid the documented warm-up.
# --------------------------------------------------------------------------- #


def test_wma_output_length_equals_input_length():
    P = np.arange(20, dtype=float)
    for N in (1, 3, 5, 10):
        out = wma(P, N, sma_filter(N))
        assert out.shape == (len(P),)


def test_wma_kernel_length_mismatch_raises():
    P = np.arange(10, dtype=float)
    with pytest.raises(ValueError):
        wma(P, N=3, kernel=np.array([0.5, 0.5]))  # kernel too short


@pytest.mark.parametrize("bad_kernel", [1.0, np.array(1.0), np.array([[1.0, 0.0, 0.0]])])
def test_wma_kernel_not_1d_raises(bad_kernel):
    P = np.arange(10, dtype=float)
    with pytest.raises(ValueError, match=r"kernel must be a 1-D array with length N"):
        wma(P, N=3, kernel=bad_kernel)


def test_wma_series_shorter_than_window_raises():
    P = np.array([1.0, 2.0])
    with pytest.raises(ValueError, match=r"len\(P\)=2, N=5"):
        wma(P, N=5, kernel=sma_filter(5))


def test_sma_hand_computed_values():
    """Plain SMA on a ramp [1..10] with N=3.

    SMA[i] = mean(P[i-N+1 : i+1]) for i >= N-1.
    """
    P = np.arange(1, 11, dtype=float)
    out = wma(P, N=3, kernel=sma_filter(3))
    # Indices >= 2 (= N-1) avoid the flip-pad warm-up.
    expected = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    np.testing.assert_allclose(out[2:], expected)


def test_lma_hand_computed_values():
    """LMA on a ramp [1..10] with N=3, kernel=[1/2, 1/3, 1/6].

    LMA[i] = (1/6)*P[i-2] + (1/3)*P[i-1] + (1/2)*P[i]  (most recent gets
    largest weight; convolution applies kernel reversed across the window).
    """
    P = np.arange(1, 11, dtype=float)
    K = lma_filter(3)
    out = wma(P, N=3, kernel=K)
    # Hand-computed from index 2 onwards.
    expected = np.array(
        [
            (1 / 6) * 1 + (1 / 3) * 2 + (1 / 2) * 3,  # i=2
            (1 / 6) * 2 + (1 / 3) * 3 + (1 / 2) * 4,  # i=3
            (1 / 6) * 3 + (1 / 3) * 4 + (1 / 2) * 5,  # i=4
        ]
    )
    np.testing.assert_allclose(out[2:5], expected)


def test_ema_hand_computed_values():
    """EMA on a ramp [1..10] with N=3, alpha=0.5, kernel=[0.5, 0.25, 0.125]."""
    P = np.arange(1, 11, dtype=float)
    K = ema_filter(N=3, alpha=0.5)
    out = wma(P, N=3, kernel=K)
    expected = np.array(
        [
            0.125 * 1 + 0.25 * 2 + 0.5 * 3,  # i=2  -> 2.125
            0.125 * 2 + 0.25 * 3 + 0.5 * 4,  # i=3  -> 3.0
            0.125 * 3 + 0.25 * 4 + 0.5 * 5,  # i=4  -> 3.875
        ]
    )
    np.testing.assert_allclose(out[2:5], expected)


def test_wma_constant_series_preserves_constant_after_warmup():
    """For SMA/LMA (weights sum to 1), a constant input gives a constant
    output beyond the warm-up region (i >= N-1)."""
    P = np.full(50, 7.5)
    for kernel_factory in (sma_filter, lma_filter):
        for N in (2, 5, 10):
            out = wma(P, N, kernel_factory(N))
            np.testing.assert_allclose(out[N - 1 :], 7.5, atol=1e-12)


def test_wma_n_equals_one_is_identity():
    """N=1 with a length-1 unit kernel should reproduce the input exactly."""
    P = np.array([3.0, 1.4, 1.5, 9.2, 6.5, 3.5])
    out = wma(P, N=1, kernel=np.array([1.0]))
    np.testing.assert_allclose(out, P)


# --------------------------------------------------------------------------- #
# Cross-WMA qualitative relationship — PDF Figure 5: at the same window size,
# EMA reacts faster than LMA, which reacts faster than SMA.
# --------------------------------------------------------------------------- #


def test_responsiveness_ema_faster_than_lma_faster_than_sma():
    """On a step input, the WMA that reacts fastest reaches a higher value
    sooner. We compare values at the first post-step sample."""
    # Step from 0 to 1 at index 30, then constant.
    P = np.zeros(60)
    P[30:] = 1.0
    N = 10

    # alpha=0.5 makes EMA appreciably more recency-biased than LMA.
    sma = wma(P, N, sma_filter(N))
    lma = wma(P, N, lma_filter(N))
    ema = wma(P, N, ema_filter(N, alpha=0.5))

    # Right at the step (i=30), the WMAs see only one "1" (the current sample),
    # weighted by the most-recent-tap of each kernel. EMA's first tap is the
    # largest of the three, so EMA[30] > LMA[30] > SMA[30].
    assert ema[30] > lma[30] > sma[30]
