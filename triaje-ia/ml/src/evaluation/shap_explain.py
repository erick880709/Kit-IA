"""Explicabilidad SHAP (TT-E3-08)."""

from __future__ import annotations

import json

import numpy as np

from ml.src import ARTIFACTS_SHAP

# Mapeo de features a lenguaje clínico (CA1 de HU-E4-02).
NOMBRES_CLINICOS = {
    "saturacion_o2": "saturación de O₂",
    "frecuencia_respiratoria": "frecuencia respiratoria",
    "temperatura": "temperatura corporal",
    "presion_sistolica": "presión arterial sistólica",
    "presion_diastolica": "presión arterial diastólica",
    "frecuencia_cardiaca": "frecuencia cardíaca",
    "edad": "edad",
    "via_llegada": "vía de llegada",
    "episodios_previos_urgencias": "episodios previos en urgencias",
    "peso": "peso",
    "talla": "talla",
    "imc": "índice de masa corporal",
    "sexo": "sexo",
    "regimen": "régimen de afiliación",
    "departamento": "departamento",
}


def explicar_shap(modelo, X, *, nombres_features: list[str] | None = None) -> dict:
    """TreeExplainer para XGBoost/RF (RT-005). Devuelve top-5 con signo."""
    import shap

    explainer = shap.TreeExplainer(modelo)
    valores = explainer.shap_values(X)
    proba = modelo.predict_proba(X)
    idx = proba.argmax(axis=1)
    if isinstance(valores, list):  # multiclase: una matriz por clase
        por_fila = np.vstack([valores[c][i] for i, c in enumerate(idx)])
    else:
        valores = np.asarray(valores)
        if valores.ndim == 3:  # (n, features, clases)
            por_fila = valores[np.arange(len(idx)), :, idx]
        else:
            por_fila = valores
    medias = np.abs(por_fila).mean(axis=0)
    orden = np.argsort(-medias)[:5]
    nombres = nombres_features or [f"f{i}" for i in range(X.shape[1])]
    return {
        "top": [
            {
                "feature": nombres[int(i)],
                "clinico": NOMBRES_CLINICOS.get(nombres[int(i)], nombres[int(i)]),
                "impacto_medio": float(por_fila[:, int(i)].mean()),
                "peso_absoluto": float(medias[int(i)]),
            }
            for i in orden
        ]
    }


def guardar_shap(nombre: str, explicacion: dict) -> None:
    (ARTIFACTS_SHAP / f"{nombre}.json").write_text(
        json.dumps(explicacion, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
