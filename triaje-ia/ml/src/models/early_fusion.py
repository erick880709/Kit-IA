"""Early Fusion (TT-E3-05, RT-002 Opción A).

Features estructuradas + embeddings concatenados → clasificador único (XGBoost).
Mismo esquema de validación que los baselines (comparabilidad).
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from ml.src.evaluation.metrics import CLASES, guardar_metricas, metricas_por_clase
from ml.src.models.encoding import (
    codificar_contiguo,
    decodificar_a_clases,
    expandir_proba,
)


def concatenar_features(X_estructurada: np.ndarray, X_texto: np.ndarray | None) -> np.ndarray:
    if X_texto is None:
        return X_estructurada
    if sp.issparse(X_texto):  # TF-IDF disperso (vocabulario completo CIE-11)
        est = X_estructurada if sp.issparse(X_estructurada) else sp.csr_matrix(X_estructurada)
        return sp.hstack([est, X_texto]).tocsr()
    return np.hstack([X_estructurada, X_texto])


def entrenar_early_fusion(
    X_estructurada: np.ndarray,
    y: np.ndarray,
    X_texto: np.ndarray | None = None,
    *,
    semilla: int = 42,
    k_folds: int = 10,
) -> dict:
    X = concatenar_features(X_estructurada, X_texto)
    encoder = LabelEncoder().fit(CLASES)
    y_enc = encoder.transform(y)
    y_cont, mapeo = codificar_contiguo(y_enc)
    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=semilla)
    folds = []
    for train_idx, test_idx in skf.split(X, y_cont):
        modelo = XGBClassifier(
            n_estimators=250, eval_metric="mlogloss", random_state=semilla, n_jobs=-1
        )
        modelo.fit(X[train_idx], y_cont[train_idx])
        proba_k = modelo.predict_proba(X[test_idx])
        pred_cont = modelo.predict(X[test_idx])
        folds.append(
            metricas_por_clase(
                decodificar_a_clases(y_cont[test_idx], mapeo),
                decodificar_a_clases(pred_cont, mapeo),
                expandir_proba(proba_k, mapeo),
            )
        )
    macro = {k: float(np.mean([f["macro"][k] for f in folds])) for k in folds[0]["macro"]}
    guardar_metricas("early_fusion", {"macro_cv": macro, "k_folds": k_folds})
    return {"macro_cv": macro, "pipeline": "early_fusion"}
