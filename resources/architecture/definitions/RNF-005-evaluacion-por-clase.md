# RNF-005: Evaluación por Clase y Reproducibilidad

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento
**Fuente:** `context/01-CONTEXTO-MAESTRO-CONSOLIDADO.md` §4 · `context/contexto-tfm.md` §6

## Descripción
La evaluación del modelo no puede basarse solo en métricas globales; debe ser por clase y reproducible.

## Criterio medible / restricción concreta
- Matriz de confusión y métricas (precision/recall/F1/AUC-ROC) por nivel (I–V) y macro.
- AUPRC adicional para clases minoritarias.
- Validación con split train/test + **10-fold cross-validation** estratificada.
- Un F1 global alto no debe ocultar mal desempeño en Nivel I.

## Impacto en la arquitectura
Exige un módulo de evaluación parametrizable (por clase, CV estratificado) y almacenamiento de artefactos de evaluación para el TFM.

## Notas del analista
La reproducibilidad también requiere trazabilidad de experimentos (MLflow/DVC) — cubierta por el skill `validacion-cientifica-ml` en fases posteriores.
