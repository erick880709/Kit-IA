# RT-002: Arquitectura Multimodal — Early y Late Fusion (ambas)

**Tipo:** Requisito técnico
**Categoría:** Arquitectura
**Fuente:** `context/CONTEXTO TRIAJE.txt` §5 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §2

## Descripción
Se implementan, evalúan y comparan **ambas** estrategias de fusión multimodal; gana la de mejor Recall en Niveles I–II sin descuidar F1 global.

## Criterio medible / restricción concreta
- **Early fusion:** vector de features estructuradas + embedding de texto concatenados antes del clasificador (XGBoost/RF sobre vector combinado, o red densa).
- **Late fusion:** Submodelo A (estructurado → XGBoost/RF) + Submodelo B (texto → BERT clínico + clasificador), combinados por promedio ponderado, stacking o meta-clasificador (método a determinar empíricamente — ver RT-010).
- Ambas arquitecturas coexisten como versiones del modelo durante la validación (RNA-006, RF-MOD-*).

## Impacto en la arquitectura
Define la estructura del pipeline de entrenamiento y el diseño de gestión de modelos; obliga a interfaces comunes de features y de salida para poder comparar.

## Notas del analista
Decisión cerrada en v2.0 (16 jul 2026). El documento funcional (CONTEXT TRIA.txt) no explicitaba esta dualidad — hallazgo #4 de la validación.
