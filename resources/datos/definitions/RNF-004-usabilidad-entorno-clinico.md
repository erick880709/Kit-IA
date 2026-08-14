# RNF-004: Usabilidad para Entorno Clínico

**Tipo:** Requerimiento no funcional
**Categoría:** Usabilidad
**Fuente:** CONTEXT TRIA.txt — Sección 18, OC-007; 04-ESPECIFICACION-APLICACION-DEMO.md

## Descripción
La interfaz de usuario debe ser intuitiva y eficiente para personal clínico (enfermeras y médicos) que opera bajo presión asistencial, con alto volumen de pacientes y tiempo limitado. El sistema debe minimizar la carga cognitiva, reducir el número de clics para completar el flujo principal y proporcionar retroalimentación visual clara sobre el estado de cada paciente.

## Criterio medible / restricción concreta
- **OC-007 — Facilidad de uso:** Un profesional de enfermería sin entrenamiento previo en el sistema debe poder completar un triaje completo (registro → signos vitales → evaluación → IA → validación) en menos de 5 minutos desde el primer uso.
- El flujo principal de triaje (paciente nuevo) no debe requerir más de 3 pantallas o cambios de contexto.
- Los valores críticos (signos vitales fuera de rango, Nivel I sugerido por IA) deben ser visualmente prominentes (color rojo, iconos de alerta) sin depender únicamente del color (accesibilidad).
- Los tiempos de carga deben indicarse con indicadores de progreso visibles.
- La interfaz debe ser responsive y funcionar en tablet (formato común en estaciones de enfermería).

## Impacto en la arquitectura
- La UI debe diseñarse siguiendo principios de usabilidad clínica (heuristic evaluation con profesionales de salud).
- El flujo de pantallas definido en `04-ESPECIFICACION-APLICACION-DEMO.md` prioriza el recorrido lineal (Login → Registro → Signos Vitales → Evaluación → Clasificación IA → Validación) sobre la navegación libre.
- Los formularios deben implementar validación en tiempo real (no solo al enviar) para reducir errores y re-trabajo.

## Notas del analista
- El test de usabilidad con profesionales reales del Hospital San Juan de Dios sería ideal pero puede no ser viable en el alcance del TFM. Documentar como trabajo futuro.
- La medición objetiva de "facilidad de uso" requiere un estudio de usabilidad (SUS, tiempo por tarea, tasa de errores). Para la demo, se acepta una validación cualitativa con la directora o colegas.
