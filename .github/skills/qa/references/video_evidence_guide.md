# Guía de Evidencia en Video (Playwright)

Cómo grabar, conservar, organizar y reportar los videos de ejecución de
pruebas para que cada caso del runbook tenga evidencia trazable y revisable.

---

## Índice

- [Política de Grabación](#politica-de-grabacion)
- [Configuración de Playwright](#configuracion-de-playwright)
- [Legibilidad del Video (por qué se ve acelerado)](#legibilidad-del-video-por-que-se-ve-acelerado)
- [Estructura de Carpetas](#estructura-de-carpetas)
- [Convención de Id de Caso](#convencion-de-id-de-caso)
- [Organizar la Evidencia Después de una Ejecución](#organizar-la-evidencia-despues-de-una-ejecucion)
- [Subida de Artefactos en CI](#subida-de-artefactos-en-ci)
- [Almacenamiento y Retención](#almacenamiento-y-retencion)
- [Solución de Problemas](#solucion-de-problemas)

---

## Política de Grabación

Por defecto en este proyecto: **grabar cada prueba, en cada ejecución, y
conservar cada video** — no solo los que fallan. Esto da evidencia de
auditoría completa por ejecución, a costa del uso de disco. Se aplica así:

| Prioridad | Video | Trace | Screenshot |
|---|---|---|---|
| Critical / High | Siempre activado, siempre conservado | Siempre activado | Siempre activado |
| Medium / Low | Siempre activado, siempre conservado | Siempre activado | Siempre activado |

Si el almacenamiento se vuelve una restricción real más adelante, la
primera palanca a mover es `video: 'retain-on-failure'` en
`playwright.config.ts` (sin borrar los videos de casos críticos) —
comunicá esto explícitamente al usuario antes de cambiar el valor por
defecto, ya que cambia lo que los auditores pueden ver después de los hechos.

## Configuración de Playwright

Usá `../scripts/playwright.config.template.ts` como base. Bloque relevante:

```typescript
use: {
  video: { mode: 'on', size: { width: 1280, height: 720 } },
  trace: 'on',
  screenshot: 'on',
},
```

Notas:
- `video` es una opción a **nivel de contexto**: solo aplica a los
  contextos de navegador creados después de que la config/fixture la
  establece. No intentes alternarla a mitad de una prueba.
- Un `size` fijo mantiene los videos chicos y consistentes; sin eso,
  Playwright escala al viewport, lo que puede producir tamaños de archivo
  inconsistentes entre specs.
- Grabar en modo headless está totalmente soportado y es el default en CI;
  no hace falta `headless: false` para obtener video.

## Legibilidad del Video (por qué se ve acelerado)

Playwright graba el video en tiempo real de ejecución: si el test hace clic,
tipea y navega sin ninguna pausa deliberada, el video muestra esas acciones
a la velocidad real (muy rápida) a la que corre el navegador, sin transición
visible entre pasos. El resultado es un video técnicamente correcto pero
inútil para que una persona entienda qué se probó. Dos ajustes lo resuelven
juntos:

**1. `slowMo` — pausa entre acciones.** `../scripts/playwright.config.template.ts`
ya lo trae configurado vía la variable de entorno `QA_SLOWMO_MS`:

```typescript
const SLOWMO_MS = Number(process.env.QA_SLOWMO_MS ?? 300);

export default defineConfig({
  use: {
    launchOptions: {
      slowMo: SLOWMO_MS,
    },
  },
});
```

`slowMo` agrega una demora fija (en ms) antes de cada acción de Playwright,
tanto en modo headed como headless — no afecta las aserciones ni introduce
no-determinismo, solo espacia las acciones en el tiempo para que el video
se pueda seguir. Guía de valores (variable `QA_SLOWMO_MS` en `.env.qa`):

| Valor | Cuándo usarlo |
|---|---|
| `0` | Gate de CI puramente funcional, donde nadie va a mirar el video, y la velocidad de la suite importa más que la legibilidad. |
| `250`-`400` (default `300`) | Evidencia de ejecución estándar: legible para un humano sin alargar demasiado la suite. |
| `600`+ | Video pensado para demo/presentación a stakeholders, no para un gate de CI. |

Si subís mucho `QA_SLOWMO_MS`, un test con muchos pasos puede superar el
timeout por defecto de Playwright; la plantilla ya escala el `timeout`
global en función de `SLOWMO_MS` para cubrir ese caso.

**2. `test.step()` — puntos de referencia nombrados.** `slowMo` hace que el
video se pueda seguir, pero no le dice a quien lo mira *qué* está pasando
en cada momento. Envolver los pasos lógicos del test en `test.step()` los
etiqueta en el reporte HTML y en el trace viewer de Playwright, así se
puede saltar directo a "llenar formulario de pago" en vez de scrubear todo
el video a ciegas:

```typescript
test('TC-01 [critical] - Login con credenciales válidas', async ({ page }) => {
  await test.step('Abrir la página de login', async () => {
    await page.goto('/login');
  });

  await test.step('Completar credenciales', async () => {
    await page.getByLabel('Email').fill(process.env.QA_USER_EMAIL!);
    await page.getByLabel('Password').fill(process.env.QA_USER_PASSWORD!);
  });

  await test.step('Enviar y verificar redirección', async () => {
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page).toHaveURL('/dashboard');
  });
});
```

Regla práctica: si un caso tiene más de 3-4 acciones de UI, dividilo en
`test.step()` con nombres que describan la intención (no la acción cruda:
"Completar credenciales", no "fill inputs").

## Estructura de Carpetas

Todo vive bajo `resources/qa/` en la raíz del proyecto (ver
`../SKILL.md#estructura-de-entregables-carpeta-de-salida`). Si alguna de
estas carpetas no existe, creala antes de escribir el primer archivo ahí.

Cada vez que se ejecuta un caso o un set de pruebas, `organize-evidence.mjs`
crea (o reutiliza) **una carpeta con el nombre del caso directamente dentro
de `resources/qa/`**, con una subcarpeta por `runId` adentro para no perder
la evidencia de ejecuciones anteriores del mismo caso:

```
resources/qa/
├── test-results/<runId>/            # Salida cruda de Playwright (carpetas por prueba + results.json)
├── playwright-report/<runId>/       # Reporte HTML de Playwright
├── TC-01/
│   ├── <runId-1>/
│   │   ├── video.webm
│   │   ├── trace.zip
│   │   └── screenshot-0.png
│   └── <runId-2>/
│       └── ...                      # ejecución posterior del mismo caso, no pisa la anterior
├── TC-02/
│   └── <runId-1>/
│       ├── video.webm
│       └── screenshot-0.png
└── reports/
    ├── <runId>-manifest.json        # id de caso -> estado, prioridad, rutas de artefactos
    └── <runId>-execution-report.md
```

`<runId>` debe ser un identificador compartido entre `test-results`, las
subcarpetas de cada caso, y el nombre del manifest/reporte para una sola
ejecución (timestamp, ej. `2026-07-08T14-30-00Z`, o un número de build de
CI). `organize-evidence.mjs` lo infiere automáticamente del nombre de la
carpeta que contiene `results.json`. Nunca reutilices un `runId` entre
ejecuciones distintas del mismo caso — sobrescribe silenciosamente la
evidencia anterior.

## Convención de Id de Caso

Todo título de spec automatizado debe empezar con el id de caso del
runbook, opcionalmente seguido de una etiqueta de prioridad entre corchetes:

```typescript
test('TC-01 [critical] - Login con credenciales válidas', async ({ page }) => {
  // ...
});
```

Esto es lo que permite que `scripts/organize-evidence.mjs` y
`scripts/generate-execution-report.mjs` mapeen un video de vuelta al caso
exacto del runbook sin ningún trabajo manual. Las pruebas sin un id
`TC-xxx` en el título igual obtienen evidencia, pero agrupada por un título
slugificado en su lugar — tratá eso como un hueco a corregir, no como un
resultado normal.

## Organizar la Evidencia Después de una Ejecución

```bash
npx playwright test
node scripts/organize-evidence.mjs \
  --results resources/qa/test-results/<runId>/results.json \
  --out resources/qa
node scripts/generate-execution-report.mjs \
  --manifest resources/qa/reports/<runId>-manifest.json \
  --out resources/qa/reports/<runId>-execution-report.md
```

Después, adjuntá `resources/qa/reports/<runId>-execution-report.md` y las
rutas de `resources/qa/<CASE-ID>/<runId>/video.webm` relevantes al resumen
final de QA que le entregás al usuario.

## Subida de Artefactos en CI

```yaml
- run: npx playwright test
- run: node scripts/organize-evidence.mjs --results resources/qa/test-results/${{ github.run_id }}/results.json --out resources/qa
  if: always()
- run: node scripts/generate-execution-report.mjs --manifest resources/qa/reports/${{ github.run_id }}-manifest.json --out resources/qa/reports/${{ github.run_id }}-execution-report.md --fail-on-no-go
  if: always()
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: qa-evidence-${{ github.run_id }}
    path: |
      resources/qa/*/${{ github.run_id }}
      resources/qa/reports/${{ github.run_id }}-manifest.json
      resources/qa/reports/${{ github.run_id }}-execution-report.md
    retention-days: 30
```

El patrón `resources/qa/*/${{ github.run_id }}` toma la subcarpeta de esa
ejecución dentro de cada carpeta de caso, sin tener que enumerar cada
`TC-xxx` a mano.

Usá `if: always()` en los tres pasos (organizar evidencia, generar reporte y
subir artefacto) — no `if: failure()` — ya que la política acá es conservar
la evidencia también de los casos que pasan, y generar/subir el reporte
incluso cuando `playwright test` falló. `--fail-on-no-go` en
`generate-execution-report.mjs` es lo que efectivamente bloquea el pipeline
si el veredicto agregado es `NO-GO`, después de haber escrito igual el
reporte — ver `../references/testing_strategies.md#estrategias-de-integración-con-cicd`
para el job completo.

## Almacenamiento y Retención

- El `.webm` de Playwright ya viene comprimido; evitá re-codificarlo salvo
  que algún stakeholder necesite `.mp4` para una herramienta que no pueda
  reproducir `.webm` — si es así, convertí bajo demanda
  (`ffmpeg -i video.webm video.mp4`), no lo hagas por defecto en cada ejecución.
- Ignorá en git toda `resources/qa/` salvo `resources/qa/plans/` y
  `resources/qa/runbooks/`, que sí conviene versionar (son documentos, no
  evidencia binaria):
  ```gitignore
  resources/qa/*
  !resources/qa/plans/
  !resources/qa/runbooks/
  ```
  La evidencia (carpetas por caso, `test-results/`, `playwright-report/`,
  `reports/`) va en almacenamiento de artefactos de CI o un object store,
  no en el repositorio de git.
- Establecé una ventana de retención explícita (ej. `retention-days: 30` en
  CI, o una regla de ciclo de vida si se sube a S3/GCS) — "conservar todo
  para siempre" sin una política de retención crece sin límite.

## Solución de Problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| No se produce ningún archivo de video | `video` no está configurado, o el contexto se creó antes de aplicar la config | Confirmar `use.video` en la config que gobierna el proyecto en ejecución; verificar que los contextos creados por fixtures también la hereden |
| El video corre tan rápido que no se distingue qué se probó | Falta `slowMo` entre acciones, o el caso no está dividido en pasos | Subir `QA_SLOWMO_MS` (default 300) y envolver los pasos del test en `test.step()` — ver [Legibilidad del Video](#legibilidad-del-video-por-que-se-ve-acelerado) |
| El video existe pero dura 0 segundos / está corrupto | La prueba crasheó antes de cerrar el contexto | Playwright finaliza el video al cerrar el contexto; asegurate de que el teardown no esté matando el proceso (`process.exit`) a mitad de la prueba |
| El video pesa demasiado en toda la suite | Viewport grande, specs largos, o `video: 'on'` en specs de bajo valor y alto volumen | Fijar `size` en la config; considerar `retain-on-failure` solo para specs de baja prioridad, con el visto bueno del usuario |
| `organize-evidence.mjs` agrupa por slug en vez de por id de caso | Al título de la prueba le falta el prefijo `TC-xxx` | Renombrar el título de la prueba para que empiece con el id de caso |
| Un caso aparece con carpeta `__DUP2`/`__DUP3` | El mismo id `TC-xxx` se usó en dos títulos de prueba distintos | Corregir el id duplicado en el runbook o en el título del spec; mientras tanto la evidencia de ambos queda separada, no pisada |
| El reporte muestra `NO-GO` inesperadamente | Falló un caso etiquetado `[critical]` | Revisar primero `resources/qa/<CASE-ID>/<runId>/video.webm` y `trace.zip` de ese caso |
| El pipeline de CI sigue en verde aunque el veredicto sea `NO-GO` | Falta `--fail-on-no-go` (o `--fail-on-risk`) en el paso de `generate-execution-report.mjs` | Agregar el flag — ver [Subida de Artefactos en CI](#subida-de-artefactos-en-ci) |
| La evidencia de una ejecución anterior desapareció | Se reutilizó el mismo `runId` para dos ejecuciones distintas | Nunca fijes `QA_RUN_ID` manualmente a un valor ya usado; dejá que se autogenere por timestamp |
| No queda claro si un caso es flaky o falló una sola vez | No hay ninguna herramienta cruzando corridas históricas | Correr `node scripts/flaky-trend.mjs --reports resources/qa/reports --out resources/qa/reports/flaky-trend.md` |
