# RF-PAC-002: Buscar Paciente

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 40, Módulo de Gestión del Paciente
**Prioridad:** Alta

## Descripción
El sistema permitirá localizar pacientes registrados previamente mediante múltiples criterios de búsqueda: número de documento, nombre, número de historia clínica o identificador interno.

## Actores involucrados
- Personal Administrativo
- Enfermera de Triaje
- Médico de Urgencias

## Criterios de aceptación
- Búsqueda por documento de identidad (tipo + número).
- Búsqueda por nombre (parcial o completo).
- Búsqueda por número de historia clínica.
- Búsqueda por identificador interno del sistema.
- Resultados paginados si hay múltiples coincidencias.
- Recuperación de información previa del paciente cuando exista (reduce re-captura de datos demográficos).

## Dependencias / relacionados
- RF-PAC-001: Registrar Paciente.
- RF-PAC-003: Consultar Historial.
- CU-001: Registrar Paciente (flujo alternativo: documento existente).

## Notas del analista
- La búsqueda por nombre debe soportar coincidencias parciales y tolerancia a errores tipográficos menores.
- Si el paciente ya existe, el sistema debe recuperar sus datos demográficos y antecedentes para no duplicar captura.
