# RF-TRI-001: Crear Evento de Triaje

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 41, Módulo de Triaje
**Prioridad:** Crítica

## Descripción
Cada ingreso de un paciente al servicio de urgencias generará automáticamente un nuevo evento de triaje independiente. El evento de triaje es la entidad central que agrupa toda la información clínica, la predicción de IA, la validación del profesional y la auditoría.

## Actores involucrados
- Sistema (automático al registrar paciente)
- Personal Administrativo

## Criterios de aceptación
- El evento se crea automáticamente al completar el registro del paciente (RF-PAC-001).
- Se asigna un identificador único (UUID) al evento.
- Se registra automáticamente la fecha y hora de ingreso.
- El estado inicial del evento es "Registrado".
- El evento queda asociado al paciente y al profesional responsable.

## Dependencias / relacionados
- RF-PAC-001: Registrar Paciente (dispara la creación del evento).
- RNG-004: Cada ingreso genera un nuevo evento de triaje independiente.
- ENT-002: Evento de Triaje (entidad de dominio).

## Notas del analista
- Los estados posibles del evento se detallan en RF-TRI-003.
- El modelo de datos original de ENT-002 fue extendido en `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` para incluir los campos `NivelSugeridoIA`, `ProbabilidadesIA`, `NivelAsignadoProfesional`, `Concordancia`, `MotivoDiscrepancia` y `VersionModeloUsado`, necesarios para la comparativa IA vs. profesional.
