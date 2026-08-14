---
id: TT-E3-05
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 8
---

# TT-E3-05: Entrenamiento de arquitectura Early Fusion

## Descripción
Entrenar la Opción A de RT-002: vector de features estructuradas + embeddings concatenados antes del clasificador (XGBoost/RF sobre vector combinado, o red densa).

## Criterios de Done
- [ ] Pipeline de features combinado estructuradas + embedding.
- [ ] Mismo esquema de validación que baselines (10-fold CV estratificado).
- [ ] Métricas por clase guardadas en `artifacts/metrics/`.
- [ ] Comparabilidad con Late Fusion garantizada (mismos splits y métricas).

## Dependencias
TT-E3-03 + TT-E3-04

## Subtareas
- [ ] Concatenador de features
- [ ] Entrenamiento XGBoost/RF sobre vector combinado
- [ ] Variante red densa (opcional)
