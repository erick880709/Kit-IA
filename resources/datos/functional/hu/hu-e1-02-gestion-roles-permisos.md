---
id: HU-E1-02
type: Historia de Usuario
epic: 001-fundacion-del-sistema
priority: Alta
points: 5
---

# HU-E1-02: Gestión de Roles y Permisos (RBAC)

## Como
Administrador del Sistema

## Quiero
Crear, editar y desactivar usuarios, y asignarles roles (Administrador, Médico, Enfermera, Investigador, Auditor)

## Para
Controlar quién accede a cada funcionalidad del sistema según el principio de mínimo privilegio

## Criterios de Aceptación
- [ ] CA1: El Administrador ve una pantalla de "Gestión de Usuarios" con listado de todos los usuarios
- [ ] CA2: Puede crear un nuevo usuario (nombre, contraseña inicial, rol)
- [ ] CA3: Puede editar el rol de un usuario existente
- [ ] CA4: Puede desactivar un usuario (no se elimina, se marca como inactivo)
- [ ] CA5: Un usuario con rol "Enfermera" NO puede ver las pantallas de "Gestión de Modelos" ni "Auditoría"
- [ ] CA6: Un usuario con rol "Médico" puede ver el flujo clínico y el dashboard, pero NO puede gestionar modelos
- [ ] CA7: Cada cambio de rol o estado de usuario genera un registro de auditoría (RNAU-002)

## Recurso de datos involucrado
- **Nombre:** Usuario (extensión de HU-E1-01)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdUsuario | UUID | Sí | Heredado de HU-E1-01 |
| Rol | Catálogo | Sí | Administrador / Médico / Enfermera / Investigador / Auditor |
| Activo | Booleano | Sí | true = activo, false = desactivado |
| ModificadoPor | UUID | Sí | Usuario administrador que realizó el cambio |
| FechaModificacion | DateTime | Sí | Automático |

### Relaciones con otros recursos
- `Auditoria` (1:N): cada cambio de rol/estado genera registro de auditoría

## Subtareas
- [ ] Diseñar pantalla de Gestión de Usuarios (solo visible para Admin)
- [ ] Implementar CRUD de usuarios en backend
- [ ] Implementar decorador/interceptor de permisos por rol
- [ ] Configurar visibilidad condicional de pantallas según rol
- [ ] Conectar cambios de rol con módulo de auditoría
