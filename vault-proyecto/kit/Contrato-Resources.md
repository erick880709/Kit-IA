---
fecha: 2026-08-13
tags: [kit-ia, contrato]
proyecto: Kit IA
---

# Contrato `resources/`

Carpetas de entrada/salida que todo skill respeta:

| Carpeta | Contenido |
|---|---|
| `resources/functional/requests/` | RF extraídos por janus |
| `resources/functional/hu/` | HU/TT generadas por desglosador |
| `resources/architecture/` | Documento de arquitectura, despliegues |
| `resources/architecture/definitions/` | RNF/RT |
| `resources/architecture/adr/` | Decisiones de arquitectura |
| `resources/design/models/` | Información de diseño (RD) |
| `resources/design/mockups/` | Mockups de figma-prd-mockups |
| `resources/engineering/` | Código generado por builder/tdd |
| `resources/engineering/release/` | Artefactos de entrega |
| `resources/qa/` | Planes, runbooks, evidencia |
| `resources/security/` | Auditorías y hardening |
| `resources/summary/` | Resúmenes de licitación |
| `resources/session/` | Estado entre sesiones (memoria) |

> Nota: en el repo del Kit IA, `resources/` contiene hoy solo `architecture/adr/` y `session/` — las 13 carpetas se crean al usar el kit sobre un proyecto real.
