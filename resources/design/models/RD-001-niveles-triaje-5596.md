# RD-001: Modelo Conceptual de Niveles de Triaje (Resolución 5596 de 2015)

**Tipo:** Información de diseño
**Fuente:** `context/CONTEXTO TRIAJE.txt` §2 · `context/contexto-tfm.md` §3

## Descripción
Los 5 niveles de triaje que el sistema debe clasificar, con sus tiempos máximos de atención, según la Resolución 5596 del 24 de diciembre de 2015 del Ministerio de Salud y Protección Social de Colombia.

| Nivel | Denominación | Tiempo máx. de atención |
|---|---|---|
| I | Resucitación (riesgo vital inminente) | Inmediata |
| II | Emergencia (deterioro rápido posible) | ≤ 30 min |
| III | Urgencia (requiere medidas en urgencias) | 2 a 4 horas |
| IV | Menor urgencia (estable, sin riesgo) | 4 a 12 horas |
| V | No urgencia (remitible a consulta externa) | 12 a 24 horas |

## Validación con datos reales (2026-08-13)

Tiempo real entre ingreso y atención en el dataset público de triaje (89.453 eventos, `datasets/clasificacion_triage_urgencias_20260813.csv`):

| Nivel | Norma 5596 | Mediana real | p90 real |
|---|---|---|---|
| I | Inmediata | 28 min | 119 min |
| II | ≤ 30 min | 22 min | 80 min |
| III | 2 a 4 h | 35 min | 130 min |
| IV | 4 a 12 h | 74 min | 188 min |
| V | 12 a 24 h | 79 min | 219 min |

**Lectura para el TFM:** el Nivel I real espera 28 min de mediana (119 min en p90) cuando la norma exige atención inmediata — evidencia cuantitativa del problema de saturación que motiva el sistema. El Nivel II cumple la norma. Insume directo del Cap. 2 (problema) y del dashboard (RF-013).

## Notas de diseño
- I y II = clínicamente críticos; IV y V = no urgentes; III es la "zona gris" con mayor valor de clasificación correcta.
- Nivel I es raro pero crítico → evaluación por clase obligatoria (RNF-005).
- Los tiempos (30 min/2 h/4 h/24 h) son la base de los indicadores del dashboard (RF-013).
