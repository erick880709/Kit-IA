"""Benchmarks de la literatura (TT-E3-08, RT-008)."""

from __future__ import annotations

BENCHMARKS = [
    {"referencia": "CTAS (Canadá)", "auc": 0.882, "f1": None, "nota": "Triage and Acuity Scale"},
    {"referencia": "Hong et al. 2021", "auc": 0.93, "f1": None, "nota": "ML en triaje ED"},
    {"referencia": "Ueareekul et al.", "auc": 0.917, "f1": None, "nota": "XGBoost triaje"},
    {"referencia": "Levin et al.", "auc": None, "f1": 0.81, "nota": "Benchmark F1"},
]

VARIABLES_LITERATURA = [
    "saturacion_o2", "frecuencia_respiratoria", "temperatura",
    "presion_sistolica", "edad", "via_llegada",
]


def tabla_comparativa(metricas: dict) -> list[dict]:
    """Compara el modelo ganador contra benchmarks con las mismas métricas."""
    filas = []
    for b in BENCHMARKS:
        filas.append({**b, "modelo": b["referencia"], "es_benchmark": True})
    filas.append(
        {
            "referencia": "TriajeIA (este proyecto)",
            "auc": metricas.get("auc_roc_ovr"),
            "f1": metricas.get("macro", {}).get("f1"),
            "nota": "Fusión tardía — dataset sintético demo",
            "es_benchmark": False,
        }
    )
    return filas
