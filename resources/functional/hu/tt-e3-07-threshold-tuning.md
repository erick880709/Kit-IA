---
id: TT-E3-07
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 5
---

# TT-E3-07: Threshold tuning por clase y evaluación final

## Descripción
Optimizar el umbral de decisión por clase sobre la curva ROC/PR del modelo ganador (RT-009, RNF-003): maximizar Recall en Niveles I-II; argmax estándar para III-V; documentar el punto de equilibrio elegido.

## Criterios de Done
- [ ] Vector de umbrales por clase persistido junto a la versión del modelo.
- [ ] Evaluación final sobre test set con umbrales aplicados (matriz de confusión por nivel).
- [ ] Metas RNF-001 verificadas: F1 ≥ 0,82 · Precisión ≥ 0,85 · Recall ≥ 0,80 · AUC ≥ 0,87.
- [ ] Reporte del punto de equilibrio por clase.

## Dependencias
TT-E3-06
