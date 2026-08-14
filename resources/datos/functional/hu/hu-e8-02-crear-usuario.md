---
id: HU-E8-02
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Alta
points: 3
---

# HU-E8-02: Administrador crea nuevo usuario

## Como
Administrador

## Quiero
Registrar un nuevo usuario (enfermera, médico, investigador o auditor) con nombre, email, contraseña y rol

## Para
Dar acceso al sistema a nuevo personal sin intervención técnica

## Criterios de Aceptación
- [ ] CA1: El formulario solicita: Nombre de Usuario, Email, Contraseña, Rol (select: Enfermera/Médico/Investigador/Auditor)
- [ ] CA2: No se permite crear usuarios con rol "Administrador"
- [ ] CA3: Si el nombre de usuario ya existe, se muestra mensaje de error
- [ ] CA4: La contraseña debe tener al menos 6 caracteres
- [ ] CA5: Al crear exitosamente, el usuario aparece en la tabla inmediatamente
- [ ] CA6: El nuevo usuario se crea con estado "Activo"

## Recurso de datos involucrado

### Recurso
- **Nombre:** Usuario (ya existe)
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| NombreUsuario | TEXT | Sí | Único, sin espacios |
| Email | TEXT | Sí | Formato email válido |
| PasswordHash | TEXT | Sí | Bcrypt generado por AuthService |
| Rol | TEXT | Sí | CHECK: Enfermera, Médico, Investigador, Auditor |
| Activo | INTEGER | Sí | DEFAULT 1 |

## Subtareas
- [ ] Agregar formulario de creación en `user_management_page.py`
- [ ] Validar username único usando `list_users()` para verificar duplicados
- [ ] Validar contraseña ≥ 6 caracteres
- [ ] Filtrar rol "Administrador" del select de roles disponibles
