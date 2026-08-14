---
id: TT-09
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "TT-07"
---

# TT-09: Implementar PatientRouter + ControlCambiosRouter

## Descripción

Crear routers para pacientes y control de cambios que expongan los métodos de `PatientService` como endpoints REST.

## Criterios de Done

- [ ] `routers/patients.py` creado con endpoints:
  - `POST /api/patients` — registrar paciente (usa `PatientService.register_patient()`).
  - `GET /api/patients/{documento}` — buscar por documento.
  - `GET /api/patients/id/{id}` — buscar por ID interno.
  - `GET /api/patients?q=&tipo_doc=&limit=20` — búsqueda textual con filtros.
  - `GET /api/patients/{id}/triages` — histórico de triajes del paciente.
  - `GET /api/patients/{id}/active-triage` — triaje activo del paciente.
  - `POST /api/patients/{id}/recount` — recalcular episodios previos.
- [ ] `routers/control_cambios.py` creado con endpoints:
  - `GET /api/control-cambios` — historial de cambios.
  - `POST /api/control-cambios` — registrar cambio.
- [ ] Manejo de errores: `DuplicatePatientError` → 409 Conflict.
- [ ] Validación de tipos de documento, EPS, grupo sanguíneo contra catálogos.
- [ ] Todos los endpoints protegidos con `get_current_user`.

## Recurso de datos involucrado

- **Nombre del recurso:** Paciente
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| tipo_documento | str | Sí | Catálogo: CC, CE, TI, PA, RC |
| numero_documento | str | Sí | Único |
| nombre | str | Sí | |
| apellido | str | Sí | |
| fecha_nacimiento | str | Sí | YYYY-MM-DD |
| sexo | str | Sí | Catálogo: M, F |
| grupo_sanguineo | str | Sí | Catálogo: A+, A-, B+, B-, AB+, AB-, O+, O- |
| alergias | str | No | Texto libre |
| eps | str | Sí | Catálogo EPS_COLOMBIA (21 opciones) |
| via_llegada | str | No | Catálogo: Caminando, Silla de ruedas, Camilla, Ambulancia |
| departamento | str | No | Catálogo DEPARTAMENTOS_COLOMBIA |
| municipio | str | No | |
| telefono | str | No | Formato colombiano |
| correo | str | No | email válido |

### Relaciones con otros recursos
- `Triaje` (1:N): un paciente tiene múltiples triajes.

## Subtareas

- [ ] Crear `routers/patients.py` con 7 endpoints
- [ ] Crear `routers/control_cambios.py` con 2 endpoints
- [ ] Manejar `DuplicatePatientError` → 409
- [ ] Probar CRUD pacientes con Swagger UI
