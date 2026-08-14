# RT-001: Arquitectura Multimodal — Early Fusion y Late Fusion

**Tipo:** Requisito técnico
**Categoría:** Arquitectura de IA / Modelado
**Fuente:** 01-CONTEXTO-MAESTRO-CONSOLIDADO.md §3; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §2; CONTEXTO_TRIAJE.txt v2.0 §5

## Descripción
Se implementarán, entrenarán, evaluarán y compararán **ambas** estrategias de fusión multimodal (early fusion y late fusion). No se elige una a priori: ambas se desarrollan en paralelo y la selección del modelo ganador se basa en resultados empíricos, con criterio principal de mejor Recall en Niveles I-II sin descuidar el F1 global.

## Criterio medible / restricción concreta

### Opción A — Early Fusion
- Vector de features estructuradas (signos vitales, demográficos, antecedentes, vía de llegada, etc.) concatenado con el vector de embeddings del texto clínico.
- Clasificador sobre el vector combinado: XGBoost o Random Forest como primera opción; red neuronal densa como alternativa.
- Entrada única al modelo, una sola fase de entrenamiento.

### Opción B — Late Fusion
- Submodelo A (estructurado): XGBoost o Random Forest sobre features tabulares.
- Submodelo B (texto): BERT clínico (BioBERT-es o equivalente afinado en español médico) + capa clasificadora.
- Combinación de salidas: promedio ponderado, stacking (meta-clasificador) o regresión logística sobre las probabilidades de ambos submodelos — el método específico se determina empíricamente en Fase 3.
- Cada submodelo se entrena por separado; la combinación se optimiza sobre el conjunto de validación.

### Regla de selección del modelo ganador
- Mejor **Recall en Niveles I y II** (prioridad clínica).
- Como criterio secundario, mejor F1-score global.
- Se documenta la comparativa completa (no solo el ganador) en el Capítulo 5 del TFM.
- Ambas arquitecturas coexisten como versiones distintas del modelo (RNA-006, RF-MOD-*) durante la fase de validación.

### Baselines obligatorios
- Modelos unimodales (solo datos estructurados, sin texto): Regresión Logística, Random Forest, XGBoost.
- Estos baselines son necesarios para poder afirmar que el enfoque multimodal aporta valor sobre el enfoque tradicional.

## Impacto en la arquitectura
- El pipeline de datos debe generar dos representaciones: vector estructurado (numérico + one-hot) y vector de embeddings (texto).
- El servicio de inferencia debe poder cargar y ejecutar tanto modelos de early fusion como de late fusion.
- El módulo de gestión de modelos (RF-MOD-*) debe soportar el registro de ambas arquitecturas como versiones diferentes.
- La comparación de modelos (RF-IA-007) se implementa como una funcionalidad que ejecuta ambos pipelines sobre el mismo conjunto de datos y presenta métricas lado a lado.

## Notas del analista
- Esta decisión está **cerrada** en `CONTEXTO_TRIAJE.txt` v2.0 (16 jul 2026) y `01-CONTEXTO-MAESTRO-CONSOLIDADO.md`. No es una decisión pendiente.
- El método de combinación en late fusion (promedio ponderado vs. stacking vs. meta-clasificador) **sí está abierto** y se determina empíricamente. Es uno de los pendientes listados en `05-PENDIENTES-PARA-DIRECTORA.md` (#4).
- Implementar ambas arquitecturas duplica el esfuerzo de entrenamiento pero triplica el valor académico del TFM (comparativa experimental sólida).
