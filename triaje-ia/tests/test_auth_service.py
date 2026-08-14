"""Pruebas del servicio de autenticación (HU-E1-01).

Cubren los criterios de aceptación CA2 (hash, nunca texto plano) y CA3
(bloqueo temporal tras 5 intentos fallidos).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Rol, Usuario
from app.domain.exceptions import (
    AutenticacionError,
    TokenInvalidoError,
    UsuarioBloqueadoError,
    ValidationError,
)
from app.infra.auth import hash_password, verify_password
from app.services import auth_service
from app.services.auth_service import autenticar, recuperar_contrasena, registrar_usuario

CORREO = "medico@hospital.gov.co"
PASSWORD = "Demo123!"


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        s.add(Rol(nombre="Medico"))
        s.commit()
        yield s


def test_ca2_password_nunca_en_texto_plano(session: Session) -> None:
    usuario = registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    assert usuario.password_hash != PASSWORD
    assert usuario.password_hash.startswith("$2")
    assert verify_password(PASSWORD, usuario.password_hash)
    # el hash de la utilidad coincide con el almacenado
    assert hash_password(PASSWORD) != usuario.password_hash  # salt aleatorio


def test_ca1_credenciales_validas_devuelven_usuario(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    usuario = autenticar(session, correo=CORREO, password=PASSWORD)
    assert usuario.correo == CORREO
    assert usuario.rol.nombre == "Medico"
    assert usuario.intentos_fallidos == 0


def test_correo_inexistente_rechaza(session: Session) -> None:
    with pytest.raises(AutenticacionError):
        autenticar(session, correo="nadie@hospital.gov.co", password=PASSWORD)


def test_password_incorrecta_incrementa_intentos(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    with pytest.raises(AutenticacionError) as exc1:
        autenticar(session, correo=CORREO, password="mala1")
    assert "4" in str(exc1.value.detalle)  # restan 4 de 5
    usuario = session.query(Usuario).filter_by(correo=CORREO).one()
    assert usuario.intentos_fallidos == 1


def test_ca3_bloqueo_temporal_tras_5_intentos(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    for _ in range(4):
        with pytest.raises(AutenticacionError):
            autenticar(session, correo=CORREO, password="mala")
    with pytest.raises(UsuarioBloqueadoError):
        autenticar(session, correo=CORREO, password="mala")

    usuario = session.query(Usuario).filter_by(correo=CORREO).one()
    assert usuario.bloqueado_hasta is not None
    # bloqueado: ni con la contraseña correcta
    with pytest.raises(UsuarioBloqueadoError):
        autenticar(session, correo=CORREO, password=PASSWORD)


def test_bloqueo_expirado_permite_reintento(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    for _ in range(5):
        with pytest.raises((AutenticacionError, UsuarioBloqueadoError)):
            autenticar(session, correo=CORREO, password="mala")
    usuario = session.query(Usuario).filter_by(correo=CORREO).one()
    usuario.bloqueado_hasta = datetime.now(UTC) - timedelta(minutes=20)
    session.commit()
    ok = autenticar(session, correo=CORREO, password=PASSWORD)
    assert ok.correo == CORREO


def test_correo_duplicado_rechaza(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Uno", rol_nombre="Medico"
    )
    with pytest.raises(ValidationError):
        registrar_usuario(
            session, correo=CORREO, password=PASSWORD, nombre="Dos", rol_nombre="Medico"
        )


def test_correo_normalizado_en_minusculas(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO.upper(), password=PASSWORD, nombre="X", rol_nombre="Medico"
    )
    assert session.query(Usuario).filter_by(correo=CORREO).one() is not None


# ---------- HU-E1-03: recuperación de contraseña ----------

def test_recuperacion_token_valido_cambia_password(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    token = auth_service.solicitar_recuperacion(session, correo=CORREO)
    assert token is not None

    recuperar_contrasena(
        session, correo=CORREO, token=token, nueva_password="NuevaClave123"
    )
    ok = autenticar(session, correo=CORREO, password="NuevaClave123")
    assert ok.correo == CORREO
    # el token quedó invalidado
    usuario = session.query(Usuario).filter_by(correo=CORREO).one()
    assert usuario.token_recuperacion is None


def test_recuperacion_token_un_solo_uso(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    token = auth_service.solicitar_recuperacion(session, correo=CORREO)
    recuperar_contrasena(session, correo=CORREO, token=token, nueva_password="NuevaClave123")
    with pytest.raises(TokenInvalidoError):
        recuperar_contrasena(
            session, correo=CORREO, token=token, nueva_password="OtraClave456"
        )


def test_recuperacion_token_expirado(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    token = auth_service.solicitar_recuperacion(session, correo=CORREO)
    usuario = session.query(Usuario).filter_by(correo=CORREO).one()
    usuario.token_expira = datetime.now(UTC) - timedelta(minutes=16)
    session.commit()
    with pytest.raises(TokenInvalidoError):
        recuperar_contrasena(
            session, correo=CORREO, token=token, nueva_password="NuevaClave123"
        )


def test_recuperacion_token_incorrecto(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    auth_service.solicitar_recuperacion(session, correo=CORREO)
    with pytest.raises(TokenInvalidoError):
        recuperar_contrasena(
            session, correo=CORREO, token="token-falso", nueva_password="NuevaClave123"
        )


def test_recuperacion_politica_minima_8(session: Session) -> None:
    registrar_usuario(
        session, correo=CORREO, password=PASSWORD, nombre="Medico Demo", rol_nombre="Medico"
    )
    token = auth_service.solicitar_recuperacion(session, correo=CORREO)
    with pytest.raises(ValidationError):
        recuperar_contrasena(session, correo=CORREO, token=token, nueva_password="corta")


def test_recuperacion_correo_inexistente_no_revela(session: Session) -> None:
    assert auth_service.solicitar_recuperacion(session, correo="nadie@hospital.gov.co") is None
