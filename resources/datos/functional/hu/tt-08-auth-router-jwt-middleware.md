---
id: TT-08
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 5
dependencies: "TT-07, TT-01"
---

# TT-08: Implementar AuthRouter + JWT middleware

## Descripción

Crear el router de autenticación (`routers/auth.py`) con endpoints de login, logout, permisos, y reset de contraseña. Implementar el middleware de verificación JWT como una dependencia reutilizable de FastAPI (`get_current_user`).

## Criterios de Done

- [ ] `routers/auth.py` creado con endpoints:
  - `POST /api/auth/login` — recibe `LoginRequest`, valida con `AuthService.authenticate()`, genera JWT con claims `{sub, rol, exp}`, retorna `LoginResponse`.
  - `POST /api/auth/logout` — endpoint protegido, llama a `AuthService.logout()`, retorna confirmación (el frontend descarta el token).
  - `GET /api/auth/permissions` — endpoint protegido, retorna `AuthService.get_allowed_pages(rol)` para el usuario autenticado.
  - `POST /api/auth/reset-token` — endpoint público, genera token de reset.
  - `POST /api/auth/reset-password` — endpoint público, valida token + nueva contraseña.
- [ ] `middleware/auth.py` creado con dependencia `get_current_user`:
  - Extrae token del header `Authorization: Bearer <token>`.
  - Decodifica JWT con `python-jose`.
  - Verifica expiración.
  - Retorna `TokenData` o lanza `HTTPException(401)`.
- [ ] Dependencia `require_role(rol)` para endpoints admin-only.
- [ ] Contraseñas nunca se retornan en responses (usar `exclude` en Pydantic).
- [ ] Login con credenciales inválidas retorna 401 con mensaje genérico (no revelar si el usuario existe).

## Recurso de datos involucrado

- **Nombre del recurso:** Token (JWT)
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| access_token | str | Sí | JWT firmado con HS256 |
| token_type | str | Sí | "bearer" |
| user | dict | Sí | `{username, rol, email}` sin contraseña |
| permissions | list[str] | Sí | Lista de páginas permitidas según rol |

## Subtareas

- [ ] Crear `routers/auth.py` con 5 endpoints
- [ ] Crear `middleware/auth.py` con `get_current_user` y `require_role`
- [ ] Configurar JWT en `settings.py` (secret, algorithm, expiration)
- [ ] Probar login/logout con Swagger UI
- [ ] Probar endpoints protegidos con token válido e inválido
