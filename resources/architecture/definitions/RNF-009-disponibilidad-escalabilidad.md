# RNF-009: Disponibilidad, Escalabilidad y Modo Degradado

**Tipo:** Requerimiento no funcional
**Categoría:** Disponibilidad / Escalabilidad
**Fuente:** `context/CONTEXT TRIA.txt` (OC-001, OC-003, RNO-006, RNO-007) · `resources/datos/definitions/RNF-002` (extracción previa)

## Descripción
El sistema debe mantener disponibilidad en el entorno clínico, permitir escalado horizontal para absorber picos de demanda, y ofrecer un **modo degradado** que garantice la continuidad del triaje manual cuando el modelo de IA no esté disponible.

## Criterio medible / restricción concreta
- **OC-001 (Alta disponibilidad):** sistema operativo durante el horario del servicio de urgencias (24/7 idealmente). Para la demo: disponible durante las sesiones de validación con profesionales.
- **OC-003 (Escalabilidad horizontal):** añadir instancias del servicio de inferencia sin cambios de código.
- **RNO-006 (Modo degradado):** si el modelo no está disponible (fallo, timeout), el sistema permite continuar el triaje manual, registrando la indisponibilidad.
- **RNO-007:** toda indisponibilidad del modelo queda en auditoría con timestamp y causa.

## Impacto en la arquitectura
- Separación clara entre servicio de inferencia IA y aplicación web (API desacoplada): cada componente escala y falla de forma independiente.
- Circuit breaker o timeout en las llamadas al servicio de IA, con fallback a modo manual.
- Para el alcance TFM la demo corre en una instancia única, pero la arquitectura debe documentar cómo escalaría en producción.

## Notas del analista
El modo degradado (RNO-006) es un requisito de **seguridad clínica crítico**: un fallo técnico no puede interrumpir la atención de pacientes. Aplica como requisito de arquitectura (diseñar para producción), no como requisito operativo de la demo.
