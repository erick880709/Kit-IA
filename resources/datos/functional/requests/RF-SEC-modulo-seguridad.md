# RF-SEC: Módulo de Seguridad

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 50, Módulo Seguridad
**Prioridad:** Crítica

## Descripción
El sistema implementará mecanismos de autenticación, autorización basada en roles, protección de datos en tránsito y en reposo, y gestión de sesiones, en cumplimiento de la Ley 1581 de 2012 de protección de datos personales y de las políticas institucionales de seguridad de la información.

## Actores involucrados
- Administrador del Sistema (gestión de usuarios y roles)
- Todos los usuarios (autenticación)

## Criterios de aceptación

### RF-SEC-001 — Inicio de Sesión (Autenticación)
- Todo acceso al sistema requiere autenticación (RNS-001).
- Mecanismo: usuario + contraseña (con posibilidad de integrar autenticación institucional si existe).
- Las contraseñas nunca se almacenan en texto plano (RNS-006: hashing + salt).

### RF-SEC-002 — Gestión de Roles
- Roles definidos: Administrador, Médico, Enfermera, Investigador, Auditor.
- Cada rol tiene permisos diferenciados según el principio de mínimo privilegio (RNS-005).
- El Administrador puede crear, editar y desactivar usuarios, y asignar/revocar roles.

### RF-SEC-003 — Recuperación de Contraseña
- Flujo de recuperación de contraseña cuando el sistema utilice autenticación propia (no integrada con directorio institucional).
- Envío de enlace de restablecimiento por correo electrónico.

### RF-SEC-004 — Cierre Automático de Sesión
- Las sesiones inactivas expiran automáticamente después de un tiempo configurable (RNS-007).
- La expiración redirige a la pantalla de login.
- El tiempo de inactividad debe ser configurable por el Administrador.

### Seguridad en Tránsito y Reposo (derivado de RNS-002, RNS-003)
- Toda comunicación entre el cliente y el servidor utiliza TLS (HTTPS).
- Los datos sensibles (identificadores de pacientes, datos clínicos) se cifran en reposo en la base de datos.
- Las claves de cifrado se gestionan de forma segura (no en texto plano en archivos de configuración).

## Dependencias / relacionados
- RNS-001 a 010: Reglas de Seguridad.
- RNS-009: Cumplimiento Ley 1581 de 2012.
- `04-ESPECIFICACION-APLICACION-DEMO.md`: pantalla de Login.

## Notas del analista
- Para el alcance de la demo (TFM Tipo 2+3), la autenticación puede simplificarse (ej. autenticación básica sin integración LDAP/OAuth), pero los principios de seguridad (hash de contraseñas, TLS, roles) deben estar presentes.
- El cifrado en reposo puede ser provisto por el motor de base de datos (ej. TDE en SQL Server, o cifrado a nivel de aplicación).
