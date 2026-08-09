---
name: tdd-implementacion
description: 'Toma el scaffold generado por `builder` (o cualquier código existente) y lo lleva a lógica de negocio real, en slices verticales pequeños y con Red-Green-Refactor obligatorio. Úsala SIEMPRE que el usuario pida "implementar la lógica de", "completar el módulo que generó builder", "escribir el código de la HU-XX", "hacer TDD de", o en general cualquier tarea de programación que toque más de un archivo. NO la uses para el scaffold inicial (eso es `builder`), para diseño de arquitectura (`archi`) ni para pruebas E2E de UI grabadas en navegador (`qa`) — esta skill es para pruebas unitarias/integración y para el código de producción que las hace pasar. Adaptación al español y al contrato de `resources/` de las skills `incremental-implementation` y `test-driven-development` de addyosmani/agent-skills.'
---

# TDD + Implementación Incremental

## Resumen

Envuelve dos skills del pack `agent-skills` de Addy Osmani —
`incremental-implementation` y `test-driven-development` — en un único flujo,
adaptado para consumir la salida de `builder` y producir evidencia dentro de
`resources/engineering/`. Referencia completa (en inglés, sin traducir porque
es material de proceso de solo lectura): `.github/skills-addy/skills/incremental-implementation/SKILL.md`
y `.github/skills-addy/skills/test-driven-development/SKILL.md`.

## Entrada esperada

Uno de estos, en orden de preferencia:

1. `resources/functional/hu/HU-<n>.md` o `TT-<n>.md` (de `desglosador` o `janus`) — la
   historia/tarea que define el criterio de aceptación a implementar.
2. El scaffold ya generado por `builder` en el módulo correspondiente
   (`resources/architecture/overview.md` y `resources/architecture/stack.md`
   documentan convenciones y patrón arquitectónico a respetar).
3. Si no existe ninguno de los dos, pregunta antes de escribir código: no hay
   slice válido sin un criterio de aceptación verificable.

## Salida

- Código de producción + pruebas, en el árbol real del proyecto (no en `resources/`).
- `resources/engineering/plans/plan-<slice>.md`: el plan de slices verticales
  (uno por criterio de aceptación), con el estado de cada uno.
- `resources/engineering/tests/coverage-<modulo>.md`: evidencia de la corrida
  (comando ejecutado, resultado, cobertura si aplica) para cada slice, no un
  resumen narrado — pegá la salida real del test runner.

## Flujo de trabajo

### 1. Planificar en slices verticales, no en capas

Un slice = un cambio end-to-end pequeño y verificable (típicamente <100 líneas
de diff), no "toda la capa de repositorio primero, después todo el servicio".
Cada slice debe:
- Tocar todas las capas necesarias para que el criterio de aceptación sea
  observable (ruta HTTP + servicio + repositorio + test), aunque sea de forma
  mínima.
- Poder mergearse solo, detrás de un feature flag si el resto de la feature
  no está listo.
- Quedar registrado como una fila en `plan-<slice>.md` antes de tocar código.

### 2. Rojo → Verde → Refactor, sin saltarse el rojo

1. Escribí el test que describe el comportamiento esperado del slice.
   **Corré el test y confirmá que falla** (y que falla por la razón correcta,
   no por un error de sintaxis). Pegá la salida en `coverage-<modulo>.md`.
2. Escribí el código mínimo para que pase. No adelantes funcionalidad de
   slices futuros.
3. Refactorizá manteniendo el test en verde. Corré la suite completa del
   módulo, no solo el test nuevo, antes de dar el slice por terminado.

Pirámide de pruebas objetivo (heredada de `test-driven-development`): ~80%
unitarias, ~15% de integración, ~5% E2E. Las E2E de UI en navegador quedan a
cargo de `qa`, no de este skill — acá solo se cubre unitario/integración.

### 3. Respetar la arquitectura que ya existe

Antes de escribir, releé `resources/architecture/overview.md` y
`resources/architecture/stack.md` (los deja `builder`/`genesis`). El patrón
arquitectónico, las convenciones de nombres y el módulo de referencia ya están
decididos — no los reinventes dentro de este skill. Si el patrón no alcanza
para el slice actual, para y señalalo explícitamente en vez de improvisar una
capa nueva sin documentarla.

### 4. Contexto y fuentes antes de codear librerías nuevas

Si el slice usa una librería/framework con el que no hay certeza de la API
correcta, consultá primero `.github/skills-addy/skills/source-driven-development/SKILL.md`
(verificación contra documentación oficial, cita la fuente) antes de escribir
código a partir de memoria.

## Rationalizaciones comunes (y por qué no aplican)

| Excusa | Realidad |
|---|---|
| "El scaffold de `builder` ya tiene la estructura, puedo llenarla toda de una" | Un slice grande sin test intermedio no da evidencia de qué parte falla; volvé a partirlo. |
| "Este cambio es tan simple que no necesita test primero" | Si es tan simple, escribir el test toma menos de dos minutos; si toma más, es la señal de que no era tan simple. |
| "Ya probé manualmente en el navegador, funciona" | Una prueba manual no es evidencia reproducible ni queda en `coverage-<modulo>.md`; corré el test automatizado. |
| "Voy a refactorizar y agregar tests después" | El refactor sin red de tests es exactamente el escenario que TDD existe para evitar. |

## Red flags

- Un slice que toca más de ~5 archivos sin una razón arquitectónica explícita.
- Tests que se agregan después de que el código ya "funciona a ojo".
- `coverage-<modulo>.md` con narración ("los tests pasan") en vez de output real.
- Cambios fuera del alcance de la HU/TT actual (ver regla de disciplina de
  alcance del `orquestador`).

## Verificación antes de cerrar el slice

- [ ] El test falló primero (rojo confirmado) y después pasó (verde confirmado).
- [ ] La suite completa del módulo corre en verde, no solo el test nuevo.
- [ ] `plan-<slice>.md` y `coverage-<modulo>.md` están actualizados con evidencia real.
- [ ] El slice respeta el patrón arquitectónico de `resources/architecture/overview.md`.
- [ ] No se tocó código fuera del alcance de la HU/TT (o se documentó por qué sí).

Al cerrar todos los slices de una HU/TT, el siguiente paso natural es
`revision-calidad` (review de 5 ejes) antes de `entrega-continua`.
