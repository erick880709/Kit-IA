"""Pruebas de RBAC (HU-E1-02)."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Auditoria, Rol, Usuario
from app.domain.exceptions import ProhibidoError
from app.services.authorization_service import (
    cambiar_rol_usuario,
    puede_acceder,
    verificar_acceso,
)


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        s.add_all([Rol(nombre="Medico"), Rol(nombre="Auditor")])
        s.flush()
        medico = Usuario(
            correo="m@hospital.gov.co",
            nombre="Medico",
            password_hash="x",
            rol_id=s.query(Rol).filter_by(nombre="Medico").one().id,
        )
        s.add(medico)
        s.commit()
        yield s


def test_ca1_cinco_roles_definidos() -> None:
    from app.domain.entities import ROLES_DEMO

    assert set(ROLES_DEMO) == {
        "Medico", "Enfermera", "Administrador", "Investigador", "Auditor"
    }


def test_ca2_medico_puede_registrar_paciente() -> None:
    assert puede_acceder("Medico", "registro_paciente") is True
    assert puede_acceder("Medico", "clasificacion_ia") is True


def test_ca2_auditor_solo_auditoria_y_dashboard() -> None:
    assert puede_acceder("Auditor", "auditoria") is True
    assert puede_acceder("Auditor", "dashboard") is True
    assert puede_acceder("Auditor", "registro_paciente") is False
    assert puede_acceder("Auditor", "clasificacion_ia") is False


def test_ca3_verificar_acceso_lanza_prohibido() -> None:
    with pytest.raises(ProhibidoError):
        verificar_acceso("Auditor", "registro_paciente")
    verificar_acceso("Medico", "registro_paciente")  # no lanza


def test_ca3_admin_roles_solo_administrador() -> None:
    assert puede_acceder("Administrador", "admin_roles") is True
    assert puede_acceder("Medico", "admin_roles") is False


def test_ca4_cambio_rol_queda_auditado(session: Session) -> None:
    session.add(Rol(nombre="Investigador"))
    session.commit()
    usuario = session.query(Usuario).filter_by(correo="m@hospital.gov.co").one()
    admin_id = usuario.id

    cambiar_rol_usuario(
        session, usuario_id=usuario.id, nuevo_rol="Investigador", admin_id=admin_id
    )
    registros = session.query(Auditoria).all()
    assert any(r.accion == "CAMBIO_ROL" and "Medico → Investigador" in r.detalle for r in registros)
    assert usuario.rol.nombre == "Investigador"
