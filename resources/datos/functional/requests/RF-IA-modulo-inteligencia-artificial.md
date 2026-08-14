# RF-IA: Módulo de Inteligencia Artificial

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 45, Módulo IA; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md; 01-CONTEXTO-MAESTRO-CONSOLIDADO.md
**Prioridad:** Crítica

## Descripción
El sistema ejecutará un pipeline de inferencia multimodal que, a partir de los datos estructurados (signos vitales, demográficos, antecedentes) y no estructurados (embeddings de texto clínico) del paciente, generará una predicción del nivel de triaje (I-V) con probabilidades por clase, nivel de confianza y metadatos del modelo utilizado. Este módulo es el núcleo diferenciador del sistema.

## Actores involucrados
- Sistema (ejecución automática)
- Enfermera de Triaje / Médico (dispara la ejecución)
- Científico de Datos / Administrador IA (gestión de modelos)

## Criterios de aceptación

### RF-IA-001 — Ejecutar Inferencia
- El profesional selecciona "Ejecutar IA" desde la pantalla de clasificación.
- El sistema valida que los datos mínimos estén completos (signos vitales + motivo de consulta).
- Se ejecuta el pipeline completo: normalización → embeddings NLP → modelo → predicción.
- La ejecución es asíncrona (RF-IA-010): no bloquea la interfaz de usuario.

### RF-IA-002 — Generar Probabilidades por Nivel
- Se calcula y muestra la probabilidad para cada uno de los 5 niveles (I-V).
- Las probabilidades se presentan en formato numérico y visual (barras/gráfico).

### RF-IA-003 — Seleccionar Predicción
- El sistema selecciona la clase con mayor probabilidad como nivel sugerido.
- **Corrección de implementación (ver Notas):** la selección aplica el umbral de decisión optimizado por clase para los Niveles I y II, calibrado para maximizar Recall aunque implique una ligera caída de Precisión en esas dos clases. Para Niveles III-V se usa el umbral estándar (argmax).
- Las probabilidades de todos los niveles permanecen visibles, no solo la del nivel ganador.

### RF-IA-004 — Registrar Modelo y Versión
- Toda inferencia almacena: identificador del modelo, versión, algoritmo, fecha de la versión.
- Estos metadatos son inmutables y garantizan la reproducibilidad (RNA-004).

### RF-IA-005 — Registrar Tiempo de Inferencia
- Se mide y almacena el tiempo total empleado por la inferencia (desde el clic hasta la presentación de resultados).
- El tiempo se muestra al profesional y se registra para monitoreo de desempeño.

### RF-IA-006 — Registrar Confianza
- Se almacena el score de confianza asociado a la predicción.
- La confianza se presenta junto al nivel sugerido para que el profesional evalúe la solidez de la recomendación.

### RF-IA-007 — Comparación de Modelos
- Permitirá comparar múltiples modelos (early fusion vs. late fusion) sobre el mismo conjunto de datos.
- Accesible para el rol Investigador desde la pantalla de Comparación de modelos.
- Visualiza métricas lado a lado: Accuracy, Precision, Recall, F1, AUC-ROC, matriz de confusión.

### RF-IA-008 — Cambio de Modelo Activo
- Solo usuarios autorizados (Administrador IA) pueden seleccionar qué versión del modelo está activa para producción.
- El cambio de modelo activo genera un registro de auditoría.

### RF-IA-009 — Reprocesamiento de Inferencia
- Permite volver a ejecutar la inferencia cuando se modifican los datos clínicos del paciente (ej. nuevos signos vitales).
- La nueva predicción se registra como una versión adicional, sin sobrescribir la anterior.

### RF-IA-010 — Inferencia Asíncrona
- La ejecución del modelo no bloquea la interfaz de usuario.
- Se muestra un indicador de carga mientras el modelo procesa.
- Si el modelo no está disponible, se informa al profesional y se permite continuar con clasificación manual (RNO-006).

## Dependencias / relacionados
- RNA-001 a 010: Reglas de Inteligencia Artificial.
- RNP-001: Tiempo objetivo de inferencia < 3 segundos.
- RNO-006: Funcionamiento sin IA disponible (clasificación manual).
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`: arquitectura early/late fusion, umbral por clase, pipeline técnico.
- `01-CONTEXTO-MAESTRO-CONSOLIDADO.md`: decisión cerrada de implementar ambas arquitecturas y comparar.

## Notas del analista
- **RF-IA-003 requiere corrección en el documento fuente.** `CONTEXT_TRIA.txt` describe la selección como "clase con mayor probabilidad" (argmax puro), pero la decisión técnica cerrada en `CONTEXTO_TRIAJE.txt` v2.0 y `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` establece umbral optimizado por clase para Niveles I-II priorizando Recall. Este archivo refleja la versión corregida. Se recomienda actualizar el texto original de RF-IA-003 en `CONTEXT_TRIA.txt` (ver `05-PENDIENTES-PARA-DIRECTORA.md`).
- Las metas cuantitativas son: F1 ≥ 0.82, Precisión ≥ 0.85, Recall ≥ 0.80, AUC-ROC ≥ 0.87 (consistentes en todos los documentos).
