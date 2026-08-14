---
id: TT-E7-02
type: Tarea Técnica
epic: E7 - Datos Personales del Paciente
priority: High
points: 3
---

# TT-E7-02: Actualizar PatientService con nuevos campos y validaciones

## Descripción
Actualizar el servicio de pacientes para los 9 campos nuevos: firma de `register_patient()`, validaciones y búsqueda por nombre.

## Criterios de Done
- [ ] `register_patient()` acepta los 9 parámetros nuevos.
- [ ] `_validar_telefono()`: ≥10 dígitos, acepta +57.
- [ ] `_validar_correo()`: contiene @ y . si no está vacío.
- [ ] `search_patients()` busca por nombre y apellidos.
- [ ] Toda modificación dispara `ControlCambios`.

## Dependencias
TT-E7-01

## Subtareas
- [ ] Validaciones de teléfono y correo
- [ ] INSERT actualizado
- [ ] Búsqueda por nombre
