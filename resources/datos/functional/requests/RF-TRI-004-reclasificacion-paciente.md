# RF-TRI-004: Reclasificación del Paciente

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 41, Módulo de Triaje
**Prioridad:** Alta

## Descripción
El sistema permitirá reclasificar a un paciente cuando existan cambios en su condición clínica que justifiquen una modificación del nivel de triaje previamente asignado. Toda reclasificación debe ser justificada y trazable.

## Actores involucrados
- Enfermera de Triaje
- Médico de Urgencias

## Criterios de aceptación
- La reclasificación solo es posible sobre eventos en estado "Validado" o "Cerrado".
- Es obligatorio registrar: motivo clínico, profesional responsable, fecha y hora, y observaciones.
- El sistema conserva el historial completo de clasificaciones previas (RNG-008: ningún dato se sobrescribe sin conservar su valor anterior).
- Cada reclasificación genera un nuevo registro de auditoría (RNAU-002).
- La reclasificación puede implicar una nueva ejecución de inferencia IA (RF-IA-009) si las variables clínicas cambiaron.

## Dependencias / relacionados
- RNO-008: El sistema permite reclasificaciones justificadas.
- RNO-009: Toda reclasificación requiere motivo clínico.
- RNO-010: Las reclasificaciones conservan el historial completo.
- RNG-008: Conservación del valor anterior.
- RF-IA-009: Reprocesamiento de inferencia.

## Notas del analista
- La reclasificación es un evento separado de la validación inicial. En el modelo de datos, el campo `NivelAsignadoProfesional` captura la clasificación inicial del profesional, y una reclasificación posterior genera un nuevo registro sin sobrescribir el original.
