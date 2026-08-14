---
id: HU-01
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 3
---

# HU-01: Login y autenticación JWT

## Como
Profesional sanitario (enfermero/a, médico/a, administrador)

## Quiero
Iniciar sesión en el sistema con mis credenciales y que mi sesión se mantenga activa mientras uso la aplicación

## Para
Acceder al sistema de triaje de forma segura y que mis acciones queden registradas con mi identidad

## Criterios de Aceptación

- [ ] CA1: La pantalla de login muestra un formulario con campos de Usuario y Contraseña, centrado en un card con el logo/título del sistema.
- [ ] CA2: Al ingresar credenciales correctas y presionar "Iniciar Sesión", el sistema valida contra `POST /api/auth/login`, almacena el token JWT en `localStorage`, y redirige al Dashboard.
- [ ] CA3: Si las credenciales son incorrectas, se muestra un mensaje de error genérico "Usuario o contraseña inválidos" (sin revelar cuál de los dos falló).
- [ ] CA4: Si el token JWT expira (15 min por defecto), la siguiente llamada a la API recibe 401 y el sistema redirige automáticamente a la pantalla de login con mensaje "Sesión expirada".
- [ ] CA5: El botón "Cerrar Sesión" en el sidebar limpia el token de `localStorage`, llama a `POST /api/auth/logout`, y redirige al login.
- [ ] CA6: Existe un enlace "¿Olvidó su contraseña?" que inicia el flujo de recuperación (solicitar token → ingresar token → nueva contraseña).
- [ ] CA7: Los campos de contraseña tienen un botón para mostrar/ocultar (toggle visibility).
- [ ] CA8: El formulario de login es responsive y funciona correctamente en tablet (768px).

## Recurso de datos involucrado

No aplica — es flujo de autenticación.

## Subtareas

- [ ] Crear `pages/LoginPage.tsx` con formulario (React Hook Form + Zod)
- [ ] Crear `api/auth.ts` (login, logout, resetToken, resetPassword)
- [ ] Implementar `useAuth` hook con React Context
- [ ] Implementar interceptor Axios para 401 → redirigir a login
- [ ] Implementar flujo de "olvidó su contraseña" (3 pasos)
- [ ] Estilos responsive para tablet
- [ ] Probar login exitoso, fallido, sesión expirada
