"""Herramientas de validación científica (skill validacion-cientifica-ml).

- Brier score multiclase y ECE (calibración de probabilidades).
- Intervalos de confianza por bootstrap (1000 remuestreos).
- Auditoría de equidad por subgrupo demográfico.
- Generación de model card en Markdown.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score

from ml.src.evaluation.metrics import CLASES


def brier_score_multiclase(y_true_enc: np.ndarray, proba: np.ndarray) -> float:
    """Brier multiclase: menor es mejor (0 = perfecto)."""
    y_oh = np.eye(proba.shape[1])[y_true_enc.astype(int)]
    return float(np.mean(np.sum((proba - y_oh) ** 2, axis=1)))


def calibration_error(y_true_enc: np.ndarray, proba: np.ndarray, n_bins: int = 10) -> float:
    """Expected Calibration Error (ECE) por confianza máxima."""
    confianzas = proba.max(axis=1)
    correctas = (proba.argmax(axis=1) == y_true_enc).astype(float)
    bordes = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mascara = (confianzas >= bordes[i]) & (confianzas < bordes[i + 1])
        if mascara.sum() == 0:
            continue
        conf_media = confianzas[mascara].mean()
        acc_media = correctas[mascara].mean()
        ece += mascara.mean() * abs(conf_media - acc_media)
    return float(ece)


def intervalo_confianza_bootstrap(
    y_true: np.ndarray, proba: np.ndarray, *, metrica: str = "f1_macro",
    n_iter: int = 1000, semilla: int = 42,
) -> dict:
    """IC 95% por bootstrap empírico sobre la métrica elegida."""
    rng = np.random.default_rng(semilla)
    n = len(y_true)
    valores = np.empty(n_iter)
    for i in range(n_iter):
        idx = rng.integers(0, n, n)
        y_t, p_t = y_true[idx], proba[idx]
        pred = p_t.argmax(axis=1)
        if metrica == "f1_macro":
            valores[i] = f1_score(y_t, pred, average="macro", labels=np.arange(len(CLASES)),
                                  zero_division=0)
        elif metrica == "accuracy":
            valores[i] = accuracy_score(y_t, pred)
        elif metrica == "recall_i_ii":
            mascara = np.isin(y_t, [CLASES.index("I"), CLASES.index("II")])
            valores[i] = recall_score(
                y_t[mascara], pred[mascara], average="macro",
                labels=np.arange(len(CLASES)), zero_division=0,
            )
        else:
            raise ValueError(f"Métrica desconocida: {metrica}")
    return {
        "metrica": metrica,
        "punto": float(valores.mean()),
        "ic95": [float(np.percentile(valores, 2.5)), float(np.percentile(valores, 97.5))],
        "n_bootstrap": n_iter,
    }


def equidad_por_subgrupo(y_true: np.ndarray, pred: np.ndarray, grupo: np.ndarray) -> dict:
    """Métricas desagregadas por subgrupo (recall I-II priorizado).

    `grupo` es un array del mismo largo que y_true con el valor del subgrupo.
    """
    resultado = {}
    for valor in sorted(set(grupo)):
        mascara = grupo == valor
        y_t, p_t = y_true[mascara], pred[mascara]
        if len(y_t) < 10:
            resultado[str(valor)] = {"n": int(len(y_t)), "nota": "muestra insuficiente"}
            continue
        mascara_criticos = np.isin(y_t, [CLASES.index("I"), CLASES.index("II")])
        resultado[str(valor)] = {
            "n": int(len(y_t)),
            "f1_macro": float(f1_score(y_t, p_t, average="macro",
                                       labels=np.arange(len(CLASES)), zero_division=0)),
            "recall_i_ii": float(recall_score(
                y_t[mascara_criticos], p_t[mascara_criticos], average="macro",
                labels=np.arange(len(CLASES)), zero_division=0,
            )) if mascara_criticos.sum() > 0 else None,
        }
    return resultado


def generar_model_card(
    *,
    version: str,
    algoritmo: str,
    fecha_entrenamiento: str,
    datos: dict,
    metricas: dict,
    calibracion: dict,
    ic_bootstrap: dict,
    equidad: dict,
    limitaciones: list[str],
    destino: Path,
) -> Path:
    """Fase 7: model card en Markdown + respaldo JSON."""
    por_clase = metricas.get("por_clase", {})
    filas = "\n".join(
        f"| {n} | {por_clase.get(n, {}).get('precision', '—')} | "
        f"{por_clase.get(n, {}).get('recall', '—')} | "
        f"{por_clase.get(n, {}).get('f1-score', '—')} |"
        for n in CLASES
    )
    contenido = f"""# Model Card — {version}

- **Algoritmo:** {algoritmo} · **Fecha de entrenamiento:** {fecha_entrenamiento}
- **Clases:** {' · '.join(CLASES)} (triaje I–V, Res. 5596/2015)

## Datos de entrenamiento
{json.dumps(datos, ensure_ascii=False, indent=2)}

## Métricas por clase
| Nivel | Precisión | Recall | F1 |
|---|---|---|---|
{filas}

- **Macro-F1:** {metricas.get('macro', {}).get('f1')} · **AUC-ROC (OVR):**
  {metricas.get('auc_roc_ovr')}

## Intervalos de confianza (bootstrap 1000)
{json.dumps(ic_bootstrap, ensure_ascii=False, indent=2)}

## Calibración de probabilidades
- Brier multiclase: {calibracion.get('brier')} · ECE: {calibracion.get('ece')}

## Auditoría de equidad por subgrupo
{json.dumps(equidad, ensure_ascii=False, indent=2)}

## Casos de uso previstos
- Apoyo a la decisión de triaje en urgencias (no autónomo).
- Monitoreo de concordancia IA vs profesional.

## Casos de uso NO previstos
- Decisión clínica sin validación profesional.
- Poblaciones fuera del contexto colombiano / datos sintéticos de demo.

## Limitaciones conocidas
{chr(10).join('- ' + lim for lim in limitaciones)}
"""
    destino.write_text(contenido, encoding="utf-8")
    destino.with_suffix(".json").write_text(
        json.dumps(
            {
                "version": version, "algoritmo": algoritmo, "datos": datos,
                "metricas": metricas, "calibracion": calibracion,
                "ic_bootstrap": ic_bootstrap, "equidad": equidad,
                "limitaciones": limitaciones,
            },
            ensure_ascii=False, indent=2, default=str,
        ), encoding="utf-8",
    )
    return destino
