---
id: TT-E3-03
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 8
---

# TT-E3-03: Generación de embeddings NLP con BERT clínico en español

## Descripción
Implementar el módulo NLP (RF-005, RT-003): limpieza de texto, tokenización y generación de embeddings con BERT clínico en español (evaluar BioBERT-es o equivalente; alternativas ligeras distilBERT/BETO por RNP-001).

## Criterios de Done
- [ ] Detección de texto vacío → pipeline continúa con estructuradas (RF-NLP-004).
- [ ] Idioma español como principal (RF-NLP-005).
- [ ] Embeddings cacheados por texto para la demo (inferencia < 3 s).
- [ ] Notebook de evaluación del modelo NLP elegido (dimensión, latencia, calidad).

## Dependencias
TT-E3-02

## Subtareas
- [ ] Limpieza y tokenización de notas
- [ ] Selección y descarga del modelo BERT clínico español
- [ ] Cache de embeddings
