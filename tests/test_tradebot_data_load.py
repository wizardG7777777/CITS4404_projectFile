from __future__ import annotations

import pytest

from tradebot.data.load import load_ohlcv


def test_load_ohlcv_invalid_split_message() -> None:
    with pytest.raises(
        ValueError,
        match=r"split must be one of \{'train', 'test'\}; got split='dev'",
    ):
        load_ohlcv("dev")
