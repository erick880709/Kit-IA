---
id: HU-E2-03
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Media
points: 3
---

# HU-E2-03: Consultar Historial de Triajes del Paciente

## Como
Médico de Urgencias / Enfermera de Triaje

## Quiero
Ver los eventos de triaje anteriores del paciente (fecha, nivel asignado, motivo de consulta)

## Para
Tener contexto clínico que mejore la precisión de la clasificación actual

## Criterios de Aceptación
- [ ] CA1: Al abrir un paciente existente, se muestra un resumen de sus últimos 5 eventos de triaje
- [ ] CA2: Cada evento muestra: fecha, nivel asignado (I-V), profesional responsable, motivo de consulta
- [ ] CA3: Indicador visual del número total de episodios previos (variable EpisodiosPreviosUrgencias)
- [ ] CA4: La información se obtiene de la base de datos local (no depende de integración con HCE)
- [ ] CA5: Si no hay historial previo, se muestra "Primer episodio registrado en el sistema"

## Recurso de datos involucrado
- **Nombre:** EventoTriaje (consulta)
- **Capa(s):** backend + frontend

## Subtareas
- [ ] Diseñar sección de historial en pantalla de paciente
- [ ] Implementar consulta de últimos eventos por paciente
- [ ] Implementar contador de episodios previos
