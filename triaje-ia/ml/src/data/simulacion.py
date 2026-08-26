"""Simulación balanceada condicionada a la distribución real de entrenamiento.

Mejora 2026-08-26 (máxima precisión): el demo replica la prevalencia nacional
(I 0.23% · V 0.46%), lo que deja las clases extremas con decenas de ejemplos
frente a miles de III. Este módulo genera datos sintéticos que REPLICAN las
distribuciones empíricas por nivel (media/desviación/rango observado) de los
datos reales etiquetados, equilibrando las 5 clases (oversampling multivariado
tipo SMOTE condicionado a la clase).

Reglas de honestidad (auditables por tests):
- Se genera SOLO desde el split de entrenamiento (nunca val/test ni holdouts).
- Signos muestreados de normales truncadas al rango observado por nivel,
  acotado a límites fisiológicos plausibles (mismos rangos RNQ-003).
- Anclas clínicas: toda fila I queda con ≥1 signo en zona de peligro y toda
  fila V completamente normal (consistente con la red de contención).
- Los motivos (código CIE-11 + texto) se re-muestrean de la distribución
  empírica por nivel — no se inventan motivos nuevos.
- NO entra en la calibración de umbrales ni en el test honesto del demo.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import truncnorm

from ml.src.evaluation.metrics import CLASES

# Rangos fisiológicos plausibles (RNQ-003, mismos límites de limpieza.py).
_LIMITES: dict[str, tuple[float, float]] = {
    "temperatura": (34.0, 43.0),
    "frecuencia_cardiaca": (20.0, 300.0),
    "frecuencia_respiratoria": (4.0, 60.0),
    "saturacion_o2": (50.0, 100.0),
    "presion_sistolica": (40.0, 300.0),
    "presion_diastolica": (20.0, 200.0),
    "peso": (30.0, 160.0),
    "talla": (1.3, 2.1),
    "episodios_previos_urgencias": (0.0, 30.0),
    "anio_nacimiento": (1930.0, 2010.0),
}

# Piso de desviación por variable: evita normales degeneradas cuando una clase
# tiene pocos ejemplos (p. ej. 6 filas I reales en el demo).
_PISO_DESV: dict[str, float] = {
    "temperatura": 0.2,
    "frecuencia_cardiaca": 5.0,
    "frecuencia_respiratoria": 2.0,
    "saturacion_o2": 1.0,
    "presion_sistolica": 6.0,
    "presion_diastolica": 4.0,
    "peso": 4.0,
    "talla": 0.04,
    "episodios_previos_urgencias": 1.0,
    "anio_nacimiento": 4.0,
}

_ENTERAS = {
    "frecuencia_cardiaca", "frecuencia_respiratoria", "saturacion_o2",
    "presion_sistolica", "presion_diastolica",
    "episodios_previos_urgencias", "anio_nacimiento",
}
_1_DECIMAL = {"temperatura", "peso"}
_2_DECIMALES = {"talla"}


def _redondear(valores: np.ndarray, columna: str) -> np.ndarray:
    if columna in _ENTERAS:
        return np.rint(valores).astype(int)
    if columna in _1_DECIMAL:
        return np.round(valores, 1)
    if columna in _2_DECIMALES:
        return np.round(valores, 2)
    return valores


def _en_zona_peligro(df: pd.DataFrame) -> pd.Series:
    """Criterio de la red de contención clínica (riesgo vital → nivel I)."""
    return (
        (df["saturacion_o2"] < 90)
        | (df["presion_sistolica"] < 90)
        | (df["frecuencia_cardiaca"] > 120)
        | (df["frecuencia_respiratoria"] > 28)
        | (df["temperatura"] > 39.0)
    )


def _todo_normal(df: pd.DataFrame) -> pd.Series:
    """Perfil completamente estable (compatible con nivel V)."""
    return (
        df["saturacion_o2"].between(96, 100)
        & df["frecuencia_cardiaca"].between(60, 100)
        & df["frecuencia_respiratoria"].between(12, 20)
        & df["temperatura"].between(36.0, 38.0)
        & df["presion_sistolica"].between(100, 140)
    )


def _muestras_categoricas(
    sub: pd.DataFrame, columna: str, n: int, rng: np.random.Generator, respaldo: str,
) -> np.ndarray:
    serie = sub[columna].dropna().astype(str)
    if serie.empty:
        return np.full(n, respaldo)
    return rng.choice(serie.to_numpy(), size=n)


def _motivos_empiricos(
    sub: pd.DataFrame, n: int, rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    parejas = sub[["motivo_codigo_cie10", "motivo_texto"]].fillna("").astype(str)
    parejas = parejas[
        (parejas["motivo_codigo_cie10"] != "") & (parejas["motivo_texto"] != "")
    ]
    if parejas.empty:
        return np.full(n, "R51"), np.full(n, "Síntoma general no especificado")
    indices = rng.integers(0, len(parejas), n)
    filas = parejas.iloc[indices]
    return filas["motivo_codigo_cie10"].to_numpy(), filas["motivo_texto"].to_numpy()


def _generar_nivel(
    sub: pd.DataFrame, nivel: str, n: int, rng: np.random.Generator,
) -> pd.DataFrame:
    """Muestrea n filas sintéticas que replican la distribución de `sub`."""
    filas: dict[str, np.ndarray] = {}
    for columna, (limite_bajo, limite_alto) in _LIMITES.items():
        if columna not in sub.columns:
            continue
        serie = pd.to_numeric(sub[columna], errors="coerce").dropna()
        if serie.empty:
            continue
        media = float(serie.mean())
        desviacion = max(float(serie.std(ddof=1)), _PISO_DESV.get(columna, 1.0))
        bajo = max(limite_bajo, float(serie.min()))
        alto = min(limite_alto, float(serie.max()))
        if bajo >= alto:  # rango observado degenerado → usar rango fisiológico
            bajo, alto = limite_bajo, limite_alto
        a = (bajo - media) / desviacion
        b = (alto - media) / desviacion
        valores = truncnorm.rvs(a, b, loc=media, scale=desviacion, size=n,
                                random_state=rng)
        filas[columna] = _redondear(valores, columna)

    if "anio_nacimiento" not in filas:
        filas["anio_nacimiento"] = rng.integers(1960, 2011, n)

    codigos, textos = _motivos_empiricos(sub, n, rng)
    sexo = _muestras_categoricas(sub, "sexo", n, rng, "Femenino")
    via = _muestras_categoricas(sub, "via_llegada", n, rng, "Particular")
    regimen = _muestras_categoricas(sub, "regimen", n, rng, "Contributivo")
    departamento = _muestras_categoricas(sub, "departamento", n, rng, "Cundinamarca")

    salida = pd.DataFrame(
        {
            "tipo_documento": "CC",
            "numero_documento": [f"9000000000{i:04d}" for i in range(n)],
            "nombres": [f"Simulado{i}" for i in range(n)],
            "apellidos": [f"{nivel}{i}" for i in range(n)],
            "sexo": sexo,
            "via_llegada": via,
            "episodios_previos_urgencias": filas.get(
                "episodios_previos_urgencias", np.zeros(n, dtype=int)
            ),
            "telefono": [f"3500000{i:04d}" for i in range(n)],
            "correo": [f"simulado{i}@demo.co" for i in range(n)],
            "contacto_emergencia": [f"Familiar{i % 50}" for i in range(n)],
            "numero_contacto_emergencia": [f"3600000{i:04d}" for i in range(n)],
            "departamento": departamento,
            "ciudad": "Bogotá D.C.",
            "direccion_residencia": [f"Calle {i % 200}" for i in range(n)],
            "regimen": regimen,
            "temperatura": filas["temperatura"],
            "frecuencia_cardiaca": filas["frecuencia_cardiaca"],
            "frecuencia_respiratoria": filas["frecuencia_respiratoria"],
            "saturacion_o2": filas["saturacion_o2"],
            "presion_sistolica": filas["presion_sistolica"],
            "presion_diastolica": filas["presion_diastolica"],
            "peso": filas["peso"],
            "talla": filas["talla"],
            "anio_nacimiento": filas["anio_nacimiento"],
            "motivo_codigo_cie10": codigos,
            "motivo_texto": textos,
            "nivel_triaje": nivel,
            "fuente": "simulacion_balanceada",
        }
    )

    # Anclas clínicas deterministas SOBRE el DataFrame final: toda fila I debe
    # tener ≥1 signo en zona de peligro y toda fila V debe ser normal.
    if nivel == "I":
        peligro = _en_zona_peligro(salida)
        if not bool(peligro.all()):
            k = int((~peligro).sum())
            salida.loc[~peligro, "saturacion_o2"] = rng.integers(70, 90, k)
            salida.loc[~peligro, "frecuencia_cardiaca"] = rng.integers(121, 161, k)
    elif nivel == "V":
        normal = _todo_normal(salida)
        if not bool(normal.all()):
            k = int((~normal).sum())
            salida.loc[~normal, "saturacion_o2"] = rng.integers(97, 101, k)
            salida.loc[~normal, "frecuencia_cardiaca"] = rng.integers(60, 81, k)
            salida.loc[~normal, "frecuencia_respiratoria"] = rng.integers(12, 19, k)
            salida.loc[~normal, "temperatura"] = np.round(rng.uniform(36.3, 37.5, k), 1)
            salida.loc[~normal, "presion_sistolica"] = rng.integers(105, 136, k)

    return salida


def generar_simulados_balanceados(
    df_train: pd.DataFrame, *, n_por_nivel: int = 800, semilla: int = 42,
) -> pd.DataFrame:
    """Genera n_por_nivel filas sintéticas POR nivel, replicando df_train.

    SOLO debe llamarse con el split de entrenamiento (anti-leakage).
    """
    rng = np.random.default_rng(semilla)
    niveles = [n for n in CLASES if n in set(df_train["nivel_triaje"])]
    partes = [
        _generar_nivel(
            df_train[df_train["nivel_triaje"] == nivel], nivel, n_por_nivel, rng
        )
        for nivel in niveles
    ]
    return pd.concat(partes, ignore_index=True)


def resumen_similitud(df_train: pd.DataFrame, df_sim: pd.DataFrame) -> dict:
    """Desviación del promedio simulado vs real, por nivel, en desv. estándar.

    Auditoría de la hipótesis «el simulado replica la distribución real»:
    un valor ≤1 significa que el promedio simulado está dentro de 1 desviación
    estándar del promedio real de entrenamiento.
    """
    informe: dict[str, dict[str, float]] = {}
    for nivel in sorted(set(df_train["nivel_triaje"])):
        sub_real = df_train[df_train["nivel_triaje"] == nivel]
        sub_sim = df_sim[df_sim["nivel_triaje"] == nivel]
        desviaciones: dict[str, float] = {}
        for columna in _LIMITES:
            if columna not in sub_real.columns or columna not in sub_sim.columns:
                continue
            real = pd.to_numeric(sub_real[columna], errors="coerce").dropna()
            sim = pd.to_numeric(sub_sim[columna], errors="coerce").dropna()
            if len(real) < 5 or sim.empty:
                continue
            desv_real = float(real.std(ddof=1)) or 1.0
            desviaciones[columna] = round(
                abs(float(sim.mean()) - float(real.mean())) / desv_real, 3
            )
        informe[nivel] = desviaciones
    return informe
