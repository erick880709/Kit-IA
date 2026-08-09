---
name: revision-calidad
description: 'Revisa un cambio de código antes de mergear usando el review de cinco ejes (corrección, diseño, mantenibilidad, consistencia con el estilo del proyecto, testing) y detecta complejidad innecesaria para simplificar sin cambiar el comportamiento. Úsala SIEMPRE que el usuario pida "revisar este PR", "hacer code review", "¿este código está listo para mergear?", "simplificar este módulo", o cuando `tdd-implementacion` termine todos los slices de una HU/TT y haga falta el gate de calidad antes de `entrega-continua`. Adaptación al español y al contrato de `resources/` de las skills `code-review-and-quality` y `code-simplification` de addyosmani/agent-skills.'
---

# Revisión de Calidad (Review + Simplificación)

## Resumen

Envuelve `code-review-and-quality` y `code-simplification` del pack `agent-skills`
en un único gate, pensado para correr después de `tdd-implementacion` y antes de
`entrega-continua`. Referencia completa (inglés, solo lectura):
`.github/skills-addy/skills/code-review-and-quality/SKILL.md` y
`.github/skills-addy/skills/code-simplification/SKILL.md`.

## Entrada esperada

- El diff o PR a revisar (rama, commit range, o archivos modificados).
- `resources/engineering/tests/coverage-<modulo>.md` de `tdd-implementacion`
  (para confirmar que la evidencia de tests existe antes de revisar el diseño).
- `resources/architecture/overview.md` como vara de consistencia arquitectónica.

## Salida

- `resources/engineering/reviews/review-<PR-o-slice>.md` con los hallazgos
  clasificados por severidad y eje.

## Los cinco ejes

1. **Corrección** — ¿el código hace lo que el criterio de aceptación de la
   HU/TT pide? Contrastá contra `resources/functional/hu/HU-<n>.md`.
2. **Diseño** — ¿las abstracciones ganan su complejidad? ¿Encaja con el patrón
   arquitectónico ya decidido por `archi`/`builder`?
3. **Mantenibilidad** — nombres, tamaño de funciones, acoplamiento.
4. **Consistencia** — con las convenciones de código que `builder` documentó
   en `resources/architecture/overview.md` (sección "Convenciones de código").
5. **Testing** — ¿la evidencia en `coverage-<modulo>.md` corresponde a este
   cambio, no a uno anterior?

## Tamaño de cambio y velocidad de revisión

Cambios de ~100 líneas se revisan a fondo en una sola pasada. Si el diff supera
eso, primero sugerí cómo partirlo (por capa, por criterio de aceptación, por
slice de `tdd-implementacion`) antes de revisar en detalle — un diff gigante
oculta más de lo que muestra.

## Etiquetas de severidad

- **Bloqueante** — no se mergea así (bug, hueco de seguridad, rompe contrato de API).
- **Debe corregirse** — antes de considerar la HU/TT cerrada.
- **Nit** — estilo/preferencia, no bloquea.
- **FYI** — informativo, sin acción requerida.

## Simplificación (Chesterton's Fence)

Antes de proponer eliminar o simplificar algo que parece innecesariamente
complejo, entendé primero por qué está ahí — revisá el commit/PR que lo
introdujo o preguntá, no lo borres a ciegas asumiendo que es cruft. Una vez
entendido, simplificá preservando exactamente el comportamiento observable
(mismos tests en verde antes y después). "Regla de las 500 líneas": si un
archivo/función supera eso sin una razón clara, es candidato fuerte a dividir.

## Rationalizaciones comunes

| Excusa | Realidad |
|---|---|
| "El PR es grande pero está todo relacionado" | Relacionado no es lo mismo que revisable de una sola pasada; pedí partirlo. |
| "Esto es solo un nit, no hace falta anotarlo" | Anotalo igual con severidad Nit — la trazabilidad importa más que el ahorro de una línea. |
| "No entiendo por qué está esta validación rara, la saco" | Chesterton's Fence: investigá el porqué antes de tocarlo. |
| "Los tests pasan, entonces el diseño está bien" | Tests en verde prueban corrección, no diseño ni mantenibilidad — son ejes distintos. |

## Red flags

- Un review que solo comenta estilo y no toca corrección ni diseño.
- Hallazgos "Bloqueante" que se resuelven cambiando la severidad en vez de el código.
- Simplificación que cambia comportamiento observable (aunque sea "mejora").

## Verificación antes de aprobar

- [ ] Los cinco ejes fueron evaluados explícitamente, no solo el que salta a la vista.
- [ ] Todo hallazgo Bloqueante o Debe-corregirse tiene una acción concreta, no solo la observación.
- [ ] Si hubo simplificación, los mismos tests siguen en verde después del cambio.
- [ ] `review-<PR>.md` queda guardado en `resources/engineering/reviews/`.

Con el review aprobado, el siguiente paso es `seguridad-rendimiento` (si el
cambio toca input de usuario, auth o rutas calientes) y luego `entrega-continua`.
