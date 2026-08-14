---
id: TT-E4-01
type: Tarea Técnica
epic: E4 - Motor de IA y Explicabilidad
priority: Highest
points: 3
---

# TT-E4-01: Servicio de carga del modelo serializado al iniciar la app

## Descripción
Cargar en memoria el artefacto del modelo (TT-E3-09) al iniciar la demo, con caché de embeddings NLP y fallback a modo degradado si el modelo no está disponible (RNF-009, RNO-006/007).

## Criterios de Done
- [ ] Carga en el arranque con log de versión del modelo cargado.
- [ ] Circuit breaker/timeout en la llamada de inferencia con fallback a triaje manual.
- [ ] Indisponibilidad registrada en auditoría con timestamp y causa (RNO-007).
- [ ] Tiempo de carga documentado en README.

## Dependencias
TT-E3-09 + E2 completo
