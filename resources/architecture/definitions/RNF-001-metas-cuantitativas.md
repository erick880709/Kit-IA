# RNF-001: Metas Cuantitativas de Desempeño del Modelo

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento
**Fuente:** `context/01-CONTEXTO-MAESTRO-CONSOLIDADO.md` §4 · `context/contexto-tfm.md` §4

## Descripción
El modelo de clasificación debe alcanzar las metas cuantitativas definidas y consistentes en todos los documentos del proyecto.

## Criterio medible / restricción concreta
- F1-score ≥ 0,82
- Precisión ≥ 0,85
- Recall ≥ 0,80
- AUC-ROC ≥ 0,87

## Impacto en la arquitectura
Define el umbral de éxito para la selección del modelo ganador y condiciona la comparativa early vs late fusion. Las metas globales no son suficientes: ver [[RNF-005]].

## Notas del analista
Metas consistentes entre contexto-tfm.md, CONTEXTO TRIAJE.txt y el PDF del TFM — sin cambios.
