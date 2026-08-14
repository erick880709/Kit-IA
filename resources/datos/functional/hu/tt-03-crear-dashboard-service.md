---
id: TT-03
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "Ninguna"
---

# TT-03: Crear DashboardService

## Descripción

Actualmente `dashboard_page.py` ejecuta consultas SQL directas contra la base de datos (usa `get_connection()` y `rows_to_dicts()`). Hay que extraer esas queries a un nuevo servicio `DashboardService` con métodos puros que retornen diccionarios, sin dependencias de Streamlit.

Queries a extraer (identificadas en la exploración de código):
- Total de triajes (general)
- Triajes por estado
- Triajes por nivel IA
- Tasa de concordancia (profesional vs IA)
- Tiempo promedio de inferencia
- Total de pacientes registrados
- Triajes de los últimos 7 días (para el gráfico de tendencia)

## Criterios de Done

- [ ] Archivo `app/services/dashboard_service.py` creado con clase `DashboardService`.
- [ ] Constructor recibe `db_path: str`.
- [ ] Método `get_kpis() -> Dict` retorna todos los KPIs en una sola llamada (minimizar round-trips).
- [ ] Método `get_triages_7d() -> List[Dict]` retorna los triajes de los últimos 7 días.
- [ ] Todas las queries usan `get_connection()` de `database.py` (consistente con otros servicios).
- [ ] `dashboard_page.py` se actualiza para usar `DashboardService` en vez de SQL directo.
- [ ] El dashboard de Streamlit sigue mostrando los mismos datos.
- [ ] Sin dependencias de Streamlit en el nuevo servicio.

## Recurso de datos involucrado

- **Nombre del recurso:** DashboardKPI
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| total_triages | int | Sí | Conteo total de triajes en la BD |
| triages_por_estado | dict | Sí | `{estado: count}` para cada estado del flujo |
| triages_por_nivel_ia | dict | Sí | `{nivel: count}` para niveles I-V |
| tasa_concordancia | float | Sí | % de casos donde nivel profesional == nivel IA |
| tiempo_inferencia_promedio | float | Sí | Promedio de `tiempo_inferencia_ms` en ms |
| total_pacientes | int | Sí | Conteo de pacientes únicos |
| triages_ultimos_7_dias | list | Sí | Lista de `{fecha, count}` para gráfico de tendencia |

## Subtareas

- [ ] Identificar las 5-7 queries SQL exactas en `dashboard_page.py`
- [ ] Crear `DashboardService` con método `get_kpis()`
- [ ] Crear método `get_triages_7d()`
- [ ] Actualizar `dashboard_page.py` para usar el servicio
- [ ] Verificar que el dashboard muestra los mismos datos
