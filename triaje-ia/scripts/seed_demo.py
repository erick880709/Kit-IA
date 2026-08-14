"""Seed de la demo (TT-E1-01): roles y usuarios de prueba.

Idempotente: no duplica correos ni roles.
Contraseña demo de todos los usuarios: Demo123!

Uso:  python scripts/seed_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

from app.domain.entities import ROLES_DEMO, Rol, Usuario  # noqa: E402
from app.infra.db import SessionLocal, init_db  # noqa: E402
from app.services.auth_service import registrar_usuario  # noqa: E402

USUARIOS_DEMO = [
    ("medico", "Medico"),
    ("enfermera", "Enfermera"),
    ("admin", "Administrador"),
    ("investigador", "Investigador"),
    ("auditor", "Auditor"),
]


def seed() -> None:
    init_db()
    with SessionLocal() as session:
        for nombre_rol in ROLES_DEMO:
            existe = session.scalar(select(Rol).where(Rol.nombre == nombre_rol))
            if existe is None:
                session.add(Rol(nombre=nombre_rol))
        session.commit()

        creados = 0
        for alias, rol in USUARIOS_DEMO:
            correo = f"{alias}@hospital.gov.co"
            existe = session.scalar(select(Usuario).where(Usuario.correo == correo))
            if existe is None:
                registrar_usuario(
                    session,
                    correo=correo,
                    password="Demo123!",
                    nombre=f"{alias.capitalize()} Demo",
                    rol_nombre=rol,
                )
                creados += 1
                print(f"creado: {correo} ({rol})")
            else:
                print(f"ya existe: {correo}")
        print(f"Seed completo — {creados} usuarios nuevos.")


if __name__ == "__main__":
    seed()
