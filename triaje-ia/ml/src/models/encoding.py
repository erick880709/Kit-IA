"""Codificación contigua de clases (XGBoost exige 0..k-1)."""

from __future__ import annotations

import numpy as np

from ml.src.evaluation.metrics import CLASES


def codificar_contiguo(y_enc: np.ndarray) -> tuple[np.ndarray, dict[int, int]]:
    """Re-mapea códigos LabelEncoder a 0..k-1 contiguos (clases ausentes no
    rompen XGBoost). Devuelve (y_contiguo, mapeo codigo_original -> nuevo)."""
    codigos = np.unique(y_enc)
    mapeo = {int(c): i for i, c in enumerate(codigos)}
    return np.asarray([mapeo[int(v)] for v in y_enc]), mapeo


def decodificar_a_clases(y_cont: np.ndarray, mapeo: dict[int, int]) -> np.ndarray:
    """Convierte códigos contiguos a los nombres romanos de CLASES."""
    inverso = {i: CLASES[c] for c, i in mapeo.items()}
    return np.asarray([inverso[int(v)] for v in y_cont])


def expandir_proba(proba: np.ndarray, mapeo: dict[int, int]) -> np.ndarray:
    """Expande la matriz de probabilidades a 5 columnas (orden de CLASES)."""
    proba5 = np.zeros((len(proba), len(CLASES)))
    for codigo_original, j in mapeo.items():
        proba5[:, CLASES.index(CLASES[codigo_original])] = proba[:, j]
    return proba5
