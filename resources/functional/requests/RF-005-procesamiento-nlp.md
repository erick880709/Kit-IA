# RF-005: Procesamiento NLP de Texto Clínico

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-NLP-001 a 005) · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §1.2
**Prioridad:** Alta

## Descripción
El sistema debe procesar el texto clínico libre (motivo de consulta, notas de admisión, historia clínica narrativa si está autorizada): limpieza del texto, generación de embeddings clínicos (BERT afinado en español médico, p. ej. BioBERT-es), detección de texto vacío y asunción del español como idioma principal.

Cubre los requerimientos fuente: RF-NLP-001 (Procesar), RF-NLP-002 (Embeddings), RF-NLP-003 (Limpieza), RF-NLP-004 (Texto vacío), RF-NLP-005 (Idioma).

## Actores involucrados
Sistema (automático); no requiere interacción del usuario.

## Criterios de aceptación
- Texto vacío → el pipeline continúa solo con variables estructuradas (sin error).
- Los embeddings se generan con un modelo BERT clínico en español (evaluar BioBERT-es o equivalente).
- Todo procesamiento de texto respeta la anonimización previa ([[RNF-006]]).

## Dependencias / relacionados
[[RF-004]], [[RF-006]], [[RT-003]].

## Notas del analista
El módulo NLP alimenta el submodelo de texto de la late fusion y el vector combinado de la early fusion.
