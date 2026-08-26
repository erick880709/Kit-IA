"""Pruebas del servicio de inferencia (TT-E4-01, HU-E4-01) y ENT-009."""

from __future__ import annotations

import json
from datetime import date

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Modelo, Paciente
from app.domain.exceptions import ValidationError
from app.services import triaje_service
from app.services.inference_service import InferenceService
from ml.src.data.ingesta import FuenteSinteticaDemo
from ml.src.evaluation.metrics import CLASES
from ml.src.features.feature_engineering import construir_matriz_estructurada
from ml.src.models.embeddings import VectorizadorTexto
from ml.src.models.late_fusion import LateFusionClassifier, PromedioPonderado
from ml.src.registry import serializar_paquete


@pytest.fixture(scope="module")
def dir_modelos(tmp_path_factory):
    """Empaqueta una fusión tardía (RF + LR texto) con las 5 clases."""
    destino = tmp_path_factory.mktemp("modelos")
    df = FuenteSinteticaDemo(n=300, semilla=3).generar()
    X_df, pipeline = construir_matriz_estructurada(df)
    X = X_df.to_numpy()
    n = len(X)
    y_enc = np.tile(np.arange(len(CLASES)), n // len(CLASES) + 1)[:n]
    sub_a = RandomForestClassifier(n_estimators=20, random_state=0).fit(X, y_enc)

    textos = pd.Series(df["motivo_texto"].fillna(""))
    vectorizador = VectorizadorTexto(max_features=60).fit(textos)
    X_txt = vectorizador.transformar(textos)
    sub_b = LogisticRegression(max_iter=1000).fit(X_txt, y_enc)
    modelo = LateFusionClassifier(sub_a, sub_b, PromedioPonderado(0.7), clases=CLASES)
    serializar_paquete(
        modelo=modelo,
        pipeline_estructurado=pipeline,
        vectorizador_texto=vectorizador,
        umbrales={c: 0.5 for c in CLASES},
        metricas={"macro": {"f1": 0.9}},
        nombre_algoritmo="rf-test",
        fecha=date(2026, 8, 14),
        destino=destino / "modelo-rf-test-v20260814.joblib",
    )
    return destino


def _datos_completos() -> dict:
    return {
        "temperatura": 38.9,
        "frecuencia_cardiaca": 121,
        "frecuencia_respiratoria": 30,
        "saturacion_o2": 86,
        "presion_sistolica": 98,
        "presion_diastolica": 62,
        "peso": 70.0,
        "talla": 1.7,
        "episodios_previos_urgencias": 2,
        "anio_nacimiento": 1980,
        "sexo": "Masculino",
        "via_llegada": "Ambulancia",
        "regimen": "subsidiado",
        "departamento": "Cundinamarca",
        "motivo_texto": "Dolor opresivo retroesternal de 2 horas",
    }


def test_predecir_con_modelo_cargado(dir_modelos):
    servicio = InferenceService(dir_modelos=dir_modelos)
    resultado = servicio.predecir(_datos_completos())
    assert resultado["estado"] == "ok"
    assert set(resultado["probabilidades"]) == set(CLASES)
    assert sum(resultado["probabilidades"].values()) == pytest.approx(1.0, abs=1e-3)
    assert resultado["nivel_sugerido"] in CLASES
    assert resultado["tiempo_ms"] < 3000  # RNF-007: presupuesto < 3 s
    assert resultado["version"] == "modelo-rf-test-v20260814"
    assert resultado["confianza"] > 0
    assert 1 <= len(resultado["explicacion"]) <= 5
    assert all("clinico" in item for item in resultado["explicacion"])


def test_predecir_indisponible_sin_artefacto(tmp_path):
    servicio = InferenceService(dir_modelos=tmp_path / "vacio")
    resultado = servicio.predecir(_datos_completos())
    assert resultado["estado"] == "indisponible"
    assert "motivo" in resultado


def test_predecir_proba_modelo_plano_sin_submodelo_texto():
    """Regresión (bug real 2026-08-14): un modelo plano (XGBoost/RF) recibía
    X_txt como 2º argumento posicional de predict_proba, que XGBoost interpreta
    como ntree_limit/validate_features → ValueError de array ambiguo → fallback
    manual. Debe predecir solo con features estructuradas."""
    rng = np.random.RandomState(0)
    modelo = RandomForestClassifier(n_estimators=10, random_state=0).fit(
        rng.rand(40, 5), np.tile(np.arange(5), 8)
    )
    X_est = rng.rand(2, 5)
    X_txt = rng.rand(2, 3)
    proba = InferenceService._predecir_proba(
        {"modelo": modelo, "version": "modelo-plano-v1"}, X_est, X_txt
    )
    assert proba.shape == (2, 5)
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_timeout_devuelve_fallback_sin_bloquear(dir_modelos, monkeypatch):
    """Debe corregirse resuelto: timeout → fallback y sin shutdown bloqueante."""
    import time

    servicio = InferenceService(dir_modelos=dir_modelos, timeout_s=0.0)
    # Determinístico: la inferencia nunca termina antes del timeout (evita la
    # carrera entre el hilo trabajador y future.result(timeout=0)).
    monkeypatch.setattr(
        servicio,
        "_predecir_proba",
        lambda *args, **kwargs: time.sleep(0.5),
    )
    inicio = time.perf_counter()
    for _ in range(3):
        resultado = servicio.predecir(_datos_completos())
        assert resultado["estado"] == "indisponible"
        assert resultado["motivo"] == "timeout"
    assert time.perf_counter() - inicio < 5, "shutdown no debe bloquear"


def test_vista_gestion_modelos_usa_el_singleton_recargable():
    """Regresión: activar modelo llamaba inference_service.recargar() sobre el
    MÓDULO (AttributeError). La vista debe importar el singleton."""
    from app.views import gestion_modelos

    assert callable(getattr(gestion_modelos.inference_service, "recargar", None))


def test_recargar_usa_modelo_activo_desde_bd(tmp_path, monkeypatch):
    """Bloqueante resuelto: el rollback de modelo invalida la caché."""
    # Dos artefactos distintos en el directorio temporal
    df = FuenteSinteticaDemo(n=200, semilla=5).generar()
    X_df, pipeline = construir_matriz_estructurada(df)
    X = X_df.to_numpy()
    n = len(X)
    y_enc = np.tile(np.arange(len(CLASES)), n // len(CLASES) + 1)[:n]
    for version in ("modelo-v1-test", "modelo-v2-test"):
        sub_a = RandomForestClassifier(n_estimators=10, random_state=0).fit(X, y_enc)
        serializar_paquete(
            modelo=sub_a, pipeline_estructurado=pipeline, vectorizador_texto=None,
            umbrales={c: 0.5 for c in CLASES}, metricas={"macro": {"f1": 0.8}},
            nombre_algoritmo=version.replace("modelo-", ""),
            fecha=date(2026, 8, 14),
            destino=tmp_path / f"{version}.joblib",
        )
    # BD en memoria con v1 activa
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        s.add(Modelo(version="modelo-v1-test", algoritmo="rf-test",
                     fecha_entrenamiento=date(2026, 8, 14), ruta_artefacto=str(
                         tmp_path / "modelo-v1-test.joblib"), activo=True))
        s.add(Modelo(version="modelo-v2-test", algoritmo="rf-test",
                     fecha_entrenamiento=date(2026, 8, 14), ruta_artefacto=str(
                         tmp_path / "modelo-v2-test.joblib"), activo=False))
        s.commit()
    monkeypatch.setattr("app.infra.db.SessionLocal", factory)

    servicio = InferenceService(dir_modelos=tmp_path)
    assert servicio.version == "modelo-v1-test-v20260814"
    # Rollback simulado: activa v2 y recarga
    with factory() as s:
        from app.services import modelo_service

        modelo_service.activar(s, version="modelo-v1-test", usuario_id="u-test")
        modelo_service.activar(s, version="modelo-v2-test", usuario_id="u-test")
    servicio.recargar()
    assert servicio.version == "modelo-v2-test-v20260814"


def test_normaliza_regimen_y_desconocidos(dir_modelos):
    servicio = InferenceService(dir_modelos=dir_modelos)
    fila = servicio._construir_fila({})
    assert fila["regimen"].iloc[0] == "Contributivo"
    assert fila["saturacion_o2"].iloc[0] == 0  # default numérico
    resultado = servicio.predecir(_datos_completos())
    assert resultado["estado"] == "ok"


# ---------- Robustez en Cloud (2026-08-26) ----------

def test_precalentar_carga_modelo_y_explainer(dir_modelos):
    servicio = InferenceService(dir_modelos=dir_modelos)
    assert servicio.precalentar() is True
    # Tras el precalentamiento la primera inferencia usa la caché caliente.
    resultado = servicio.predecir(_datos_completos())
    assert resultado["estado"] == "ok"
    assert servicio._explainer is not None


def test_precalentar_sin_artefacto_no_explota(tmp_path):
    servicio = InferenceService(dir_modelos=tmp_path / "vacio")
    assert servicio.precalentar() is False


def test_resolver_ruta_relativa_y_absoluta(tmp_path):
    modelo = tmp_path / "modelo-x.joblib"
    modelo.write_bytes(b"x")
    candidatas = [modelo]
    # Ruta relativa persistida (bug Cloud 2026-08-26): se resuelve contra el
    # directorio de modelos, sin depender del CWD.
    relativa = InferenceService._resolver_ruta(
        f"artifacts/models/{modelo.name}", candidatas, tmp_path
    )
    assert relativa == modelo
    # Ruta absoluta válida se usa tal cual.
    absoluta = InferenceService._resolver_ruta(str(modelo), candidatas, tmp_path)
    assert absoluta == modelo
    # Ruta que no existe → None (la inferencia degrada al más reciente).
    inexistente = InferenceService._resolver_ruta(
        "artifacts/models/no-existe.joblib", candidatas, tmp_path
    )
    assert inexistente is None


def test_predecir_reintenta_una_vez_tras_timeout(dir_modelos, monkeypatch):
    """Cloud gratuito: primer intento en contenedor frío puede exceder el
    presupuesto; un reintento único debe rescatar la inferencia."""
    import time

    servicio = InferenceService(dir_modelos=dir_modelos, timeout_s=0.2)
    llamadas = {"n": 0}

    def fake_proba(paquete, X_est, X_txt):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            time.sleep(0.6)  # primer intento lento (contenedor frío)
        proba = np.zeros((1, len(CLASES)))
        proba[0, 2] = 1.0
        return proba

    monkeypatch.setattr(servicio, "_predecir_proba", fake_proba)
    monkeypatch.setattr(servicio, "explicar", lambda fila: [])
    resultado = servicio.predecir(_datos_completos())
    assert resultado["estado"] == "ok"
    assert resultado["nivel_sugerido"] == "III"
    assert llamadas["n"] == 2


def test_artefacto_activo_vectorizador_tiene_cache() -> None:
    """Regresión Cloud 2026-08-26 (error_inferencia · vectorizacion_texto ·
    AttributeError '_cache'): el artefacto ganador del repositorio debe
    cargarse con un vectorizador funcional."""
    from pathlib import Path

    from ml.src import ARTIFACTS_MODELS
    from ml.src.registry import cargar_paquete

    candidatas = [
        p for p in sorted(ARTIFACTS_MODELS.glob("*.joblib"), key=lambda p: p.stat().st_mtime)
        if Path(str(p).replace(".joblib", ".manifest.json")).is_file()
    ]
    assert candidatas, "sin artefacto ganador en el repositorio"
    paquete = cargar_paquete(candidatas[-1])
    vectorizador = paquete["vectorizador_texto"]
    assert hasattr(vectorizador, "_cache")
    matriz = vectorizador.transformar(pd.Series(["MD30 Dolor torácico opresivo"]))
    assert matriz.shape[0] == 1 and matriz.shape[1] > 1000


def test_registrar_modelo_reactiva_version_inactiva(dir_modelos, session):
    """BD persistida de un despliegue anterior: si la versión existe pero
    quedó inactiva, registrar_modelo debe re-activarla."""
    servicio = InferenceService(dir_modelos=dir_modelos)
    session.add(Modelo(
        version="modelo-rf-test-v20260814", algoritmo="rf-test",
        fecha_entrenamiento=date(2026, 8, 14),
        ruta_artefacto=str(dir_modelos / "modelo-rf-test-v20260814.joblib"),
        activo=False,
    ))
    session.add(Modelo(
        version="otra-antigua", algoritmo="rf-test",
        fecha_entrenamiento=date(2026, 8, 10),
        ruta_artefacto=str(dir_modelos / "otra.joblib"), activo=True,
    ))
    session.commit()
    version = servicio.registrar_modelo(session)
    assert version == "modelo-rf-test-v20260814"
    filas = session.scalars(select(Modelo)).all()
    activas = [m.version for m in filas if m.activo]
    assert activas == ["modelo-rf-test-v20260814"]


def test_sincronizar_modelo_activo_corrige_activa_desactualizada(
    tmp_path, monkeypatch
):
    """El bootstrap sincroniza la fila activa con el artefacto más reciente
    (la BD de /tmp puede persistir entre despliegues en Cloud)."""
    df = FuenteSinteticaDemo(n=200, semilla=5).generar()
    X_df, pipeline = construir_matriz_estructurada(df)
    X = X_df.to_numpy()
    n = len(X)
    y_enc = np.tile(np.arange(len(CLASES)), n // len(CLASES) + 1)[:n]
    for version in ("modelo-v1-test", "modelo-v2-test"):
        sub_a = RandomForestClassifier(n_estimators=10, random_state=0).fit(X, y_enc)
        serializar_paquete(
            modelo=sub_a, pipeline_estructurado=pipeline, vectorizador_texto=None,
            umbrales={c: 0.5 for c in CLASES}, metricas={"macro": {"f1": 0.8}},
            nombre_algoritmo=version.replace("modelo-", ""),
            fecha=date(2026, 8, 14),
            destino=tmp_path / f"{version}.joblib",
        )
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        s.add(Modelo(version="modelo-v1-test-v20260814", algoritmo="rf-test",
                     fecha_entrenamiento=date(2026, 8, 14),
                     ruta_artefacto=str(tmp_path / "modelo-v1-test.joblib"),
                     activo=True))
        s.commit()
    monkeypatch.setattr("app.infra.db.SessionLocal", factory)
    servicio = InferenceService(dir_modelos=tmp_path)
    with factory() as s:
        servicio.sincronizar_modelo_activo(s)
        activas = [m.version for m in s.scalars(select(Modelo)).all() if m.activo]
    assert activas == ["modelo-v2-test-v20260814"]


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        yield s


def test_registrar_modelo_entidad_idempotente(dir_modelos, session):
    servicio = InferenceService(dir_modelos=dir_modelos)
    version = servicio.registrar_modelo(session)
    assert version == "modelo-rf-test-v20260814"
    servicio.registrar_modelo(session)  # idempotente
    modelos = session.scalars(select(Modelo)).all()
    assert len(modelos) == 1
    assert modelos[0].activo is True


def _resultado_ok() -> dict:
    return {
        "estado": "ok",
        "nivel_sugerido": "II",
        "probabilidades": {c: 0.2 for c in CLASES},
        "confianza": 0.2,
        "tiempo_ms": 45.6,
        "version": "modelo-rf-test-v20260814",
        "algoritmo": "rf-test",
        "explicacion": [{"feature": "saturacion_o2", "clinico": "saturación de O₂",
                         "impacto": 0.2, "peso_absoluto": 0.3}],
    }


def test_registrar_clasificacion_ia_persiste_metadatos(session):
    paciente = Paciente(
        tipo_documento="CC", numero_documento="555", nombres="Ana", apellidos="Pérez",
        fecha_nacimiento=date(1990, 1, 1), sexo="Femenino", via_llegada="Particular",
        contacto_emergencia="X", numero_contacto_emergencia="311",
        departamento="Cundinamarca", ciudad="Bogotá D.C.",
    )
    session.add(paciente)
    session.commit()
    evento = triaje_service.crear_evento(
        session, paciente_id=paciente.id, usuario_id="usr-1"
    )
    triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id="usr-1",
        datos={
            "temperatura": 38.0, "frecuencia_cardiaca": 110,
            "frecuencia_respiratoria": 26, "saturacion_o2": 88,
            "presion_sistolica": 105, "presion_diastolica": 70,
            "peso": 60.0, "talla": 1.6,
        },
    )
    triaje_service.registrar_evaluacion(
        session, evento_id=evento.id, usuario_id="usr-1",
        datos={
            "codigo_cie10": "R07.4",
            "descripcion_estructurada": "Dolor torácico",
            "escala_dolor": 6, "glasgow": 15, "nivel_conciencia": "Alerta",
        },
    )
    evento = triaje_service.registrar_clasificacion_ia(
        session, evento_id=evento.id, usuario_id="usr-1", resultado=_resultado_ok()
    )
    assert evento.nivel_sugerido_ia == "II"
    assert json.loads(evento.probabilidades_ia)["I"] == 0.2
    assert evento.version_modelo == "modelo-rf-test-v20260814"
    assert evento.tiempo_inferencia_ms == pytest.approx(45.6)
    assert evento.confianza_ia == pytest.approx(0.2)
    assert evento.fecha_inferencia is not None
    assert len(json.loads(evento.explicacion_shap)) == 1


def test_registrar_clasificacion_ia_rechaza_indisponible(session):
    paciente = Paciente(
        tipo_documento="CC", numero_documento="556", nombres="Luis", apellidos="Ríos",
        fecha_nacimiento=date(1995, 5, 5), sexo="Masculino", via_llegada="Remisión",
        contacto_emergencia="Y", numero_contacto_emergencia="312",
        departamento="Cundinamarca", ciudad="Bogotá D.C.",
    )
    session.add(paciente)
    session.commit()
    evento = triaje_service.crear_evento(
        session, paciente_id=paciente.id, usuario_id="usr-1"
    )
    with pytest.raises(ValidationError):
        triaje_service.registrar_clasificacion_ia(
            session, evento_id=evento.id, usuario_id="usr-1",
            resultado={"estado": "indisponible", "motivo": "timeout"},
        )
