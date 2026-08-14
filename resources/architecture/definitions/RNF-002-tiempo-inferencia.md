# RNF-002: Rendimiento — Inferencia, Concurrencia y Operación

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §6 · `context/CONTEXT TRIA.txt` (RNP-001 a 004) · `resources/datos/definitions/RNF-001` (extracción previa)

## Descripción
El tiempo de inferencia debe permitir su uso en un flujo clínico real sin bloquear la operación, incluso bajo concurrencia.

## Criterio medible / restricción concreta
- **RNP-001:** Tiempo de inferencia < 3 segundos desde el clic en "Ejecutar IA" hasta la presentación completa de resultados, **incluida la generación SHAP**.
- **RNP-002:** Soportar al menos 10 inferencias concurrentes sin que el tiempo individual supere el doble del base (objetivo < 6 s en carga).
- **RNP-003:** Las consultas operativas (búsqueda de pacientes, carga de historial, consulta de auditoría) responden en < 1 segundo.
- **RNP-004:** SHAP no debe bloquear el flujo asistencial: la predicción se muestra de inmediato y la explicación puede completarse en segundo plano.

## Impacto en la arquitectura
Condiciona la elección del stack de serving (modelo ligero o pre-carga del artefacto), el dimensionamiento del submodelo BERT y el uso de caché de embeddings. La inferencia debe ejecutarse de forma asíncrona (RF-IA-010). SHAP debe usar TreeExplainer (XGBoost/RF) en lugar de KernelExplainer.

## Notas del analista
3 s es ambicioso con NLP (BERT) + predicción + SHAP en secuencia: los embeddings suelen dominar el pipeline. Evaluar modelos ligeros (distilBERT, BETO) o pre-computar embeddings para la demo. Si no se alcanza, documentar el tiempo real y su justificación clínica.
