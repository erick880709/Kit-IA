"""Mapeo CIE-10 → CIE-11 para el re-codificado del vocabulario de entrenamiento.

El catálogo de motivos de la aplicación pasó a CIE-11 (catalogos.py). Este
módulo traduce los códigos CIE-10 presentes en los datos etiquetados (demo
sintético, cohorte SJdD, MIMIC) para que el TF-IDF del submodelo de texto
aprenda los MISMOS tokens CIE-11 que produce la pantalla de evaluación clínica.

Nota: mapeo de grado demo (mismas entradas del catálogo) — validar con un
referente clínico antes de uso real. Los códigos fuera del catálogo pasan
intactos (p. ej. la mayoría de diagnósticos reales de SJdD).
"""

from __future__ import annotations

MAPEO_CIE10_A_CIE11: dict[str, str] = {
    # Digestivo
    "R10.4": "DD30", "K59.0": "ME05", "R11": "MD90", "K92.2": "DB24.B",
    "K35.80": "DB10", "A09": "1A40", "R10.0": "MD81.3", "K29.7": "DA42",
    # Respiratorio
    "J00": "CA00", "J06.9": "CA07", "J20.9": "CA42", "J45.9": "CA23",
    "J18.9": "CA40", "R05": "MD12", "R06.0": "MD11", "J96.0": "CB41",
    # Neurológico
    "R51": "8A8Z", "R42": "MB48", "R55": "MG45", "R56.9": "8A68",
    "G43.9": "8A80", "S09.9": "NA0Z",
    # Cardiovascular
    "R07.4": "MD30", "I10": "BA00", "R00.0": "MC81", "R00.1": "MC80",
    # Musculoesquelético
    "M54.5": "ME84.2", "S93.4": "ND14", "S52.9": "NC32", "S61.9": "ND12",
    "T14.1": "ND9Z", "T30.0": "ND90",
    # Trauma
    "T14.2": "ND5Z", "S62.9": "NC52", "S72.9": "NC72", "S82.9": "NC92",
    "S06.9": "NA07", "W34.9": "PA80", "W26.0": "PA75", "T14.3": "ND13",
    "T07": "ND0Z", "T14.7": "ND50", "W54": "PA50", "W19.9": "PA60",
    "T75.4": "PB80", "T75.1": "NF08",
    # Genitourinario
    "N39.0": "GC08", "N23": "MF56", "R30.0": "MF50.7", "R31": "MF50.4",
    # Ginecológico/Obstétrico
    "N94.6": "GA34.3", "O26.9": "JA65",
    # Piel/Alergia
    "L03.90": "EF50", "R21": "ME65", "L29.9": "EC90", "T78.40": "4A80",
    "L50.9": "EB00",
    # ORL/Oftalmológico
    "J02.9": "CA09", "J03.90": "CA0A", "H66.90": "AB00", "H10.9": "9A60",
    # Salud mental
    "F41.9": "6B00", "R45.1": "MB24.3",
    # Endocrino/Metabólico
    "E16.2": "5A41",
    # Hematológico
    "D50.9": "3A00",
    # Signos/Síntomas generales
    "R50.9": "MG26", "E86.0": "5C70", "R53": "MG22", "R63.0": "MG43.7",
    "R41.0": "MB20", "B34.9": "1D9Z",
}


def _normalizar(codigo: str) -> str:
    """CIE-10 codificado sin punto y sin sufijo X (p. ej. 'R10.4' → 'R104')."""
    codigo = (codigo or "").strip().upper().replace(".", "")
    while codigo.endswith("X"):
        codigo = codigo[:-1]
    return codigo


_INDICE: dict[str, str] = {
    _normalizar(cie10): cie11 for cie10, cie11 in MAPEO_CIE10_A_CIE11.items()
}


def remapear_cie11(codigo) -> str:
    """Devuelve el código CIE-11 si está en el catálogo; si no, el original.

    Soporta CIE-10 con/sin punto y sufijos X (normalización previa).
    """
    codigo = (codigo or "").strip()
    if not codigo:
        return ""
    return _INDICE.get(_normalizar(codigo), codigo)
