---
id: TT-E8-02
type: Tarea Técnica
epic: E8-Gestión-Usuarios
priority: Alta
points: 5
---

# TT-E8-02: Crear página de Gestión de Usuarios (UI)

## Descripción
Crear `user_management_page.py` con tres secciones: tabla de usuarios, formulario de creación, panel de edición. Integrar en el router de `app.py` bajo el menú "Soporte" del Administrador. La página debe usar los métodos extendidos del `AuthService` (TT-E8-01).

## Criterios de Done
- [ ] Página renderiza tabla con todos los usuarios usando `list_users()`
- [ ] Formulario "Nuevo Usuario" con validaciones (username único, contraseña ≥ 6 caracteres, rol ≠ Administrador)
- [ ] Cada fila tiene botones: Editar, Restablecer Contraseña, Activar/Desactivar
- [ ] Panel de edición permite cambiar Rol, Email, y toggle Activo/Inactivo
- [ ] Restablecer contraseña muestra la nueva contraseña en un `st.success()` destacado
- [ ] La página solo renderiza si `st.session_state.user.rol == "Administrador"`
- [ ] Se integra en `app.py` como `elif page == "gestion_usuarios"` y en el sidebar en "Soporte"

## Dependencias
TT-E8-01 (métodos `update_user()` y `reset_password()`)

## Subtareas
- [ ] Crear `app/ui/user_management_page.py` con `render_user_management()`
- [ ] Implementar `_render_users_table()` con `st.dataframe` o `st.columns` por fila
- [ ] Implementar formulario "Nuevo Usuario" en `st.expander` o sección dedicada
- [ ] Implementar panel de edición con `st.form` dentro de `st.expander` por usuario
- [ ] Agregar lógica de Restablecer Contraseña con `st.button` + `reset_password()`
- [ ] Agregar ruta en `app.py` y botón en sidebar del Admin
- [ ] Probar flujo completo: crear → editar → desactivar → restablecer contraseña
