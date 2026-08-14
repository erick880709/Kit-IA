---
id: HU-12
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Media
points: 3
---

# HU-12: Gestión de usuarios (admin)

## Como
Administrador del sistema

## Quiero
Crear, editar, desactivar y resetear contraseñas de usuarios del sistema, asignándoles roles específicos

## Para
Administrar el acceso al sistema según los perfiles del personal sanitario

## Criterios de Aceptación

- [ ] CA1: La página muestra una tabla con todos los usuarios: Username, Email, Rol, Estado (Activo/Inactivo), Último Acceso.
- [ ] CA2: **Crear usuario**: botón "➕ Nuevo Usuario" que abre un modal/formulario con campos: Username, Email, Rol (select: Administrador, Médico, Enfermera, Investigador, Auditor), Contraseña inicial.
- [ ] CA3: **Editar usuario**: click en una fila abre panel/modal de edición con Email, Rol, Estado (toggle Activo/Inactivo).
- [ ] CA4: **Desactivar usuario**: toggle o botón que hace soft delete (no elimina el registro, lo marca como inactivo).
- [ ] CA5: **Resetear contraseña**: botón "🔑 Reset Password" que genera una nueva contraseña aleatoria y la muestra una vez (luego el usuario debe cambiarla).
- [ ] CA6: Validaciones: username único, email formato válido, rol debe ser uno de los 5 definidos.
- [ ] CA7: Solo visible para usuarios con rol "Administrador" (validado tanto en frontend como en backend).

## Recurso de datos involucrado

- **Nombre del recurso:** Usuario
- **Capa(s):** frontend (consume GET/POST/PATCH/DELETE /api/users)

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| username | string | Sí | Único |
| email | string | Sí | Formato email, único |
| rol | select | Sí | Catálogo: Administrador, Médico, Enfermera, Investigador, Auditor |
| activo | boolean | Sí | Default: true |
| password | string | Sí (solo en create/reset) | Nunca se muestra almacenada |

## Subtareas

- [ ] Crear `pages/UserManagementPage.tsx`
- [ ] Implementar tabla de usuarios
- [ ] Implementar modal de crear usuario
- [ ] Implementar panel de editar usuario
- [ ] Implementar reset de contraseña
- [ ] Validaciones de formulario
- [ ] Proteger ruta con `requireRole("Administrador")`
- [ ] Probar CRUD completo
