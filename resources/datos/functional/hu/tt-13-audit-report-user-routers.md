---
id: TT-13
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 3
dependencies: "TT-07"
---

# TT-13: Implementar AuditRouter + ReportRouter + UserRouter

## Descripción

Crear los routers restantes para auditoría, reportes y gestión de usuarios. Son endpoints más simples (principalmente consultas) pero necesarios para completar la API.

## Criterios de Done

- [ ] `routers/audit.py` creado con endpoints:
  - `GET /api/audit?fecha_desde=&fecha_hasta=&accion=&entidad=&usuario=&page=&limit=` — consulta paginada de auditoría con filtros.
  - `GET /api/audit/actions` — lista de acciones auditables distintas.
  - `GET /api/audit/users` — lista de usuarios que han generado auditoría.
  - `GET /api/audit/export/csv` — descarga CSV de resultados.
- [ ] `routers/reports.py` creado con endpoints:
  - `GET /api/reports/triage/{id}/html` — retorna informe HTML del triaje.
  - `GET /api/reports/triage/{id}/download` — descarga como archivo `.html`.
- [ ] `routers/users.py` creado con endpoints (admin):
  - `GET /api/users` — lista todos los usuarios.
  - `POST /api/users` — crea un nuevo usuario.
  - `PATCH /api/users/{id}` — actualiza email, rol, activo.
  - `DELETE /api/users/{id}` — desactiva usuario (soft delete).
  - `POST /api/users/{id}/reset-password` — genera nueva contraseña aleatoria.
- [ ] User router protegido con `require_role("Administrador")`.
- [ ] Reportes usan `ReportService` existente sin modificaciones.

## Recurso de datos involucrado

- **Nombre del recurso:** Auditoria, Reporte, Usuario
- **Capa(s):** backend

## Subtareas

- [ ] Crear `routers/audit.py` con 4 endpoints
- [ ] Crear `routers/reports.py` con 2 endpoints
- [ ] Crear `routers/users.py` con 5 endpoints
- [ ] Implementar paginación en audit
- [ ] Probar con Swagger UI
