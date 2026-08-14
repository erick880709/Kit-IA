"""Ingesta y anonimización (TT-E3-01)."""

from __future__ import annotations

from .anonimizacion import anonimizar
from .ingesta import (
    FuenteSinteticaDemo,
    generar_datos_sinteticos,
    ingestar_csv_local,
)

__all__ = [
    "FuenteSinteticaDemo",
    "generar_datos_sinteticos",
    "ingestar_csv_local",
    "anonimizar",
]
