# RNF-002: Disponibilidad y Escalabilidad

**Tipo:** Requerimiento no funcional
**Categoría:** Disponibilidad / Escalabilidad
**Fuente:** CONTEXT TRIA.txt — Sección 18, OC-001, OC-003; RNO-006

## Descripción
El sistema debe mantener alta disponibilidad para el entorno clínico, con capacidad de funcionamiento degradado (clasificación manual) cuando el modelo de IA no esté disponible, y arquitectura que permita escalado horizontal para absorber picos de demanda.

## Criterio medible / restricción concreta
- **OC-001 — Alta disponibilidad:** El sistema debe estar operativo durante el horario de funcionamiento del servicio de urgencias (24/7 idealmente). Para la demo, se espera disponibilidad durante las sesiones de validación con profesionales.
- **OC-003 — Escalabilidad horizontal:** La arquitectura debe permitir añadir instancias adicionales del servicio de inferencia sin cambios de código, para manejar incrementos en la carga de pacientes.
- **RNO-006 — Modo degradado:** Si el modelo de IA no está disponible (fallo del servicio, timeout), el sistema debe permitir continuar el proceso de triaje de forma manual (clasificación tradicional), registrando la indisponibilidad (RNO-007).
- Toda indisponibilidad del modelo debe quedar registrada en auditoría con timestamp y causa.

## Impacto en la arquitectura
- Separación clara entre el servicio de inferencia IA y la aplicación web (API REST desacoplada), permitiendo que cada componente escale y falle independientemente.
- La app web debe implementar un circuit breaker o timeout para las llamadas al servicio de IA, con fallback a modo manual.
- La demo puede ejecutarse en una sola instancia (no se requiere alta disponibilidad real para el TFM), pero la arquitectura debe documentar cómo escalaría en producción.

## Notas del analista
- Para el alcance de la demo TFM, la alta disponibilidad 24/7 no es un requisito realista ni necesario. Este RNF aplica como requisito de arquitectura (diseñar para producción) más que como requisito de la demo.
- El modo degradado sin IA (RNO-006) es un requisito de seguridad clínica crítico: un fallo técnico no puede interrumpir la atención de pacientes.
