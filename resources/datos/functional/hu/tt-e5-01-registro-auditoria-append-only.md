---
id: TT-E5-01
type: Tarea Técnica
epic: 005-auditoria-trazabilidad-cumplimiento
priority: Alta
points: 5
---

# TT-E5-01: Implementar Registro de Auditoría Append-Only

## Descripción
Implementar la capa de auditoría que registra automáticamente cada acción del sistema (creación, modificación, inferencia, validación, login/logout) en una tabla append-only. Este módulo es transversal: todas las HU de E2 y E4 deben disparar eventos de auditoría.

## Criterios de Done
- [ ] Tabla `Auditoria` en SQLite con campos: IdAuditoria (UUID), Usuario, FechaHora (UTC), Accion (catálogo), EntidadAfectada, IdEntidad, ValorAnterior (JSON), ValorNuevo (JSON), IP, Dispositivo, Observaciones
- [ ] La tabla NO tiene permisos de UPDATE ni DELETE (append-only a nivel de aplicación y BD)
- [ ] Decorador/interceptor `@auditar(accion="...")` que registra automáticamente cualquier llamado a funciones marcadas
- [ ] Eventos mínimos auditados:
  - LOGIN_EXITOSO, LOGIN_FALLIDO, LOGOUT, SESION_EXPIRADA
  - PACIENTE_CREADO, PACIENTE_MODIFICADO
  - TRIAGE_CREADO, TRIAGE_ESTADO_CAMBIADO, TRIAGE_CERRADO
  - SIGNOS_VITALES_REGISTRADOS, SIGNOS_VITALES_MODIFICADOS
  - EVALUACION_CLINICA_REGISTRADA
  - INFERENCIA_EJECUTADA, INFERENCIA_FALLIDA
  - CLASIFICACION_VALIDADA, RECLASIFICACION
  - MODELO_ACTIVADO, MODELO_DESACTIVADO
- [ ] Test que verifica que no se puede eliminar un registro de auditoría

## Dependencias
TT-E1-02 (BD y modelo de dominio)

## Subtareas
- [ ] Crear tabla Auditoria en el esquema
- [ ] Implementar decorador @auditar
- [ ] Integrar eventos de auditoría en HU-E1-01 (login), HU-E2-01 (registro paciente), HU-E2-04 (signos vitales), HU-E2-06 (estados), HU-E4-01 (inferencia), HU-E4-03 (validación)
- [ ] Implementar test de inmutabilidad
