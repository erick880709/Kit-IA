---
id: HU-14
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Baja
points: 1
---

# HU-14: Control de cambios

## Como
Administrador o auditor

## Quiero
Ver un registro de todos los cambios realizados sobre los datos de pacientes (modificaciones de documento, nombre, EPS, etc.), con trazabilidad de quién hizo el cambio y cuándo

## Para
Tener un historial de modificaciones que garantice la integridad de los datos del paciente

## Criterios de Aceptación

- [ ] CA1: La página muestra una tabla con columnas: Fecha, Usuario, Paciente (documento + nombre), Campo Modificado, Valor Anterior, Valor Nuevo.
- [ ] CA2: La tabla se carga desde `GET /api/control-cambios`.
- [ ] CA3: Opcional: filtro por documento de paciente para ver solo los cambios de una persona.
- [ ] CA4: La tabla está ordenada por fecha descendente.

## Recurso de datos involucrado

- **Nombre del recurso:** ControlCambios
- **Capa(s):** frontend (consume GET /api/control-cambios)

## Subtareas

- [ ] Crear `pages/ControlCambiosPage.tsx`
- [ ] Implementar tabla con datos de cambios
- [ ] Implementar filtro opcional por documento
- [ ] Probar con datos de prueba
