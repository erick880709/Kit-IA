"""Umbrales por clase (TT-E3-07, RT-009, RNF-003).

Maximiza recall en Niveles I-II; argmax para III-V. El vector de umbrales se
persiste junto a la versión del modelo.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import roc_curve

from ml.src.evaluation.metrics import CLASES


def ajustar_umbrales(
    y_true: np.ndarray, y_proba: np.ndarray, *, priorizar: tuple[str, ...] = ("I", "II")
) -> dict[str, float]:
    """Umbral óptimo por clase maximizando recall en las clases priorizadas."""
    umbrales: dict[str, float] = {}
    for i, clase in enumerate(CLASES):
        if clase not in priorizar:
            umbrales[clase] = 0.5  # argmax estándar para III-V
            continue
        y_bin = (y_true == clase).astype(int)
        if y_bin.sum() == 0:  # clase ausente en validación: conservador 0.5
            umbrales[clase] = 0.5
            continue
        fpr, tpr, thresholds = roc_curve(y_bin, y_proba[:, i])
        puntajes = tpr - fpr  # Youden J
        mejor = int(np.argmax(puntajes))
        umbral = float(thresholds[mejor]) if mejor < len(thresholds) else 0.5
        if not np.isfinite(umbral):
            umbral = 0.5
        umbrales[clase] = min(max(umbral, 0.01), 0.99)
    return umbrales


def aplicar_umbrales(y_proba: np.ndarray, umbrales: dict[str, float]) -> np.ndarray:
    """Clasifica maximizando proba/umbral por clase (no argmax puro).

    El cociente pᵢ/uᵢ corrige el sesgo hacia la clase mayoritaria: una clase
    priorizada con umbral bajo compite en igualdad de condiciones.
    """
    orden = [CLASES.index(c) for c in CLASES]
    ratios = y_proba[:, orden] / np.array([max(umbrales[c], 1e-6) for c in CLASES])
    return np.asarray(orden)[ratios.argmax(axis=1)]


def sugerir_nivel(probabilidades: dict[str, float], umbrales: dict[str, float]) -> str:
    """Nivel sugerido: clase con mayor cociente proba/umbral (fallback argmax)."""
    ratios = {
        c: probabilidades.get(c, 0.0) / max(umbrales.get(c, 0.5), 1e-6) for c in CLASES
    }
    return max(ratios, key=lambda c: ratios[c])
