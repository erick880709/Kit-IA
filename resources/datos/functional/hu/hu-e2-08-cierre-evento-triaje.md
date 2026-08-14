---
id: HU-E2-08
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 3
---

# HU-E2-08: Cierre del Evento de Triaje

## Como
Médico de Urgencias

## Quiero
Cerrar formalmente el evento de triaje cuando la clasificación está completa y validada

## Para
Finalizar el proceso y dejar el evento disponible para consulta, auditoría y reportes

## Criterios de Aceptación
- [ ] CA1: El botón "Cerrar Evento" solo se habilita cuando: (1) hay clasificación asignada, (2) el profesional registró su nivel, (3) hay registro de auditoría mínimo
- [ ] CA2: Si hay discrepancia (NivelSugeridoIA ≠ NivelAsignadoProfesional), el campo MotivoDiscrepancia es OBLIGATORIO antes de permitir el cierre
- [ ] CA3: Si hay concordancia (NivelSugeridoIA == NivelAsignadoProfesional), el campo Concordancia se calcula automáticamente como true
- [ ] CA4: Al cerrar, el estado cambia a "Cerrado" y se registra timestamp de cierre
- [ ] CA5: Un evento cerrado no puede ser modificado directamente — solo mediante reclasificación formal (HU-E2-07)
- [ ] CA6: El evento cerrado queda disponible en las pantallas de consulta, auditoría y dashboard

## Recurso de datos involucrado
- **Nombre:** EventoTriaje (campos de cierre)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| NivelSugeridoIA | Catálogo | Sí (si hubo inferencia) | I-V |
| NivelAsignadoProfesional | Catálogo | Sí | I-V, campo independiente |
| Concordancia | Booleano | Sí | Calculado: NivelSugeridoIA == NivelAsignadoProfesional |
| MotivoDiscrepancia | Texto | Solo si Concordancia = No | Obligatorio cuando hay discrepancia |
| FechaHoraCierre | DateTime | Sí | Automático al cerrar |

## Subtareas
- [ ] Implementar validación de condiciones de cierre
- [ ] Implementar cálculo automático de concordancia
- [ ] Implementar exigencia de MotivoDiscrepancia
- [ ] Implementar bloqueo de edición post-cierre
