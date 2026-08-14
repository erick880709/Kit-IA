"""Excepciones de dominio y de aplicación.

Formato de error centralizado (Sección 10 del documento de arquitectura):
    {"error": {"codigo": ..., "mensaje": ..., "detalle": ...}}
"""

from __future__ import annotations


class AppError(Exception):
    """Error base con código estable para clientes/logs."""

    codigo: str = "ERROR_INTERNO"

    def __init__(self, mensaje: str, *, detalle: str | None = None) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.detalle = detalle

    def to_dict(self) -> dict:
        payload: dict = {"codigo": self.codigo, "mensaje": self.mensaje}
        if self.detalle:
            payload["detalle"] = self.detalle
        return payload


class ValidationError(AppError):
    """Entrada inválida en el límite del sistema (formularios)."""

    codigo = "VALIDACION"


class InferenceError(AppError):
    """Fallo del motor de inferencia (dispara modo degradado, RNF-009)."""

    codigo = "INFERENCIA"


class NotFoundError(AppError):
    """Recurso inexistente."""

    codigo = "NO_ENCONTRADO"


class AutenticacionError(AppError):
    """Credenciales inválidas o usuario inactivo (HU-E1-01)."""

    codigo = "AUTENTICACION"


class UsuarioBloqueadoError(AppError):
    """Bloqueo temporal vigente tras intentos fallidos (HU-E1-01 CA3)."""

    codigo = "USUARIO_BLOQUEADO"


class ProhibidoError(AppError):
    """El rol del usuario no tiene permiso sobre la pantalla (HU-E1-02 CA3)."""

    codigo = "PROHIBIDO"


class TokenInvalidoError(AppError):
    """Token de recuperación inválido, usado o expirado (HU-E1-03 CA2)."""

    codigo = "TOKEN_INVALIDO"
