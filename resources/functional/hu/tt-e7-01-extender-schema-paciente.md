---
id: TT-E7-01
type: Tarea Técnica
epic: E7 - Datos Personales del Paciente
priority: High
points: 3
---

# TT-E7-01: Extender schema de BD con 9 campos en Paciente

## Descripción
Agregar los 11 campos del paciente a la tabla Paciente: 9 de datos personales (fuente: `resources/datos/functional/reqs/resumen-cambios-pendientes.md`) + 2 clínicos complementarios decididos en el refinador (TipoSangre y Alergias, para medicación segura).

## Criterios de Done
- [ ] Migración no destructiva (`ADD COLUMN` con verificación de existencia).
- [ ] Catálogos `DEPARTAMENTOS_COLOMBIA` (32) y `CIUDADES_POR_DEPARTAMENTO` (~200).
- [ ] Ciudad es dependiente del Departamento (dropdown encadenado).

## Recurso de datos involucrado
### Recurso
- **Nombre:** Paciente (extensión)
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Nombres, Apellidos | texto | Sí | Búsqueda por nombre |
| Telefono | texto | Sí | ≥10 dígitos, acepta +57 |
| Correo | texto | No | Con @ y . si no vacío |
| ContactoEmergencia, NumeroContactoEmergencia | texto | Sí | Contacto de emergencia |
| Departamento | catálogo | Sí | 32 departamentos |
| Ciudad | catálogo | Sí | Dependiente de Departamento |
| DireccionResidencia | texto | Sí | — |
| TipoSangre | catálogo | No | A+ / A- / B+ / B- / AB+ / AB- / O+ / O- — apoyo a medicación |
| Alergias | texto/catálogo | No | Sustancia y tipo de alergia — apoyo a medicación |

## Dependencias
E2 completo

## Subtareas
- [ ] ALTER TABLE con los 9 campos
- [ ] Catálogos de departamentos y ciudades
- [ ] Verificación de migración idempotente
