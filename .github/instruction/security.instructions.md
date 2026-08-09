---
description: "Reglas base de seguridad del kit — cuándo un módulo requiere auditoría profunda de Muralla más allá del eje de seguridad de Centinela, y los mínimos no negociables de autenticación, secretos y validación de input. Siempre activas sobre código que maneje auth, datos sensibles o integraciones externas."
applyTo: "**/*.{ts,tsx,js,jsx,py,java,kt,cs,go,rb,php,sql,yml,yaml,env}"
---

# Seguridad — Reglas Base del Kit

Este archivo define cuándo el eje de seguridad de `centinela` (una verificación
entre cinco) no es suficiente, y hace falta la auditoría dedicada de
`muralla`. También fija los mínimos no negociables que aplican siempre,
se invoque o no una skill formal.

Este archivo es **complementario**, no un reemplazo, de
`security-and-owasp.instructions.md` (la guía genérica OWASP Top 10 completa
ya presente en el proyecto) — ese archivo cubre el detalle técnico
exhaustivo por categoría OWASP; este archivo define el criterio de cuándo
escalar a auditoría formal y los mínimos que se verifican siempre.

## Cuándo un módulo requiere `muralla` (no solo el eje de seguridad de `centinela`)

- Maneja autenticación o autorización (login, tokens, sesiones, permisos).
- Procesa o almacena datos sensibles o PII (datos personales, médicos,
  financieros).
- Recibe input externo que llega sin validar desde fuera del sistema
  (endpoints públicos, webhooks, carga de archivos).
- Maneja secretos, credenciales o llaves de API.
- Se integra con un servicio de terceros (pagos, mensajería, servicios
  externos).
- `centinela` marcó un hallazgo en su eje de seguridad que requiere
  contexto de amenaza más profundo que un comentario puntual.

Si ninguna de estas condiciones aplica, el eje de seguridad de `centinela`
es suficiente y no hace falta invocar `muralla` aparte.

## Mínimos no negociables (siempre, con o sin skill invocada)

- Ningún secreto, contraseña, token o llave en código, logs, mensajes de
  commit o configuración versionada — siempre en variables de entorno o
  gestor de secretos.
- Todo input externo se valida y sanitiza antes de usarse — nunca se confía
  en el origen.
- Toda consulta a base de datos es parametrizada — nunca concatenación de
  strings.
- Toda ruta protegida verifica autenticación primero y autorización
  después (permiso específico, no solo "está logueado").
- Deny by default: acceso solo si hay una regla explícita que lo permite.
- Dependencias nuevas se verifican contra vulnerabilidades conocidas antes
  de incorporarse.

## Relación con el resto del kit

- `centinela` verifica estos mínimos como parte de su eje 1 de seguridad,
  en cada revisión de código.
- `muralla` los verifica en profundidad — con checklist OWASP Top 10
  completo, modelado de amenazas básico y auditoría de dependencias — solo
  cuando el módulo entra en alguna de las condiciones de escalamiento de
  arriba.
- `security-and-owasp.instructions.md` (genérico, en inglés) queda como
  referencia técnica exhaustiva por categoría OWASP para cuando `muralla`
  necesita el detalle completo de una vulnerabilidad específica.
