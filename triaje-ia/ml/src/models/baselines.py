"""Baselines unimodales (TT-E3-04, RT-004).

LR, RF y XGBoost solo con datos estructurados, 10-fold CV estratificado,
class weights para desbalance (ADR-003). Métricas por clase guardadas en
artifacts/metrics/ para validacion-cientifica-ml.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from ml.src.evaluation.metrics import CLASES, guardar_metricas, metricas_por_clase
from ml.src.models.encoding import (
    codificar_contiguo,
    decodificar_a_clases,
    expandir_proba,
)

_BASELINES = {
    "regresion_logistica": lambda semilla: LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=semilla
    ),
    "random_forest": lambda semilla: RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=semilla, n_jobs=-1
    ),
    "xgboost": lambda semilla: XGBClassifier(
        n_estimators=200, eval_metric="mlogloss", random_state=semilla, n_jobs=-1
    ),
}


def _codificar(y: np.ndarray) -> tuple[np.ndarray, LabelEncoder]:
    encoder = LabelEncoder().fit(CLASES)
    return encoder.transform(y), encoder


def entrenar_baselines(
    X: np.ndarray, y: np.ndarray, *, semilla: int = 42, k_folds: int = 10
) -> dict:
    """Entrena y evalúa los 3 baselines con CV estratificado; guarda métricas."""
    resultados: dict = {}
    encoder = LabelEncoder().fit(CLASES)
    y_enc = encoder.transform(y)
    y_cont, mapeo = codificar_contiguo(y_enc)
    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=semilla)

    for nombre, factory in _BASELINES.items():
        folds = []
        for train_idx, test_idx in skf.split(X, y_cont):
            modelo = factory(semilla)
            modelo.fit(X[train_idx], y_cont[train_idx])
            proba_k = modelo.predict_proba(X[test_idx])
            pred_cont = modelo.predict(X[test_idx])
            y_str = decodificar_a_clases(y_cont[test_idx], mapeo)
            pred_str = decodificar_a_clases(pred_cont, mapeo)
            m = metricas_por_clase(y_str, pred_str, expandir_proba(proba_k, mapeo))
            folds.append(m)
        macro = {k: float(np.mean([f["macro"][k] for f in folds])) for k in folds[0]["macro"]}
        resultados[nombre] = {
            "macro_cv": macro,
            "mejor_fold": max(folds, key=lambda f: f["macro"]["f1"]),
        }
        guardar_metricas(
            f"baseline_{nombre}",
            {"macro_cv": macro, "k_folds": k_folds, "mejor_fold": resultados[nombre]["mejor_fold"]},
        )
    return resultados
