---
id: HU-E6-03
type: Historia de Usuario
epic: 006-dashboard-gestion-modelos-analitica
priority: Baja
points: 3
---

# HU-E6-03: Exportación de Reportes

## Como
Coordinador / Auditor / Investigador

## Quiero
Exportar los datos del dashboard y los reportes en Excel, PDF y CSV

## Para
Compartir informes con la dirección médica, incluir evidencia en el TFM y realizar análisis externos

## Criterios de Aceptación
- [ ] CA1: Desde el dashboard, botón "Exportar" que genera un PDF con todos los indicadores visibles en el período seleccionado
- [ ] CA2: Desde el dashboard, botón "Descargar datos" que exporta un CSV/Excel con los datos crudos subyacentes
- [ ] CA3: Desde la pantalla de Auditoría, exportación con los filtros aplicados (CSV, Excel, PDF)
- [ ] CA4: Desde la pantalla de Gestión de Modelos, exportación del historial de versiones con métricas comparativas (CSV)
- [ ] CA5: Las exportaciones en PDF tienen formato profesional con membrete, fecha de generación y numeración de página
- [ ] CA6: Los datos exportados de pacientes se anonimizan automáticamente (sin NumeroDocumento)

## Recurso de datos involucrado
- **Nombre:** Ninguno nuevo (usa datos de EventoTriaje, PrediccionIA, Auditoria, Modelo)
- **Capa(s):** backend

## Subtareas
- [ ] Implementar exportación PDF del dashboard
- [ ] Implementar exportación CSV/Excel de datos crudos
- [ ] Implementar anonimización en exportaciones
- [ ] Unificar formato de PDFs (membrete, numeración)
