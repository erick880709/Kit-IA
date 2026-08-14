---
id: HU-E8-04
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Media
points: 2
---

# HU-E8-04: Administrador restablece contraseña de usuario

## Como
Administrador

## Quiero
Generar una nueva contraseña temporal para cualquier usuario

## Para
Resolver bloqueos de acceso sin depender del flujo de "olvidé mi contraseña"

## Criterios de Aceptación
- [ ] CA1: Cada fila de la tabla tiene un botón "Restablecer Contraseña"
- [ ] CA2: Al hacer clic, se genera una contraseña aleatoria de 8 caracteres y se muestra en pantalla
- [ ] CA3: La nueva contraseña se hashea con bcrypt antes de guardarse
- [ ] CA4: Se muestra un mensaje: "Nueva contraseña temporal: XXXXXXXX — entréguela al usuario de forma segura"
- [ ] CA5: La contraseña temporal se muestra UNA sola vez; al recargar la página ya no es visible
- [ ] CA6: [SUPUESTO] No se fuerza el cambio de contraseña en el próximo inicio de sesión en esta iteración

## Subtareas
- [ ] Implementar `reset_password()` en AuthService (TT-E8-01)
- [ ] Agregar botón "Restablecer Contraseña" en cada fila de la tabla
- [ ] Usar `secrets.token_urlsafe(6)` para generar contraseña aleatoria
- [ ] Mostrar contraseña en `st.success()` con estilo destacado
