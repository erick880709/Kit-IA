"""Pruebas de las herramientas de validación científica (paso 2)."""

from __future__ import annotations

import numpy as np
import pytest

from ml.src.evaluation.validacion_cientifica import (
    brier_score_multiclase,
    calibration_error,
    equidad_por_subgrupo,
    intervalo_confianza_bootstrap,
)


@pytest.fixture
def prediccion_perfecta():
    proba = np.array([[0.9, 0.1, 0.0, 0.0, 0.0], [0.05, 0.9, 0.05, 0.0, 0.0]])
    y = np.array([0, 1])
    return y, proba


def test_brier_perfecto_es_cero(prediccion_perfecta):
    y, proba = prediccion_perfecta
    assert brier_score_multiclase(y, proba) < 0.1


def test_brier_aleatorio_es_peor(prediccion_perfecta):
    y, _ = prediccion_perfecta
    proba_mal = np.array([[0.2, 0.2, 0.2, 0.2, 0.2], [0.2, 0.2, 0.2, 0.2, 0.2]])
    assert brier_score_multiclase(y, proba_mal) > 0.3


def test_ece_calibrado_es_pequeno(prediccion_perfecta):
    y, proba = prediccion_perfecta
    assert calibration_error(y, proba, n_bins=5) < 0.2


def test_bootstrap_intervalo_valido(prediccion_perfecta):
    y, proba = prediccion_perfecta
    resultado = intervalo_confianza_bootstrap(y, proba, metrica="accuracy", n_iter=100)
    assert 0.0 <= resultado["ic95"][0] <= resultado["ic95"][1] <= 1.0
    assert resultado["n_bootstrap"] == 100


def test_equidad_distingue_grupos():
    y = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
    pred = np.array([0, 0, 1, 0, 2, 2, 3, 3, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
    grupo = np.array(["A"] * 10 + ["B"] * 10)
    resultado = equidad_por_subgrupo(y, pred, grupo)
    assert set(resultado) == {"A", "B"}
    assert resultado["A"]["n"] == 10 and resultado["B"]["n"] == 10
    # Grupo B perfecto > grupo A (un error de recall en II).
    assert resultado["B"]["f1_macro"] > resultado["A"]["f1_macro"]


def test_equidad_grupo_pequeno_marca_insuficiente():
    y = np.array([0, 1, 2])
    pred = y.copy()
    grupo = np.array(["X", "Y", "Z"])
    resultado = equidad_por_subgrupo(y, pred, grupo)
    assert all("nota" in valor for valor in resultado.values())
