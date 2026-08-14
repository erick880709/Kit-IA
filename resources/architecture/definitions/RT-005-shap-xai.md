# RT-005: Explicabilidad con SHAP

**Tipo:** Requisito técnico
**Categoría:** Arquitectura
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §6 · `context/contexto-tfm.md` §6

## Descripción
La explicabilidad del modelo se implementa con SHAP sobre el modelo ganador, con salida en lenguaje clínico y visualizaciones interpretables.

## Criterio medible / restricción concreta
- SHAP sobre el modelo ganador (post-selección).
- Salida: Top-5 a Top-10 variables con mayor influencia, en lenguaje clínico (ej. "saturación de O₂ baja (88%) fue el factor de mayor peso").
- Comparación implícita con criterio MTS/Manchester cuando coincida.
- La explicación forma parte del contrato de salida de toda predicción (RF-009).

## Impacto en la arquitectura
Añade un componente XAI post-inferencia; para late fusion con submodelo BERT puede requerir SHAP sobre el submodelo estructurado y atención/interpretación sobre el texto.

## Notas del analista
Referencia: Lee, Lee & Shin 2022 (SHAP sobre modelo de triaje). Detalle de variables por signo en RF-XAI-003/004.
