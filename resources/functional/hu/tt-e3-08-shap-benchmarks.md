---
id: TT-E3-08
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 5
---

# TT-E3-08: Generación de SHAP y comparativa contra benchmarks

## Descripción
Generar explicaciones SHAP del modelo ganador (TreeExplainer para XGBoost/RF — RT-005) y producir la comparativa contra los benchmarks de la literatura (RT-008: CTAS 0.882, Hong 0.93, Ueareekul 0.917, Levin F1 0.81).

## Criterios de Done
- [ ] Top 5-10 variables SHAP por predicción, con mapeo a lenguaje clínico.
- [ ] Artefactos SHAP guardados en `artifacts/shap/`.
- [ ] Tabla comparativa vs benchmarks con mismas métricas (AUC-ROC, F1).
- [ ] Análisis de variables de mayor peso vs literatura (SpO₂, FR, temperatura, PA sistólica, edad, vía de llegada).

## Dependencias
TT-E3-07
