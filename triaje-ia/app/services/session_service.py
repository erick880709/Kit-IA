"""Servicio de sesión (HU-E1-04).

Cierre automático por inactividad. El timeout es configurable sin
re-desplegar (CA3): variable SESSION_TIMEOUT_MIN en .env.
"""

from __future__ import annotations

from datetime import datetime

from app.infra.config import settings


def debe_expirar(
    ultima_actividad: datetime, ahora: datetime, timeout_min: int | None = None
) -> bool:
    """True si pasó más de `timeout_min` minutos desde la última actividad (CA1)."""
    timeout = timeout_min if timeout_min is not None else settings.session_timeout_min
    delta = (ahora - ultima_actividad).total_seconds()
    return delta > timeout * 60


def tiempo_inactividad_segundos(ultima_actividad: datetime, ahora: datetime) -> float:
    """Segundos transcurridos desde la última actividad (para logs/aviso)."""
    return max(0.0, (ahora - ultima_actividad).total_seconds())
