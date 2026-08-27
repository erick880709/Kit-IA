"""Tests de la pantalla de clasificación IA (UX de visitas anteriores)."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import EventoTriaje, Paciente
from app.views.clasificacion_ia import _mismo_paciente, _resultado_de_otro_evento


def test_resultado_de_otro_evento_detecta_visita_anterior() -> None:
    """El resultado almacenado de OTRO evento debe marcarse como visita
    anterior (2026-08-26): evita mostrar la recomendación vieja como si
    fuera la del triaje en curso."""
    resultado = {"estado": "ok"}
    assert _resultado_de_otro_evento(resultado, "ev-1", "ev-2") is True
    assert _resultado_de_otro_evento(resultado, "ev-1", "ev-1") is False


def test_resultado_sin_evento_asociado_se_trata_como_anterior() -> None:
    resultado = {"estado": "ok"}
    assert _resultado_de_otro_evento(resultado, None, "ev-1") is True
    assert _resultado_de_otro_evento(resultado, "ev-1", None) is True


def test_sin_resultado_no_es_visita_anterior() -> None:
    assert _resultado_de_otro_evento(None, None, "ev-1") is False
    assert _resultado_de_otro_evento(None, "ev-1", "ev-1") is False


def _paciente(numero: str, nombres: str, apellidos: str) -> Paciente:
    return Paciente(
        tipo_documento="CC",
        numero_documento=numero,
        nombres=nombres,
        apellidos=apellidos,
        fecha_nacimiento=date(1990, 1, 1),
        sexo="Femenino",
        via_llegada="Caminando",
        contacto_emergencia="Contacto",
        numero_contacto_emergencia="3000000000",
        departamento="Cundinamarca",
        ciudad="Bogotá D.C.",
    )


@pytest.fixture()
def session_eventos() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        pac_a = _paciente("9011000001", "Paciente A", "Prueba")
        pac_b = _paciente("9022000002", "Paciente B", "Prueba")
        s.add_all([pac_a, pac_b])
        s.flush()
        s.add_all(
            [
                EventoTriaje(paciente_id=pac_a.id),
                EventoTriaje(paciente_id=pac_a.id),
                EventoTriaje(paciente_id=pac_b.id),
            ]
        )
        s.commit()
        yield s


def _ids(session: Session) -> tuple[str, str, str]:
    pac_a = (
        session.query(Paciente)
        .filter(Paciente.numero_documento == "9011000001")
        .one()
    )
    pac_b = (
        session.query(Paciente)
        .filter(Paciente.numero_documento == "9022000002")
        .one()
    )
    de_a = (
        session.query(EventoTriaje)
        .filter(EventoTriaje.paciente_id == pac_a.id)
        .order_by(EventoTriaje.id)
        .all()
    )
    de_b = (
        session.query(EventoTriaje)
        .filter(EventoTriaje.paciente_id == pac_b.id)
        .one()
    )
    return de_a[0].id, de_a[1].id, de_b.id


def test_mismo_paciente_verifica_pertenencia_de_eventos(session_eventos: Session) -> None:
    """El resultado de OTRO paciente no debe mostrarse como visita anterior
    del paciente en curso (2026-08-27)."""
    a1, a2, b1 = _ids(session_eventos)
    assert _mismo_paciente(session_eventos, a1, a2) is True
    assert _mismo_paciente(session_eventos, a2, a1) is True
    assert _mismo_paciente(session_eventos, a1, b1) is False


def test_mismo_paciente_maneja_ids_inexistentes_o_nulos(session_eventos: Session) -> None:
    a1, _, _ = _ids(session_eventos)
    assert _mismo_paciente(session_eventos, a1, None) is False
    assert _mismo_paciente(session_eventos, None, None) is False
    assert _mismo_paciente(session_eventos, a1, "no-existe") is False


def test_claves_sesion_limpian_resultado_ia_al_cerrar_sesion() -> None:
    """El resultado de un paciente no debe filtrarse a la sesión de otro
    usuario: al cerrar sesión se elimina junto a su evento."""
    from app.main import CLAVES_SESION

    assert "resultado_ia" in CLAVES_SESION
    assert "resultado_ia_evento_id" in CLAVES_SESION
