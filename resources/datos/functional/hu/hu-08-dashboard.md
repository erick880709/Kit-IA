---
id: HU-08
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Media
points: 5
---

# HU-08: Dashboard operacional

## Como
Profesional sanitario o administrador

## Quiero
Ver un panel de control con indicadores clave del servicio de urgencias: total de triajes, distribución por estado y nivel, tasa de concordancia, y tendencia de los últimos 7 días

## Para
Monitorear la operación del servicio de urgencias y tomar decisiones basadas en datos

## Criterios de Aceptación

- [ ] CA1: El dashboard carga al iniciar sesión (es la página principal después del login).
- [ ] CA2: **KPIs en cards** (4-6 cards en grid responsive):
  - Total de triajes hoy (número grande).
  - Pacientes en sala de espera (triajes en estado "Registro" o "SignosVitales").
  - Tasa de concordancia IA-Profesional (porcentaje con indicador visual: verde >80%, amarillo 60-80%, rojo <60%).
  - Tiempo promedio de inferencia (ms).
  - Total de pacientes registrados.
- [ ] CA3: **Gráfico de distribución por nivel IA**: gráfico de barras o dona con los 5 niveles (I-V) y colores clínicos.
- [ ] CA4: **Gráfico de tendencia 7 días**: línea de tiempo con triajes por día. Eje X: fechas, eje Y: cantidad.
- [ ] CA5: **Gráfico de distribución por estado**: barras horizontales con los estados del flujo (Registro, SignosVitales, EvaluacionClinica, ClasificacionIA, Validacion, Cerrado).
- [ ] CA6: Los datos se refrescan automáticamente cada 60 segundos (polling con TanStack Query `refetchInterval`).
- [ ] CA7: El dashboard es responsive: en tablet los KPIs se apilan en 2 columnas, los gráficos se reducen.
- [ ] CA8: Estados de carga: skeletons mientras los datos se obtienen de `GET /api/dashboard/kpis`.

## Recurso de datos involucrado

- **Nombre del recurso:** DashboardKPI
- **Capa(s):** frontend (consume GET /api/dashboard/kpis, GET /api/dashboard/triages-7d)

## Subtareas

- [ ] Crear `pages/DashboardPage.tsx`
- [ ] Crear `components/dashboard/KpiCard.tsx`
- [ ] Crear `components/dashboard/TriagesChart.tsx` (línea 7 días)
- [ ] Crear gráficos con Recharts (barras, dona, línea)
- [ ] Implementar polling cada 60s
- [ ] Implementar skeletons de carga
- [ ] Estilos responsive
- [ ] Probar con datos reales
