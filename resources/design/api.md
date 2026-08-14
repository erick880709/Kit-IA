# Patrones de API — TriajeIA

> Generado por `genesis` (FASE 7). TriajeIA es una demo Streamlit **sin API REST pública**; estas convenciones rigen los servicios internos de la app y el contrato si se evoluciona a FastAPI (ADR-001).

## Endpoint de referencia (módulo existente)

No hay endpoints REST en el scaffold. Referencia interna: `scripts/healthcheck.py` → `app/infra/db.db_ok()`.

## Estructura de respuesta exitosa

```json
{ "data": { } }
```

- Objetos individuales: `{ "data": { ... } }`
- Listas paginadas: `{ "data": [ ... ], "meta": { "page": 1, "page_size": 20, "total": 0 } }`

## Estructura de respuesta de error

```json
{ "error": { "codigo": "VALIDACION", "mensaje": "Campo obligatorio ausente", "detalle": "motivo_discrepancia" } }
```

Códigos: `VALIDACION`, `NO_AUTORIZADO`, `PROHIBIDO`, `NO_ENCONTRADO`, `CONFLICTO`, `INFERENCIA`, `ERROR_INTERNO`.

## Paginación

Parámetros `page` (1-based) y `page_size` (default 20, máx 100). Respuesta con `meta`.

## Autenticación

Local en la demo: correo + contraseña (hash bcrypt) + token simulado por email para recuperación. Bloqueo tras 3 intentos (15 min). Si se expone API: header `Authorization: Bearer <token>`.

## Historial de cambios del contrato

- v0.1.0 (2026-08-13): convenciones base definidas por `genesis` (sin recursos de negocio).
