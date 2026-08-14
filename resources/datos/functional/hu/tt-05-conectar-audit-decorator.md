---
id: TT-05
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 1
dependencies: "TT-01"
---

# TT-05: Conectar audit_decorator.py a AuditService

## Descripción

El decorador `@auditar` en `audit_decorator.py` es actualmente un stub que solo imprime en consola (`print()`). No está conectado al `AuditService.register()`, por lo que no persiste las auditorías. Para la API REST, se necesita que el middleware de auditoría registre automáticamente cada acción en la tabla `Auditoria`.

## Criterios de Done

- [ ] El decorador `@auditar` acepta una acción (string) y registra en `AuditService` en vez de imprimir en consola.
- [ ] El decorador captura automáticamente el usuario desde el contexto (en Streamlit: `st.session_state.user`; en FastAPI: `request.state.user`).
- [ ] Se documenta el contrato del decorador: qué parámetros requiere la función decorada, qué información se registra.
- [ ] Alternativamente, si el enfoque de decorador no escala bien para FastAPI, se implementa un middleware de FastAPI que registre cada request en `Auditoria`.
- [ ] Los registros de auditoría aparecen en la tabla `Auditoria` y son visibles desde la página de auditoría.

## Recurso de datos involucrado

No aplica — es infraestructura transversal.

## Subtareas

- [ ] Analizar si el enfoque de decorador funciona para FastAPI o es mejor un middleware
- [ ] Implementar la conexión a `AuditService.register()`
- [ ] Verificar que las entradas aparecen en la tabla Auditoria
