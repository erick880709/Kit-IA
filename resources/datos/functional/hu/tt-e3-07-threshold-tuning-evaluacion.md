---
id: TT-E3-07
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 5
---

# TT-E3-07: Threshold Tuning por Clase y Evaluación Final

## Descripción
Implementar los pasos 9 y 10 del pipeline: optimizar el umbral de decisión para maximizar Recall en Niveles I-II sobre el modelo ganador, y ejecutar la evaluación final completa sobre el conjunto de test.

## Criterios de Done
- [ ] Threshold tuning sobre el conjunto de validación para el modelo ganador
- [ ] Para Niveles I y II: buscar el umbral que maximice Recall, documentando el trade-off con Precision
- [ ] Para Niveles III-V: umbral estándar (argmax)
- [ ] Umbrales óptimos almacenados como metadatos del modelo
- [ ] Evaluación final sobre conjunto de test (nunca usado durante entrenamiento/validación):
  - Matriz de confusión 5×5 (valores absolutos y normalizada)
  - Métricas por clase: Precision, Recall, F1, AUC-ROC
  - Macro-promedio y weighted-promedio
  - AUPRC para Niveles I y II
- [ ] Comparativa de métricas con y sin threshold tuning (demostrar la mejora en Recall I-II)

## Dependencias
TT-E3-06 (modelo ganador seleccionado)

## Subtareas
- [ ] Implementar threshold tuning sobre curva ROC/PR por clase
- [ ] Implementar evaluación final sobre test set
- [ ] Generar matriz de confusión y métricas por clase
- [ ] Documentar trade-off Precision vs Recall para Niveles I-II
