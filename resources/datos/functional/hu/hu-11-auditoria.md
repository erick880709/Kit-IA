---
id: HU-11
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Media
points: 3
---

# HU-11: Consulta de auditoría

## Como
Auditor o administrador

## Quiero
Consultar el registro de auditoría del sistema filtrando por fecha, acción, entidad y usuario, y poder exportar los resultados a CSV

## Para
Realizar seguimiento de todas las acciones realizadas en el sistema con fines de control, cumplimiento normativo y trazabilidad

## Criterios de Aceptación

- [ ] CA1: La página muestra una tabla paginada (AG Grid server-side) con columnas: Fecha/Hora, Usuario, Acción, Entidad, Detalle, IP.
- [ ] CA2: **Filtros**:
  - Rango de fechas (date picker desde/hasta).
  - Acción (select múltiple con acciones disponibles desde `GET /api/audit/actions`).
  - Entidad (select: Paciente, Triaje, SignosVitales, EvaluacionClinica, Usuario, Modelo, etc.).
  - Usuario (select con usuarios desde `GET /api/audit/users`).
- [ ] CA3: La tabla se actualiza al cambiar cualquier filtro (refetch automático con TanStack Query).
- [ ] CA4: **Paginación**: controles de página, tamaño de página (10, 25, 50, 100), y contador de resultados totales.
- [ ] CA5: **Exportar CSV**: botón que descarga los resultados actuales (con filtros aplicados) como archivo CSV.
- [ ] CA6: La tabla es responsive: en tablet se ocultan columnas menos relevantes.

## Recurso de datos involucrado

- **Nombre del recurso:** Auditoria
- **Capa(s):** frontend (consume GET /api/audit, GET /api/audit/actions, GET /api/audit/users, GET /api/audit/export/csv)

## Subtareas

- [ ] Crear `pages/AuditPage.tsx`
- [ ] Configurar AG Grid con server-side pagination
- [ ] Implementar filtros (fecha, acción, entidad, usuario)
- [ ] Implementar exportación CSV
- [ ] Estilos responsive
- [ ] Probar con datos reales de auditoría
