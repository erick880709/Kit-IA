---
id: TT-14
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 5
dependencies: "TT-08, TT-09, TT-10, TT-11, TT-12, TT-13"
---

# TT-14: Tests de API con pytest

## Descripción

Crear tests de integración para los endpoints críticos de la API usando `pytest` + `httpx` (TestClient de FastAPI). Los tests deben cubrir los flujos principales: login, registro de paciente, flujo de triaje completo, inferencia, dashboard.

## Criterios de Done

- [ ] Archivo `tests/conftest.py` con fixtures: `client` (TestClient), `db_path` (BD temporal), `auth_headers` (token JWT de prueba).
- [ ] Tests de auth: login exitoso, login fallido, acceso sin token → 401, token expirado → 401.
- [ ] Tests de pacientes: crear paciente, buscar por documento, duplicado → 409.
- [ ] Tests de triaje: flujo completo (crear → signos → evaluación → inferencia → cerrar).
- [ ] Tests de inferencia: predict con datos válidos, modelo no cargado → 503.
- [ ] Tests de dashboard: KPIs retornan estructura esperada.
- [ ] Tests de auditoría: query con filtros, paginación.
- [ ] Cobertura > 70% de los endpoints.
- [ ] Tests usan BD SQLite en memoria (`:memory:`) para no afectar la BD de desarrollo.

## Recurso de datos involucrado

No aplica — es infraestructura de calidad.

## Subtareas

- [ ] Crear `conftest.py` con fixtures
- [ ] Tests de auth (4 casos)
- [ ] Tests de pacientes (3 casos)
- [ ] Tests de triaje (flujo completo)
- [ ] Tests de inferencia (2 casos)
- [ ] Tests de dashboard + auditoría
- [ ] Configurar coverage
