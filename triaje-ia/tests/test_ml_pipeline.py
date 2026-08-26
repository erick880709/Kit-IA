"""Pruebas del pipeline ML (Épica E3) — TT-E3-01/02/04/05/06/07/08/09.

Ejecutar desde triaje-ia con PYTHONPATH=triaje-ia.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from ml.src.data.anonimizacion import anonimizar
from ml.src.data.ingesta import (
    FuenteSinteticaDemo,
    generar_datos_sinteticos,
    generar_refuerzo_iv,
    ingestar_san_juan_de_dios,
)
from ml.src.evaluation.metrics import (
    CLASES,
    metricas_por_clase,
    verificar_metas,
)
from ml.src.evaluation.shap_explain import explicar_shap
from ml.src.features.feature_engineering import construir_matriz_estructurada
from ml.src.features.limpieza import LimpiezaOutliers, NormalizadorRegimen, ValidadorCalidad
from ml.src.models.baselines import entrenar_baselines
from ml.src.models.early_fusion import entrenar_early_fusion
from ml.src.models.embeddings import vectorizar_texto
from ml.src.models.late_fusion import LateFusionClassifier, PromedioPonderado, entrenar_late_fusion
from ml.src.models.thresholds import ajustar_umbrales, aplicar_umbrales, sugerir_nivel
from ml.src.registry import cargar_paquete, serializar_paquete


@pytest.fixture(scope="module")
def df_demo() -> pd.DataFrame:
    return FuenteSinteticaDemo(n=900, semilla=7).generar()


@pytest.fixture(scope="module")
def df_preparado(df_demo: pd.DataFrame) -> pd.DataFrame:
    df = anonimizar(df_demo)
    df = ValidadorCalidad.validar(df)
    df = NormalizadorRegimen.normalizar(df)
    numericas = [
        "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
        "saturacion_o2", "presion_sistolica", "presion_diastolica", "peso", "talla",
    ]
    return LimpiezaOutliers([c for c in numericas if c in df.columns]).fit_transform(df)


# ---------- TT-E3-01 · Ingesta + anonimización ----------

def test_fuente_sintetica_calibrada(df_demo):
    assert len(df_demo) == 900
    distribucion = df_demo["nivel_triaje"].value_counts(normalize=True)
    assert distribucion["III"] > 0.7  # clase mayoritaria dominante (RNF-004)
    assert distribucion.get("I", 0.0) < 0.05


def test_anonimizacion_hash_identificadores(df_demo):
    antes = df_demo.copy()
    salida = anonimizar(df_demo)
    assert "numero_documento" in salida.columns
    assert "fecha_nacimiento" not in salida.columns  # generalizada a año
    assert "anio_nacimiento" in salida.columns
    assert salida["numero_documento"].nunique() == len(salida)  # hash 1:1
    assert not any(str(v).isdigit() and len(str(v)) == 12 for v in salida["numero_documento"])
    # no muta la entrada
    assert antes["numero_documento"].iloc[0] == df_demo["numero_documento"].iloc[0]


def test_generar_datos_sinteticos_persiste():
    ruta = generar_datos_sinteticos(n=50, semilla=11)
    assert ruta.exists()
    df = pd.read_csv(ruta)
    assert len(df) >= 50  # idempotente: no sobreescribe el demo de 4000


def test_refuerzo_iv_perfiles_discriminativos() -> None:
    ref = generar_refuerzo_iv(n_i=40, n_v=40, semilla=7)
    assert len(ref) == 80
    assert set(ref["nivel_triaje"]) == {"I", "V"}
    i_rows = ref[ref["nivel_triaje"] == "I"]
    v_rows = ref[ref["nivel_triaje"] == "V"]
    assert i_rows["saturacion_o2"].max() < 85
    assert i_rows["frecuencia_cardiaca"].min() >= 140
    assert v_rows["saturacion_o2"].min() >= 98
    assert v_rows["frecuencia_cardiaca"].max() <= 80
    # códigos CIE-11 del catálogo
    from app.domain.catalogos import CATALOGO_MOTIVOS

    codigos = {c for c, _, _ in CATALOGO_MOTIVOS}
    assert set(ref["motivo_codigo_cie10"]) <= codigos
    # columnas mínimas para el pipeline
    for col in ("temperatura", "frecuencia_respiratoria", "presion_sistolica",
                "motivo_texto", "sexo", "via_llegada", "regimen"):
        assert col in ref.columns


def test_ingesta_san_juan_de_dios_mapea_columnas(tmp_path):
    csv = tmp_path / "sjd.csv"
    pd.DataFrame(
        {
            "triage": ["III", "I", "II"],
            "codigo de diagnostico": ["R104", "R074", "J189"],
            "diagnostico": ["Dolor abdominal", "Dolor torácico", "Neumonía"],
            "eps o ips": ["Hospital / EPS A"] * 3,
            "fecha": ["03/21/2023"] * 3,
            "hora de entrada": ["01:53:00 PM"] * 3,
            "hora de salida": ["10:29:00 PM"] * 3,
            "edad": ["24 AÑOS", "80 AÑOS", "35 AÑOS"],
            "año": [2023, 2023, 2358],  # último año corrupto → anio NaN
        }
    ).to_csv(csv, index=False)
    salida = ingestar_san_juan_de_dios(csv)
    assert list(salida["nivel_triaje"]) == ["III", "I", "II"]
    assert salida["motivo_codigo_cie10"].iloc[0] == "R104"
    assert salida["anio_nacimiento"].iloc[0] == pytest.approx(1999.0)
    assert pd.isna(salida["anio_nacimiento"].iloc[2])
    assert "eps o ips" not in salida.columns  # identificador descartado


def test_late_fusion_classifier_combina_submodelos():
    rng = np.random.default_rng(4)
    n = 60
    X_est = rng.normal(size=(n, 4))
    X_txt = rng.normal(size=(n, 6))
    y = np.tile(np.arange(len(CLASES)), n // len(CLASES) + 1)[:n]
    sub_a = RandomForestClassifier(n_estimators=10, random_state=0).fit(X_est, y)
    from sklearn.linear_model import LogisticRegression

    sub_b = LogisticRegression(max_iter=500).fit(X_txt, y)
    ganador = LateFusionClassifier(sub_a, sub_b, PromedioPonderado(0.7), clases=CLASES)
    proba = ganador.predict_proba(X_est[:5], X_txt[:5])
    assert proba.shape == (5, 5)
    assert np.allclose(proba.sum(axis=1), 1.0)
    # sin texto → probabilidad neutra en el submodelo b
    proba_sin_texto = ganador.predict_proba(X_est[:5])
    assert proba_sin_texto.shape == (5, 5)


# ---------- TT-E3-02 · Limpieza ----------

def test_validador_calidad_invalida_fuera_de_rango():
    df = pd.DataFrame(
        {"temperatura": [36.5, 99.9, 45.0], "saturacion_o2": [95, 150, 98],
         "via_llegada": ["Ambulancia", "Helicoptero", "Particular"]}
    )
    salida = ValidadorCalidad.validar(df)
    assert pd.isna(salida.loc[1, "temperatura"])
    assert pd.isna(salida.loc[1, "saturacion_o2"])
    assert pd.isna(salida.loc[1, "via_llegada"])


def test_normalizador_regimen_typos_rt006():
    df = pd.DataFrame({"regimen": ["contributivo", "SUBSIDIADO.", "subsidiado", "X"]})
    salida = NormalizadorRegimen.normalizar(df)
    assert salida["regimen"].tolist()[:3] == ["Contributivo", "Subsidiado", "Subsidiado"]


def test_limpieza_outliers_imputa_mediana():
    df = pd.DataFrame({"peso": [70.0, np.nan, 5000.0]})
    salida = LimpiezaOutliers(["peso"]).fit_transform(df)
    assert not salida["peso"].isna().any()
    assert salida["peso"].max() < 5000  # outlier recortado
    assert salida["peso"].min() >= 70.0  # mediana imputada


# ---------- TT-E3-02/03 · Features + embeddings ----------

def test_matriz_estructurada_sin_nan(df_preparado):
    X, pipeline = construir_matriz_estructurada(df_preparado)
    assert X.shape[0] == len(df_preparado)
    assert not X.isna().any().any()
    assert X.shape[1] > 5


def test_vectorizador_texto_vacio_no_bloquea():
    df = pd.DataFrame({"motivo_texto": ["", "", ""]})
    matriz, vectorizador = vectorizar_texto(df, max_features=50)
    assert matriz is None and vectorizador is None  # RF-NLP-004


def test_vectorizador_texto_cache(df_preparado):
    matriz, vectorizador = vectorizar_texto(df_preparado, max_features=80)
    assert matriz is not None and vectorizador is not None
    assert matriz.shape[0] == len(df_preparado)


# ---------- TT-E3-04/05/06 · Modelos ----------

@pytest.fixture(scope="module")
def datos_modelo(df_preparado):
    X_df, pipeline = construir_matriz_estructurada(df_preparado)
    X = X_df.to_numpy()
    y = df_preparado["nivel_triaje"].to_numpy()
    return X, y, pipeline


def test_baselines_cv_completo(datos_modelo, tmp_path, monkeypatch):
    # Los entrenamientos de prueba NUNCA deben sobrescribir las métricas reales
    # de artifacts/metrics/ (LNN-006).
    monkeypatch.setattr("ml.src.evaluation.metrics.ARTIFACTS_METRICS", tmp_path)
    X, y, _ = datos_modelo
    resultados = entrenar_baselines(X, y, k_folds=3)
    assert set(resultados) == {"regresion_logistica", "random_forest", "xgboost"}
    for _nombre, res in resultados.items():
        for k in ("precision", "recall", "f1"):
            assert 0.0 <= res["macro_cv"][k] <= 1.0
    assert (tmp_path / "baseline_xgboost.json").exists()


def test_early_fusion_metricas(datos_modelo, tmp_path, monkeypatch):
    monkeypatch.setattr("ml.src.evaluation.metrics.ARTIFACTS_METRICS", tmp_path)
    X, y, _ = datos_modelo
    X_txt, _ = vectorizar_texto(
        pd.DataFrame({"motivo_texto": [""] * len(y)}), max_features=50
    )
    res = entrenar_early_fusion(X, y, X_txt, k_folds=3)
    assert 0.0 <= res["macro_cv"]["f1"] <= 1.0
    assert (tmp_path / "early_fusion.json").exists()


def test_late_fusion_combinadores(datos_modelo, tmp_path, monkeypatch):
    monkeypatch.setattr("ml.src.evaluation.metrics.ARTIFACTS_METRICS", tmp_path)
    X, y, _ = datos_modelo
    X_txt, _ = vectorizar_texto(
        pd.DataFrame({"motivo_texto": [""] * len(y)}), max_features=50
    )
    res = entrenar_late_fusion(X, y, X_txt, k_folds=3,
                               combinadores=("promedio_ponderado", "stacking"))
    assert set(res) == {"promedio_ponderado", "stacking"}
    for _nombre, macro in res.items():
        assert 0.0 <= macro["f1"] <= 1.0
    assert (tmp_path / "late_fusion_stacking.json").exists()


# ---------- TT-E3-07 · Umbrales ----------

def test_umbrales_priorizan_recall_i_ii():
    rng = np.random.default_rng(0)
    y = np.array(["I"] * 100 + ["II"] * 100 + ["III"] * 600)
    proba = np.zeros((len(y), 5))
    for i, _c in enumerate(CLASES):
        proba[:, i] = rng.uniform(0.01, 0.99, len(y))
    proba[np.arange(len(y)), np.searchsorted(CLASES, y)] += 0.3
    proba = proba / proba.sum(axis=1, keepdims=True)
    umbrales = ajustar_umbrales(y, proba)
    assert all(0.01 <= u <= 0.99 for u in umbrales.values())
    pred = aplicar_umbrales(proba, umbrales)
    assert set(CLASES[i] for i in pred) <= set(CLASES)


def test_sugerir_nivel_respeta_umbrales():
    probas = {"I": 0.01, "II": 0.10, "III": 0.70, "IV": 0.15, "V": 0.04}
    umbrales = {"I": 0.5, "II": 0.15, "III": 0.5, "IV": 0.5, "V": 0.5}
    # ratios: II=0.67, III=1.40 → gana III
    assert sugerir_nivel(probas, umbrales) == "III"
    # con proba II=0.22 → ratio 1.467 > 1.40 → gana II
    assert sugerir_nivel(dict(probas, II=0.22), umbrales) == "II"


# ---------- TT-E3-08 · SHAP + métricas ----------

def test_explicar_shap_top5_lenguaje_clinico():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(80, 6))
    y = rng.integers(0, 5, 80)
    modelo = RandomForestClassifier(n_estimators=20, random_state=0).fit(X, y)
    expl = explicar_shap(modelo, X, nombres_features=["spo2", "fr", "temp", "pas", "edad", "via"])
    assert len(expl["top"]) == 5
    assert all("clinico" in item and item["peso_absoluto"] >= 0 for item in expl["top"])


def test_metricas_por_clase_y_metas():
    y_true = np.array(["III"] * 90 + ["II"] * 10)
    y_pred = np.array(["III"] * 95 + ["II"] * 5)
    proba = np.zeros((100, 5))
    proba[:, CLASES.index("III")] = 0.9
    proba[:, CLASES.index("II")] = 0.1
    m = metricas_por_clase(y_true, y_pred, proba)
    assert set(m["por_clase"]) == set(CLASES)
    assert 0.0 <= m["macro"]["f1"] <= 1.0
    metas = verificar_metas(m)
    assert isinstance(metas["f1"], bool)


# ---------- TT-E3-09 · Serialización ----------

def test_serializar_y_cargar_paquete(tmp_path):
    rng = np.random.default_rng(2)
    X = rng.normal(size=(100, 5))
    y = rng.integers(0, 5, 100)
    modelo = RandomForestClassifier(n_estimators=10, random_state=0).fit(X, y)
    umbrales = {c: 0.5 for c in CLASES}
    ruta = serializar_paquete(
        modelo=modelo, pipeline_estructurado=None, vectorizador_texto=None,
        umbrales=umbrales, metricas={"macro": {"f1": 0.8}},
        nombre_algoritmo="test", fecha=__import__("datetime").date(2026, 1, 1),
        destino=tmp_path / "test_modelo.joblib",
    )
    assert ruta.exists()
    paquete = cargar_paquete(ruta)
    assert paquete["modelo"] is not None
    assert paquete["umbrales"] == umbrales
    # predicción consistente tras recarga
    assert np.array_equal(
        modelo.predict(X), paquete["modelo"].predict(X)
    )


def test_cargar_paquete_detecta_corrupcion(tmp_path):
    rng = np.random.default_rng(3)
    X = rng.normal(size=(20, 4))
    y = rng.integers(0, 5, 20)
    modelo = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    ruta = serializar_paquete(
        modelo=modelo, pipeline_estructurado=None, vectorizador_texto=None,
        umbrales={c: 0.5 for c in CLASES}, metricas={},
        nombre_algoritmo="corrupto", fecha=__import__("datetime").date(2026, 1, 1),
        destino=tmp_path / "corrupto.joblib",
    )
    (tmp_path / "corrupto.manifest.json").write_text('{"sha256_16": "0000"}')
    with pytest.raises(ValueError):
        cargar_paquete(ruta)


def test_cargar_paquete_verifica_hash_antes_de_deserializar(tmp_path, monkeypatch):
    """BLOQUEANTE Muralla: joblib.load deserializa pickle (ejecuta código).

    Con un hash de manifiesto inválido, `joblib.load` no debe ejecutarse
    jamás: la verificación de integridad ocurre ANTES de deserializar.
    """
    ruta = tmp_path / "malicioso.joblib"
    ruta.write_bytes(b"\x80\x04contenido-sin-verificar")
    (tmp_path / "malicioso.manifest.json").write_text(
        '{"version": "malicioso", "sha256_16": "0000"}'
    )
    llamadas: list = []

    def _load_prohibido(p):
        llamadas.append(p)
        raise AssertionError("joblib.load no debe ejecutarse con hash inválido")

    monkeypatch.setattr("ml.src.registry.joblib.load", _load_prohibido)
    with pytest.raises(ValueError):
        cargar_paquete(ruta)
    assert llamadas == []


def test_cargar_paquete_rechaza_artefacto_sin_manifiesto(tmp_path):
    """Fail-closed: sin manifiesto no hay procedencia verificable → se rechaza."""
    ruta = tmp_path / "huerfano.joblib"
    ruta.write_bytes(b"\x80\x04datos-sin-manifiesto")
    with pytest.raises(ValueError):
        cargar_paquete(ruta)


def test_serializar_paquete_escribe_manifiesto_junto_al_artefacto(tmp_path):
    """El manifiesto viaja junto al artefacto, en el mismo directorio.

    Antes se escribía SIEMPRE en artifacts/models aunque el destino fuera
    otro directorio — la verificación de hash quedaba ciega en esos casos.
    """
    rng = np.random.default_rng(4)
    X = rng.normal(size=(20, 4))
    y = rng.integers(0, 5, 20)
    modelo = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    destino = tmp_path / "aislado" / "modelo.joblib"
    ruta = serializar_paquete(
        modelo=modelo, pipeline_estructurado=None, vectorizador_texto=None,
        umbrales={c: 0.5 for c in CLASES}, metricas={},
        nombre_algoritmo="aislado", fecha=__import__("datetime").date(2026, 1, 1),
        destino=destino,
    )
    assert (tmp_path / "aislado" / "modelo.manifest.json").is_file()
    paquete = cargar_paquete(ruta)
    assert paquete["modelo"] is not None
