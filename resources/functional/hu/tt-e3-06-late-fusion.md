---
id: TT-E3-06
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 8
---

# TT-E3-06: Entrenamiento de arquitectura Late Fusion

## Descripción
Entrenar la Opción B de RT-002: submodelo A (estructurado → XGBoost/RF) + submodelo B (texto → BERT + clasificador), con combinación configurable (promedio ponderado por defecto [SUPUESTO], stacking y meta-clasificador como experimentos — RT-010).

## Criterios de Done
- [ ] Estrategia de combinación parametrizable (patrón strategy).
- [ ] Submodelos guardados por separado + combinador serializado.
- [ ] Métricas por clase y por método de combinación guardadas.
- [ ] Comparativa documentada con Early Fusion (Cap. 5 del TFM).

## Dependencias
TT-E3-03 + TT-E3-04 + TT-E3-05

## Subtareas
- [ ] Submodelo estructurado
- [ ] Submodelo texto
- [ ] Combinadores (promedio/stacking/meta)
