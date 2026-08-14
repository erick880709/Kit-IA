---
id: HU-E8-01
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Alta
points: 2
---

# HU-E8-01: Administrador visualiza lista de usuarios

## Como
Administrador

## Quiero
Ver una tabla con todos los usuarios del sistema (nombre, rol, email, estado, último acceso)

## Para
Tener visibilidad completa de quién tiene acceso al sistema

## Criterios de Aceptación
- [ ] CA1: La página "Gestión de Usuarios" solo es accesible para el rol Administrador
- [ ] CA2: Se muestra una tabla con columnas: Usuario, Email, Rol, Activo (Sí/No), Último Acceso, Fecha Creación
- [ ] CA3: Los usuarios activos se muestran con badge verde, los inactivos con badge gris
- [ ] CA4: La tabla se ordena por fecha de creación (más reciente primero)
- [ ] CA5: Se muestra el total de usuarios en la cabecera

## Subtareas
- [ ] Crear `user_management_page.py` con estructura base
- [ ] Implementar `_render_users_table()` con datos de `list_users()`
- [ ] Agregar badges de estado (activo/inactivo) con colores
- [ ] Registrar ruta en `app.py` y sidebar del Administrador
