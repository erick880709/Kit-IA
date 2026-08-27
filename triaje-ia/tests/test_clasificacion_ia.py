"""Tests de la pantalla de clasificación IA (UX de visitas anteriores)."""

from __future__ import annotations

from app.views.clasificacion_ia import _resultado_de_otro_evento


def test_resultado_de_otro_evento_detecta_visita_anterior() -> None:
    """El resultado almacenado de OTRO evento debe marcarse como visita
    anterior (2026-08-26): evita mostrar la recomendación vieja como si
    fuera la del triaje en curso."""
    resultado = {"estado": "ok"}
    assert _resultado_de_otro_evento(resultado, "ev-1", "ev-2") is True
    assert _resultado_de_otro_evento(resultado, "ev-1", "ev-1") is False


def test_resultado_sin_evento_asociado_se_trata_como_anterior() -> None:
    resultado = {"estado": "ok"}
    assert _resultado_de_otro_evento(resultado, None, "ev-1") is True
    assert _resultado_de_otro_evento(resultado, "ev-1", None) is True


def test_sin_resultado_no_es_visita_anterior() -> None:
    assert _resultado_de_otro_evento(None, None, "ev-1") is False
    assert _resultado_de_otro_evento(None, "ev-1", "ev-1") is False


def test_claves_sesion_limpian_resultado_ia_al_cerrar_sesion() -> None:
    """El resultado de un paciente no debe filtrarse a la sesión de otro
    usuario: al cerrar sesión se elimina junto a su evento."""
    from app.main import CLAVES_SESION

    assert "resultado_ia" in CLAVES_SESION
    assert "resultado_ia_evento_id" in CLAVES_SESION
