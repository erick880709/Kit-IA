"""Limpieza: validaciones RNQ, normalización de régimen y outliers (TT-E3-02)."""

from __future__ import annotations

import numpy as np
import pandas as pd

# Reglas de calidad (RNQ-001/003/004).
_RANGOS = {
    "temperatura": (34.0, 43.0),
    "frecuencia_cardiaca": (20, 300),
    "frecuencia_respiratoria": (4, 60),
    "saturacion_o2": (50, 100),
    "presion_sistolica": (40, 300),
    "presion_diastolica": (20, 200),
    "peso": (1.0, 400.0),
    "talla": (0.3, 2.5),
}

# Typos documentados en RT-006 (normalización de REGIMEN).
_NORMALIZACION_REGIMEN = {
    "contributivo": "Contributivo",
    "subsidiado": "Subsidiado",
    "especial": "Especial",
    "no afiliado": "NoAfiliado",
    "noafiliado": "NoAfiliado",
    "subsidiado.": "Subsidiado",
    "contributivo.": "Contributivo",
}

_VIA_LLEGADA_VALIDA = {"Ambulancia", "Particular", "Remisión"}  # RNQ-004


class ValidadorCalidad:
    """Valida rangos fisiológicos y marca registros inválidos (RNQ-003)."""

    @staticmethod
    def validar(df: pd.DataFrame) -> pd.DataFrame:
        for col, (minimo, maximo) in _RANGOS.items():
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df.loc[~df[col].between(minimo, maximo), col] = np.nan
        if "via_llegada" in df.columns:
            df.loc[~df["via_llegada"].isin(_VIA_LLEGADA_VALIDA), "via_llegada"] = np.nan
        return df


class NormalizadorRegimen:
    """Normaliza REGIMEN con los typos documentados en RT-006."""

    @staticmethod
    def normalizar(df: pd.DataFrame) -> pd.DataFrame:
        if "regimen" in df.columns:
            df["regimen"] = (
                df["regimen"].astype(str).str.strip().str.lower()
                .map(_NORMALIZACION_REGIMEN)
                .fillna(df["regimen"])
            )
        return df


class LimpiezaOutliers:
    """Imputa nulos (mediana) y recorta outliers extremos (percentil 1-99)."""

    def __init__(self, columnas: list[str]) -> None:
        self.columnas = columnas

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        salida = df.copy()
        for col in self.columnas:
            if col not in salida.columns:
                continue
            mediana = salida[col].median()
            salida[col] = salida[col].fillna(mediana)
            bajo, alto = salida[col].quantile(0.01), salida[col].quantile(0.99)
            salida[col] = salida[col].clip(bajo, alto)
        return salida
