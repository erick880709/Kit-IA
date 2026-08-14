"""Utilidades de autenticación local (Sección 10 del documento de arquitectura).

Login por correo + contraseña con hash bcrypt. Los endpoints/UI de login los
genera `builder` (HU-E1-01); aquí solo vive la plomería de hashing.
"""

from __future__ import annotations

import bcrypt


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
