---
id: TT-02
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 1
dependencies: "TT-01"
---

# TT-02: Mover SQL fallback de login_page.py a AuthService

## Descripción

Actualmente `login_page.py` (L72-82) contiene un bloque de código que hace una consulta SQL directa (`SELECT * FROM Usuario`) como fallback cuando `auth.login()` falla. Esto viola la separación de capas y sería imposible de replicar en React.

El fallback debe integrarse en `AuthService.authenticate()` o eliminarse si ya no es necesario. Dado que el fallback existe porque `auth.login()` delega en `authenticate()` y aparentemente había un problema de caché de Streamlit, al migrar a FastAPI este caché no existirá.

## Criterios de Done

- [ ] Se analiza el motivo real del fallback SQL en L72-82 (¿es un workaround para el caché de Streamlit? ¿o maneja un caso de borde real?)
- [ ] Si es un workaround de caché: se elimina el bloque SQL del UI y se ajusta `authenticate()` si es necesario.
- [ ] Si es un caso de borde legítimo: la lógica se mueve a `AuthService.authenticate()` como parte del flujo normal de autenticación.
- [ ] `login_page.py` ya no contiene consultas SQL directas.
- [ ] Login funciona correctamente tanto en Streamlit (mientras coexista) como en la futura API.

## Recurso de datos involucrado

No aplica — es movimiento de código entre capas.

## Subtareas

- [ ] Identificar la causa raíz del fallback SQL (¿Streamlit cache? ¿bcrypt fallback?)
- [ ] Integrar la lógica en `AuthService.authenticate()` o eliminarla
- [ ] Limpiar `login_page.py` L72-82
- [ ] Verificar login
