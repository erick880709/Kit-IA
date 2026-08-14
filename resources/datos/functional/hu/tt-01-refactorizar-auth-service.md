---
id: TT-01
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 2
dependencies: "Ninguna"
---

# TT-01: Refactorizar AuthService — eliminar dependencias de Streamlit

## Descripción

Extraer las 3 referencias a `st.session_state` del archivo `app/services/auth_service.py` para que el servicio sea 100% independiente del framework de presentación. Esto es un pre-requisito para exponer `AuthService` vía API REST.

Los métodos afectados son:
- `logout()` (L128-130): actualmente hace `st.session_state.user = None`, `st.session_state.login_time = None`, `st.session_state.page = "login"`. Debe convertirse en un método puro que solo retorne sin dependencias de Streamlit.
- `check_session_timeout()` (L373-381): actualmente accede a `st.session_state.login_time` y `st.session_state.app_config`. Debe recibir `login_time` y `timeout_minutes` como parámetros.
- `get_timeout_minutes()` (L388): actualmente accede a `st.session_state.app_config`. Debe recibir `config` como parámetro.

## Criterios de Done

- [ ] `logout()` ya no importa ni usa `st`. Es un método puro. La limpieza de sesión se maneja en la capa de presentación (sea Streamlit o FastAPI).
- [ ] `check_session_timeout(login_time, timeout_minutes)` recibe los parámetros necesarios y no accede a `st.session_state`.
- [ ] `get_timeout_minutes(config)` recibe la configuración como parámetro.
- [ ] Los tests unitarios existentes (si los hay) siguen pasando. Si no hay tests, se verifica manualmente que Streamlit sigue funcionando con los cambios.
- [ ] `import streamlit as st` se elimina del archivo si ya no es necesario en ningún otro método.

## Recurso de datos involucrado

No aplica — es una refactorización interna.

## Subtareas

- [ ] Refactorizar `logout()` a método puro
- [ ] Refactorizar `check_session_timeout()` a recibir parámetros
- [ ] Refactorizar `get_timeout_minutes()` a recibir config
- [ ] Actualizar `login_page.py` para pasar parámetros a los métodos refactorizados (mantener Streamlit funcional)
- [ ] Verificar que login/logout en Streamlit sigue funcionando
