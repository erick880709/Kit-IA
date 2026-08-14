# RF-PAC-001: Registrar Paciente

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 40, Módulo de Gestión del Paciente
**Prioridad:** Alta

## Descripción
El sistema permitirá registrar la información básica del paciente para iniciar un episodio de atención en el servicio de urgencias. Este registro constituye el punto de entrada al flujo de triaje y genera un identificador único del episodio.

## Actores involucrados
- Personal Administrativo (principal)
- Enfermera de Triaje (secundario)

## Criterios de aceptación
- Se genera un identificador único del episodio (UUID).
- Se valida la información obligatoria: tipo de documento, número de documento, fecha de nacimiento, sexo.
- Se registra automáticamente la fecha y hora de ingreso.
- Se crea el evento de triaje asociado al paciente.

## Dependencias / relacionados
- RNG-004: Cada ingreso genera un nuevo evento de triaje independiente.
- RNS-009: Cumplimiento de Ley 1581 de 2012 (protección de datos personales).
- RF-PAC-002: Búsqueda de paciente.
- RF-PAC-004: Validación de datos.

## Notas del analista
- El sistema debe verificar duplicados antes de crear un nuevo registro (búsqueda por documento).
- Los campos `ViaLlegada` y `EpisodiosPreviosUrgencias` fueron añadidos posteriormente como variables de alto peso predictivo (ver `03-CATALOGO-DATOS-Y-VARIABLES.md`); deben incorporarse al formulario de registro aunque no estaban en la especificación original de ENT-001.
