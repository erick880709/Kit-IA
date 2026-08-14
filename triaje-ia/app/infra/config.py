"""Carga de configuración desde variables de entorno (.env)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Raíz del proyecto triaje-ia/ (dos niveles arriba de app/infra).
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _get(name: str, default: str) -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    """Configuración tipada de la aplicación."""

    app_name: str = _get("APP_NAME", "TriajeIA")
    app_secret: str = _get("APP_SECRET_KEY", "cambiar-en-produccion")
    db_path: str = _get("DB_PATH", str(PROJECT_ROOT / "triaje.db"))
    log_level: str = _get("LOG_LEVEL", "INFO")
    models_dir: str = _get("MODELS_DIR", str(PROJECT_ROOT / "artifacts" / "models"))
    max_intentos_login: int = int(_get("MAX_INTENTOS_LOGIN", "5"))  # HU-E1-01 CA3
    bloqueo_login_min: int = int(_get("BLOQUEO_LOGIN_MIN", "15"))
    session_timeout_min: int = int(_get("SESSION_TIMEOUT_MIN", "5"))  # HU-E1-04 CA1/CA3
    token_recuperacion_min: int = int(_get("TOKEN_RECUPERACION_MIN", "15"))  # HU-E1-03 CA2


settings = Settings()
