"""Construcción de la matriz de features estructuradas (TT-E3-02)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

_NUMERICAS = [
    "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
    "saturacion_o2", "presion_sistolica", "presion_diastolica",
    "peso", "talla", "episodios_previos_urgencias", "anio_nacimiento",
]
_CATEGORICAS = ["sexo", "via_llegada", "regimen", "departamento"]


def _agregar_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    salida = df.copy()
    if "imc" not in salida.columns and {"peso", "talla"}.issubset(salida.columns):
        salida["imc"] = salida["peso"] / (salida["talla"].replace(0, np.nan) ** 2)
        if "imc" not in _NUMERICAS:
            salida["imc"] = salida["imc"].clip(5, 100)
    if "anio_nacimiento" in salida.columns:
        salida["edad"] = 2026 - pd.to_numeric(salida["anio_nacimiento"], errors="coerce")
    return salida


def construir_matriz_estructurada(df: pd.DataFrame) -> tuple[pd.DataFrame, Pipeline]:
    """Devuelve (X_estructurada, pipeline) — el mismo pipeline se serializa
    junto al modelo (anti training-serving skew)."""
    df = _agregar_derivadas(df)
    numericas = [c for c in _NUMERICAS if c in df.columns]
    categoricas = [c for c in _CATEGORICAS if c in df.columns]

    pipeline = Pipeline(
        steps=[
            (
                "columnas",
                ColumnTransformer(
                    transformers=[
                        (
                            "num",
                            Pipeline(
                                [
                                    ("imputa", SimpleImputer(strategy="median")),
                                    ("escala", StandardScaler()),
                                ]
                            ),
                            numericas,
                        ),
                        (
                            "cat",
                            Pipeline(
                                [
                                    ("imputa", SimpleImputer(strategy="most_frequent")),
                                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                                ]
                            ),
                            categoricas,
                        ),
                    ]
                ),
            )
        ]
    )
    matriz = pipeline.fit_transform(df)
    return pd.DataFrame(matriz.toarray() if hasattr(matriz, "toarray") else matriz), pipeline
