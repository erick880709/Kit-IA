"""Modelos (Épica E3): baselines, early fusion y late fusion."""

from __future__ import annotations

from .baselines import entrenar_baselines
from .early_fusion import entrenar_early_fusion
from .late_fusion import Combinador, entrenar_late_fusion

__all__ = [
    "entrenar_baselines",
    "entrenar_early_fusion",
    "entrenar_late_fusion",
    "Combinador",
]
