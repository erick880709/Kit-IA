---
id: TT-E3-05
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 8
---

# TT-E3-05: Entrenamiento de Arquitectura Early Fusion

## Descripción
Implementar el paso 8 (parte A) del pipeline: concatenar el vector de features estructuradas con el vector de embeddings de texto, y entrenar un clasificador XGBoost o red neuronal densa sobre el vector combinado.

## Criterios de Done
- [ ] Concatenación de features estructuradas (numéricas + one-hot) con embeddings NLP (768 dims)
- [ ] Entrenamiento con XGBoost sobre vector combinado (principal) y red neuronal densa (alternativa)
- [ ] Manejo de desbalance: class_weight='balanced' en XGBoost, class weights en red neuronal
- [ ] 10-fold CV con las mismas particiones que los baselines (para comparabilidad)
- [ ] Métricas reportadas: Accuracy, Precision, Recall, F1 (macro y por clase), AUC-ROC (macro), AUPRC (I, II)
- [ ] Comparativa contra mejor baseline unimodal: ¿ΔF1 ≥ 0.03?
- [ ] Documentación de hiperparámetros óptimos encontrados

## Dependencias
TT-E3-03 (embeddings NLP), TT-E3-04 (split de datos y baselines)

## Subtareas
- [ ] Implementar concatenación de features
- [ ] Entrenar XGBoost early fusion
- [ ] Entrenar red neuronal densa (alternativa)
- [ ] Evaluar y comparar contra baseline
- [ ] Documentar hiperparámetros
