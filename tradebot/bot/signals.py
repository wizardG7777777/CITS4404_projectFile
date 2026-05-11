"""Crossover signal generation.

Implements PDF §2.2 *Crossover Points as Buy and Sell Signals* and §2.3
*Building a Bot* on top of the WMA module:

  diff = high_freq - low_freq            # difference of two indicators
  sign_series = sign(diff)               # values in {-1, 0, +1}
  signals = sign_series * Eq.(6) kernel  # via 1-D convolution

PDF Eq.(6) defines the kernel as ``[0.5, -0.5]``: it responds to a
sign-flip in its input. Combined with the sign of `diff`, the pipeline
recovers golden-cross (buy) and death-cross (sell) events from any two
indicator series.

Author: CITS4404 Team 20 (Qiurong Chen, Yanchen Yu).
"""
from __future__ import annotations

import numpy as np


__all__ = ["edge_filter", "crossover_signals"]


def edge_filter() -> np.ndarray:
    """PDF Eq.(6): two-tap kernel for detecting sign changes in a series.

    K_k = 0.5 if k == 0, -0.5 if k == 1, 0 otherwise.
    """
    return np.array([0.5, -0.5], dtype=np.float64)


def crossover_signals(high_freq: np.ndarray, low_freq: np.ndarray) -> np.ndarray:
    """Convert two indicator series into buy/sell crossover signals.

    Output has the same length as the inputs. Positions where the value is:
      * positive → golden cross (high_freq crossed above low_freq) → buy
      * negative → death  cross (high_freq crossed below low_freq) → sell
      * zero     → no transition

    By construction the very first sample is 0 (no prior sample to compare
    with). Boundary behaviour is handled by pre-padding the sign series with
    a copy of its first value, so no spurious events appear at index 0.
    """
    hf = np.asarray(high_freq, dtype=np.float64)
    lf = np.asarray(low_freq, dtype=np.float64)
    if hf.shape != lf.shape:
        raise ValueError(
            f"high_freq and low_freq must have the same shape; "
            f"got {hf.shape} and {lf.shape}"
        )
    if hf.ndim != 1:
        raise ValueError(f"inputs must be 1-D; got shape={hf.shape}")
    if hf.size == 0:
        raise ValueError("inputs must be non-empty")

    diff = hf - lf
    sign_series = np.sign(diff)
    # Pre-pad so the convolution produces a length-N output without using
    # 'same' / 'full' modes (which would introduce spurious boundary events).
    padded = np.concatenate(([sign_series[0]], sign_series))
    return np.convolve(padded, edge_filter(), "valid")
