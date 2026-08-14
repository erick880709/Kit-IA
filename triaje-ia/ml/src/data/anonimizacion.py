"""Anonimización obligatoria previa a cualquier procesamiento (TT-E3-01, RNF-006).

Se ejecuta SIEMPRE antes de limpieza (sin excepciones). Identificadores directos
(documento, nombres, correo, teléfono, dirección) se seudonimizan con hash o se
eliminan. Datos personales Ley 1581/2012.
"""

from __future__ import annotations

import hashlib

import pandas as pd

_COLUMNAS_IDENTIFICADORAS = [
    "tipo_documento", "numero_documento", "nombres", "apellidos",
    "telefono", "correo", "contacto_emergencia", "numero_contacto_emergencia",
    "direccion_residencia",
]

_COLUMNAS_SEUDONIMIZABLES = [
    "tipo_documento", "numero_documento", "nombres", "apellidos",
    "telefono", "correo", "contacto_emergencia", "numero_contacto_emergencia",
    "direccion_residencia",
]


def _seudonimo(valor) -> str | None:
    if pd.isna(valor):
        return None
    return hashlib.sha256(str(valor).encode("utf-8")).hexdigest()[:16]


def anonimizar(df: pd.DataFrame) -> pd.DataFrame:
    """Hash de identificadores directos; k-anonimización básica en fechas.

    No modifica el DataFrame de entrada.
    """
    salida = df.copy()
    for col in _COLUMNAS_IDENTIFICADORAS:
        if col in salida.columns:
            salida[col] = salida[col].map(_seudonimo)
    if "fecha_nacimiento" in salida.columns:  # generalizar a año de nacimiento
        salida["anio_nacimiento"] = pd.to_datetime(
            salida["fecha_nacimiento"], errors="coerce"
        ).dt.year
        salida = salida.drop(columns=["fecha_nacimiento"])
    return salida
