---
id: TT-06
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "TT-01, TT-02, TT-03, TT-04"
---

# TT-06: Setup proyecto FastAPI — estructura base, CORS, lifespan

## Descripción

Crear la aplicación FastAPI (`main.py`) que reemplaza a `app.py` como punto de entrada del backend. La app debe inicializar la base de datos, cargar el modelo IA en el evento `lifespan`, configurar CORS para el frontend React, y montar todos los routers.

## Criterios de Done

- [ ] Archivo `sistema-triaje-ia/main.py` creado con la factory `create_app()`.
- [ ] `lifespan` event: `startup` inicializa `init_db()` + carga el modelo con `InferenceService.load_model()`. `shutdown` limpia recursos.
- [ ] CORS configurado para `http://localhost:5173` (Vite dev) y el origen de producción.
- [ ] `settings.py` extendido con variables: `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRATION_MINUTES`, `CORS_ORIGINS`, `MODELS_DIR`.
- [ ] Estructura de carpetas creada: `routers/`, `schemas/`, `middleware/`.
- [ ] `requirements.txt` actualizado con: `fastapi`, `uvicorn[standard]`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `pydantic`.
- [ ] La app arranca con `uvicorn main:app --reload --port 8000`.
- [ ] Swagger UI accesible en `http://localhost:8000/docs`.

## Recurso de datos involucrado

No aplica — es infraestructura del proyecto.

## Subtareas

- [ ] Crear `main.py` con factory y lifespan
- [ ] Extender `settings.py` con variables de entorno para JWT y CORS
- [ ] Crear estructura de carpetas: `routers/`, `schemas/`, `middleware/`
- [ ] Configurar `requirements.txt` con nuevas dependencias
- [ ] Verificar arranque y Swagger UI
