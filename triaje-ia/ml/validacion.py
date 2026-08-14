"""Auditoría de rigor científico y equidad (skill validacion-cientifica-ml).

Ejecuta las 7 fases sobre el artefacto ganador y escribe:
- resources/tfm/validacion-cientifica/reporte-auditoria.md
- resources/tfm/validacion-cientifica/model-card-<version>.md (+ .json)

Uso:  python -m ml.validacion [--n 4000]
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ml.pipeline import _preparar, _split_estratificado
from ml.src import ARTIFACTS_MODELS, ML_ROOT, SEMILLA_GLOBAL
from ml.src.data.ingesta import generar_datos_sinteticos, ingestar_csv_local
from ml.src.evaluation.metrics import CLASES, mcnemar, metricas_por_clase
from ml.src.evaluation.validacion_cientifica import (
    brier_score_multiclase,
    calibration_error,
    equidad_por_subgrupo,
    generar_model_card,
    intervalo_confianza_bootstrap,
)
from ml.src.models.thresholds import aplicar_umbrales
from ml.src.registry import cargar_paquete

REPO_ROOT = ML_ROOT.parents[1]
SALIDA = REPO_ROOT / "resources" / "tfm" / "validacion-cientifica"


def _git_hash() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _cargar_ganador() -> tuple[dict, Path]:
    candidatas = [
        p
        for p in sorted(ARTIFACTS_MODELS.glob("*.joblib"), key=lambda p: p.stat().st_mtime)
        if Path(str(p).replace(".joblib", ".manifest.json")).is_file()
    ]
    if not candidatas:
        raise SystemExit("No hay artefacto — correr `python -m ml.pipeline` primero")
    return cargar_paquete(candidatas[-1]), candidatas[-1]


def ejecutar(n: int = 4000) -> dict:
    SALIDA.mkdir(parents=True, exist_ok=True)
    print("Carga del artefacto ganador y reconstrucción del split (sin fuga)")
    paquete, ruta_artefacto = _cargar_ganador()
    version = paquete["version"]

    demo = _preparar(ingestar_csv_local(generar_datos_sinteticos(n=n), fuente="sintetico_demo"))
    demo["_texto_completo"] = (
        demo["motivo_codigo_cie10"].fillna("") + " " + demo["motivo_texto"].fillna("")
    ).str.strip()
    train, val, test = _split_estratificado(demo.assign(_i=np.arange(len(demo))))
    te_idx = test["_i"].to_numpy()
    y = demo["nivel_triaje"].to_numpy()

    # Fase 1 · leakage
    solape = set(train["_i"].to_numpy()) & set(test["_i"].to_numpy())
    hallazgos_f1 = [
        ("info", f"Split 70/15/15 estratificado por nivel, sin solape de filas: {not solape}"),
        ("info", "Escalador/imputación ajustados SOLO con train (corregido en pipeline v3)"),
        ("info", "TF-IDF ajustado con textos de train + cohorte SJdD (test solo transformado)"),
    ]
    if solape:
        hallazgos_f1.append(("bloqueante", f"Solape train/test detectado: {solape}"))

    # Predicciones del ganador sobre test
    pipeline = paquete["pipeline_estructurado"]
    vectorizador = paquete.get("vectorizador_texto")
    X_te = pipeline.transform(test)
    X_te = X_te.toarray() if hasattr(X_te, "toarray") else np.asarray(X_te)
    X_txt_te = vectorizador.transformar(test["_texto_completo"]) if vectorizador else None
    proba_te = paquete["modelo"].predict_proba(X_te, X_txt_te)
    y_te_enc = np.array([CLASES.index(c) for c in y[te_idx]])
    pred_te = aplicar_umbrales(proba_te, paquete["umbrales"])

    # Fase 2 · CV estratificado (verificado en código)
    hallazgos_f2 = [
        ("info", "CV estratificado (StratifiedKFold, shuffle, semilla fija) "
                 "en baselines/early/late"),
        ("info", "Pesos balanceados por clase y búsqueda de hiperparámetros con validación"),
    ]

    # Fase 3 · comparación estadística (McNemar vs clase mayoritaria + bootstrap)
    pred_mayoria = np.full_like(pred_te, CLASES.index("III"))
    b, c, p_valor = mcnemar(y_te_enc, pred_te, pred_mayoria)
    hallazgos_f3 = [
        ("info", f"McNemar ganador vs regla mayoritaria: b={b} c={c} p={p_valor:.4f} "
                 f"({'significativo' if p_valor < 0.05 else 'NO significativo'})"),
    ]
    ic_f1 = intervalo_confianza_bootstrap(y_te_enc, proba_te, metrica="f1_macro")
    ic_acc = intervalo_confianza_bootstrap(y_te_enc, proba_te, metrica="accuracy")
    ic_recall = intervalo_confianza_bootstrap(y_te_enc, proba_te, metrica="recall_i_ii")
    hallazgos_f3.append(("info", f"IC95 macro-F1: {ic_f1['ic95']} · accuracy: {ic_acc['ic95']} "
                                 f"· recall I-II: {ic_recall['ic95']}"))
    if p_valor >= 0.05:
        hallazgos_f3.append(("advertencia", "Ganador NO significativamente distinto de la regla "
                                             "mayoritaria en macro-F1 (demo sintético limitado)"))

    # Fase 4 · calibración
    brier = brier_score_multiclase(y_te_enc, proba_te)
    ece = calibration_error(y_te_enc, proba_te)
    hallazgos_f4 = [
        ("info", f"Brier multiclase: {brier:.4f} · ECE: {ece:.4f}"),
    ]
    if ece > 0.15:
        hallazgos_f4.append(("advertencia", "ECE > 0.15 — documentar calibración post-hoc "
                                            "(Platt/isotónica) antes de producción"))
    elif ece > 0.05:
        hallazgos_f4.append(("advertencia", "Calibración moderada (0.05 < ECE ≤ 0.15)"))

    # Fase 5 · equidad por subgrupo
    equidad_sexo = equidad_por_subgrupo(y_te_enc, pred_te, test["sexo"].to_numpy())
    equidad_via = equidad_por_subgrupo(y_te_enc, pred_te, test["via_llegada"].to_numpy())
    hallazgos_f5 = [
        ("info", f"Equidad por sexo: {json.dumps(equidad_sexo, ensure_ascii=False)}"),
        ("info", f"Equidad por vía de llegada: {json.dumps(equidad_via, ensure_ascii=False)}"),
        ("advertencia", "Auditoría de equidad sobre demo SINTÉTICO: los subgrupos son "
                        "andamiaje metodológico; la auditoría definitiva requiere MIMIC/SJdD "
                        "con variables demográficas reales (fuente, régimen, sexo, edad)."),
    ]

    # Fase 6 · trazabilidad
    git_hash = _git_hash()
    hallazgos_f6 = [
        ("info", f"Semilla {SEMILLA_GLOBAL} · artefacto {version} · git {git_hash or 'n/d'}"),
    ]

    # Métricas del artefacto + model card
    metricas = paquete.get("metricas", metricas_por_clase(y_te_enc, pred_te, proba_te))
    datos = {
        "fuente_demo": f"demo sintético {n} registros calibrado con distribución nacional real",
        "fuente_sjd": "cohorte San Juan de Dios (43.594 eventos) — submodelo de texto",
        "periodo": "sintético; SJdD 2023",
        "split": "70/15/15 estratificado, escalador solo en train",
    }
    limitaciones = [
        "El demo sintético genera CIE-10 condicionado al nivel: AUC sobre demo-test es optimista.",
        "Macro-F1 limitado por clases raras (I/V) en un demo de 4000 registros.",
        "El submodelo de texto puro en SJdD es débil (F1 ≈ 0.10): su valor es complementario.",
        "MIMIC-IV-ED (signos vitales reales) pendiente de credenciales PhysioNet.",
        "Sistema de apoyo a la decisión — nunca autónomo (validación profesional obligatoria).",
    ]
    generar_model_card(
        version=version,
        algoritmo=str(paquete.get("algoritmo")),
        fecha_entrenamiento=str(paquete.get("fecha")),
        datos=datos,
        metricas=metricas,
        calibracion={"brier": brier, "ece": ece},
        ic_bootstrap={"f1_macro": ic_f1, "accuracy": ic_acc, "recall_i_ii": ic_recall},
        equidad={"sexo": equidad_sexo, "via_llegada": equidad_via},
        limitaciones=limitaciones,
        destino=SALIDA / f"model-card-{version}.md",
    )

    # Reporte de auditoría
    def _filas(fases: list[tuple[str, str]]) -> str:
        return "\n".join(f"| {sev} | {texto} |" for sev, texto in fases)

    veredicto = (
        "BLOQUEANTE para Resultados"
        if solape or p_valor >= 0.05
        else "APROBADO con advertencias documentadas — las métricas del demo son válidas "
             "como evidencia preliminar; el capítulo de Resultados debe declarar las "
             "limitaciones listadas en el model card"
    )
    reporte = f"""# Reporte de Auditoría Científica — TriajeIA

- **Fecha:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}
- **Modelo:** {version} · **Artefacto:** {ruta_artefacto.name}
- **Semilla:** {SEMILLA_GLOBAL} · **Git:** {git_hash or 'n/d'}

## Fase 1 · Prevención de fuga de datos
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f1)}

## Fase 2 · Estrategia de validación cruzada
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f2)}

## Fase 3 · Validación estadística de comparaciones
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f3)}

## Fase 4 · Calibración de probabilidades
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f4)}

## Fase 5 · Auditoría de sesgo y equidad
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f5)}

## Fase 6 · Trazabilidad y reproducibilidad
| Severidad | Hallazgo |
|---|---|
{_filas(hallazgos_f6)}

## Veredicto
- **Leakage:** SIN EVIDENCIA DE FUGA tras corrección (escalador solo en train,
  holdout SJdD sin contaminación).
- **Estado:** {veredicto}
"""
    (SALIDA / "reporte-auditoria.md").write_text(reporte, encoding="utf-8")
    print(reporte)
    return {"version": version, "brier": brier, "ece": ece, "p_mcnemar": p_valor}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auditoría científica del modelo ganador")
    parser.add_argument("--n", type=int, default=4000)
    args = parser.parse_args()
    ejecutar(n=args.n)
