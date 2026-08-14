---
id: HU-E8-03
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Alta
points: 3
---

# HU-E8-03: Administrador actualiza datos de usuario

## Como
Administrador

## Quiero
Modificar el rol, email y estado (activar/desactivar) de cualquier usuario

## Para
Mantener el control de acceso actualizado según cambios organizacionales

## Criterios de Aceptación
- [ ] CA1: Cada fila de la tabla tiene un botón "Editar" que abre un formulario de edición
- [ ] CA2: Se puede modificar: Rol, Email, Activo/Inactivo
- [ ] CA3: Al desactivar un usuario, se muestra confirmación: "¿Está seguro? El usuario no podrá iniciar sesión."
- [ ] CA4: Al reactivar un usuario inactivo, se resetea el contador de intentos fallidos
- [ ] CA5: Los cambios se reflejan inmediatamente en la tabla
- [ ] CA6: No se puede cambiar el rol del propio administrador que está logueado

## Subtareas
- [ ] Implementar modal/formulario de edición con `st.expander` o `st.dialog`
- [ ] Agregar toggle Activo/Inactivo con `st.checkbox` y confirmación
- [ ] Validar que el admin no se edite a sí mismo (comparar `id_usuario`)
- [ ] Llamar a `update_user()` del AuthService extendido (TT-E8-01)
