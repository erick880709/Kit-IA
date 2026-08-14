---
id: TT-E3-08
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 5
---

# TT-E3-08: SHAP y Comparativa contra Benchmarks

## Descripción
Implementar los pasos 11 y 12 del pipeline: generar explicaciones SHAP globales y por instancia para el modelo ganador, y comparar sus métricas contra los benchmarks de la literatura (CTAS AUROC 0.882, Raita 2019, Hong 2018, Ueareekul 2024, Levin 2021).

## Criterios de Done
- [ ] SHAP TreeExplainer (si el modelo ganador es RF/XGBoost) o KernelExplainer (si es red neuronal)
- [ ] Summary plot: top 15 variables globales por importancia SHAP
- [ ] Waterfall plot para 5 instancias de ejemplo (una por nivel de triaje)
- [ ] Dependence plot para las 3 variables más importantes
- [ ] Tabla comparativa: métricas de este proyecto vs. CTAS (0.882), Raita (0.87), Hong (0.93), Ueareekul (0.917 AUROC, 0.629 AUPRC), Levin (F1 0.81)
- [ ] Discusión de resultados: ¿el modelo es competitivo con el estado del arte? ¿En qué nivel(es) destaca o falla?

## Dependencias
TT-E3-07 (modelo ganador con métricas finales)

## Subtareas
- [ ] Generar SHAP summary plot
- [ ] Generar waterfall plots por nivel
- [ ] Generar dependence plots
- [ ] Construir tabla comparativa contra literatura
- [ ] Redactar discusión de resultados
