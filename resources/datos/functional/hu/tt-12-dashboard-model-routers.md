---
id: TT-12
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 2
dependencies: "TT-03, TT-04, TT-07"
---

# TT-12: Implementar DashboardRouter + ModelRouter

## Descripción

Crear routers para los nuevos servicios `DashboardService` y `ModelManagementService`. Estos endpoints no existían en Streamlit (se consultaban con SQL directo en la UI), así que son netamente nuevos.

## Criterios de Done

- [ ] `routers/dashboard.py` creado con endpoints:
  - `GET /api/dashboard/kpis` — retorna todos los KPIs: total triajes, por estado, por nivel IA, concordancia, tiempo inferencia promedio, total pacientes.
  - `GET /api/dashboard/triages-7d` — retorna lista de `{fecha, count}` para gráfico de tendencia.
- [ ] `routers/models.py` creado con endpoints:
  - `GET /api/models` — lista modelos registrados en BD.
  - `POST /api/models` — registra un nuevo modelo (admin).
  - `PATCH /api/models/{id}` — activa/desactiva un modelo (admin). Solo uno puede estar activo.
  - `GET /api/models/scan` — escanea directorio y retorna modelos serializados en disco.
- [ ] Dashboard usa caché de corta duración (30s) para evitar consultas repetitivas.
- [ ] Model router valida que el modelo exista en disco antes de registrarlo.

## Recurso de datos involucrado

- **Nombre del recurso:** DashboardKPI (ver TT-03), Modelo (ver TT-04)
- **Capa(s):** backend

## Subtareas

- [ ] Crear `routers/dashboard.py` con 2 endpoints
- [ ] Crear `routers/models.py` con 4 endpoints
- [ ] Implementar caché de 30s en dashboard
- [ ] Probar con Swagger UI
