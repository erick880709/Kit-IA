"""Servicio de autenticación (HU-E1-01) y recuperación de contraseña (HU-E1-03).

Reglas:
- Contraseñas solo con hash bcrypt (HU-E1-01 CA2), nunca texto plano.
- Bloqueo temporal tras N intentos fallidos (HU-E1-01 CA3: 5 intentos).
- Recuperación con token de un solo uso y expiración (HU-E1-03 CA2: 15 min).
- La sesión por inactividad la implementa HU-E1-04 (session_service).
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Rol, Usuario
from app.domain.exceptions import (
    AutenticacionError,
    TokenInvalidoError,
    UsuarioBloqueadoError,
    ValidationError,
)
from app.infra.auth import hash_password, verify_password
from app.infra.config import settings

logger = logging.getLogger(__name__)


def registrar_usuario(
    session: Session, *, correo: str, password: str, nombre: str, rol_nombre: str
) -> Usuario:
    """Crea un usuario con contraseña hasheada. Lanza ValidationError si el
    correo ya existe o el rol no está registrado."""
    correo_norm = correo.strip().lower()
    if not correo_norm or "@" not in correo_norm:
        raise ValidationError("Correo institucional inválido")
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres")

    existente = session.scalar(select(Usuario).where(Usuario.correo == correo_norm))
    if existente is not None:
        raise ValidationError("Ya existe un usuario con ese correo", detalle=correo_norm)

    rol = session.scalar(select(Rol).where(Rol.nombre == rol_nombre))
    if rol is None:
        raise ValidationError("Rol inexistente", detalle=rol_nombre)

    usuario = Usuario(
        correo=correo_norm,
        nombre=nombre.strip(),
        password_hash=hash_password(password),
        rol_id=rol.id,
    )
    session.add(usuario)
    session.commit()
    return usuario


def autenticar(session: Session, *, correo: str, password: str) -> Usuario:
    """Valida credenciales aplicando bloqueo por intentos fallidos.

    Lanza AutenticacionError si las credenciales son inválidas o el usuario
    está inactivo, y UsuarioBloqueadoError si el bloqueo temporal sigue vigente.
    """
    correo_norm = correo.strip().lower()
    usuario = session.scalar(select(Usuario).where(Usuario.correo == correo_norm))
    if usuario is None:
        logger.warning("Login fallido: correo inexistente %s", correo_norm)
        raise AutenticacionError("Credenciales incorrectas")

    if not usuario.activo:
        logger.warning("Login rechazado: usuario inactivo %s", correo_norm)
        raise AutenticacionError("Usuario inactivo — contacte al administrador")

    ahora = datetime.now(UTC)
    if usuario.bloqueado_hasta is not None:
        if usuario.bloqueado_hasta.tzinfo is None:  # naive por SQLite
            bloqueado = usuario.bloqueado_hasta.replace(tzinfo=UTC)
        else:
            bloqueado = usuario.bloqueado_hasta
        if bloqueado > ahora:
            minutos = int((bloqueado - ahora).total_seconds() // 60) + 1
            logger.warning(
                "Login rechazado: bloqueo temporal vigente para %s (%d min)",
                correo_norm, minutos,
            )
            raise UsuarioBloqueadoError(
                f"Cuenta bloqueada temporalmente — reintente en {minutos} min",
                detalle=str(bloqueado),
            )

    if not verify_password(password, usuario.password_hash):
        usuario.intentos_fallidos += 1
        if usuario.intentos_fallidos >= settings.max_intentos_login:
            usuario.bloqueado_hasta = ahora + timedelta(minutes=settings.bloqueo_login_min)
            usuario.intentos_fallidos = 0
            session.commit()
            logger.warning(
                "Cuenta bloqueada por intentos fallidos: %s (%d min)",
                correo_norm, settings.bloqueo_login_min,
            )
            raise UsuarioBloqueadoError(
                f"Demasiados intentos fallidos — cuenta bloqueada por "
                f"{settings.bloqueo_login_min} minutos"
            )
        session.commit()
        restantes = settings.max_intentos_login - usuario.intentos_fallidos
        logger.warning(
            "Login fallido (contraseña incorrecta): %s — intentos restantes %d",
            correo_norm, restantes,
        )
        raise AutenticacionError(
            "Credenciales incorrectas", detalle=f"Intentos restantes: {restantes}"
        )

    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    session.commit()
    logger.info("Login exitoso: %s", correo_norm)
    return usuario


def solicitar_recuperacion(session: Session, *, correo: str) -> str | None:
    """Genera token temporal de recuperación (HU-E1-03 CA1/CA2).

    Devuelve el token (en la demo se muestra en pantalla simulando el email;
    en producción se enviaría por SMTP). Devuelve None si el correo no existe
    para no revelar qué cuentas están registradas.
    """
    correo_norm = correo.strip().lower()
    usuario = session.scalar(select(Usuario).where(Usuario.correo == correo_norm))
    if usuario is None or not usuario.activo:
        return None
    token = secrets.token_urlsafe(32)
    # En reposo solo el hash (un leak de BD no revela tokens usables).
    usuario.token_recuperacion = hashlib.sha256(token.encode()).hexdigest()
    usuario.token_expira = datetime.now(UTC) + timedelta(
        minutes=settings.token_recuperacion_min
    )
    session.commit()
    logger.info("Token de recuperación generado para %s", correo_norm)
    return token


def recuperar_contrasena(
    session: Session, *, correo: str, token: str, nueva_password: str
) -> Usuario:
    """Aplica nueva contraseña con token válido de un solo uso (CA2/CA3)."""
    if len(nueva_password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres")

    correo_norm = correo.strip().lower()
    usuario = session.scalar(select(Usuario).where(Usuario.correo == correo_norm))
    if usuario is None or usuario.token_recuperacion is None:
        raise TokenInvalidoError("Token inválido o ya usado")

    token_hash = hashlib.sha256(token.strip().encode()).hexdigest()
    if not secrets.compare_digest(usuario.token_recuperacion, token_hash):
        raise TokenInvalidoError("Token inválido o ya usado")

    expira = usuario.token_expira
    if expira is not None and expira.tzinfo is None:
        expira = expira.replace(tzinfo=UTC)
    if expira is None or expira <= datetime.now(UTC):
        usuario.token_recuperacion = None
        usuario.token_expira = None
        session.commit()
        raise TokenInvalidoError("El token expiró — solicite uno nuevo")

    usuario.password_hash = hash_password(nueva_password)
    usuario.token_recuperacion = None  # un solo uso
    usuario.token_expira = None
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    session.commit()
    return usuario
