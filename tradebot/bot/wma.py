"""Weighted Moving Average building blocks for the trading bot.

Implements PDF §2.1 *Weighted Moving Averages* faithfully:
- `pad`         — flip-pad edge handling (PDF §2.1 paragraph after Eq.(3)).
- `sma_filter`  — boxcar kernel from Eq.(2).
- `lma_filter`  — triangular kernel from Eq.(4).
- `ema_filter`  — exponential kernel from Eq.(5).
- `wma`         — apply any kernel via 1-D discrete convolution per Eq.(3).

The PDF code skeleton (just before §2.2) is followed directly; this module
exposes the same five callables with type hints, validation, and docstrings.

Note on the warm-up region (first N-1 outputs of any WMA):
PDF's `pad = -np.flip(P[1:N])` produces edge values that do not equal P[0],
so `wma(P, N, ...)[ : N-1]` is artefactual. Downstream signal generation
should skip the longest warm-up window across all WMAs in the bot before
emitting any buy/sell decisions.

References (PDF §3 *Rules of Engagement*: "you may adapt for your use code
provided in conjunction with a specific research paper ... providing you
acknowledge the code source"):

  Project specification, CITS4404 Team Project — Building AI Trading Bots,
  §2.1, Eqs. (1)-(5) and the code listing immediately preceding §2.2.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np


__all__ = ["pad", "sma_filter", "lma_filter", "ema_filter", "wma"]


def _validate_window(N: int) -> None:
    if not isinstance(N, (int, np.integer)) or N < 1:
        raise ValueError(f"N must be a positive integer; got N={N!r}")


def pad(P: np.ndarray, N: int) -> np.ndarray:
    """Flip-pad a price series so a window-N convolution is filled at t=0.

    Per PDF §2.1: "we will 'flip' the first part of the sequence over (rotate
    it 180°), so that if for example the series is rising from p_0, it will
    also be rising into p_0."

    Requires ``len(P) >= N``. Output length is then ``len(P) + N - 1``, so that
    ``np.convolve(pad(P, N), kernel, 'valid')`` has length len(P).
    """
    _validate_window(N)
    P = np.asarray(P, dtype=np.float64)
    if P.size < N:
        raise ValueError(
            f"price series must have length >= N; got len(P)={P.size}, N={N}"
        )
    if N == 1:
        # No padding needed; convolve with a length-1 kernel preserves length.
        return P
    padding = -np.flip(P[1:N])
    return np.append(padding, P)


def sma_filter(N: int) -> np.ndarray:
    """Boxcar kernel of length N (PDF Eq.(2)). Weights sum to 1."""
    _validate_window(N)
    return np.ones(N, dtype=np.float64) / N


def lma_filter(N: int) -> np.ndarray:
    """Triangular (linearly decaying) kernel of length N (PDF Eq.(4)).

    Weights are higher for more recent data points and decay linearly to a
    minimum at the oldest point in the window. Sum of weights == 1 exactly.
    """
    _validate_window(N)
    k = np.arange(N, dtype=np.float64)
    return (2.0 / (N + 1.0)) * (1.0 - k / N)


def ema_filter(N: int, alpha: float) -> np.ndarray:
    """Exponential kernel of length N with smoothing factor alpha (PDF Eq.(5)).

    Weights = alpha * (1 - alpha) ** k for k = 0, 1, ..., N - 1. Per PDF §2.1
    this is a fixed-window approximation of the (theoretically infinite) EMA;
    weights sum to 1 - (1 - alpha) ** N, which is < 1 for finite N. We follow
    PDF Eq.(5) verbatim and do *not* re-normalise.

    `alpha` must be in (0, 1].
    """
    _validate_window(N)
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha must satisfy 0 < alpha <= 1; got alpha={alpha!r}")
    k = np.arange(N, dtype=np.float64)
    return alpha * (1.0 - alpha) ** k


def wma(P: np.ndarray, N: int, kernel: np.ndarray) -> np.ndarray:
    """Apply a length-N kernel to a price series via 1-D convolution (PDF Eq.(3)).

    Output length matches len(P). The first N-1 outputs are influenced by the
    flip-pad warm-up region and should be discarded for trading decisions
    (see module docstring).

    Raises if `len(kernel) != N` or `len(P) < N`.
    """
    _validate_window(N)
    P = np.asarray(P, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)
    if kernel.ndim != 1 or kernel.size != N:
        raise ValueError(
            f"kernel must be a 1-D array with length N; got shape={kernel.shape}, N={N}"
        )
    if P.size < N:
        raise ValueError(
            f"price series must have length >= N; got len(P)={P.size}, N={N}"
        )
    return np.convolve(pad(P, N), kernel, "valid")
