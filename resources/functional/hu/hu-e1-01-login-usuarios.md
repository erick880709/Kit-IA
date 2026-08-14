---
id: HU-E1-01
type: Historia de Usuario
epic: E1 - Fundación del Sistema
priority: Highest
points: 3
---

# HU-E1-01: Login de usuarios con autenticación

## Como
Cualquier usuario registrado (Médico, Enfermera, Administrador, Investigador, Auditor)

## Quiero
Iniciar sesión con usuario y contraseña

## Para
acceder solo a las pantallas de mi rol (RF-SEC-001).

## Criterios de Aceptación
- [ ] CA1: Credenciales válidas → acceso a la pantalla inicial del rol.
- [ ] CA2: Contraseñas almacenadas con hash (bcrypt/argon2), nunca en texto plano.
- [ ] CA3: Bloqueo temporal tras 5 intentos fallidos.
- [ ] CA4: Sesión expira por inactividad (ver HU-E1-04).

## Dependencias
TT-E1-02

## Subtareas
- [ ] Formulario de login
- [ ] Hash y verificación de contraseñas
- [ ] Bloqueo por intentos fallidos
