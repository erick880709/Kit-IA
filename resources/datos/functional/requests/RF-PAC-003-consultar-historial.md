# RF-PAC-003: Consultar Historial

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 40, Módulo de Gestión del Paciente
**Prioridad:** Media

## Descripción
El sistema permitirá visualizar eventos anteriores de triaje del paciente cuando la política institucional y la disponibilidad de la Historia Clínica Electrónica (HCE) lo permitan. Esto proporciona contexto clínico al profesional para mejorar la precisión de la clasificación actual.

## Actores involucrados
- Médico de Urgencias
- Enfermera de Triaje

## Criterios de aceptación
- Visualización de eventos de triaje previos del paciente (fecha, nivel asignado, motivo de consulta).
- Indicador visual de si el paciente tiene episodios previos de urgencias (variable de alto peso predictivo).
- Acceso condicionado a la disponibilidad de integración con HCE (RF-INT-001).
- No debe bloquear el flujo de triaje si el historial no está disponible.

## Dependencias / relacionados
- RF-PAC-002: Buscar Paciente.
- RF-INT-001: Integración con Historia Clínica Electrónica (condicionado a disponibilidad institucional).
- ENT-001: Variable `EpisodiosPreviosUrgencias`.

## Notas del analista
- La variable "episodios previos de urgencias" fue identificada como de alto peso predictivo en la literatura y añadida como campo en `03-CATALOGO-DATOS-Y-VARIABLES.md`. Aunque no estaba en la especificación original de ENT-001, este requerimiento le da soporte funcional.
- Si no hay integración con HCE, este dato se captura por autorreporte en RF-EVA-005.
