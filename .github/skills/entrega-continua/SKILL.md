---
name: entrega-continua
description: 'Cierra el ciclo de una HU/TT: commits atómicos con historia limpia, pipeline de CI/CD con quality gates automatizados, checklist de pre-lanzamiento con plan de rollback, y retiro seguro de código/features viejos cuando corresponde. Úsala SIEMPRE que el usuario pida "commitear este cambio", "armar el pipeline de CI/CD", "preparar el release", "desplegar a producción", "dar de baja este endpoint/feature viejo", o cuando `revision-calidad` y `seguridad-rendimiento` ya aprobaron el cambio y falta el paso final. Adaptación al español y al contrato de `resources/` de las skills `git-workflow-and-versioning`, `ci-cd-and-automation`, `shipping-and-launch` y `deprecation-and-migration` de addyosmani/agent-skills.'
---

# Entrega Continua (Git, CI/CD, Shipping, Deprecación)

## Resumen

Envuelve cuatro skills del pack `agent-skills`: `git-workflow-and-versioning`,
`ci-cd-and-automation`, `shipping-and-launch` y `deprecation-and-migration`.
Referencia completa (inglés, solo lectura) en
`.github/skills-addy/skills/<nombre>/SKILL.md` de cada una, más
`.github/skills-addy/references/definition-of-done.md`.

Es el último eslabón del pipeline unificado: solo corre después de que
`revision-calidad` y (si aplicaba) `seguridad-rendimiento` ya aprobaron el cambio.

## Entrada esperada

- `resources/engineering/reviews/review-<PR>.md` aprobado.
- `resources/engineering/security/hardening-<modulo>.md` y
  `resources/engineering/perf/budget-<modulo>.md` si el módulo los requería.
- `resources/engineering/adr/` actualizado si hubo decisiones nuevas.

## Salida

- Historia de commits limpia en el repositorio real.
- `resources/engineering/release/checklist-<version>.md`.
- Configuración de pipeline (`.github/workflows/`, `Jenkinsfile`, etc. según
  el stack que ya decidió `genesis`/`builder` — no se reinventa la herramienta de CI/CD aquí).

## Git — commits como punto de guardado

Trunk-based development: ramas de vida corta, commits atómicos (un cambio
lógico por commit, ~100 líneas como referencia igual que en `revision-calidad`),
mensaje que explica el porqué no solo el qué. Cada commit debe dejar el
repositorio en un estado que compila y con tests en verde — es un punto de
guardado real, no un checkpoint a medio terminar.

## CI/CD — Shift Left, Faster is Safer

El pipeline corre los mismos gates que ya se aplicaron manualmente
(`revision-calidad`, tests de `tdd-implementacion`, checklist de
`seguridad-rendimiento`) de forma automática en cada push — "shift left"
significa que el error se detecta lo antes posible en el pipeline, no en
producción. Un pipeline más rápido con gates reales es más seguro que uno
lento que la gente empieza a saltarse.

## Shipping — checklist de pre-lanzamiento

Antes de marcar una feature como lista para producción:

- [ ] Feature flag definido (si aplica) con plan de quién lo activa y cuándo.
- [ ] Plan de rollback explícito, no "revertimos el commit y ya" sin probarlo.
- [ ] Monitoreo (de `documentacion-observabilidad`) activo antes del rollout, no después.
- [ ] Rollout escalonado si el blast radius de un fallo es alto.

## Deprecación — el código es un pasivo, no un activo

Cuando este skill retira código/features viejos: distinguí deprecación
**obligatoria** (rompe si no migran, con fecha límite comunicada) de
**advisoria** (sigue funcionando, se recomienda migrar). Nunca borres código
"zombie" (código muerto que ya no se ejecuta) sin confirmar que de verdad no
tiene camino de ejecución vivo — usá el mismo principio de Chesterton's Fence
que `revision-calidad` aplica a la simplificación.

## Rationalizaciones comunes

| Excusa | Realidad |
|---|---|
| "Total esto lo mergeamos directo a main, es rápido" | Rápido sin gate es rápido hasta que rompe producción; el pipeline existe justamente para no depender de la memoria de nadie. |
| "El rollback lo pensamos si hace falta" | Un plan de rollback pensado después del incidente llega tarde; se define antes del deploy. |
| "Dejamos el endpoint viejo activo por las dudas, no molesta" | El código sin dueño ni fecha de baja es deuda técnica silenciosa; si se deprecó, tiene fecha. |

## Red flags

- Commits gigantes con mensaje "fix" o "changes" sin contexto.
- Un pipeline verde que en realidad tiene un gate deshabilitado "temporalmente".
- Feature en producción sin monitoreo activo desde el minuto uno.
- Deprecación sin fecha ni comunicación a quien consume lo deprecado.

## Verificación antes de cerrar

- [ ] Historia de commits atómica y legible, sin "WIP" ni squashes que pierdan contexto útil.
- [ ] El pipeline de CI/CD corre los mismos gates que se validaron manualmente.
- [ ] `checklist-<version>.md` completo, con plan de rollback explícito y monitoreo confirmado activo.
- [ ] Si hubo deprecación, tiene fecha, comunicación y verificación de que no queda código zombie.

Con esto se cierra el ciclo completo de la HU/TT — el `orquestador` decide si
corresponde volver a `archi` (si el despliegue reveló algo que cambia el
AS-IS) o si la iniciativa continúa con la siguiente HU del backlog de `desglosador`.
