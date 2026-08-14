---
id: TT-E3-04
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 5
---

# TT-E3-04: Entrenamiento de 3 baselines unimodales

## Descripción
Entrenar y evaluar los baselines obligatorios (RT-004): Regresión Logística, Random Forest y XGBoost sobre solo datos estructurados, con 10-fold CV estratificado.

## Criterios de Done
- [ ] Split train/test estratificado por nivel de triaje.
- [ ] Métricas por clase + macro: precisión, recall, F1, AUC-ROC, AUPRC (RNF-005).
- [ ] Manejo del desbalance documentado: class weights / SMOTE comparados (RNF-004).
- [ ] Artefactos de métricas guardados en `artifacts/metrics/` para validacion-cientifica-ml.

## Dependencias
TT-E3-02
