"""Evaluación: métricas por clase, McNemar y verificación de metas (TT-E3-04/07)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize

from ml.src import ARTIFACTS_METRICS

CLASES = ["I", "II", "III", "IV", "V"]

METAS = {"f1": 0.82, "precision": 0.85, "recall": 0.80, "auc_roc": 0.87}  # RNF-001


def metricas_por_clase(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
    y_true = np.asarray(y_true)
    if np.issubdtype(y_true.dtype, np.number):  # etiquetas codificadas 0..4
        labels_cod = list(range(len(CLASES)))
        clases_cod = [CLASES[i] for i in labels_cod]
    else:
        labels_cod = CLASES
        clases_cod = CLASES
    reporte = classification_report(
        y_true, y_pred, labels=labels_cod, target_names=clases_cod,
        output_dict=True, zero_division=0,
    )
    resumen = {
        "macro": {
            "precision": float(precision_score(
                y_true, y_pred, labels=labels_cod, average="macro", zero_division=0
            )),
            "recall": float(recall_score(
                y_true, y_pred, labels=labels_cod, average="macro", zero_division=0
            )),
            "f1": float(f1_score(
                y_true, y_pred, labels=labels_cod, average="macro", zero_division=0
            )),
        },
        "por_clase": {
            c: reporte.get(c, {}) for c in clases_cod
        },
        "accuracy": float(accuracy_score(y_true, y_pred)),
    }
    try:
        y_bin = label_binarize(y_true, classes=labels_cod)
        resumen["auc_roc_ovr"] = float(
            roc_auc_score(y_bin, y_proba, multi_class="ovr", average="macro")
        )
    except ValueError:
        resumen["auc_roc_ovr"] = None
    return resumen


def verificar_metas(metricas: dict) -> dict[str, bool | None]:
    """RNF-001: F1 ≥ 0.82 · Precisión ≥ 0.85 · Recall ≥ 0.80 · AUC ≥ 0.87.

    Si el AUC no pudo calcularse, la meta queda `None` (sin_dato) — nunca
    se reporta como cumplida sin dato.
    """
    m = metricas["macro"]
    auc = metricas.get("auc_roc_ovr")
    return {
        "f1": m["f1"] >= METAS["f1"],
        "precision": m["precision"] >= METAS["precision"],
        "recall": m["recall"] >= METAS["recall"],
        "auc_roc": None if auc is None else auc >= METAS["auc_roc"],
    }


def guardar_metricas(nombre: str, metricas: dict, *, extra: dict | None = None) -> Path:
    destino = ARTIFACTS_METRICS / f"{nombre}.json"
    destino.write_text(
        json.dumps({"modelo": nombre, "metricas": metricas, **({"extra": extra} if extra else {})},
                   ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return destino


def matriz_confusion(y_true, y_pred) -> pd.DataFrame:
    return pd.crosstab(
        pd.Series(y_true, name="real"), pd.Series(y_pred, name="predicho")
    ).reindex(index=CLASES, columns=CLASES, fill_value=0)


def mcnemar(y_true, pred_a, pred_b) -> tuple[int, int, float]:
    """Test de McNemar entre dos modelos (validación estadística)."""
    a = np.asarray(pred_a) == np.asarray(y_true)
    b = np.asarray(pred_b) == np.asarray(y_true)
    b_ = (~a) & b
    c_ = a & (~b)
    b_cnt, c_cnt = int(b_.sum()), int(c_.sum())
    if b_cnt + c_cnt == 0:
        return b_cnt, c_cnt, 1.0
    from scipy.stats import binomtest

    p_valor = binomtest(min(b_cnt, c_cnt), b_cnt + c_cnt, 0.5).pvalue
    return b_cnt, c_cnt, float(p_valor)
