---
id: HU-E2-07
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 5
---

# HU-E2-07: Reclasificación del Paciente

## Como
Médico de Urgencias / Enfermera de Triaje

## Quiero
Modificar el nivel de triaje de un paciente ya clasificado cuando su condición clínica cambia

## Para
Reflejar la nueva realidad clínica sin perder el historial de clasificaciones anteriores

## Criterios de Aceptación
- [ ] CA1: La reclasificación solo está disponible para eventos en estado "Validado" o "Cerrado"
- [ ] CA2: El profesional selecciona un nuevo nivel (I-V) y DEBE registrar: motivo clínico (texto obligatorio), observaciones (opcional)
- [ ] CA3: La clasificación anterior NO se sobrescribe — se conserva en el historial (RNG-008)
- [ ] CA4: La reclasificación genera un nuevo registro de auditoría (RNAU-002)
- [ ] CA5: Si las variables clínicas cambiaron, se puede ejecutar nueva inferencia IA (RF-IA-009) como parte de la reclasificación
- [ ] CA6: El historial de reclasificaciones es visible en la pantalla del evento (timeline de cambios)

## Recurso de datos involucrado
- **Nombre:** EventoTriaje (extensión) + HistoricoReclasificaciones
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdReclasificacion | UUID | Sí | Generado automáticamente |
| IdTriaje | UUID | Sí | FK a EventoTriaje |
| NivelAnterior | Catálogo | Sí | I-V |
| NivelNuevo | Catálogo | Sí | I-V |
| Motivo | Texto | Sí | Justificación clínica obligatoria |
| Observaciones | Texto | No | |
| ProfesionalResponsable | UUID | Sí | FK a Usuario |
| FechaHora | DateTime | Sí | Automático |

### Relaciones con otros recursos
- `EventoTriaje` (N:1): múltiples reclasificaciones por evento
- `Auditoria` (1:1): cada reclasificación genera registro de auditoría

## Subtareas
- [ ] Diseñar pantalla/modal de reclasificación
- [ ] Implementar registro de histórico sin sobrescribir
- [ ] Implementar timeline visual de cambios en el evento
- [ ] Conectar reclasificación con módulo de auditoría
- [ ] Implementar re-ejecución opcional de inferencia IA
