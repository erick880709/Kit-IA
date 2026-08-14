"""Pantalla de comparación de modelos (HU-E4-04, rol Investigador).

Compara lado a lado todos los experimentos del pipeline (Épica E3) contra los
benchmarks de la literatura (RT-008), leyendo los JSON de artifacts/metrics.
"""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from ml.src import ARTIFACTS_METRICS

_FILAS = [
    ("Baseline Regresión Logística", "baseline_regresion_logistica.json", "macro_cv"),
    ("Baseline Random Forest", "baseline_random_forest.json", "macro_cv"),
    ("Baseline XGBoost", "baseline_xgboost.json", "macro_cv"),
    ("Early Fusion (XGBoost)", "early_fusion.json", "macro_cv"),
    ("Late Fusion · Promedio ponderado", "late_fusion_promedio_ponderado.json", "macro_cv"),
    ("Late Fusion · Stacking", "late_fusion_stacking.json", "macro_cv"),
    ("📝 Texto SJdD (holdout, fine-tuning)", "texto_sjd_holdout.json", "macro"),
    ("🏆 Modelo ganador (test)", "modelo_ganador.json", "macro"),
]


def _cargar(nombre: str) -> dict | None:
    ruta = ARTIFACTS_METRICS / nombre
    if not ruta.exists():
        return None
    return json.loads(ruta.read_text(encoding="utf-8"))


def render() -> None:
    st.title("Comparación de modelos de triaje")
    st.caption("Rol Investigador · resultados del pipeline de la Épica E3")

    filas = []
    for etiqueta, archivo, clave in _FILAS:
        doc = _cargar(archivo)
        if doc is None:
            continue
        metricas = doc.get("metricas", doc)
        macro = metricas.get(clave, {})
        filas.append(
            {
                "Modelo": etiqueta,
                "Precisión (macro)": round(float(macro.get("precision", 0)), 4),
                "Recall (macro)": round(float(macro.get("recall", 0)), 4),
                "F1 (macro)": round(float(macro.get("f1", 0)), 4),
                "AUC-ROC (OVR)": (
                    round(float(metricas.get("auc_roc_ovr")), 4)
                    if metricas.get("auc_roc_ovr") is not None
                    else None
                ),
            }
        )

    if filas:
        st.subheader("Modelos entrenados en este proyecto")
        st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    else:
        st.info("Aún no hay métricas — ejecutar `python -m ml.pipeline` primero.")

    comparativa = _cargar("comparativa_benchmarks.json")
    if comparativa:
        st.subheader("Benchmarks de la literatura (RT-008)")
        filas_bench = []
        for item in comparativa:
            filas_bench.append(
                {
                    "Referencia": item.get("referencia"),
                    "AUC-ROC": (
                        round(float(item["auc"]), 4) if item.get("auc") is not None else None
                    ),
                    "F1": (
                        round(float(item["f1"]), 4) if item.get("f1") is not None else None
                    ),
                    "Nota": item.get("nota", ""),
                }
            )
        st.dataframe(pd.DataFrame(filas_bench), hide_index=True, width="stretch")

    metas = _cargar("modelo_ganador.json")
    if metas and metas.get("extra", {}).get("metas"):
        st.subheader("Metas RNF-001 del modelo ganador")
        st.json(metas["extra"]["metas"])

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
