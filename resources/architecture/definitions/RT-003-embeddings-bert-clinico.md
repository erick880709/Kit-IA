# RT-003: Embeddings Clínicos en Español (BERT)

**Tipo:** Requisito técnico
**Categoría:** Stack tecnológico
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §1.2 · `context/CONTEXTO TRIAJE.txt` §4.2 · `context/contexto-tfm.md` §6

## Descripción
El texto clínico libre (motivo de consulta, notas de admisión, historia narrativa autorizada) se procesa con embeddings tipo BERT clínico, idealmente afinado en español médico.

## Criterio medible / restricción concreta
- Evaluar BioBERT-es o equivalente afinado en español médico (RF-NLP-002).
- Idioma principal del sistema: español (RF-NLP-005).
- Referencia de la literatura: Levin et al. 2021 (estructurado + BERT, F1 0.81).
- Texto vacío → pipeline continúa solo con estructuradas (RF-NLP-004).

## Impacto en la arquitectura
Componente NLP independiente con contrato de salida (vector de embedding) consumido por early y late fusion; condiciona recursos de cómputo para inferencia < 3 s (RNF-002).

## Notas del analista
La elección del modelo BERT concreto es decisión de implementación a documentar en Cap. 4.
