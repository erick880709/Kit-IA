---
id: TT-E3-03
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 8
---

# TT-E3-03: Generación de Embeddings NLP con BERT Clínico

## Descripción
Implementar el paso 5 del pipeline: procesamiento de texto libre (motivo de consulta y notas clínicas) mediante un modelo BERT clínico en español (BioBERT-es o BETO), generando vectores de embeddings que alimentan la arquitectura multimodal.

## Criterios de Done
- [ ] Selección y justificación del modelo NLP (BioBERT-es, BETO, o similar) documentada
- [ ] Preprocesamiento de texto: normalización Unicode, lowercase, eliminación de caracteres especiales, tokenización
- [ ] Generación de embeddings: vector de dimensión fija (768 para BERT base) por cada texto clínico
- [ ] Manejo de texto vacío: si el campo está vacío, se genera un vector de ceros (o se omite la rama NLP en late fusion)
- [ ] Los embeddings se generan offline y se almacenan como features adicionales en el dataset
- [ ] El tokenizador y el modelo NLP se serializan junto con el modelo para reproducibilidad en la demo
- [ ] Tiempo de generación de embeddings documentado (para planificar RT-001: <3s en inferencia online)

## Dependencias
TT-E3-02 (datos limpios y normalizados)

## Subtareas
- [ ] Evaluar y seleccionar modelo NLP (BioBERT-es vs BETO vs alternativas)
- [ ] Implementar preprocesamiento de texto clínico en español
- [ ] Implementar generación de embeddings
- [ ] Implementar manejo de texto vacío
- [ ] Serializar tokenizador y modelo NLP
- [ ] Documentar tiempo de generación de embeddings por texto
