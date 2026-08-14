"""Helper de presentación de errores con formato centralizado."""

from __future__ import annotations

from app.domain.exceptions import AppError


def format_error(exc: Exception) -> dict:
    """Normaliza cualquier excepción al contrato {error:{codigo,mensaje,detalle}}."""
    if isinstance(exc, AppError):
        return {"error": exc.to_dict()}
    return {"error": {"codigo": "ERROR_INTERNO", "mensaje": str(exc) or type(exc).__name__}}
