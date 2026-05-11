"""Data loading & train/test split.

Implements PDF §3 *Data* requirements:
- Source: "the Bitcoin Historical Dataset" on Kaggle (2014-2022 daily/hourly/minute).
- Train: data prior to 2020.
- Test:  data from 2020 onwards (held-out, only touched at the very end).
"""
