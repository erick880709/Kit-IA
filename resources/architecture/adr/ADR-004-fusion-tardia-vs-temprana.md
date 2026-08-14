# ADR-004: Fusión tardía como candidata principal (comparada con fusión temprana)

- **Estado:** Aceptado
- **Fecha:** 2026-08-13
- **Decisión relacionada en el documento:** `Documento_Arquitectura_TriajeIA.md` §5.2, §7 y `Arquitectura_Modelos_TriajeIA.md`

## Contexto

RT-002 exige implementar y comparar **ambas** estrategias de fusión multimodal (estructurado + texto). El TFM estudia cuál aporta mejor desempeño; no es solo una decisión de implementación.

## Decisión

1. Entrenar y evaluar **fusión temprana** (concatenación de features + clasificador único) y **fusión tardía** (submodelo XGBoost para estructurado + BERT clínico para texto, combinados con meta-modelo de Regresión Logística, RT-010).
2. La **tardía es la candidata principal** para producción/demo por modularidad e interpretabilidad por submodelo.
3. La comparación se valida con test estadístico (McNemar entre pares), no solo con diferencia de métricas.

## Alternativas consideradas

- **Solo fusión temprana:** más simple, pero un solo clasificador mezcla modalidades y dificulta atribuir errores por submodelo.
- **Solo texto o solo estructurado:** descartado — el aporte incremental de cada modalidad es parte de la pregunta de investigación.

## Consecuencias

- **Positivas:** explicabilidad por submodelo (SHAP TreeExplainer + SHAP de transformers), aislamiento de fallos, alineación con la literatura de triaje multimodal.
- **Negativas:** dos pipelines de entrenamiento a mantener; costo asumido porque es el objeto de estudio del TFM.
