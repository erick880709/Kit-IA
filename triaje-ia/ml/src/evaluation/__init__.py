"""Evaluación del pipeline ML."""

from __future__ import annotations

from .benchmarks import BENCHMARKS, tabla_comparativa
from .metrics import (
    CLASES,
    METAS,
    guardar_metricas,
    matriz_confusion,
    mcnemar,
    metricas_por_clase,
    verificar_metas,
)
from .shap_explain import NOMBRES_CLINICOS, explicar_shap, guardar_shap

__all__ = [
    "BENCHMARKS",
    "CLASES",
    "METAS",
    "NOMBRES_CLINICOS",
    "explicar_shap",
    "guardar_metricas",
    "guardar_shap",
    "matriz_confusion",
    "mcnemar",
    "metricas_por_clase",
    "tabla_comparativa",
    "verificar_metas",
]
