---
id: TT-E3-06
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 8
---

# TT-E3-06: Entrenamiento de Arquitectura Late Fusion

## Descripción
Implementar el paso 8 (parte B) del pipeline: entrenar dos submodelos independientes (XGBoost para datos estructurados, BERT + clasificador para texto) y combinar sus salidas.

[SUPUESTO] El método de combinación (promedio ponderado, stacking o meta-clasificador) se determina empíricamente. Se documenta cada opción evaluada.

## Criterios de Done
- [ ] Submodelo A (estructurado): XGBoost sobre features tabulares (mismo que el mejor baseline)
- [ ] Submodelo B (texto): BERT clínico + capa densa + softmax sobre 5 clases
- [ ] Evaluación de al menos 2 métodos de combinación: promedio ponderado y stacking con regresión logística
- [ ] 10-fold CV con las mismas particiones que baselines y early fusion
- [ ] Métricas reportadas para cada método de combinación
- [ ] Comparativa late fusion vs. early fusion vs. baseline: tabla completa lado a lado
- [ ] Selección del modelo ganador según criterio: mejor Recall en Niveles I-II sin descuidar F1 global

## Dependencias
TT-E3-03, TT-E3-04, TT-E3-05

## Subtareas
- [ ] Entrenar submodelo A (estructurado)
- [ ] Entrenar submodelo B (texto)
- [ ] Implementar promedio ponderado
- [ ] Implementar stacking con regresión logística
- [ ] Comparar late vs. early vs. baseline
- [ ] Seleccionar modelo ganador
