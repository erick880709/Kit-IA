"""Catálogos de dominio (RD-002, HU-E2-01).

- DEPARTAMENTOS_COLOMBIA: 32 departamentos.
- CIUDADES_POR_DEPARTAMENTO: ciudades principales por departamento
  (subconjunto demo — el catálogo completo ~200 ciudades se siembra con
  datos reales en TT-E7-01).
- VIA_LLEGADA: catálogo exigido por HU-E2-01 CA1.
- SEXO: catálogo demográfico.
"""

from __future__ import annotations

DEPARTAMENTOS_COLOMBIA: list[str] = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá",
    "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba",
    "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira",
    "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo",
    "Quindío", "Risaralda", "San Andrés y Providencia", "Santander",
    "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada",
]

CIUDADES_POR_DEPARTAMENTO: dict[str, list[str]] = {
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": ["Medellín", "Bello", "Envigado", "Itagüí", "Rionegro"],
    "Arauca": ["Arauca", "Saravena", "Tame"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo"],
    "Bolívar": ["Cartagena", "Magangué", "Turbaco"],
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá"],
    "Caldas": ["Manizales", "La Dorada", "Chinchiná"],
    "Caquetá": ["Florencia", "San Vicente del Caguán"],
    "Casanare": ["Yopal", "Aguazul", "Villanueva"],
    "Cauca": ["Popayán", "Santander de Quilichao", "Puerto Tejada"],
    "Cesar": ["Valledupar", "Aguachica"],
    "Chocó": ["Quibdó", "Istmina"],
    "Córdoba": ["Montería", "Cereté", "Lorica"],
    "Cundinamarca": ["Bogotá D.C.", "Soacha", "Zipaquirá", "Girardot", "Facatativá"],
    "Guainía": ["Inírida"],
    "Guaviare": ["San José del Guaviare"],
    "Huila": ["Neiva", "Pitalito", "Garzón", "La Plata"],
    "La Guajira": ["Riohacha", "Maicao", "Uribia"],
    "Magdalena": ["Santa Marta", "Ciénaga", "Fundación"],
    "Meta": ["Villavicencio", "Acacías", "Granada"],
    "Nariño": ["Pasto", "Ipiales", "Tumaco"],
    "Norte de Santander": ["Cúcuta", "Ocaña", "Pamplona"],
    "Putumayo": ["Mocoa", "Puerto Asís"],
    "Quindío": ["Armenia", "Calarcá", "Montenegro"],
    "Risaralda": ["Pereira", "Dosquebradas", "Santa Rosa de Cabal"],
    "San Andrés y Providencia": ["San Andrés", "Providencia"],
    "Santander": ["Bucaramanga", "Floridablanca", "Barrancabermeja", "Girón"],
    "Sucre": ["Sincelejo", "Corozal", "San Marcos"],
    "Tolima": ["Ibagué", "Espinal", "Melgar"],
    "Valle del Cauca": ["Cali", "Palmira", "Buenaventura", "Tuluá", "Buga"],
    "Vaupés": ["Mitú"],
    "Vichada": ["Puerto Carreño"],
}

VIA_LLEGADA: list[str] = ["Ambulancia", "Particular", "Remisión"]

SEXO: list[str] = ["Femenino", "Masculino", "Intersexual", "Prefiero no informar"]

GRUPOS_SANGUINEOS: list[str] = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Niveles de triaje Res. 5596/2015 (RD-001).
NIVELES_TRIaje: list[str] = ["I", "II", "III", "IV", "V"]

# Top-10 motivos reales sembrados desde RD-002 (código CIE-10, descripción).
CATALOGO_MOTIVOS: list[tuple[str, str]] = [
    ("R10.4", "Dolor abdominal no especificado"),
    ("J00", "Rinofaringitis aguda (resfriado común)"),
    ("R51", "Cefalea"),
    ("A09", "Gastroenteritis de presunto origen infeccioso"),
    ("M54.5", "Lumbago no especificado"),
    ("R07.4", "Dolor torácico no especificado"),
    ("R50.9", "Fiebre no especificada"),
    ("J18.9", "Neumonía no especificada"),
    ("N39.0", "Infección de vías urinarias"),
    ("S09.9", "Traumatismo craneal no especificado"),
]

NIVEL_CONCIENCIA: list[str] = [
    "Alerta",
    "Responde a voz",
    "Responde al dolor",
    "No responde",
]

# Máquina de estados del triaje (HU-E2-06 CA1) y transiciones válidas (CA2).
ESTADOS_TRIaje: list[str] = [
    "Registrado",
    "SignosVitales",
    "EvaluacionClinica",
    "ClasificacionIA",
    "ValidacionProfesional",
    "Cerrado",
    "Reclasificado",
]

TRANSICIONES_VALIDAS: dict[str, set[str]] = {
    "Registrado": {"SignosVitales"},
    "SignosVitales": {"EvaluacionClinica"},
    "EvaluacionClinica": {"ClasificacionIA"},
    "ClasificacionIA": {"ValidacionProfesional"},
    "ValidacionProfesional": {"Cerrado"},
    "Cerrado": {"Reclasificado"},
    "Reclasificado": set(),
}

# Rangos fisiológicos (HU-E2-04): {campo: (min, max, unidad, prioritaria)}
RANGOS_SIGNOS: dict[str, tuple[float, float, str, bool]] = {
    "temperatura": (34.0, 43.0, "°C", True),
    "frecuencia_cardiaca": (20, 300, "lpm", False),
    "frecuencia_respiratoria": (4, 60, "rpm", True),
    "saturacion_o2": (50, 100, "%", True),
    "presion_sistolica": (40, 300, "mmHg", True),
    "presion_diastolica": (20, 200, "mmHg", False),
    "peso": (1.0, 400.0, "kg", False),
    "talla": (0.3, 2.5, "m", False),
}
