---
id: TT-E3-09
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 3
---

# TT-E3-09: Serialización del modelo ganador + transformadores

## Descripción
Serializar el modelo ganador junto con sus transformadores de features, umbrales por clase y metadatos (versión, algoritmo, fecha) para que la demo lo cargue sin re-entrenar (RT-007).

## Criterios de Done
- [ ] Artefacto único versionado (`artifacts/models/modelo-<version>.*`).
- [ ] Pipeline completo serializable (preprocesadores + modelo + umbrales + NLP cache).
- [ ] Manifiesto de versión con métricas resumidas y hash de integridad.
- [ ] Test de carga y predicción con el artefacto.

## Dependencias
TT-E3-07
