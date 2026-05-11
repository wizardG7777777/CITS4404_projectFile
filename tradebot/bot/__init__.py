"""Bot building blocks & backtest engine.

Modules will implement:
- `wma`     — PDF §2.1 SMA / LMA / EMA via 1-D convolution + flip-padding.
- `signals` — PDF §2.2 / §2.3 crossover signals & sign-change edge filter (Eq.6).
- `bot`     — Two configurable bots:
              B1 (2-D): two SMAs + crossover (PDF §2.3 example).
              B2 (~14-D): high/low-frequency components each as a weighted sum
                          of SMA/LMA/EMA per PDF §3 Eq.(7).
- `backtest`— PDF §3 *Evaluation of Bots*: $1000 start, all-in trades,
              3% fee, final liquidation, fitness = ending cash.
"""
