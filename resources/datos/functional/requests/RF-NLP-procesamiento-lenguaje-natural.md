# RF-NLP: Procesamiento de Lenguaje Natural

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 44, Módulo NLP; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md
**Prioridad:** Alta

## Descripción
El sistema procesará automáticamente el texto clínico no estructurado (motivo de consulta en texto libre y observaciones de enfermería) transformándolo en representaciones numéricas (embeddings) que el modelo de IA pueda utilizar como features de entrada. Este módulo es esencial para la arquitectura multimodal, ya que sin él el modelo operaría únicamente con datos estructurados.

## Actores involucrados
- Sistema (automático)

## Criterios de aceptación

**RF-NLP-001 — Procesar Texto Libre:**
- El sistema procesa automáticamente las notas clínicas al ejecutar la inferencia.
- El procesamiento es transparente para el usuario clínico.

**RF-NLP-002 — Generar Embeddings:**
- Transformación del texto clínico en representaciones numéricas vectoriales utilizando un modelo de lenguaje clínico.
- Modelo objetivo: BERT clínico afinado en español médico (evaluar BioBERT-es o equivalente).
- Los embeddings se generan como parte del pipeline de inferencia, no como preprocesamiento offline.

**RF-NLP-003 — Limpieza del Texto:**
- Normalización de caracteres (unicode, tildes, mayúsculas/minúsculas).
- Eliminación de caracteres inválidos o no informativos.
- Tokenización del texto.
- Lematización cuando aplique (español).

**RF-NLP-004 — Detección de Texto Vacío:**
- Si el campo de texto libre está vacío, el pipeline continúa utilizando únicamente las variables estructuradas.
- No se genera error ni se bloquea la inferencia.
- Se registra en los metadatos de la predicción que la inferencia se ejecutó sin features de texto.

**RF-NLP-005 — Idioma:**
- El sistema asume español como idioma principal para el procesamiento de texto.
- El modelo NLP debe estar optimizado para texto clínico en español colombiano.

## Dependencias / relacionados
- RF-EVA-001: Captura de motivo de consulta (texto libre).
- RF-EVA-007: Captura de observaciones clínicas (texto libre).
- RF-IA-001: El pipeline NLP se ejecuta como parte de la inferencia.
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`: arquitectura de fusión early/late y especificación técnica de embeddings.

## Notas del analista
- La elección del modelo NLP específico (BioBERT-es vs. otro) queda como decisión experimental de la Fase 3, pero el contrato funcional (entrada: texto libre → salida: vector de embeddings) es fijo.
- La capacidad de operar sin texto (RF-NLP-004) es crítica para entornos clínicos reales donde el texto libre puede no estar disponible por urgencia de la atención.
