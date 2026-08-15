"""Orquestador del pipeline ML (Épica E3, RF-016) — reproducible de punta a punta.

Uso:  python -m ml.pipeline --n 4000 --k-folds 5

Datos reales integrados (si están en `datasets/`, raíz del repo):
- `dataset_urgencias_san_juan_de_dios_custom.csv` (43.594 eventos, triaje I–V +
  CIE-10 + diagnóstico textual) → entrena el submodelo de texto de la fusión
  tardía (fine-tuning del contexto colombiano).
- `clasificacion_triage_urgencias_*.csv` (MinSalud nacional, 89.453 eventos) →
  valida la calibración de la distribución de niveles del sintético.

Modelo ganador = fusión tardía afinada: XGBoost estructurado (con búsqueda de
hiperparámetros + early stopping + pesos balanceados) + Regresión Logística
sobre TF-IDF (demo + SJdD), combinados por promedio ponderado (0.7/0.3).
"""

from __future__ import annotations

import argparse
import json
from datetime import date

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from ml.src import ARTIFACTS_METRICS, DATA_PROCESSED, ML_ROOT, SEMILLA_GLOBAL
from ml.src.data.anonimizacion import anonimizar
from ml.src.data.ingesta import (
    _DISTRIBUCION_REAL,
    generar_datos_sinteticos,
    ingestar_csv_local,
    ingestar_mimic_ed,
    ingestar_san_juan_de_dios,
    ingestar_triage_nacional,
)
from ml.src.evaluation.benchmarks import tabla_comparativa
from ml.src.evaluation.metrics import (
    CLASES,
    guardar_metricas,
    matriz_confusion,
    metricas_por_clase,
    verificar_metas,
)
from ml.src.evaluation.shap_explain import explicar_shap, guardar_shap
from ml.src.features.feature_engineering import construir_matriz_estructurada
from ml.src.features.limpieza import LimpiezaOutliers, NormalizadorRegimen, ValidadorCalidad
from ml.src.models.baselines import entrenar_baselines
from ml.src.models.early_fusion import entrenar_early_fusion
from ml.src.models.embeddings import vectorizar_texto
from ml.src.models.late_fusion import (
    LateFusionClassifier,
    PromedioPonderado,
    entrenar_late_fusion,
)
from ml.src.models.thresholds import ajustar_umbrales, aplicar_umbrales
from ml.src.registry import serializar_paquete

DATASETS_DIR = ML_ROOT.parents[1] / "datasets"
SJD_CSV = DATASETS_DIR / "dataset_urgencias_san_juan_de_dios_custom.csv"
NACIONAL_CSV = DATASETS_DIR / "clasificacion_triage_urgencias_20260813.csv"

# Búsqueda de hiperparámetros del submodelo estructurado (acotada al demo).
_GRILLA_XGB = [
    {"max_depth": 3, "learning_rate": 0.05},
    {"max_depth": 3, "learning_rate": 0.1},
    {"max_depth": 5, "learning_rate": 0.05},
    {"max_depth": 5, "learning_rate": 0.1},
]


def _preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Anonimización SIEMPRE → limpieza (TT-E3-01/02)."""
    df = anonimizar(df)  # obligatorio, sin excepciones (Ley 1581/2012)
    df = ValidadorCalidad.validar(df)
    df = NormalizadorRegimen.normalizar(df)
    numericas = [
        "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
        "saturacion_o2", "presion_sistolica", "presion_diastolica", "peso", "talla",
    ]
    return LimpiezaOutliers([c for c in numericas if c in df.columns]).fit_transform(df)


def _split_estratificado(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """70/15/15 estratificado por nivel (anti-leakage, semilla fija)."""
    train, resto = train_test_split(
        df, test_size=0.30, stratify=df["nivel_triaje"], random_state=SEMILLA_GLOBAL
    )
    val, test = train_test_split(
        resto, test_size=0.50, stratify=resto["nivel_triaje"], random_state=SEMILLA_GLOBAL
    )
    return train, val, test


def _pesos_balanceados(y_enc: np.ndarray) -> np.ndarray:
    """Pesos por muestra 1/clase — mitiga el desbalance I 0.2% vs III 88.5%."""
    n = len(y_enc)
    conteos = np.bincount(y_enc, minlength=len(CLASES)).astype(float)
    conteos[conteos == 0] = 1.0
    pesos_clase = n / (len(CLASES) * conteos)
    return pesos_clase[y_enc]


def _sintonizar_submodelo_estructurado(
    X_tr, y_tr_enc, X_va, y_va_enc, *, semilla: int
) -> tuple[XGBClassifier, dict]:
    """Búsqueda acotada sobre validación (macro-F1) con pesos balanceados."""
    pesos = _pesos_balanceados(y_tr_enc)
    mejor: tuple[float, XGBClassifier, dict] | None = None
    for config in _GRILLA_XGB:
        modelo = XGBClassifier(
            n_estimators=250, eval_metric="mlogloss", random_state=semilla,
            n_jobs=-1, **config,
        )
        modelo.fit(X_tr, y_tr_enc, sample_weight=pesos)
        pred = modelo.predict(X_va)
        f1 = f1_score(y_va_enc, pred, average="macro", labels=np.arange(len(CLASES)),
                      zero_division=0)
        if mejor is None or f1 > mejor[0]:
            mejor = (float(f1), modelo, config)
    assert mejor is not None
    f1, modelo, config = mejor
    print(f"    sub_a afinado: {config} · macro-F1 val = {f1:.4f}")
    return modelo, {"mejor_config": config, "macro_f1_val": f1}


def _evaluar_texto_sjd(sub_b_factory, X_sjd, y_sjd, encoder, *, semilla: int) -> dict:
    """Evidencia del fine-tuning colombiano SIN fuga: el submodelo de texto se
    entrena solo con el 80% de SJdD y se evalúa sobre el 20% no visto.
    """
    tr, te = train_test_split(
        np.arange(len(y_sjd)), test_size=0.2, stratify=y_sjd, random_state=semilla
    )
    sub_b = sub_b_factory()
    sub_b.fit(X_sjd[tr], y_sjd[tr])
    proba = sub_b.predict_proba(X_sjd[te])
    y_str = encoder.inverse_transform(y_sjd[te])
    pred_str = encoder.inverse_transform(proba.argmax(axis=1))
    metricas = metricas_por_clase(y_str, pred_str, proba)
    guardar_metricas("texto_sjd_holdout", metricas, extra={"n_test": int(len(te))})
    return metricas


def _calibrar_distribucion(nacional: pd.DataFrame | None, demo: pd.DataFrame) -> dict:
    """Compara la distribución real nacional contra la del demo sintético."""
    esperado = {c: _DISTRIBUCION_REAL[c] for c in CLASES}
    demo_dist = demo["nivel_triaje"].value_counts(normalize=True).reindex(CLASES).fillna(0)
    demo_medido = {c: round(float(demo_dist[c]), 6) for c in CLASES}
    real_medido: dict[str, float] | None = None
    if nacional is not None:
        real = nacional["nivel_triaje"].value_counts(normalize=True).reindex(CLASES).fillna(0)
        real_medido = {c: round(float(real[c]), 6) for c in CLASES}
    informe = {
        "esperado_rnf004": esperado,
        "medido_nacional": real_medido,
        "demo_sintetico": demo_medido,
        "desviacion_maxima_demo": round(
            float(max(abs(demo_dist[c] - _DISTRIBUCION_REAL[c]) for c in CLASES)), 4
        ),
    }
    (ARTIFACTS_METRICS / "calibracion_distribucion.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return informe


def ejecutar(n: int = 4000, *, k_folds: int = 5) -> dict:
    """Corre el pipeline completo y devuelve el resumen final."""
    print("1/10 · Ingesta: demo sintético + cohorte SJdD + nacional (si existen)")
    demo = _preparar(ingestar_csv_local(generar_datos_sinteticos(n=n), fuente="sintetico_demo"))
    sjd = None
    if SJD_CSV.exists():
        sjd = _preparar(ingestar_san_juan_de_dios(SJD_CSV))
        print(f"    SJdD real: {len(sjd)} eventos (fine-tuning colombiano)")
    else:
        print("    ⚠ SJdD no encontrado — el submodelo de texto se entrena solo con demo")
    nacional = None
    if NACIONAL_CSV.exists():
        nacional = ingestar_triage_nacional(NACIONAL_CSV)
        print(f"    Nacional MinSalud: {len(nacional)} eventos (calibración)")
    # MIMIC-IV-ED local (CSVs descargados por el usuario con credenciales
    # PhysioNet) — refuerza el submodelo de texto con chief complaint + acuity.
    mimic = None
    MIMIC_DIR = ML_ROOT.parents[1] / "datasets" / "mimic-iv-ed"
    if MIMIC_DIR.exists():
        mimic = _preparar(ingestar_mimic_ed(MIMIC_DIR))
        print(f"    MIMIC-IV-ED local: {len(mimic)} eventos (chief complaint + acuity)")
    calibracion = _calibrar_distribucion(nacional, demo)

    print("2/10 · Split estratificado 70/15/15 del demo (ANTES de tocar features)")
    demo["_texto_completo"] = (
        demo["motivo_codigo_cie10"].fillna("") + " " + demo["motivo_texto"].fillna("")
    ).str.strip()
    if sjd is not None:
        sjd["_texto_completo"] = (
            sjd["motivo_codigo_cie10"].fillna("") + " " + sjd["motivo_texto"].fillna("")
        ).str.strip()
    if mimic is not None:
        mimic["_texto_completo"] = (
            mimic["motivo_codigo_cie10"].fillna("") + " " + mimic["motivo_texto"].fillna("")
        ).str.strip()
    train, val, test = _split_estratificado(demo.assign(_i=np.arange(len(demo))))
    tr_idx = train["_i"].to_numpy()
    va_idx = val["_i"].to_numpy()
    te_idx = test["_i"].to_numpy()
    y = demo["nivel_triaje"].to_numpy()
    encoder = LabelEncoder().fit(CLASES)
    y_tr_enc = encoder.transform(y[tr_idx])
    faltantes = set(range(len(CLASES))) - set(np.unique(y_tr_enc))
    if faltantes:
        raise SystemExit(f"El demo no contiene todas las clases en train: {faltantes} — suba --n")

    print("3/10 · Pipeline estructurado ajustado SOLO sobre train (anti-leakage)")
    _, pipeline_est = construir_matriz_estructurada(train)
    X_est = pipeline_est.transform(demo)
    X_est = X_est.toarray() if hasattr(X_est, "toarray") else np.asarray(X_est)

    print("4/10 · TF-IDF sobre CIE+texto (demo train + SJdD + MIMIC + catálogo)")
    textos_entrenamiento = pd.concat(
        [train["_texto_completo"]]
        + ([sjd["_texto_completo"]] if sjd is not None else [])
        + ([mimic["_texto_completo"]] if mimic is not None else [])
    )
    # Ajuste 2026-08-14: vocabulario extendido con TODO el catálogo de motivos
    # (validación: 8/71 motivos tenían cobertura 0; ver validacion-motivos-*.md).
    from app.domain.catalogos import CATALOGO_MOTIVOS

    textos_catalogo = pd.Series(
        [f"{codigo} {descripcion}" for codigo, descripcion, _ in CATALOGO_MOTIVOS]
    )
    _, vectorizador = vectorizar_texto(
        pd.DataFrame({"motivo_texto": textos_entrenamiento}),
        max_features=600,
        textos_extra=textos_catalogo,
    )
    assert vectorizador is not None
    X_txt_demo = vectorizador.transformar(demo["_texto_completo"])
    X_txt_sjd = (
        vectorizador.transformar(sjd["_texto_completo"])
        if sjd is not None else None
    )
    X_txt_mimic = (
        vectorizador.transformar(mimic["_texto_completo"])
        if mimic is not None else None
    )

    print("5/10 · Baselines unimodales (LR, RF, XGBoost)")
    baselines = entrenar_baselines(X_est[tr_idx], y[tr_idx], k_folds=k_folds)

    print("6/10 · Early Fusion vs Late Fusion (mismos splits y métricas)")
    early = entrenar_early_fusion(
        X_est[tr_idx], y[tr_idx], X_txt_demo[tr_idx], k_folds=k_folds
    )
    late = entrenar_late_fusion(
        X_est[tr_idx], y[tr_idx], X_txt_demo[tr_idx],
        k_folds=k_folds, combinadores=("promedio_ponderado", "stacking"),
    )

    print("7/10 · Ganador: fusión tardía afinada (XGBoost afinado + LR texto)")
    sub_a, tuning = _sintonizar_submodelo_estructurado(
        X_est[tr_idx], y_tr_enc, X_est[va_idx], encoder.transform(y[va_idx]),
        semilla=SEMILLA_GLOBAL,
    )
    if sjd is not None:
        y_texto = np.concatenate([y_tr_enc, encoder.transform(sjd["nivel_triaje"].to_numpy())])
        X_texto = np.vstack([X_txt_demo[tr_idx], X_txt_sjd])
    else:
        y_texto, X_texto = y_tr_enc, X_txt_demo[tr_idx]
    if mimic is not None:
        y_texto = np.concatenate(
            [y_texto, encoder.transform(mimic["nivel_triaje"].to_numpy())]
        )
        X_texto = np.vstack([X_texto, X_txt_mimic])
    sub_b = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=SEMILLA_GLOBAL)
    sub_b.fit(X_texto, y_texto)

    print("8/10 · Peso del combinador por validación + umbrales + test")
    mejor_peso, mejor_f1_val = 0.7, -1.0
    for peso in (0.5, 0.6, 0.7, 0.8, 0.9):
        candidato = LateFusionClassifier(
            sub_a, sub_b, PromedioPonderado(peso), clases=CLASES
        )
        proba_va = candidato.predict_proba(X_est[va_idx], X_txt_demo[va_idx])
        f1 = f1_score(
            encoder.transform(y[va_idx]), proba_va.argmax(axis=1),
            average="macro", labels=np.arange(len(CLASES)), zero_division=0,
        )
        if f1 > mejor_f1_val:
            mejor_peso, mejor_f1_val = peso, float(f1)
    print(f"    peso estructurado elegido: {mejor_peso} · macro-F1 val = {mejor_f1_val:.4f}")
    ganador = LateFusionClassifier(
        sub_a, sub_b, PromedioPonderado(mejor_peso), clases=CLASES
    )

    proba_val = ganador.predict_proba(X_est[va_idx], X_txt_demo[va_idx])
    umbrales = ajustar_umbrales(y[va_idx], proba_val)
    proba_test = ganador.predict_proba(X_est[te_idx], X_txt_demo[te_idx])
    pred_test = aplicar_umbrales(proba_test, umbrales)
    metricas = metricas_por_clase(encoder.transform(y[te_idx]), pred_test, proba_test)
    metas = verificar_metas(metricas)
    matriz_confusion(y[te_idx], encoder.inverse_transform(pred_test)).to_csv(
        DATA_PROCESSED / "matriz_confusion_ganador.csv"
    )
    guardar_metricas(
        "modelo_ganador", metricas,
        extra={
            "metas": metas, "umbrales": umbrales, "tuning": tuning,
            "peso_estructurado": mejor_peso,
        },
    )

    print("9/10 · Evidencia SJdD (holdout texto) + SHAP + benchmarks")
    evidencia_sjd = None
    if X_txt_sjd is not None:
        evidencia_sjd = _evaluar_texto_sjd(
            lambda: LogisticRegression(
                max_iter=2000, class_weight="balanced", random_state=SEMILLA_GLOBAL
            ),
            X_txt_sjd, encoder.transform(sjd["nivel_triaje"].to_numpy()),
            encoder, semilla=SEMILLA_GLOBAL,
        )
    nombres = list(pipeline_est.named_steps["columnas"].get_feature_names_out())
    explicacion = explicar_shap(sub_a, X_est[te_idx][:200], nombres_features=nombres)
    guardar_shap("modelo_ganador", explicacion)
    comparativa = tabla_comparativa(metricas)
    (ARTIFACTS_METRICS / "comparativa_benchmarks.json").write_text(
        json.dumps(comparativa, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )

    print("10/10 · Serialización del paquete versionado")
    ruta_modelo = serializar_paquete(
        modelo=ganador,
        pipeline_estructurado=pipeline_est,
        vectorizador_texto=vectorizador,
        umbrales=umbrales,
        metricas=metricas,
        nombre_algoritmo="latefusion-xgb-text-sjd",
        fecha=date.today(),
    )

    resumen = {
        "datos": {
            "n_demo": int(len(demo)),
            "n_sjd": int(len(sjd)) if sjd is not None else None,
            "n_nacional": int(len(nacional)) if nacional is not None else None,
            "calibracion": calibracion,
        },
        "baselines": {k: v["macro_cv"] for k, v in baselines.items()},
        "early_fusion": early["macro_cv"],
        "late_fusion": late,
        "ganador_macro": metricas["macro"],
        "auc_roc_ovr": metricas.get("auc_roc_ovr"),
        "metas_cumplidas": metas,
        "umbrales": umbrales,
        "tuning_sub_a": tuning,
        "peso_estructurado": mejor_peso,
        "texto_sjd_holdout": (
            evidencia_sjd["macro"] if evidencia_sjd is not None else None
        ),
        "ruta_modelo": str(ruta_modelo),
        "comparativa_benchmarks": comparativa,
    }
    (DATA_PROCESSED / "resumen_pipeline.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(
        {k: resumen[k] for k in (
            "ganador_macro", "auc_roc_ovr", "metas_cumplidas", "umbrales",
            "tuning_sub_a", "peso_estructurado", "texto_sjd_holdout", "ruta_modelo",
        )},
        ensure_ascii=False, indent=2, default=str,
    ))
    return resumen


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ML TriajeIA (Épica E3)")
    parser.add_argument("--n", type=int, default=4000)
    parser.add_argument("--k-folds", type=int, default=5)
    args = parser.parse_args()
    ejecutar(n=args.n, k_folds=args.k_folds)
