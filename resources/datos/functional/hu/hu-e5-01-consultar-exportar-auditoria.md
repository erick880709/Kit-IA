---
id: HU-E5-01
type: Historia de Usuario
epic: 005-auditoria-trazabilidad-cumplimiento
priority: Alta
points: 5
---

# HU-E5-01: Consultar y Exportar Auditoría

## Como
Auditor

## Quiero
Consultar los registros de auditoría con filtros (usuario, paciente, fecha, tipo de acción, modelo) y exportarlos en CSV, Excel y PDF

## Para
Realizar auditorías clínicas, detectar patrones de error y generar evidencia para cumplimiento normativo

## Criterios de Aceptación
- [ ] CA1: Pantalla "Auditoría" accesible solo para rol Auditor y Administrador
- [ ] CA2: Filtros disponibles: usuario, paciente, fecha (rango desde-hasta), tipo de acción (catálogo), modelo/versión, nivel de triaje
- [ ] CA3: Resultados paginados (20 por página) y ordenables por fecha
- [ ] CA4: Cada registro muestra: timestamp, usuario, acción, entidad afectada, valor anterior/nuevo (si aplica)
- [ ] CA5: Exportación a CSV (datos crudos), Excel (formateado) y PDF (resumen legible)
- [ ] CA6: La exportación respeta los filtros aplicados en la consulta
- [ ] CA7: Al exportar datos que incluyan información de pacientes, se anonimizan automáticamente (eliminación de NumeroDocumento)

## Recurso de datos involucrado
- **Nombre:** Auditoria (consulta y exportación)
- **Capa(s):** backend + frontend

## Subtareas
- [ ] Diseñar pantalla de consulta de auditoría con filtros
- [ ] Implementar endpoint de consulta con filtros y paginación
- [ ] Implementar exportación CSV
- [ ] Implementar exportación Excel
- [ ] Implementar exportación PDF
- [ ] Implementar anonimización en exportaciones
