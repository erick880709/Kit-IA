# RF-001: Gestión de Pacientes

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` §44 (RF-PAC-001 a 004) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Alta

## Descripción
El sistema debe permitir el registro del paciente al ingreso a urgencias (datos demográficos, régimen de afiliación, vía de llegada, episodios previos de urgencias), la búsqueda de pacientes ya registrados para evitar duplicados, la consulta de su historial clínico dentro del sistema y la validación de los datos capturados antes de guardar.

Cubre los requerimientos fuente: RF-PAC-001 (Registrar), RF-PAC-002 (Buscar), RF-PAC-003 (Consultar historial), RF-PAC-004 (Validación de datos).

## Actores involucrados
Personal administrativo (registro); médico/enfermera (consulta de historial).

## Criterios de aceptación
- El registro captura los campos nuevos `ViaLlegada` (catálogo controlado: Ambulancia / Particular / Remisión) y `EpisodiosPreviosUrgencias` (entero), según `context/03-CATALOGO-DATOS-Y-VARIABLES.md` §1.
- La búsqueda de duplicados se ejecuta antes del alta (documento de identidad + nombre).
- Los campos obligatorios no pueden quedar vacíos (RNQ-001).
- **Campos de datos personales (extracción previa TT-E7-01, `resources/datos/functional/reqs/resumen-cambios-pendientes.md`):** Nombres, Apellidos, Teléfono (≥10 dígitos, acepta +57), Correo (con @ y . si no está vacío), Contacto de emergencia (nombre + teléfono), Departamento (catálogo de 32 departamentos), Ciudad (dropdown dependiente del departamento) y Dirección de residencia.
- **Campos clínicos complementarios (decisión refinador 2026-08-13):** TipoSangre (catálogo de 8 grupos) y Alergias (sustancia y tipo) — complementan la historia clínica y apoyan la medicación segura.
- Toda modificación de campos del paciente queda registrada en `ControlCambios` (auditoría).
- La búsqueda permite localizar por nombre o apellidos.

## Dependencias / relacionados
[[RNF-006]], RD-002 (ENT-001 Paciente), RF-014 (control de acceso por rol).

## Notas del analista
`ViaLlegada` y `EpisodiosPreviosUrgencias` fueron añadidos por la validación de hallazgos (hallazgo #3): son predictores de alto peso que no existían en el catálogo original. La extracción previa (`resources/datos`) añade 9 campos de datos personales con catálogos Colombia (32 departamentos, ~200 ciudades) y validaciones propias — pendientes de implementación como TT-E7-01/02/03 y HU-E7-01.
