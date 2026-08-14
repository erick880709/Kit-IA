"""Limpieza y feature engineering (TT-E3-02) — transformadores estilo sklearn."""

from __future__ import annotations

from .feature_engineering import construir_matriz_estructurada
from .limpieza import (
    LimpiezaOutliers,
    NormalizadorRegimen,
    ValidadorCalidad,
)

__all__ = [
    "LimpiezaOutliers",
    "NormalizadorRegimen",
    "ValidadorCalidad",
    "construir_matriz_estructurada",
]
