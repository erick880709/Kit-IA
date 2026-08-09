# Guía: Gap Analysis y Roadmap de Migración (AS-IS → TO-BE)

Esta guía detalla las secciones 14 y 15 de la plantilla de documento cuando trabajas en Caso C (evolución de arquitectura). El objetivo de estas dos secciones es que alguien que nunca vio el AS-IS ni el TO-BE entienda, sin leer nada más, qué cambia, cuánto cuesta cambiarlo y en qué orden hacerlo.

## Análisis de Brechas (Gap Analysis)

Para cada diferencia relevante entre el estado actual y el objetivo, documenta una fila. No listes diferencias triviales (renombrar una variable no es una brecha arquitectónica) — enfócate en cambios que afecten componentes, contratos entre servicios, modelo de datos, o atributos de calidad.

```markdown
| Componente / Área | Estado Actual (AS-IS) | Estado Objetivo (TO-BE) | Esfuerzo | Riesgo si no se aborda |
|---|---|---|---|---|
| Autenticación | Sesiones en memoria del monolito | Servicio de identidad centralizado (OAuth2/OIDC) | Alto | No soporta el requerimiento de SSO multi-app |
| Base de datos de catálogo | PostgreSQL única, acoplada al monolito | Base de datos propia del servicio de Catálogo | Medio | Bloquea el escalamiento independiente del catálogo |
| Notificaciones | Envío síncrono dentro del request | Cola de eventos + worker asíncrono | Bajo | Latencia alta percibida por el usuario en picos de tráfico |
```

Criterios para estimar esfuerzo (ajusta la escala si el usuario ya usa otra en su organización):
- **Bajo:** cambio contenido a un componente, sin migración de datos, sin downtime.
- **Medio:** afecta a más de un componente o requiere migración de datos con plan de rollback simple.
- **Alto:** redefine contratos entre servicios, requiere migración de datos con downtime o coexistencia temporal de dos sistemas, o toca un atributo de calidad transversal (seguridad, disponibilidad).

## Roadmap de Migración

Estructura el roadmap en fases incrementales — cada fase debe dejar el sistema en un estado desplegable y funcional, no una foto intermedia rota. Evita proponer un "big bang" (reescritura total de una sola vez) salvo que el usuario lo pida explícitamente y justifiques por qué no hay alternativa incremental razonable; los big bangs concentran todo el riesgo en un solo punto de falla.

```markdown
### Fase 1: [Nombre — ej. "Desacoplar autenticación"]
- **Qué incluye:** [componentes/cambios de esta fase]
- **Qué habilita:** [por qué esta fase debe ir primero — qué depende de ella]
- **Cómo se valida:** [criterio objetivo de que la fase fue exitosa antes de avanzar — métricas, pruebas, criterios de aceptación]
- **Riesgo principal y mitigación:** [...]

### Fase 2: [Nombre]
...
```

Pautas para secuenciar las fases:
- Prioriza primero lo que **desbloquea** otras fases (ej. separar un servicio de identidad antes de dividir servicios que dependen de autenticación centralizada), no necesariamente lo que es "más fácil" o "más visible".
- Prefiere el patrón *strangler fig* (el sistema nuevo convive con el legacy y le va quitando responsabilidades gradualmente) sobre reescrituras paralelas completas, salvo que el legacy sea tan pequeño que no lo justifique.
- Cada fase debe tener una forma clara de revertirse o al menos de detenerse sin dejar el sistema en un estado peor que antes de empezarla.
- Si el roadmap tiene más de 5-6 fases, agrúpalas en hitos/trimestres para que el documento siga siendo legible a nivel ejecutivo, y deja el detalle fase por fase como sub-secciones.
