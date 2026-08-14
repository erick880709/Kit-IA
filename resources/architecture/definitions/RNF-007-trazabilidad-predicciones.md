# RNF-007: Trazabilidad de Predicciones

**Tipo:** Requerimiento no funcional
**Categoría:** Seguridad / Cumplimiento normativo
**Fuente:** `context/CONTEXTO TRIAJE.txt` §9 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §7 · `context/CONTEXT TRIA.txt` (RNA-010, RNAU-*)

## Descripción
Cada predicción debe quedar registrada de forma permanente para auditoría clínica y detección de deriva del modelo.

## Criterio medible / restricción concreta
- Todo registro incluye: nivel sugerido, probabilidades, versión del modelo, confianza y tiempo de inferencia (RNA-002, RF-IA-004/005/006).
- El registro del evento de triaje incluye nivel IA vs. nivel humano y motivo de discrepancia (RF-010).
- Los registros permiten reconstruir qué modelo y qué umbral se usó en cada caso.

## Impacto en la arquitectura
Exige persistencia inmutable (append-only) del registro de predicciones y versionado estricto de modelos y umbrales.

## Notas del analista
La trazabilidad es también el habilitador funcional de la comparativa IA vs. profesional (RF-013).
