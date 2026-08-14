---
id: TT-E3-02
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 5
---

# TT-E3-02: Pipeline de limpieza, normalización y feature engineering

## Descripción
Implementar limpieza (imputación de nulos, outliers), normalización de numéricas, one-hot/codificación de categóricas y construcción del vector de features estructuradas (pasos 3-4 del pipeline, RF-016).

## Criterios de Done
- [ ] Reglas de calidad RNQ-001/003/004 implementadas como validaciones previas.
- [ ] `ViaLlegada` como catálogo controlado (RNQ-004).
- [ ] Imputación documentada por variable (mediana/kNN/indicador de missing).
- [ ] Config de features versionable (YAML) para reproducibilidad.
- [ ] Tests unitarios de cada transformador (patrón sklearn Transformer).

## Dependencias
TT-E3-01
