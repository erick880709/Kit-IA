"""Tests de la simulación balanceada por nivel (mejora máxima precisión 2026-08-26).

Verifican que el generador: (1) replica la distribución real de entrenamiento,
(2) cumple las anclas clínicas I/V, (3) es determinista y balanceado, y
(4) no inventa motivos fuera del vocabulario de entrenamiento.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ml.src.data.ingesta import FuenteSinteticaDemo
from ml.src.data.simulacion import (
    _LIMITES,
    generar_simulados_balanceados,
    resumen_similitud,
)

# Columnas que las anclas clínicas re-escriben deliberadamente (no se auditan
# por similitud estadística en I y V, sino por su banda clínica objetivo).
_ANCLA_I = {"saturacion_o2", "frecuencia_cardiaca"}
_ANCLA_V = {
    "saturacion_o2", "frecuencia_cardiaca", "frecuencia_respiratoria",
    "temperatura", "presion_sistolica",
}


@pytest.fixture(scope="module")
def df_train() -> pd.DataFrame:
    return FuenteSinteticaDemo(n=4000, semilla=7).generar()


def test_forma_y_balance_por_nivel(df_train: pd.DataFrame) -> None:
    sim = generar_simulados_balanceados(df_train, n_por_nivel=120, semilla=42)
    assert len(sim) == 5 * 120
    assert sim["nivel_triaje"].value_counts().to_dict() == {
        "I": 120, "II": 120, "III": 120, "IV": 120, "V": 120,
    }
    assert sim["fuente"].eq("simulacion_balanceada").all()


def test_determinismo_por_semilla(df_train: pd.DataFrame) -> None:
    a = generar_simulados_balanceados(df_train, n_por_nivel=60, semilla=42)
    b = generar_simulados_balanceados(df_train, n_por_nivel=60, semilla=42)
    c = generar_simulados_balanceados(df_train, n_por_nivel=60, semilla=43)
    pd.testing.assert_frame_equal(a, b)
    assert not a["frecuencia_cardiaca"].equals(c["frecuencia_cardiaca"])


def test_ancla_nivel_i_siempre_en_peligro(df_train: pd.DataFrame) -> None:
    sim = generar_simulados_balanceados(df_train, n_por_nivel=100, semilla=7)
    nivel_i = sim[sim["nivel_triaje"] == "I"]
    peligro = (
        (nivel_i["saturacion_o2"] < 90)
        | (nivel_i["presion_sistolica"] < 90)
        | (nivel_i["frecuencia_cardiaca"] > 120)
        | (nivel_i["frecuencia_respiratoria"] > 28)
        | (nivel_i["temperatura"] > 39.0)
    )
    assert peligro.all()


def test_ancla_nivel_v_siempre_normal(df_train: pd.DataFrame) -> None:
    sim = generar_simulados_balanceados(df_train, n_por_nivel=100, semilla=7)
    nivel_v = sim[sim["nivel_triaje"] == "V"]
    normal = (
        nivel_v["saturacion_o2"].between(96, 100)
        & nivel_v["frecuencia_cardiaca"].between(60, 100)
        & nivel_v["frecuencia_respiratoria"].between(12, 20)
        & nivel_v["temperatura"].between(36.0, 38.0)
        & nivel_v["presion_sistolica"].between(100, 140)
    )
    assert normal.all()


def test_rangos_fisiologicos_plausibles(df_train: pd.DataFrame) -> None:
    sim = generar_simulados_balanceados(df_train, n_por_nivel=80, semilla=11)
    for columna, (minimo, maximo) in _LIMITES.items():
        if columna in sim.columns:
            assert sim[columna].between(minimo, maximo).all(), f"{columna} fuera de rango"


def test_similitud_estadistica_con_entrenamiento(df_train: pd.DataFrame) -> None:
    """El promedio simulado debe quedar dentro de ~1σ del promedio real por
    nivel (excepto las columnas que las anclas clínicas re-escriben)."""
    sim = generar_simulados_balanceados(df_train, n_por_nivel=800, semilla=42)
    informe = resumen_similitud(df_train, sim)
    assert set(informe) == {"I", "II", "III", "IV", "V"}
    for nivel, desviaciones in informe.items():
        excluidas = {"I": _ANCLA_I, "V": _ANCLA_V}.get(nivel, set())
        for columna, desv in desviaciones.items():
            if columna in excluidas:
                continue
            assert desv <= 1.0, f"{nivel}/{columna} se desvía {desv}σ del train"


def test_bandas_clinicas_anclas_i_v(df_train: pd.DataFrame) -> None:
    """Distribución resultante de las anclas: I en zona de peligro, V normal."""
    sim = generar_simulados_balanceados(df_train, n_por_nivel=400, semilla=42)
    nivel_i = sim[sim["nivel_triaje"] == "I"]
    nivel_v = sim[sim["nivel_triaje"] == "V"]
    assert float(nivel_i["saturacion_o2"].mean()) <= 92
    assert float(nivel_i["frecuencia_cardiaca"].mean()) >= 115
    assert float(nivel_v["saturacion_o2"].mean()) >= 96
    assert 60 <= float(nivel_v["frecuencia_cardiaca"].mean()) <= 100
    assert float(nivel_v["presion_sistolica"].mean()) >= 100


def test_motivos_solo_del_vocabulario_de_entrenamiento(df_train: pd.DataFrame) -> None:
    sim = generar_simulados_balanceados(df_train, n_por_nivel=80, semilla=7)
    codigos_train = set(df_train["motivo_codigo_cie10"].dropna().astype(str))
    assert set(sim["motivo_codigo_cie10"]).issubset(codigos_train)
    assert sim["motivo_texto"].str.len().gt(0).all()
    # El texto simulado es idéntico a textos reales del train por nivel.
    for nivel in ["II", "III"]:
        textos_nivel = sim.loc[
            sim["nivel_triaje"] == nivel, "motivo_texto"
        ].to_numpy()
        assert np.isin(textos_nivel, df_train["motivo_texto"].to_numpy()).all()
