---
id: TT-10
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 5
dependencies: "TT-07, TT-09"
---

# TT-10: Implementar TriageRouter — flujo completo de triaje

## Descripción

Crear el router de triajes que expone el flujo clínico completo como endpoints REST: crear triaje, guardar signos vitales, guardar evaluación clínica, transicionar estado, reclasificar manualmente y cerrar triaje.

Este es el router más complejo porque orquesta la máquina de estados del triaje y coordina múltiples servicios (`TriageService`, `PatientService`).

## Criterios de Done

- [ ] `routers/triages.py` creado con endpoints:
  - `POST /api/triages` — crear triaje para paciente (body: `{id_paciente, profesional}`).
  - `GET /api/triages/{id}` — obtener triaje completo con JOIN a todas las tablas relacionadas.
  - `GET /api/triages?doc=&active_only=` — buscar triajes por documento del paciente.
  - `PUT /api/triages/{id}/vital-signs` — guardar signos vitales (FC, FR, TA, Tº, SpO2, Glasgow...).
  - `GET /api/triages/{id}/vital-signs` — obtener signos vitales + alertas.
  - `PUT /api/triages/{id}/clinical-eval` — guardar evaluación clínica (motivo, dolor, comorbilidades).
  - `GET /api/triages/{id}/clinical-eval` — obtener evaluación clínica.
  - `PATCH /api/triages/{id}/state` — transicionar estado (body: `{estado, usuario, motivo}`).
  - `POST /api/triages/{id}/reclassify` — reclasificar manualmente (body: `{nivel, motivo, usuario}`).
  - `POST /api/triages/{id}/close` — cerrar triaje (body: `{nivel_profesional, usuario, motivo_cierre}`).
- [ ] Validación de transiciones de estado contra `TRANSICIONES_VALIDAS`.
- [ ] El cierre de triaje dispara `PatientService.update_episodios_previos()` y registra en `Auditoria`.
- [ ] Manejo de errores: triaje no encontrado → 404, transición inválida → 422.
- [ ] Todos los endpoints protegidos con `get_current_user`.

## Recurso de datos involucrado

- **Nombre del recurso:** Triaje
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| id_paciente | int | Sí | FK a Paciente |
| profesional | str | Sí | Username del profesional que inicia el triaje |
| estado | str | Sí | Catálogo ESTADOS_TRIAGE: Registro, SignosVitales, EvaluacionClinica, ClasificacionIA, Validacion, Cerrado |
| nivel_sugerido_ia | str | No | Nivel I-V sugerido por el modelo |
| nivel_profesional | str | No | Nivel I-V asignado por el profesional |
| fecha_inicio | datetime | Sí (auto) | |
| fecha_cierre | datetime | No | |
| tiempo_total_minutos | float | No | Calculado al cierre |
| concordancia | bool | No | ¿nivel_ia == nivel_profesional? |

## Subtareas

- [ ] Crear `routers/triages.py` con 10 endpoints
- [ ] Implementar validación de transiciones de estado
- [ ] Implementar lógica de cierre (concordancia, episodios, auditoría)
- [ ] Probar flujo completo de triaje con Swagger UI
