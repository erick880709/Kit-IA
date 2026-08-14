---
id: TT-E3-09
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 3
---

# TT-E3-09: Serialización del Modelo Ganador para la Demo

## Descripción
Implementar el paso 13 del pipeline: serializar el modelo ganador junto con todos los transformadores necesarios (scaler, encoder, tokenizador NLP) y sus metadatos, en un formato que la demo (E4) pueda cargar con un solo comando.

## Criterios de Done
- [ ] Modelo serializado en formato compatible con la demo: joblib para sklearn/XGBoost, o SavedModel para TF/PyTorch
- [ ] Transformadores serializados junto al modelo: StandardScaler, OneHotEncoder, Tokenizador NLP
- [ ] Archivo `model_metadata.json` con: nombre, versión, algoritmo, arquitectura, fecha de entrenamiento, métricas (F1, Precision, Recall, AUC-ROC, AUPRC), umbrales por clase, fuentes de datos usadas, hiperparámetros
- [ ] Script `load_model.py` que carga el modelo + transformadores y expone una función `predict(datos_paciente) -> resultado`
- [ ] Test de carga: verificar que el modelo cargado produce la misma predicción que el modelo original para 10 instancias de prueba

## Dependencias
TT-E3-07 (modelo ganador con evaluación final)

## Subtareas
- [ ] Serializar modelo y transformadores
- [ ] Generar model_metadata.json
- [ ] Implementar load_model.py
- [ ] Test de reproducibilidad
