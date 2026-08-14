# RF-007: Selección de Nivel con Umbral Optimizado por Clase

**Tipo:** Requerimiento funcional
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §3 (corrige RF-IA-003) · `context/CONTEXTO TRIAJE.txt` §6
**Prioridad:** Alta

## Descripción
El sistema debe seleccionar el nivel de triaje sugerido aplicando umbrales de decisión optimizados por clase: en Niveles I y II el umbral se calibra para **maximizar Recall** (aunque baje levemente la Precisión), y en Niveles III–V se usa el argmax estándar. Las probabilidades de todos los niveles deben permanecer visibles.

## Actores involucrados
Sistema (selección automática), médico (validación final, ver RF-011).

## Criterios de aceptación
- La clase sugerida NO es necesariamente el argmax puro cuando el umbral optimizado de Niveles I–II lo modifica.
- Las probabilidades de los 5 niveles se muestran siempre.
- El punto de equilibrio de cada umbral queda documentado (ROC/PR por clase).

## Dependencias / relacionados
[[RNF-003]], [[RT-009]], RD-003.

## Notas del analista
**Contradicción resuelta:** RF-IA-003 del documento funcional dice "clase con mayor probabilidad" (argmax). Esta interpretación corrige y prevalece (00-VALIDACION hallazgo #5). Pendiente actualizar el texto fuente en `CONTEXT TRIA.txt`.
