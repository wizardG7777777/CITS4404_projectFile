"""Experiment matrix configuration.

A single declarative spec for the cross product of (algorithm, bot, seed).
Anything that defines "what runs" should live here so the report, the
re-run script, and the notebooks all agree on the experimental design.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from tradebot.bot.bots import Bot, BotB1, BotB2
from tradebot.optim.base import Optimizer
from tradebot.optim.hho import HHO
from tradebot.optim.pso import PSO
from tradebot.optim.random_search import RandomSearch


# Algorithm registry — each entry is a zero-arg factory returning a fresh
# Optimizer instance (so a run never re-uses prior state).
ALGORITHMS: dict[str, Callable[[], Optimizer]] = {
    "RandomSearch": RandomSearch,
    "PSO": PSO,
    "HHO": HHO,
}


# Bot registry — class objects (interface is statically the same).
BOTS: dict[str, type[Bot]] = {
    "B1_dual_sma": BotB1,
    "B2_compound": BotB2,
}


@dataclass(frozen=True)
class ExperimentConfig:
    """Declarative description of the experiment matrix to run."""

    algorithms: tuple[str, ...] = ("RandomSearch", "PSO", "HHO")
    bots: tuple[str, ...] = ("B1_dual_sma", "B2_compound")
    seeds: tuple[int, ...] = (0, 1, 2, 3, 4)
    budget: int = 5000
    split: str = "train"

    def __post_init__(self) -> None:
        for a in self.algorithms:
            if a not in ALGORITHMS:
                raise ValueError(f"unknown algorithm {a!r}; known: {list(ALGORITHMS)}")
        for b in self.bots:
            if b not in BOTS:
                raise ValueError(f"unknown bot {b!r}; known: {list(BOTS)}")
        if self.budget < 1:
            raise ValueError(f"budget must be >= 1; got {self.budget}")
        if self.split not in ("train", "test"):
            raise ValueError(f"split must be 'train' or 'test'; got {self.split!r}")

    @property
    def n_runs(self) -> int:
        return len(self.algorithms) * len(self.bots) * len(self.seeds)

    def iter_runs(self):
        """Yield (algorithm, bot, seed) triples in deterministic order."""
        for bot in self.bots:
            for algo in self.algorithms:
                for seed in self.seeds:
                    yield (algo, bot, seed)


# Default config used by `python -m tradebot.experiments.run_matrix`.
DEFAULT_CONFIG = ExperimentConfig()
