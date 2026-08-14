"""Test trivial de salud (FASE 6 de genesis)."""

from scripts.healthcheck import run


def test_healthcheck_todo_ok() -> None:
    result = run()
    assert result["estado"] == "OK"
    assert result["checks"]["base_de_datos"] is True
    assert result["checks"]["directorio_modelos"] is True
