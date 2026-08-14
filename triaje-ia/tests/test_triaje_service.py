"""Pruebas del flujo completo de triaje (HU-E2-02 a HU-E2-08)."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Auditoria, EventoTriaje, Paciente
from app.domain.exceptions import ValidationError
from app.services import history_connector, triaje_service

USUARIO = "usr-medico-1"


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        s.add(
            Paciente(
                tipo_documento="CC",
                numero_documento="52148903",
                nombres="María",
                apellidos="Gómez Ruiz",
                fecha_nacimiento=date(1986, 2, 12),
                sexo="Femenino",
                via_llegada="Ambulancia",
                contacto_emergencia="Carlos Gómez",
                numero_contacto_emergencia="3107654321",
                departamento="Cundinamarca",
                ciudad="Bogotá D.C.",
            )
        )
        s.commit()
        yield s


def _paciente_id(session: Session) -> str:
    return session.query(Paciente).one().id


def _signos(**overrides) -> dict:
    datos = {
        "temperatura": 36.8,
        "frecuencia_cardiaca": 88,
        "frecuencia_respiratoria": 16,
        "saturacion_o2": 88,
        "presion_sistolica": 120,
        "presion_diastolica": 80,
        "peso": 64.0,
        "talla": 1.62,
    }
    datos.update(overrides)
    return datos


def _evaluacion() -> dict:
    return {
        "codigo_cie10": "R07.4",
        "descripcion_estructurada": "Dolor torácico no especificado",
        "texto_libre": "Dolor opresivo desde hace 2 horas",
        "escala_dolor": 6,
        "glasgow": 15,
        "nivel_conciencia": "Alerta",
        "observaciones": "",
    }


def test_signos_invalidos_no_atan_el_evento_reintento(session):
    """Bloqueante resuelto: validar ANTES de transicionar permite reintentar."""
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    invalidos = dict(_signos(), temperatura=99.9)  # fuera de rango fisiológico
    with pytest.raises(ValidationError):
        triaje_service.registrar_signos(
            session, evento_id=evento.id, usuario_id=USUARIO, datos=invalidos
        )
    assert session.get(EventoTriaje, evento.id).estado == "Registrado"
    signos = triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    assert signos is not None
    assert session.get(EventoTriaje, evento.id).estado == "SignosVitales"


def test_signos_fuera_rango_exigen_confirmacion(session):
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    fuera = dict(_signos(), saturacion_o2=30)  # bajo el rango 50-100
    with pytest.raises(ValidationError):
        triaje_service.registrar_signos(
            session, evento_id=evento.id, usuario_id=USUARIO, datos=fuera
        )
    signos = triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=fuera,
        confirmar_fuera_rango=True,
    )
    assert signos.saturacion_o2 == 30


def _evento_cerrado(session: Session, nivel_ia: str = "III", nivel_prof: str = "III"):
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    triaje_service.registrar_evaluacion(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_evaluacion()
    )
    triaje_service.registrar_clasificacion_ia_simulada(
        session, evento_id=evento.id, nivel_sugerido=nivel_ia, usuario_id=USUARIO
    )
    triaje_service.validar_nivel_profesional(
        session,
        evento_id=evento.id,
        nivel_profesional=nivel_prof,
        usuario_id=USUARIO,
        motivo_discrepancia="riesgo vital" if nivel_ia != nivel_prof else None,
    )
    return triaje_service.cerrar_evento(session, evento_id=evento.id, usuario_id=USUARIO)


# ---------- HU-E2-06: máquina de estados ----------

def test_flujo_feliz_recorre_los_7_estados(session: Session) -> None:
    evento = _evento_cerrado(session)
    assert evento.estado == "Cerrado"
    assert evento.cierre is not None
    cambios = [
        r.detalle for r in session.query(Auditoria).all()
        if r.accion == "CAMBIO_ESTADO"
    ]
    assert len(cambios) == 5  # Registrado→Signos→Evaluación→Clasificación→Validación


def test_transicion_invalida_rechazada(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    with pytest.raises(ValidationError):
        triaje_service.transicionar_estado(
            session, evento_id=evento.id, nuevo_estado="ClasificacionIA", usuario_id=USUARIO
        )


def test_cierre_exige_clasificacion_ia(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    with pytest.raises(ValidationError):
        triaje_service.cerrar_evento(session, evento_id=evento.id, usuario_id=USUARIO)


# ---------- HU-E2-04: signos vitales ----------

def test_signos_imc_calculado_y_fuera_de_rango_rechazado(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    signos = triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    assert signos.imc == round(64.0 / (1.62**2), 1)

    evento2 = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    with pytest.raises(ValidationError):
        triaje_service.registrar_signos(
            session, evento_id=evento2.id, usuario_id=USUARIO,
            datos=_signos(temperatura=50.0),  # fuera de 34-43
        )


def test_talla_en_centimetros_se_convierte_para_imc(session: Session) -> None:
    """Regresión: talla digitada en cm (170) → 1.70 m para que el IMC no dé ≈ 0."""
    assert triaje_service.normalizar_talla_m(170.0) == (1.70, True)
    assert triaje_service.normalizar_talla_m(1.70) == (1.70, False)

    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    signos = triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos(talla=170)
    )
    assert signos.talla == 1.70
    assert signos.imc == round(64.0 / (1.70**2), 1)


# ---------- HU-E2-05: evaluación ----------

def test_evaluacion_texto_libre_vacio_no_bloquea(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    motivo, evaluacion = triaje_service.registrar_evaluacion(
        session,
        evento_id=evento.id,
        usuario_id=USUARIO,
        datos={**_evaluacion(), "texto_libre": ""},
    )
    assert motivo.texto_libre is None
    assert evaluacion.glasgow == 15


def test_evaluacion_escala_dolor_no_numerica_rechazada(session: Session) -> None:
    """Frontera externa: valor no numérico → ValidationError, nunca ValueError."""
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    with pytest.raises(ValidationError) as exc:
        triaje_service.registrar_evaluacion(
            session,
            evento_id=evento.id,
            usuario_id=USUARIO,
            datos=dict(_evaluacion(), escala_dolor="seis"),
        )
    assert exc.value.detalle == "escala_dolor"
    assert session.get(EventoTriaje, evento.id).estado == "SignosVitales"


def test_antecedentes_autorreporte_y_precarga_mockhce(session: Session) -> None:
    paciente_id = _paciente_id(session)
    triaje_service.guardar_antecedentes(
        session,
        paciente_id=paciente_id,
        antecedentes={"diabetes": True, "hta": False},
        usuario_id=USUARIO,
    )
    paciente = session.get(Paciente, paciente_id)
    previos = history_connector.history_connector.obtener_antecedentes(session, paciente)
    assert previos is not None and previos["diabetes"] is True


# ---------- HU-E2-08: validación y cierre ----------

def test_concordancia_calculada_y_motivo_obligatorio(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    triaje_service.registrar_signos(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_signos()
    )
    triaje_service.registrar_evaluacion(
        session, evento_id=evento.id, usuario_id=USUARIO, datos=_evaluacion()
    )
    triaje_service.registrar_clasificacion_ia_simulada(
        session, evento_id=evento.id, nivel_sugerido="III", usuario_id=USUARIO
    )
    # difieren sin motivo → error
    with pytest.raises(ValidationError):
        triaje_service.validar_nivel_profesional(
            session, evento_id=evento.id, nivel_profesional="II", usuario_id=USUARIO
        )
    # difieren con motivo → concordancia No
    evento = triaje_service.validar_nivel_profesional(
        session, evento_id=evento.id, nivel_profesional="II",
        usuario_id=USUARIO, motivo_discrepancia="riesgo vital",
    )
    assert evento.concordancia is False
    assert evento.motivo_discrepancia == "riesgo vital"


def test_concordancia_si(session: Session) -> None:
    evento = _evento_cerrado(session, nivel_ia="II", nivel_prof="II")
    assert evento.concordancia is True
    assert evento.motivo_discrepancia is None


# ---------- HU-E2-07: reclasificación ----------

def test_reclasificacion_solo_tras_cierre_y_como_evento_separado(session: Session) -> None:
    evento = _evento_cerrado(session)
    nuevo = triaje_service.reclasificar(
        session,
        evento_original_id=evento.id,
        nuevo_nivel="II",
        motivo="Deterioro respiratorio",
        usuario_id=USUARIO,
    )
    assert nuevo.id != evento.id
    assert nuevo.estado == "Reclasificado"
    assert nuevo.evento_anterior_id == evento.id
    assert nuevo.motivo_reclasificacion == "Deterioro respiratorio"
    # el evento original no se sobrescribe
    original = session.get(EventoTriaje, evento.id)
    assert original.nivel_asignado_profesional == "III"
    assert any(
        r.accion == "RECLASIFICACION" and "III → II" in r.detalle
        for r in session.query(Auditoria).all()
    )


def test_reclasificacion_antes_del_cierre_rechazada(session: Session) -> None:
    evento = triaje_service.crear_evento(
        session, paciente_id=_paciente_id(session), usuario_id=USUARIO
    )
    with pytest.raises(ValidationError):
        triaje_service.reclasificar(
            session, evento_original_id=evento.id, nuevo_nivel="II",
            motivo="x", usuario_id=USUARIO,
        )


# ---------- HU-E2-02 / HU-E2-03 ----------

def test_buscar_por_documento_exacto_y_parcial_por_nombre(session: Session) -> None:
    items, total = triaje_service.buscar_pacientes(session, termino="52148903")
    assert total == 1 and items[0].nombres == "María"
    items, total = triaje_service.buscar_pacientes(session, termino="góme")
    assert total == 1
    items, total = triaje_service.buscar_pacientes(session, termino="zzz")
    assert total == 0 and items == []


def test_historial_cronologico(session: Session) -> None:
    _evento_cerrado(session)
    _evento_cerrado(session)
    eventos = triaje_service.historial_eventos(
        session, paciente_id=_paciente_id(session)
    )
    assert len(eventos) == 2
    assert eventos[0].inicio >= eventos[1].inicio
