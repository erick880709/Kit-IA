"""Validación del nivel de acierto POR CLASE de urgencia (I–V).

Responde «¿qué nivel de acierto se tiene con cada nivel de urgencia?»
evaluando el artefacto ganador sobre el split de test honesto (mismo
generador y semilla del entrenamiento, sin fuga) y escribe
`artifacts/metrics/acierto_por_nivel.json`.

Uso:  python -m ml.validacion_niveles [--n 4000]

`GARANTIAS_MINIMAS` define los pisos por nivel que el test
`tests/test_garantia_niveles.py` hace cumplir: si un reentrenamiento produce
un artefacto por debajo de estos pisos, la suite falla (gate de regresión).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from ml.pipeline import _preparar, _split_estratificado
from ml.src import ARTIFACTS_METRICS, ARTIFACTS_MODELS
from ml.src.data.ingesta import generar_datos_sinteticos, ingestar_csv_local
from ml.src.data.mapeo_cie11 import normalizar_token_cie, remapear_cie11
from ml.src.evaluation.metrics import CLASES, metricas_por_clase
from ml.src.models.thresholds import aplicar_umbrales
from ml.src.registry import cargar_paquete

# Pisos de garantía por nivel (demo sintético, test honesto, semilla 42).
# Garantía demo-grade documentada en el model card — no evidencia clínica.
GARANTIAS_MINIMAS: dict[str, dict[str, float]] = {
    "I": {"recall": 0.5, "precision": 0.5},
    "II": {"recall": 0.75, "precision": 0.8},
    "III": {"recall": 0.95, "precision": 0.95},
    "IV": {"recall": 0.9, "precision": 0.9},
    "V": {"recall": 2 / 3, "precision": 0.6},
}
MACRO_F1_MINIMO = 0.9


def cargar_ganador() -> tuple[dict, Path]:
    """Carga el artefacto ganador más reciente con manifiesto."""
    candidatas = [
        p
        for p in sorted(ARTIFACTS_MODELS.glob("*.joblib"), key=lambda p: p.stat().st_mtime)
        if Path(str(p).replace(".joblib", ".manifest.json")).is_file()
    ]
    if not candidatas:
        raise SystemExit("No hay artefacto — correr `python -m ml.pipeline` primero")
    return cargar_paquete(candidatas[-1]), candidatas[-1]


def reconstruir_test_demo(n: int = 4000) -> tuple[object, object]:
    """Reconstruye el split honesto del demo EXACTAMENTE como el pipeline:
    preparación, re-mapeo CIE-11, texto completo y split 70/15/15 (semilla 42).
    Devuelve (demo, test) — el test nunca se usó en el entrenamiento.
    """
    demo = _preparar(ingestar_csv_local(generar_datos_sinteticos(n=n), fuente="sintetico_demo"))
    demo["motivo_codigo_cie10"] = (
        demo["motivo_codigo_cie10"].fillna("").map(remapear_cie11)
    )
    demo["_texto_completo"] = (
        demo["motivo_codigo_cie10"].fillna("").map(normalizar_token_cie)
        + " " + demo["motivo_texto"].fillna("")
    ).str.strip()
    _, _, test = _split_estratificado(demo.assign(_i=np.arange(len(demo))))
    return demo, test


def evaluar_por_nivel(paquete: dict, demo, test) -> dict:
    """Evalúa el paquete sobre el split de test y devuelve métricas por clase.

    Usa SOLO componentes serializados en el artefacto (pipeline estructurado,
    vectorizador de texto, umbrales) — misma ruta de producción, sin fugas.
    """
    te_idx = test["_i"].to_numpy()
    y = demo["nivel_triaje"].to_numpy()
    y_te = y[te_idx]

    pipeline = paquete["pipeline_estructurado"]
    vectorizador = paquete["vectorizador_texto"]
    X_te = pipeline.transform(test)
    X_te = X_te.toarray() if hasattr(X_te, "toarray") else np.asarray(X_te)
    X_txt_te = vectorizador.transformar(test["_texto_completo"])
    proba_te = np.asarray(paquete["modelo"].predict_proba(X_te, X_txt_te))
    pred_te = aplicar_umbrales(proba_te, paquete["umbrales"])
    # aplicar_umbrales devuelve índices 0..4 (orden CLASES): codificar y_true
    # igual para la evaluación por clase.
    y_te_enc = np.asarray([CLASES.index(c) for c in y_te])

    metricas = metricas_por_clase(y_te_enc, pred_te, proba_te)
    # Matriz de confusión fila=real, columna=predicho (orden CLASES).
    matriz = np.zeros((len(CLASES), len(CLASES)), dtype=int)
    pred_str = [CLASES[int(i)] for i in pred_te]
    for real, pred in zip(y_te, pred_str, strict=False):
        matriz[CLASES.index(real), CLASES.index(pred)] += 1
    metricas["matriz_confusion"] = {
        "clases": CLASES, "matriz": matriz.tolist(), "n_test": int(len(y_te)),
    }
    metricas["umbrales"] = paquete["umbrales"]
    metricas["version"] = paquete.get("version")
    return metricas


def verificar_garantias(metricas: dict) -> dict:
    """Contrasta las métricas contra GARANTIAS_MINIMAS (por nivel y macro)."""
    verificacion: dict[str, dict] = {}
    for clase in CLASES:
        m = metricas["por_clase"].get(clase, {})
        pisos = GARANTIAS_MINIMAS[clase]
        verificacion[clase] = {
            "recall": round(float(m.get("recall", 0.0)), 4),
            "precision": round(float(m.get("precision", 0.0)), 4),
            "f1": round(float(m.get("f1-score", 0.0)), 4),
            "piso_recall": pisos["recall"],
            "piso_precision": pisos["precision"],
            "cumple": (
                float(m.get("recall", 0.0)) >= pisos["recall"]
                and float(m.get("precision", 0.0)) >= pisos["precision"]
            ),
        }
    verificacion["_macro_f1"] = {
        "valor": round(float(metricas["macro"]["f1"]), 4),
        "piso": MACRO_F1_MINIMO,
        "cumple": float(metricas["macro"]["f1"]) >= MACRO_F1_MINIMO,
    }
    return verificacion


def ejecutar(n: int = 4000, *, destino: Path | None = None) -> dict:
    """Reporte por nivel: imprime tabla, verifica garantías y escribe JSON.

    Devuelve el informe completo; sale con código 1 si alguna garantía falla
    (usable como quality gate en CI).
    """
    paquete, _ = cargar_ganador()
    demo, test = reconstruir_test_demo(n=n)
    metricas = evaluar_por_nivel(paquete, demo, test)
    garantias = verificar_garantias(metricas)

    print(
        f"Modelo: {metricas['version']} · "
        f"test honesto n={metricas['matriz_confusion']['n_test']}"
    )
    print(f"{'Nivel':<6}{'Soporte':>9}{'Precisión':>12}{'Recall':>10}{'F1':>10}   Garantía")
    for clase in CLASES:
        m = metricas["por_clase"].get(clase, {})
        g = garantias[clase]
        print(
            f"{clase:<6}{int(m.get('support', 0)):>9}"
            f"{float(m.get('precision', 0.0)):>12.3f}"
            f"{float(m.get('recall', 0.0)):>10.3f}"
            f"{float(m.get('f1-score', 0.0)):>10.3f}   {'✓' if g['cumple'] else '✗ FALLA'}"
        )
    macro = metricas["macro"]
    print(
        f"\nMacro: precisión {macro['precision']:.3f} · recall {macro['recall']:.3f} · "
        f"F1 {macro['f1']:.3f} · accuracy {metricas['accuracy']:.3f} · "
        f"AUC {metricas.get('auc_roc_ovr')}"
    )
    print(f"Garantía macro-F1 ≥ {MACRO_F1_MINIMO}: "
          f"{'✓' if garantias['_macro_f1']['cumple'] else '✗ FALLA'}")

    informe = {"metricas": metricas, "garantias": garantias}
    ruta = destino or (ARTIFACTS_METRICS / "acierto_por_nivel.json")
    ruta.write_text(
        json.dumps(informe, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nInforme guardado: {ruta}")

    cumple = garantias["_macro_f1"]["cumple"] and all(
        garantias[c]["cumple"] for c in CLASES
    )
    if not cumple:
        raise SystemExit(1)
    return informe


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acierto por nivel de urgencia (I-V)")
    parser.add_argument("--n", type=int, default=4000)
    args = parser.parse_args()
    ejecutar(n=args.n)
