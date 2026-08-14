# RF-014: Seguridad y Control de Acceso por Roles

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-SEC-001 a 004) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §2
**Prioridad:** Alta

## Descripción
El sistema debe autenticar usuarios (login), gestionar roles y permisos por pantalla, permitir recuperación de contraseña y cerrar sesiones automáticamente por inactividad. Los roles definidos: Administrador, Médico, Enfermera, Investigador y Auditor; cada pantalla del inventario indica qué rol(es) la usan.

## Actores involucrados
Todos los roles.

## Criterios de aceptación
- Acceso denegado a pantallas fuera del rol del usuario.
- RBAC con los 5 roles definidos; permisos por pantalla.
- Contraseñas almacenadas con **hash** (no texto plano).
- Comunicaciones protegidas con **TLS** y cifrado en reposo para datos sensibles (épica E1, `resources/datos/functional/reqs/epicas-tfm-jira.csv`).
- Cierre automático de sesión por inactividad (RF-SEC-004).
- Solo administradores gestionan roles y modelos (RF-MOD-*).

## Dependencias / relacionados
[[RF-008]], [[RF-012]], [[RNF-008]].

## Notas del analista
El rol "Administrativo" aparece en el registro de pacientes; la lista canónica de roles es la de 04 §2 (RF-SEC-002).
