# RF-009: Explicabilidad SHAP

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-XAI-001 a 006) · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §6
**Prioridad:** Alta

## Descripción
Toda predicción debe incluir explicación: Top-5 a Top-10 variables de mayor influencia (SHAP) en lenguaje clínico comprensible, separando impacto positivo y negativo, con visualizaciones interpretables, comparación implícita con el criterio MTS/Manchester cuando coincida, y posibilidad de exportar la explicación.

Cubre: RF-XAI-001 a RF-XAI-006.

## Actores involucrados
Médico (consulta de la explicación), sistema (generación).

## Criterios de aceptación
- Ninguna predicción se muestra sin explicación asociada (RF-XAI-001).
- Las variables se describen en lenguaje clínico (ej. "saturación de O₂ baja (88%) fue el factor de mayor peso"), no solo con el nombre técnico.
- Exportación de resultados disponible (RF-XAI-006).

## Dependencias / relacionados
[[RF-006]], [[RT-005]], RD-006.

## Notas del analista
El contrato de salida por predicción (02 §6) define 4 elementos: nivel + probabilidad + versión de modelo; top SHAP en lenguaje clínico; comparación MTS; tiempo de inferencia.
