"""Pruebas de auditoría y trazabilidad (TT-E5-01, HU-E5-01, HU-E5-02)."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import (
    Auditoria,
    EventoTriaje,
    MotivoConsulta,
    Paciente,
    SignosVitales,
)
from app.services import audit_service, registro_pdf
from app.services.audit_service import AuditoriaProtegidaError


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        yield s


# ---------- TT-E5-01 · append-only + decorador ----------

def test_auditoria_append_only_rechaza_update_y_delete(session):
    registro = audit_service.registrar(
        session, usuario_id="u1", accion="PRUEBA", entidad="Test"
    )
    with pytest.raises(AuditoriaProtegidaError):
        registro.accion = "ALTERADA"
        session.commit()
    session.rollback()
    with pytest.raises(AuditoriaProtegidaError):
        session.delete(registro)
        session.commit()
    session.rollback()
    assert session.get(Auditoria, registro.id) is not None


def test_decorador_auditar_registra_accion(session):
    @audit_service.auditar("OPERACION_PRUEBA", "EntidadPrueba")
    def servicio(session, *, usuario_id):
        return {"ok": True}

    servicio(session, usuario_id="u2")
    filas, total = audit_service.consultar(
        session, accion="OPERACION_PRUEBA", usuario_id="u2"
    )
    assert total == 1
    assert filas[0].entidad == "EntidadPrueba"


def test_decorador_auditar_con_detalle_calculado(session):
    @audit_service.auditar(
        "OPERACION_DETALLE", "Entidad",
        detalle=lambda resultado, *args, **kwargs: f"hecho={resultado['ok']}",
    )
    def servicio(session, *, usuario_id):
        return {"ok": False}

    servicio(session, usuario_id="u3")
    filas, _ = audit_service.consultar(session, accion="OPERACION_DETALLE")
    assert "hecho=False" in filas[0].detalle


# ---------- HU-E5-01 · consulta y exportación ----------

def _sembrar(session, n=6):
    base = datetime.now(UTC).replace(tzinfo=None)
    for i in range(n):
        audit_service.registrar(
            session,
            usuario_id=f"u{i % 3}",
            accion="ACCION_A" if i % 2 == 0 else "ACCION_B",
            entidad="EventoTriaje" if i % 3 else "Paciente",
            detalle=f"registro {i}",
            evento_id=f"ev-{i % 2}",
        )
    return base


def test_consultar_filtros_ca1(session):
    _sembrar(session)
    filas, total = audit_service.consultar(session, accion="ACCION_A")
    assert total == 3
    filas, total = audit_service.consultar(session, usuario_id="u1")
    assert total == 2
    filas, total = audit_service.consultar(session, entidad="Paciente")
    assert total == 2
    filas, total = audit_service.consultar(session, evento_id="ev-1")
    assert total == 3
    for f in filas:
        assert f.evento_id == "ev-1"


def test_consultar_rango_fechas_y_paginacion(session):
    _sembrar(session)
    ahora = datetime.now(UTC).replace(tzinfo=None)
    filas, total = audit_service.consultar(
        session, desde=ahora - timedelta(days=1), hasta=ahora + timedelta(days=1),
        page=1, page_size=4,
    )
    assert total == 6 and len(filas) == 4
    filas, total = audit_service.consultar(session, desde=ahora + timedelta(days=2))
    assert total == 0


def test_exportar_formatos(session):
    _sembrar(session, n=3)
    filas, _ = audit_service.consultar(session)
    csv_bytes, nombre = audit_service.exportar(filas, formato="csv")
    assert nombre == "auditoria.csv" and csv_bytes.startswith(b"\xef\xbb\xbf")
    xlsx_bytes, nombre = audit_service.exportar(filas, formato="excel")
    assert nombre == "auditoria.xlsx" and xlsx_bytes[:2] == b"PK"
    pdf_bytes, nombre = audit_service.exportar(filas, formato="pdf", filtros="accion=A")
    assert nombre == "auditoria.pdf" and pdf_bytes.startswith(b"%PDF")
    with pytest.raises(ValueError):
        audit_service.exportar(filas, formato="json")


# ---------- HU-E5-02 · PDF normativo anonimizado ----------

def _evento_y_paciente():
    paciente = Paciente(
        id="p-1",
        tipo_documento="CC",
        numero_documento="53012487",
        nombres="Andrea",
        apellidos="López Sandoval",
        fecha_nacimiento=date(1990, 5, 12),
        sexo="Femenino",
        via_llegada="Ambulancia",
        contacto_emergencia="Juan López",
        numero_contacto_emergencia="3101112233",
        departamento="Cundinamarca",
        ciudad="Bogotá D.C.",
    )
    evento = EventoTriaje(
        id="ev-pdf-1",
        paciente_id="p-1",
        estado="Cerrado",
        nivel_sugerido_ia="II",
        nivel_asignado_profesional="II",
        concordancia=True,
        version_modelo="modelo-latefusion-xgb-text-sjd-v20260814",
        algoritmo_modelo="latefusion-xgb-text-sjd",
        confianza_ia=0.8005,
        tiempo_inferencia_ms=5.92,
        inicio=datetime.now(UTC),
        cierre=datetime.now(UTC),
        explicacion_shap=json.dumps(
            [
                {"feature": "saturacion_o2", "clinico": "saturacion de O2",
                 "impacto": 1.79, "peso_absoluto": 1.79},
            ]
        ),
    )
    signos = SignosVitales(
        id="sv-1", evento_id="ev-pdf-1", temperatura=38.9,
        frecuencia_cardiaca=121, frecuencia_respiratoria=30, saturacion_o2=86,
        presion_sistolica=98, presion_diastolica=62, peso=64.0, talla=1.62, imc=24.4,
    )
    motivo = MotivoConsulta(
        id="m-1", evento_id="ev-pdf-1", codigo_cie10="R07.4",
        descripcion_estructurada="Dolor toracico", texto_libre="Dolor opresivo",
    )
    return evento, paciente, signos, motivo


def test_pdf_anonimizado_sin_identificadores_directos():
    evento, paciente, signos, motivo = _evento_y_paciente()
    pdf = registro_pdf.generar_pdf_registro(evento, paciente, signos, motivo)
    assert pdf.startswith(b"%PDF")
    assert b"53012487" not in pdf  # documento completo ausente (CA3)
    assert b"3101112233" not in pdf  # teléfono ausente (CA3)
    assert b"Andrea S." in pdf  # iniciales (seudonimización)
    assert b"Variables de mayor peso" in pdf  # SHAP presente (CA1)
    assert b"Resoluci" in pdf  # normativa colombiana
    assert b"saturacion de O2" in pdf  # variable SHAP en lenguaje clínico


def test_pdf_sin_explicacion_shap_no_falla():
    evento, paciente, signos, motivo = _evento_y_paciente()
    evento.explicacion_shap = None
    pdf = registro_pdf.generar_pdf_registro(evento, paciente, signos, motivo)
    assert pdf.startswith(b"%PDF")
