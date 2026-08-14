# RNF-001: Rendimiento — Tiempo de Inferencia y Concurrencia

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento
**Fuente:** CONTEXT TRIA.txt — Sección 37, RNP-001 a 004; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §6

## Descripción
El sistema debe garantizar que el tiempo de inferencia del modelo de IA no exceda los 3 segundos en condiciones normales de operación, que múltiples inferencias concurrentes no degraden significativamente el servicio, y que la generación de explicaciones SHAP no bloquee el flujo asistencial.

## Criterio medible / restricción concreta
- **RNP-001:** Tiempo objetivo de inferencia < 3 segundos (desde el clic en "Ejecutar IA" hasta la presentación de resultados completos, incluyendo la generación de SHAP).
- **RNP-002:** El sistema debe soportar al menos 10 inferencias concurrentes sin que el tiempo de respuesta individual supere el doble del tiempo base (objetivo < 6s en carga).
- **RNP-003:** Las consultas operativas (búsqueda de pacientes, carga de historial, consulta de auditoría) deben responder en < 1 segundo para no interrumpir el flujo clínico.
- **RNP-004:** La generación de explicaciones SHAP no debe impedir la continuidad del proceso asistencial — se muestra la predicción inmediatamente y SHAP puede completarse en segundo plano si es necesario.

## Impacto en la arquitectura
- La inferencia debe ejecutarse de forma asíncrona (RF-IA-010) para no bloquear la UI.
- Se requiere un mecanismo de cacheo o pre-carga del modelo en memoria para evitar latencia de carga en cada inferencia.
- SHAP puede usar TreeExplainer (rápido, exacto) para XGBoost/RF, evitando KernelExplainer (lento) en producción.
- La arquitectura de despliegue debe permitir escalado horizontal si la carga concurrente supera la capacidad de una instancia.

## Notas del analista
- 3 segundos es un objetivo ambicioso si el pipeline incluye NLP (embeddings BERT) + predicción + SHAP en secuencia. Si no se alcanza, documentar el tiempo real y justificar si es clínicamente aceptable.
- El tiempo de generación de embeddings BERT suele dominar el pipeline; evaluar modelos más ligeros (distilBERT, BETO) o pre-computar embeddings para la demo.
