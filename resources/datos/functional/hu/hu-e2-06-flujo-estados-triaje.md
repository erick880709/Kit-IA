---
id: HU-E2-06
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 5
---

# HU-E2-06: Flujo de Estados del Triaje

## Como
Enfermera de Triaje / Médico

## Quiero
Que el sistema controle automáticamente el avance del triaje a través de sus estados (Registrado → En evaluación → Pendiente IA → Clasificado → Validado → Cerrado)

## Para
Garantizar que el proceso clínico se complete en el orden correcto y no se salten pasos obligatorios

## Criterios de Aceptación
- [ ] CA1: Al registrar el paciente, el evento se crea en estado "Registrado"
- [ ] CA2: Al comenzar la captura de signos vitales, el estado cambia a "En evaluación"
- [ ] CA3: Al completar la evaluación clínica y tener todos los campos obligatorios, se habilita el botón "Ejecutar IA" y el estado cambia a "Pendiente IA"
- [ ] CA4: Al ejecutar la IA, el estado cambia a "Clasificado" (tenga o no éxito la inferencia — si falla, se permite clasificación manual)
- [ ] CA5: Al registrar el profesional su clasificación, el estado cambia a "Validado"
- [ ] CA6: Al cerrar el evento (clasificación + validación + auditoría), el estado cambia a "Cerrado"
- [ ] CA7: No se permite saltar estados (ej. de "Registrado" a "Clasificado" sin pasar por "En evaluación")
- [ ] CA8: El estado actual se refleja visualmente en la interfaz (badge de color)

## Recurso de datos involucrado
- **Nombre:** EventoTriaje (ENT-002) — campo Estado
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Estado | Catálogo | Sí | Registrado, En evaluación, Pendiente IA, Clasificado, Validado, Cerrado, Cancelado |
| FechaHoraIngreso | DateTime | Sí | Automático al crear |
| FechaHoraClasificacion | DateTime | No | Se establece al pasar a "Clasificado" |

## Subtareas
- [ ] Implementar máquina de estados en backend (enum + validación de transiciones)
- [ ] Implementar indicador visual de estado en frontend
- [ ] Implementar habilitación/deshabilitación de botones según estado actual
