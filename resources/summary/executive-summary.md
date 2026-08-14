# Resumen Ejecutivo — Sistema de Triaje Multimodal basado en IA (Colombia)

**Fecha de extracción:** 2026-08-13
**Origen:** `context/` (13 documentos: 00-07, brief_finalizacion_tfm.md, CONTEXTO TRIAJE.txt v2.0, CONTEXT TRIA.txt, contexto-tfm.md, extension-orquestador-tfm-ml.md)

## Ficha del proyecto

| Campo | Valor |
|---|---|
| Título | Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia |
| Cliente / institución | TFM — Máster Universitario en Inteligencia Artificial, UNIR |
| Autores | Medina Betancur, D. · Rivera Villanueva, L. · Soto Díaz, E. (orden alfabético) |
| Directora | Damaris Fuentes Lorenzo |
| Tipología | Tipo 2 (Desarrollo software) + Tipo 3 (Piloto experimental/comparativa) |
| Alcance | Modelo offline entrenado/evaluado + demo funcional interactiva (apoyo a decisión clínica, nunca autónomo) |

## Objetivo del sistema

Dado un conjunto de datos de un paciente en urgencias (signos vitales, dolor, demográficas, antecedentes, motivo de consulta en texto libre), predecir el nivel de triaje I–V según la **Resolución 5596 de 2015**, con salida explicable (SHAP) y registro de auditoría, dejando siempre la decisión final en el profesional.

## Metas cuantitativas

F1 ≥ 0,82 · Precisión ≥ 0,85 · Recall ≥ 0,80 · AUC-ROC ≥ 0,87 — con evaluación **por clase** (Nivel I es raro pero crítico).

## Decisiones técnicas cerradas

- **Ambas arquitecturas de fusión** (early + late), se comparan y gana la de mejor Recall en Niveles I–II.
- **Umbral optimizado por clase** en Niveles I–II priorizando Recall (costo clínico del falso negativo).
- **Fuentes de datos:** MIMIC-IV-ED (base) + registro Hospital San Juan de Dios (fine-tuning, autorización ética **aprobada**) + datos.gov.co (triage, BDUA) + Supersalud (contexto).
- **XAI:** SHAP con explicación en lenguaje clínico; tiempo de inferencia objetivo < 3 s.
- **Demo:** Streamlit o Flask — **decisión pendiente de la directora**.

## Resultado de la extracción

| Categoría | Cantidad | Ubicación |
|---|---|---|
| Requerimientos funcionales (RF) | 16 | `resources/functional/requests/` |
| Requerimientos no funcionales (RNF) | 9 | `resources/architecture/definitions/` |
| Requisitos técnicos (RT) | 10 | `resources/architecture/definitions/` |
| Información de diseño (RD) | 6 | `resources/design/models/` |

## Hallazgos de fuentes complementarias (`resources/datos/`, validación 2026-08-13)

- `resources/datos/` contiene una **extracción previa completa** (2026-07-19): 7 RNF + 7 RT, 41 HU/TT (`functional/hu/`), 8 épicas Jira (`epicas-tfm-jira.csv`, `historias-jira-t2.csv`) y un consolidado de cambios pendientes. Se validó contra la extracción de este documento y se integró lo que complementa:
  - **RNF-002** enriquecido con RNP-002/003/004 (concurrencia, consultas <1 s, SHAP no bloqueante).
  - **RNF-009** nuevo (disponibilidad/escalabilidad, modo degradado sin IA).
  - **RT-007** enriquecido con el entorno de despliegue de la demo (SQLite, local sin GPU, datos sintéticos, un solo comando).
  - **RF-001/RD-002** con los 9 campos de paciente pendientes (TT-E7-01..03) y catálogos Colombia.
  - **RF-014** con RBAC, hash de contraseñas, TLS y cifrado en reposo (épica E1).
  - **RF-002** con máquina de 7 estados del evento de triaje (épica E2).
- **Validación con datos reales:** el dataset de triaje descargado (89.453 eventos) muestra Nivel III = 88,5 %, IV = 7,8 %, II = 3,0 %, V = 0,5 %, I = 0,2 % — el desbalance real es más severo que el supuesto inicial y el Nivel I es extremadamente raro (ver RNF-004).
- La extracción previa referencia un codebase `sistema-triaje-ia/` que **no existe en este workspace** — los cambios TT-E7-* son especificaciones pendientes, no evidencia de código existente.

## Cierre de ambigüedades con los datasets (janus sobre `datasets/`, 2026-08-13)

| Ambigüedad previa | Resultado del análisis de datos |
|---|---|
| ¿Qué distribución real de niveles I-V hay en Colombia? | III 88,5 % · IV 7,8 % · II 3,0 % · V 0,5 % · I 0,2 % (89.453 eventos); el hospital local replica la misma distribución (RNF-004) |
| ¿Los tiempos normativos 5596 se cumplen en la operación? | Solo Nivel II cumple (22 min ≤ 30 min); Nivel I espera 28 min de mediana con norma "inmediata" (RD-001) — evidencia del problema para Cap. 2 |
| ¿De dónde sale el dataset local del hospital? | El CSV custom es el mismo cohorte de la morbilidad RIPS pública (43.594 episodios, mismos diagnósticos top) + etiqueta de triaje (RT-006) |
| ¿Hay demográficas en fuentes locales? | Sí: SEXO, EDAD, DEPARTAMENTO, REGIMEN por episodio en morbilidad (RD-002) |
| ¿Hay signos vitales en fuentes locales? | No — confirmado en las 4 fuentes locales; MIMIC-IV-ED sigue siendo imprescindible para features (RT-006) |
| Calidad de datos para la ingesta | REGIMEN con typos; ~130 filas con AÑO corrupto (2027-2358); fechas fantasma 01/01/1900 (RF-016) |

**Ambigüedades que los datasets NO pueden cerrar:** stack de la demo (Streamlit/Flask), método de combinación late fusion, reflejo de la aprobación ética en el PDF, y RIPS `xveb-6jax` (403) — siguen pendientes de decisión humana o del portal.

## Decisiones pendientes (requieren humano)

1. ~~Stack de la demo: Streamlit vs Flask.~~ ✅ **Resuelto por refinador (2026-08-13): Streamlit.**
2. Reflejar la aprobación ética en el PDF del TFM (Cap. 3).
3. Actualizar RF-IA-003 del documento funcional (umbral por clase, no argmax puro).
4. Método de combinación en late fusion (experimental, Fase 3).
5. Pendientes normativos UNIR: sección grupal, orden de autores, anti-plagio.

## Glosario mínimo

- **Triaje:** clasificación de pacientes por prioridad clínica (Resolución 5596/2015, 5 niveles).
- **Early fusion:** concatenación de features estructuradas + embeddings antes del clasificador.
- **Late fusion:** submodelos independientes (estructurado + texto) combinados a nivel de decisión.
- **SHAP:** método de explicabilidad aditivo basado en valores de Shapley.
- **CTAS/MTS:** sistemas estándar de triaje canadiense / Manchester usados como benchmark.
- **BDUA:** Base de Datos Única de Afiliados (régimen de afiliación en salud, Colombia).
