"""Bitcoin Historical Dataset loader & train/test splitter.

Implements PDF §3 *Data* requirements:
- Source: Kaggle "Bitcoin Historical Dataset" (prasoonkottarathil/btcinusd),
  daily OHLCV with ~2652 rows from 2014-11-28 to 2022-03-01.
- Split: train < 2020-01-01, test >= 2020-01-01 (PDF: "we'll act as if it is
  the start of 2020").

The raw CSV is sorted in REVERSE chronological order (most recent first).
This loader sorts ascending so downstream code can assume time-ordered data.

Public API:
- `split_and_save(raw_path, out_dir)` — one-off preprocessing.
- `load_ohlcv(split)` — return tidy DataFrame for a given split.
- `load_close(split)` — return numpy array of close prices.

Run as a script to perform the one-time split:

    uv run python -m tradebot.data.load
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

# Repo-root anchored paths — hard-coded since project layout is fixed.
_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parents[1]
RAW_DAILY = _REPO_ROOT / "data" / "raw" / "BTC-Daily.csv"
PROCESSED_DIR = _REPO_ROOT / "data" / "processed"
TRAIN_PATH = PROCESSED_DIR / "btc_daily_train.parquet"
TEST_PATH = PROCESSED_DIR / "btc_daily_test.parquet"

# PDF §3 *Data* split point. Inclusive lower bound for test set.
SPLIT_TIMESTAMP = pd.Timestamp("2020-01-01", tz=None)


def _load_raw(raw_path: Path = RAW_DAILY) -> pd.DataFrame:
    """Load the raw Kaggle daily CSV, parse dates, sort ascending."""
    df = pd.read_csv(raw_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=True).reset_index(drop=True)
    # Keep tidy column subset; downstream code only needs OHLCV.
    return df[["date", "open", "high", "low", "close", "Volume BTC", "Volume USD"]]


def split_and_save(
    raw_path: Path = RAW_DAILY,
    out_dir: Path = PROCESSED_DIR,
    split_at: pd.Timestamp = SPLIT_TIMESTAMP,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split daily data into train (< 2020) / test (>= 2020) and save parquets."""
    df = _load_raw(raw_path)
    train = df[df["date"] < split_at].reset_index(drop=True)
    test = df[df["date"] >= split_at].reset_index(drop=True)

    out_dir.mkdir(parents=True, exist_ok=True)
    train.to_parquet(out_dir / "btc_daily_train.parquet", index=False)
    test.to_parquet(out_dir / "btc_daily_test.parquet", index=False)
    return train, test


def load_ohlcv(split: str) -> pd.DataFrame:
    """Load a processed split. `split` in {'train', 'test'}."""
    if split == "train":
        path = TRAIN_PATH
    elif split == "test":
        path = TEST_PATH
    else:
        raise ValueError(
            f"split must be one of {{'train', 'test'}}; got split={split!r}"
        )
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m tradebot.data.load` first."
        )
    return pd.read_parquet(path)


def load_close(split: str) -> np.ndarray:
    """Return close prices as a 1-D float64 ndarray, ascending in time."""
    return load_ohlcv(split)["close"].to_numpy(dtype=np.float64)


def _summarise(name: str, df: pd.DataFrame) -> None:
    print(
        f"{name:5s}  rows={len(df):>5d}  "
        f"from {df['date'].iloc[0].date()}  to {df['date'].iloc[-1].date()}"
    )


def main() -> None:
    if not RAW_DAILY.exists():
        raise FileNotFoundError(
            f"Raw daily CSV not found at {RAW_DAILY}. "
            "See data/README.md for download instructions."
        )
    train, test = split_and_save()
    print(f"Loaded raw {RAW_DAILY.name}: {len(train) + len(test)} rows")
    _summarise("train", train)
    _summarise("test", test)
    print(f"\nWrote {TRAIN_PATH.relative_to(_REPO_ROOT)}")
    print(f"Wrote {TEST_PATH.relative_to(_REPO_ROOT)}")


if __name__ == "__main__":
    main()
