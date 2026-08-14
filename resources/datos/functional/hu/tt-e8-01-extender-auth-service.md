---
id: TT-E8-01
type: Tarea Técnica
epic: E8-Gestión-Usuarios
priority: Alta
points: 3
---

# TT-E8-01: Extender AuthService con update_user() y reset_password()

## Descripción
Implementar método `update_user()` que permita modificar Email, Rol y Activo/Inactivo de cualquier usuario. Incluir método `reset_password()` para generar y guardar nueva contraseña hasheada. Refactorizar `update_user_role()` para que delegue en `update_user()`. Verificar siempre que quien ejecuta es Administrador.

## Criterios de Done
- [ ] `update_user(admin_user_id, target_user_id, email, rol, activo)` actualiza los campos indicados
- [ ] `reset_password(admin_user_id, target_user_id)` genera contraseña aleatoria de 8 caracteres, la hashea y la guarda; retorna la contraseña en texto plano
- [ ] Ambos métodos verifican que quien ejecuta es Administrador
- [ ] Ambos métodos registran la acción en `ControlCambios`
- [ ] `update_user_role()` se simplifica para llamar a `update_user()` internamente

## Recurso de datos involucrado

### Recurso
- **Nombre:** Usuario (modificación de registro existente)
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Email | TEXT | No | Formato email válido |
| Rol | TEXT | Sí | CHECK: Enfermera, Médico, Investigador, Auditor |
| Activo | INTEGER | Sí | 0 = inactivo, 1 = activo |
| PasswordHash | TEXT | Sí | Solo modificado por reset_password() |

## Dependencias
Ninguna (solo backend)

## Subtareas
- [ ] Implementar `update_user()` con validación de admin y registro en ControlCambios
- [ ] Implementar `reset_password()` con `secrets.token_urlsafe(6)` + bcrypt
- [ ] Refactorizar `update_user_role()` como wrapper de `update_user()`
- [ ] Probar ambos métodos con prueba unitaria desde línea de comandos
