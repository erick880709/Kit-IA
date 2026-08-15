"""Seed automático de la demo (usuarios y roles) — idempotente.

Usado por el bootstrap para que la app arranque funcional en entornos
efímeros (Streamlit Community Cloud, contenedores, primera ejecución local).
Misma lógica de `scripts/seed_demo.py` pero como servicio testable.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Rol, Usuario
from app.services.auth_service import registrar_usuario

ROLES_DEMO = ("Medico", "Enfermera", "Administrador", "Investigador", "Auditor")

USUARIOS_DEMO = (
    ("medico", "Medico"),
    ("enfermera", "Enfermera"),
    ("admin", "Administrador"),
    ("investigador", "Investigador"),
    ("auditor", "Auditor"),
)

PASSWORD_DEMO = "Demo123!"


def seed_demo_si_vacio(session: Session) -> int:
    """Siembra roles y usuarios demo SOLO si no hay usuarios. Devuelve los creados."""
    if session.scalar(select(Usuario).limit(1)) is not None:
        return 0

    for nombre in ROLES_DEMO:
        if session.scalar(select(Rol).where(Rol.nombre == nombre)) is None:
            session.add(Rol(nombre=nombre))
    session.commit()

    creados = 0
    for alias, rol in USUARIOS_DEMO:
        registrar_usuario(
            session,
            correo=f"{alias}@hospital.gov.co",
            password=PASSWORD_DEMO,
            nombre=f"{alias.capitalize()} Demo",
            rol_nombre=rol,
        )
        creados += 1
    return creados
