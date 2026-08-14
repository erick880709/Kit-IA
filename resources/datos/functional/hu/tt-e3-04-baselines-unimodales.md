---
id: TT-E3-04
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 5
---

# TT-E3-04: Entrenamiento de Baselines Unimodales

## Descripción
Implementar el paso 7 del pipeline: entrenar y evaluar 3 modelos baseline usando únicamente datos estructurados (sin embeddings de texto). Estos baselines son necesarios para demostrar que el enfoque multimodal aporta valor (ΔF1 ≥ 0.03 sobre el mejor baseline).

## Criterios de Done
- [ ] Split train/test estratificado por nivel de triaje (80/20)
- [ ] 10-fold cross-validation sobre el conjunto de entrenamiento
- [ ] Modelos baseline entrenados y evaluados:
  - Regresión Logística (multinomial, class_weight='balanced')
  - Random Forest (n_estimators=100, class_weight='balanced')
  - XGBoost (objective='multi:softprob', eval_metric='mlogloss')
- [ ] Métricas reportadas para cada baseline: Accuracy, Precision, Recall, F1 (macro y por clase), AUC-ROC (macro), AUPRC (Niveles I y II)
- [ ] Comparativa de baselines: tabla y gráfico de barras con F1 por clase
- [ ] Selección del mejor baseline como referencia para comparar contra early/late fusion

## Dependencias
TT-E3-02 (features estructuradas listas)

## Subtareas
- [ ] Implementar split estratificado y 10-fold CV
- [ ] Entrenar y evaluar Regresión Logística
- [ ] Entrenar y evaluar Random Forest
- [ ] Entrenar y evaluar XGBoost
- [ ] Generar comparativa de baselines
