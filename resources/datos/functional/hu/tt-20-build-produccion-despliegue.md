---
id: TT-20
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 2
dependencies: "TT-18, TT-19"
---

# TT-20: Build de producción y despliegue

## Descripción

Configurar el build de producción del frontend React y empaquetar la aplicación completa (backend FastAPI + frontend estático) para despliegue en un solo servidor, alineado con RT-007 (app autocontenida).

## Criterios de Done

- [ ] `npm run build` genera los archivos estáticos en `frontend/dist/`.
- [ ] FastAPI sirve los archivos estáticos del frontend (con `StaticFiles` de Starlette) para que la app completa se acceda desde un solo puerto (`:8000`).
- [ ] Ruta catch-all en FastAPI: cualquier ruta no reconocida por la API sirve `index.html` (para soportar React Router en modo history).
- [ ] Variables de entorno de producción documentadas en `.env.example` o README.
- [ ] Script `start.sh` / `start.ps1` que inicia el servidor uvicorn con el frontend empaquetado.
- [ ] `README.md` actualizado con instrucciones de instalación y despliegue para el nuevo stack.
- [ ] La app completa se accede desde `http://localhost:8000` (sin necesidad de puerto separado para frontend).
- [ ] Streamlit puede desactivarse una vez que React está en producción.

## Recurso de datos involucrado

No aplica — es infraestructura de despliegue.

## Subtareas

- [ ] Configurar build de producción Vite
- [ ] Configurar FastAPI para servir archivos estáticos
- [ ] Configurar ruta catch-all para React Router
- [ ] Crear script de arranque
- [ ] Actualizar README con nuevas instrucciones
- [ ] Verificar despliegue completo
