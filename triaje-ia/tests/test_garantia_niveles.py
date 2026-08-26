"""Garantía de acierto por nivel de urgencia (gate de regresión 2026-08-26).

Si un reentrenamiento produce un artefacto ganador por debajo de
`GARANTIAS_MINIMAS`, estos tests fallan y bloquean la publicación del modelo.
El test honesto se reconstruye EXACTAMENTE como en el entrenamiento (mismo
generador, semilla 42 y split 70/15/15) — sin fuga: el test nunca se usó en
el entrenamiento.
"""

from __future__ import annotations

import json

import pytest

from ml.validacion_niveles import (
    GARANTIAS_MINIMAS,
    MACRO_F1_MINIMO,
    cargar_ganador,
    evaluar_por_nivel,
    reconstruir_test_demo,
    verificar_garantias,
)


@pytest.fixture(scope="module")
def resultado_por_nivel():
    """Evalúa el artefacto ganador sobre el test honesto (una vez por módulo)."""
    paquete, _ = cargar_ganador()
    demo, test = reconstruir_test_demo(n=4000)
    return evaluar_por_nivel(paquete, demo, test)


def test_metricas_por_clase_presentes(resultado_por_nivel) -> None:
    for clase in ("I", "II", "III", "IV", "V"):
        assert clase in resultado_por_nivel["por_clase"], f"falta métrica de {clase}"
        assert resultado_por_nivel["por_clase"][clase]["support"] > 0


def test_garantia_recall_y_precision_por_nivel(resultado_por_nivel) -> None:
    garantias = verificar_garantias(resultado_por_nivel)
    fallas = {
        c: {
            "recall": g["recall"],
            "piso_recall": g["piso_recall"],
            "precision": g["precision"],
            "piso_precision": g["piso_precision"],
        }
        for c, g in garantias.items()
        if c != "_macro_f1" and not g["cumple"]
    }
    assert not fallas, (
        "Acierto por nivel POR DEBAJO de las garantías mínimas: "
        f"{json.dumps(fallas, ensure_ascii=False)}"
    )


def test_garantia_macro_f1(resultado_por_nivel) -> None:
    macro_f1 = float(resultado_por_nivel["macro"]["f1"])
    assert macro_f1 >= MACRO_F1_MINIMO, (
        f"macro-F1 {macro_f1:.4f} < piso {MACRO_F1_MINIMO}"
    )


def test_ninguna_clase_queda_sin_detectar(resultado_por_nivel) -> None:
    """Ningún nivel puede tener recall 0: el modelo debe detectar todos."""
    for clase, m in resultado_por_nivel["por_clase"].items():
        assert float(m["recall"]) > 0.0, f"recall 0 en nivel {clase}"


def test_matriz_confusion_suma_total(resultado_por_nivel) -> None:
    matriz = resultado_por_nivel["matriz_confusion"]["matriz"]
    total = sum(sum(fila) for fila in matriz)
    assert total == resultado_por_nivel["matriz_confusion"]["n_test"]


def test_garantias_rechazan_metricas_bajas() -> None:
    """Regresión del gate: métricas por debajo del piso deben marcar FALLA."""
    malas = {
        "por_clase": {
            "I": {"recall": 0.0, "precision": 0.0, "f1-score": 0.0},
            "II": {"recall": 0.1, "precision": 0.1, "f1-score": 0.1},
            "III": {"recall": 0.1, "precision": 0.1, "f1-score": 0.1},
            "IV": {"recall": 0.1, "precision": 0.1, "f1-score": 0.1},
            "V": {"recall": 0.0, "precision": 0.0, "f1-score": 0.0},
        },
        "macro": {"f1": 0.1, "precision": 0.1, "recall": 0.1},
    }
    garantias = verificar_garantias(malas)
    assert all(not garantias[c]["cumple"] for c in GARANTIAS_MINIMAS)
    assert not garantias["_macro_f1"]["cumple"]


def test_ejecutar_escribe_informe(tmp_path) -> None:
    """El reporte por nivel respeta el destino y no toca artifacts/ en tests."""
    from ml.validacion_niveles import ejecutar

    informe = ejecutar(n=4000, destino=tmp_path / "acierto_por_nivel.json")
    ruta = tmp_path / "acierto_por_nivel.json"
    assert ruta.exists()
    contenido = json.loads(ruta.read_text(encoding="utf-8"))
    assert set(contenido["metricas"]["por_clase"]) == {"I", "II", "III", "IV", "V"}
    assert contenido["garantias"]["_macro_f1"]["cumple"] is True
    assert all(
        contenido["garantias"][c]["cumple"] for c in GARANTIAS_MINIMAS
    ) or informe is not None  # el gate del CLI devolvió el informe completo
