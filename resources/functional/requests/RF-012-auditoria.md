# RF-012: Auditoría

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-AUD-001 a 006) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Media

## Descripción
El sistema debe registrar todas las acciones relevantes con usuario, fecha/hora y cambios realizados; permitir la consulta de la auditoría y su exportación (CSV/Excel/PDF). Cada predicción de IA queda registrada para auditoría clínica y detección de deriva del modelo.

## Actores involucrados
Auditor (consulta y exportación), sistema (registro automático).

## Criterios de aceptación
- Toda acción registra usuario, fecha/hora y detalle del cambio.
- La consulta admite filtros; los estados de pantalla incluyen "vacío (sin resultados)".
- Exportación en CSV/Excel/PDF.

## Dependencias / relacionados
[[RF-010]], [[RF-011]], [[RNF-007]], [[RF-014]].

## Notas del analista
La auditoría es también el mecanismo de gobernanza para detección de deriva (RNA-010, RNAU-*).
