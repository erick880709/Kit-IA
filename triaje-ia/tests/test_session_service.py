"""Pruebas de cierre de sesión por inactividad (HU-E1-04 CA1/CA3)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.services.session_service import debe_expirar

AHORA = datetime(2026, 8, 13, 12, 0, 0, tzinfo=UTC)


def test_no_expira_antes_del_timeout() -> None:
    ultima = AHORA - timedelta(minutes=4, seconds=59)
    assert debe_expirar(ultima, AHORA, timeout_min=5) is False


def test_expira_justo_despues_del_timeout() -> None:
    ultima = AHORA - timedelta(minutes=5, seconds=1)
    assert debe_expirar(ultima, AHORA, timeout_min=5) is True


def test_timeout_configurable_sin_recalcular() -> None:
    """CA3: el timeout llega por parámetro (configurable vía .env)."""
    ultima = AHORA - timedelta(minutes=2)
    assert debe_expirar(ultima, AHORA, timeout_min=1) is True
    assert debe_expirar(ultima, AHORA, timeout_min=3) is False
