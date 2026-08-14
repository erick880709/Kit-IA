---
id: TT-E5-01
type: Tarea Técnica
epic: E5 - Auditoría, Trazabilidad y Cumplimiento
priority: High
points: 5
---

# TT-E5-01: Registro de auditoría append-only

## Descripción
Implementar el registro inmutable y trazable de todas las acciones del sistema (RF-012, RNF-007): usuario, fecha/hora, acción, entidad y cambios (antes/después).

## Criterios de Done
- [ ] Tabla `Auditoria` append-only (sin UPDATE/DELETE permitidos por la app).
- [ ] Decorador/middleware `@auditar` reutilizable en servicios.
- [ ] Registro de predicciones con versión de modelo, umbrales y confianza (RNA-010).
- [ ] Detección de indisponibilidad del modelo registrada (RNO-007).
- [ ] Tests de integridad (intento de borrado rechazado).

## Dependencias
E1 completo

## Subtareas
- [ ] Esquema de auditoría
- [ ] Decorador @auditar
- [ ] Registro de inferencias
