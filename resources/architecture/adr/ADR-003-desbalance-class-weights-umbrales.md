# ADR-003: Manejo de desbalance — class weights + umbrales por clase (no SMOTE por defecto)

- **Estado:** Aceptado
- **Fecha:** 2026-08-13
- **Decisión relacionada en el documento:** `Documento_Arquitectura_TriajeIA.md` §5.3 y §11

## Contexto

La distribución real de triaje es extrema: III 88.5%, IV 7.8%, II 3.0%, V 0.5%, I 0.2% (RNF-004). Un clasificador entrenado sin tratamiento tiende a predecir siempre III. Además, el costo clínico de subclasificar riesgo vital (I/II) es el más alto (RNF-003: recall I–II prioritario).

## Decisión

1. `class_weight="balanced"` (o pesaje explícito por clase) en el entrenamiento de los submodelos.
2. Ajuste de umbrales por clase (threshold tuning, RT-009) optimizando recall en I–II sin desplomar precisión global, validado solo sobre el conjunto de validación.
3. SMOTE u oversampling sintético **no** se usa por defecto: se evalúa como experimento controlado.

## Alternativas consideradas

- **SMOTE/ADASYN:** riesgo de sobreajuste y de correlaciones artificiales en datos clínicos con solapamiento; se reserva como experimento.
- **Undersampling:** descarta datos reales valiosos en clases ya minoritarias.
- **Focal loss:** requiere red neuronal; no aplica a los baselines clásicos (LR/RF/XGBoost).

## Consecuencias

- **Positivas:** control fino del recall en las clases críticas; decisiones inspeccionables por clase.
- **Negativas:** umbrales deben re-calibrarse en cada reentrenamiento y documentarse junto al modelo (MLflow).
