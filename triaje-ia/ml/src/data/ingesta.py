"""Adaptadores de ingesta de las 5 fuentes (TT-E3-01, RT-006).

Fuentes: MIMIC-IV-ED (PhysioNet), cohorte Hospital SJdD (CSV custom),
Clasificación Triage datos.gov.co, BDUA contributivo+subsidiado, Morbilidad RIPS.

En esta máquina se ejecutan: CSVs locales (datasets/) y el generador sintético
de demo (calibrado con la distribución real RNF-004). MIMIC queda pendiente de
credenciales PhysioNet (documentado) — el adaptador ya está implementado.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from ml.src import DATA_RAW

# Distribución real medida en el dataset nacional MinSalud (89.453 eventos,
# 2020-2021): I 0.227% · II 3.030% · III 88.536% · IV 7.752% · V 0.456%
_DISTRIBUCION_REAL = {
    "I": 0.002269, "II": 0.030295, "III": 0.885359, "IV": 0.077516, "V": 0.004561,
}

_COLUMNAS_CANONICAS = [
    "tipo_documento", "numero_documento", "nombres", "apellidos",
    "fecha_nacimiento", "sexo", "via_llegada", "episodios_previos_urgencias",
    "telefono", "correo", "contacto_emergencia", "numero_contacto_emergencia",
    "departamento", "ciudad", "direccion_residencia", "regimen",
    "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
    "saturacion_o2", "presion_sistolica", "presion_diastolica",
    "peso", "talla", "motivo_codigo_cie10", "motivo_texto", "nivel_triaje",
]


def ingestar_csv_local(ruta: str | Path, *, fuente: str) -> pd.DataFrame:
    """Adaptador genérico de CSV local (hospital SJdD, Socrata, BDUA, RIPS)."""
    df = pd.read_csv(ruta, sep=None, engine="python")
    df["fuente"] = fuente
    return df


class AdaptadorPhysioNet:
    """Adaptador MIMIC-IV-ED — requiere credenciales PhysioNet + CITI (documentado).

    Uso previsto: `AdaptadorPhysioNet(usuario, password).descargar_ed_stays()`.
    """

    def __init__(self, usuario: str, password: str) -> None:
        self.usuario = usuario
        self.password = password

    def descargar_ed_stays(self, destino: Path) -> Path:
        raise NotImplementedError(
            "Descarga de MIMIC-IV-ED pendiente de credenciales PhysioNet "
            "(acción del usuario — ver resources/session/estado.json)"
        )


class AdaptadorSocrata:
    """Adaptador de datos.gov.co (triaje nacional, BDUA) vía API pública."""

    @staticmethod
    def desde_resource(resource_id: str, *, fuente: str, limite: int | None = None) -> pd.DataFrame:
        url = (
            "https://www.datos.gov.co/resource/"
            f"{resource_id}.csv?$limit={limite or 1000}"
        )
        df = pd.read_csv(url)
        df["fuente"] = fuente
        return df


class FuenteSinteticaDemo:
    """Generador de datos sintéticos calibrado con la distribución real (demo).

    Incluye identificadores directos ficticios para que el módulo de
    anonimización sea verificable de punta a punta.
    """

    def __init__(self, n: int = 2000, semilla: int = 42) -> None:
        self.n = n
        self.semilla = semilla

    def generar(self) -> pd.DataFrame:
        import numpy as np

        rng = np.random.default_rng(self.semilla)
        niveles = np.array(list(_DISTRIBUCION_REAL))
        probs = np.array(list(_DISTRIBUCION_REAL.values()))
        probs = probs / probs.sum()

        n = self.n
        nivel = rng.choice(niveles, size=n, p=probs)

        # Inyección de señal clínica: los signos se generan condicionados al nivel
        # para que el demo sea aprendible (documentado como limitación del
        # sintético frente a MIMIC real).
        altos = (nivel == "I") | (nivel == "II")
        medios = nivel == "III"
        bajos = ~(altos | medios)

        def _grupo(mask):
            return {"spo2": rng.integers(78, 94, mask.sum()),
                    "fr": rng.integers(24, 40, mask.sum()),
                    "hr": rng.integers(100, 145, mask.sum()),
                    "t": np.round(rng.uniform(37.4, 40.6, mask.sum()), 1),
                    "pas": rng.integers(70, 108, mask.sum())}

        def _grupo_medio(mask):
            return {"spo2": rng.integers(92, 98, mask.sum()),
                    "fr": rng.integers(16, 27, mask.sum()),
                    "hr": rng.integers(70, 112, mask.sum()),
                    "t": np.round(rng.uniform(36.2, 38.6, mask.sum()), 1),
                    "pas": rng.integers(100, 146, mask.sum())}

        def _grupo_leve(mask):
            return {"spo2": rng.integers(95, 100, mask.sum()),
                    "fr": rng.integers(12, 23, mask.sum()),
                    "hr": rng.integers(55, 96, mask.sum()),
                    "t": np.round(rng.uniform(35.8, 37.9, mask.sum()), 1),
                    "pas": rng.integers(105, 168, mask.sum())}

        spo2, fr, hr, t, pas = (
            np.empty(n, dtype=float), np.empty(n, dtype=float),
            np.empty(n, dtype=float), np.empty(n, dtype=float),
            np.empty(n, dtype=float),
        )
        for mask, gen in ((altos, _grupo), (medios, _grupo_medio), (bajos, _grupo_leve)):
            g = gen(mask)
            spo2[mask], fr[mask], hr[mask], t[mask], pas[mask] = (
                g["spo2"], g["fr"], g["hr"], g["t"], g["pas"],
            )

        textos_altos = [
            "Dolor opresivo retroesternal de 2 horas",
            "Tos con expectoración y disnea marcada",
            "Caída con golpe en la cabeza y somnolencia",
            "Dificultad respiratoria severa desde anoche",
        ]
        textos_medios = [
            "Dolor abdominal de 3 días de evolución",
            "Vómito y diarrea desde hace 24 horas",
            "Cefalea intensa desde anoche",
            "Fiebre de 39 grados desde ayer",
        ]
        textos_bajos = [
            "Congestión nasal y malestar general",
            "Dolor lumbar al esfuerzo",
            "Ardor al orinar",
            "Control y dolor leve de tobillo",
        ]
        motivo_texto = np.empty(n, dtype=object)
        for mask, pool in ((altos, textos_altos), (medios, textos_medios), (bajos, textos_bajos)):
            motivo_texto[mask] = rng.choice(pool, size=mask.sum())
        cie_altos = ["R07.4", "J18.9", "S09.9", "R06.0"]
        cie_medios = ["R10.4", "A09", "R51", "R50.9"]
        cie_bajos = ["J00", "M54.5", "N39.0", "S93.4"]
        cie = np.empty(n, dtype=object)
        for mask, pool in ((altos, cie_altos), (medios, cie_medios), (bajos, cie_bajos)):
            cie[mask] = rng.choice(pool, size=mask.sum())

        df = pd.DataFrame(
            {
                "tipo_documento": "CC",
                "numero_documento": [f"1000000000{i:02d}" for i in range(n)],
                "nombres": [f"Paciente{i}" for i in range(n)],
                "apellidos": [f"Demo{i % 100}" for i in range(n)],
                "fecha_nacimiento": pd.to_datetime(
                    rng.integers(1940, 2015, n), unit="D", origin="1970-01-01"
                ).date,
                "sexo": rng.choice(["Femenino", "Masculino"], size=n, p=[0.55, 0.45]),
                "via_llegada": rng.choice(
                    ["Ambulancia", "Particular", "Remisión"], size=n, p=[0.3, 0.5, 0.2]
                ),
                "episodios_previos_urgencias": rng.poisson(1.2, n).clip(0, 30),
                "telefono": [f"300{i % 10000000:07d}" for i in range(n)],
                "correo": [f"paciente{i}@demo.co" for i in range(n)],
                "contacto_emergencia": [f"Familiar{i % 50}" for i in range(n)],
                "numero_contacto_emergencia": [f"310{i % 10000000:07d}" for i in range(n)],
                "departamento": "Cundinamarca",
                "ciudad": "Bogotá D.C.",
                "direccion_residencia": [f"Calle {j % 200}" for j in range(n)],
                "regimen": rng.choice(
                    ["Contributivo", "Subsidiado", "Especial", "No afiliado"],
                    size=n, p=[0.6, 0.3, 0.05, 0.05],
                ),
                "temperatura": t.astype(float),
                "frecuencia_cardiaca": hr.astype(int),
                "frecuencia_respiratoria": fr.astype(int),
                "saturacion_o2": spo2.astype(int),
                "presion_sistolica": pas.astype(int),
                "presion_diastolica": rng.integers(50, 110, n),
                "peso": np.round(rng.normal(70, 15, n).clip(30, 160), 1),
                "talla": np.round(rng.normal(1.65, 0.1, n).clip(1.3, 2.1), 2),
                "motivo_codigo_cie10": cie,
                "motivo_texto": motivo_texto,
                "nivel_triaje": nivel,
                "fuente": "sintetico_demo",
            }
        )
        return df


def generar_datos_sinteticos(
    n: int = 2000, *, semilla: int = 42, destino: Path | None = None
) -> Path:
    """Genera y guarda el dataset sintético de demo en data/raw.

    El nombre incluye n y semilla: volver a generar con otros parámetros
    no reutiliza silenciosamente un archivo previo (hallazgo revision-calidad).
    """
    ruta = destino or (DATA_RAW / f"demo_sintetico_{n}_{semilla}.csv")
    if not ruta.exists():
        FuenteSinteticaDemo(n=n, semilla=semilla).generar().to_csv(ruta, index=False)
    return ruta


def _hash_directo(valor: str) -> str:
    return hashlib.sha256(valor.encode("utf-8")).hexdigest()[:16]


def ingestar_san_juan_de_dios(
    ruta: str | Path, *, fuente: str = "san_juan_de_dios"
) -> pd.DataFrame:
    """Adaptador del registro clínico del Hospital San Juan de Dios (fine-tuning).

    Columnas fuente: `triage` (I–V), `codigo de diagnostico` (CIE-10),
    `diagnostico` (texto libre), `eps o ips`, `fecha`, horas, `edad` ('24 AÑOS'),
    `año`. Sin signos vitales → alimenta el submodelo de texto de la fusión tardía.
    Los identificadores de institución se descartan (Ley 1581).
    """
    import numpy as np

    df = pd.read_csv(ruta, sep=None, engine="python")
    salida = pd.DataFrame()
    salida["nivel_triaje"] = df["triage"].astype(str).str.strip().str.upper()
    salida["motivo_codigo_cie10"] = (
        df["codigo de diagnostico"].astype(str).str.strip().str.upper()
    )
    salida["motivo_texto"] = df["diagnostico"].astype(str).str.strip()
    edad = pd.to_numeric(
        df["edad"].astype(str).str.extract(r"(\d+)", expand=False), errors="coerce"
    )
    anio = pd.to_numeric(df["año"], errors="coerce")
    salida["anio_nacimiento"] = anio - edad
    invalido = (salida["anio_nacimiento"] < 1900) | (salida["anio_nacimiento"] > 2026)
    salida.loc[invalido, "anio_nacimiento"] = np.nan
    salida["fuente"] = fuente
    return salida


def ingestar_triage_nacional(
    ruta: str | Path, *, fuente: str = "minsalud_nacional"
) -> pd.DataFrame:
    """Adaptador del dataset nacional de clasificación en triage (calibración).

    Aporta la distribución real de niveles I–V (sin features clínicas por
    evento), usada para validar la calibración del sintético y como contraste
    en el análisis de equidad — no entra como feature de entrenamiento.
    """
    df = pd.read_csv(ruta, sep=None, engine="python")
    salida = pd.DataFrame()
    salida["nivel_triaje"] = df["Triage"].astype(str).str.strip().str.upper()
    salida["fuente"] = fuente
    return salida
