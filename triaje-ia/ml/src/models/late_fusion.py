"""Late Fusion (TT-E3-06, RT-002 Opción B, RT-010).

Submodelo estructurado (XGBoost) + submodelo texto (Regresión Logística sobre
embeddings) combinados con estrategia parametrizable (strategy pattern):
promedio_ponderado (default), stacking y meta_clasificador.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
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


class Combinador(ABC):
    """Estrategia de combinación de probabilidades (RT-010)."""

    @abstractmethod
    def combinar(self, proba_a: np.ndarray, proba_b: np.ndarray) -> np.ndarray:
        ...


class PromedioPonderado(Combinador):
    def __init__(self, peso_estructurado: float = 0.7) -> None:
        self.peso = peso_estructurado

    def combinar(self, proba_a: np.ndarray, proba_b: np.ndarray) -> np.ndarray:
        return self.peso * proba_a + (1 - self.peso) * proba_b


class Stacking(Combinador):
    """Meta-clasificador (experimental): aprende a combinar probas.

    Se agregan 'anclas' one-hot para garantizar que el meta-modelo siempre
    emita k columnas aunque un fold no contenga todas las clases.
    """

    def __init__(self, semilla: int = 42) -> None:
        self._meta = LogisticRegression(max_iter=1000, random_state=semilla)

    def combinar(self, proba_a: np.ndarray, proba_b: np.ndarray) -> np.ndarray:
        k = proba_a.shape[1]
        x_meta = np.hstack([proba_a, proba_b])
        y_meta = proba_a.argmax(axis=1)
        anclas = np.hstack([np.eye(k), np.eye(k)])
        self._meta.fit(np.vstack([x_meta, anclas]), np.concatenate([y_meta, np.arange(k)]))
        return self._meta.predict_proba(x_meta)


def _factory_combinador(nombre: str, semilla: int) -> Combinador:
    if nombre == "stacking":
        return Stacking(semilla)
    if nombre == "meta_clasificador":
        return Stacking(semilla)
    return PromedioPonderado()


def entrenar_late_fusion(
    X_estructurada: np.ndarray,
    y: np.ndarray,
    X_texto: np.ndarray | None,
    *,
    semilla: int = 42,
    k_folds: int = 10,
    combinadores: tuple[str, ...] = ("promedio_ponderado", "stacking"),
) -> dict:
    encoder = LabelEncoder().fit(CLASES)
    y_enc = encoder.transform(y)
    y_cont, mapeo = codificar_contiguo(y_enc)
    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=semilla)
    resultado: dict = {}

    for nombre_combinador in combinadores:
        folds = []
        for train_idx, test_idx in skf.split(X_estructurada, y_cont):
            sub_a = XGBClassifier(
                n_estimators=250, eval_metric="mlogloss", random_state=semilla, n_jobs=-1
            )
            sub_a.fit(X_estructurada[train_idx], y_cont[train_idx])
            proba_a = sub_a.predict_proba(X_estructurada[test_idx])

            if X_texto is not None:
                sub_b = LogisticRegression(max_iter=1000, class_weight="balanced")
                sub_b.fit(X_texto[train_idx], y_cont[train_idx])
                proba_b = sub_b.predict_proba(X_texto[test_idx])
            else:
                proba_b = np.full_like(proba_a, 1 / len(CLASES))

            combinador = _factory_combinador(nombre_combinador, semilla)
            proba_final = combinador.combinar(proba_a, proba_b)
            folds.append(
                metricas_por_clase(
                    decodificar_a_clases(y_cont[test_idx], mapeo),
                    decodificar_a_clases(proba_final.argmax(axis=1), mapeo),
                    expandir_proba(proba_final, mapeo),
                )
            )
        macro = {k: float(np.mean([f["macro"][k] for f in folds])) for k in folds[0]["macro"]}
        resultado[nombre_combinador] = macro
        guardar_metricas(
            f"late_fusion_{nombre_combinador}",
            {"macro_cv": macro, "k_folds": k_folds, "peso_estructurado": 0.7},
        )
    return resultado


class LateFusionClassifier:
    """Contenedor serializable del modelo ganador (TT-E3-09).

    Combina el submodelo estructurado (`sub_a`) y el de texto (`sub_b`) con la
    estrategia elegida, exponiendo una API estable para la app:
    `predict_proba(X_estructurada, X_texto=None)`. Ambas salidas deben tener
    k columnas alineadas con el orden de `CLASES` (garantizado por el pipeline
    al codificar con LabelEncoder sobre CLASES cuando todas las clases están
    presentes en el entrenamiento).
    """

    def __init__(
        self,
        sub_a,
        sub_b,
        combinador: Combinador | None = None,
        clases: list[str] | None = None,
    ) -> None:
        self.sub_a = sub_a
        self.sub_b = sub_b
        self.combinador = combinador or PromedioPonderado()
        if not isinstance(self.combinador, PromedioPonderado):
            raise TypeError(
                "El combinador serializable del ganador debe ser PromedioPonderado: "
                "Stacking entrena en tiempo de predicción y no debe serializarse"
            )
        self.clases = clases or CLASES

    def predict_proba(
        self, X_estructurada: np.ndarray, X_texto: np.ndarray | None = None
    ) -> np.ndarray:
        n = len(X_estructurada)
        k = len(self.clases)
        proba_a = np.asarray(self.sub_a.predict_proba(X_estructurada))
        if proba_a.shape[1] != k:  # clases ausentes → neutro (nunca ocurre en el ganador)
            proba_a = np.full((n, k), 1 / k)
        if X_texto is None:
            proba_b = np.full((n, k), 1 / k)
        else:
            proba_b = np.asarray(self.sub_b.predict_proba(X_texto))
            if proba_b.shape[1] != k:
                proba_b = np.full((n, k), 1 / k)
        return self.combinador.combinar(proba_a, proba_b)
