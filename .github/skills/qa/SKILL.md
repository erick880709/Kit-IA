---
name: qa
description: 'Manual de ingeniería de calidad (QA). Cubre pruebas E2E con Playwright (React, Next.js, Angular, Vue), pruebas unitarias/integración con Jest/Vitest/RTL, grabación de evidencia en video, runbooks de prueba en Markdown, y estrategia de testing basada en riesgo. Usar cuando se pida "pruebas E2E", "grabar evidencia de testing", "runbook de QA", "plan de pruebas", "testing strategy", "aumentar cobertura", "diseñar quality gates de CI", o "estabilizar pruebas". Framework-agnóstico: aplica a cualquier stack frontend y backend.'
---

# QA — Ingeniero de QA Senior

Manual para diseñar, implementar, ejecutar y reportar la calidad de las
pruebas en proyectos React y Next.js, usando las referencias y scripts
incluidos en este skill.

## Cuándo Usar Este Skill

- El usuario pide crear un plan de pruebas (alcance, escenarios, datos, riesgos, criterios de entrada/salida).
- El usuario pide ejecutar pruebas a partir de un archivo Markdown que describe pasos y resultados esperados.
- El usuario pide ejecutar un plan de pruebas y producir evidencia (pass/fail, traces, screenshots, video).
- El usuario pide grabar pruebas a partir de interacciones reales en el navegador, o capturar/organizar evidencia en video de las ejecuciones.
- El usuario pide generar o mejorar pruebas unitarias, de integración o E2E.
- El usuario pide definir una estrategia de testing (pirámide, objetivos de cobertura, gates de CI).
- El usuario pide reducir pruebas inestables (flaky) o depurar suites inestables.
- El usuario pide buenas prácticas de Playwright, Jest, React Testing Library o MSW.
- El usuario pide mejorar métricas de calidad de pruebas y confianza para el release.

## Prerrequisitos

- Node.js disponible en el proyecto (el gestor de paquetes real —
  npm/yarn/pnpm/bun— se detecta en el Paso 0, no hace falta asumirlo).
- **No hace falta tener Jest/RTL/Playwright/MSW preinstalados de antemano.**
  Si el Paso 0 detecta que falta alguno de estos según lo que el plan/runbook
  requiera, el Paso 0.1 los instala automáticamente (`node
  scripts/ensure-qa-dependencies.mjs`) junto con los navegadores de
  Playwright — nunca le pidas al usuario que los instale a mano.
- Runbook de pruebas en Markdown disponible cuando la ejecución está dirigida por un documento (por ejemplo: `test-plan.md` o `qa-runbook.md`).
- Un archivo `.env.qa` (ignorado por git) con valores reales, creado a partir de
  `./references/env.example`. **Nunca escribas credenciales reales en un plan
  de pruebas, un runbook, un archivo de spec, ni en ningún lugar dentro de la
  carpeta `references/` de este skill** — siempre referenciá variables de
  entorno tipo `${QA_USER_EMAIL}` en su lugar.
- Si un caso necesita un usuario autenticado y `QA_USER_EMAIL`/`QA_USER_PASSWORD`
  (o `QA_ADMIN_*`) no están definidos en `.env.qa`, **no le pidas la
  contraseña al usuario ni inventes una credencial ad-hoc en el spec**:
  corré `node scripts/ensure-test-user.mjs --role user` (o `--role admin`).
  Genera credenciales seguras nuevas, las crea vía `QA_SEED_API_URL` si está
  configurado, o te da instrucciones para crearlas por el signup real de la
  app, y las persiste en `.env.qa`. Ver `./references/env.example`.
- Este skill incluye documentación de referencia más scripts para copiar y
  adaptar (`./scripts/`): una plantilla de configuración de Playwright, un
  organizador de evidencia y un generador de reporte de ejecución. Son
  plantillas para copiar al proyecto destino, no scripts pensados para
  correr desde dentro de la carpeta del skill.
- Todo entregable (planes, runbooks, evidencia, reportes) se guarda bajo
  `resources/qa/` en el proyecto destino — ver "Estructura de Entregables" más abajo.

## Estructura de Entregables (Carpeta de Salida)

Todo entregable que produzca este skill dentro de un proyecto — planes de
prueba, runbooks, evidencia de ejecución (video/trace/screenshot) y
reportes — se crea siempre bajo `resources/qa/` en la raíz del proyecto,
nunca suelto en otro lado. Si la ruta o alguna subcarpeta no existe,
creala primero (`mkdir -p` o el `fs.mkdirSync(..., { recursive: true })`
equivalente) y recién después escribí el archivo ahí.

**Cada vez que se ejecuta un caso o un set de pruebas, la evidencia se
organiza en una carpeta por caso directamente dentro de `resources/qa/`**
(`resources/qa/<CASE-ID>/`), con una subcarpeta por `runId` adentro para no
perder la evidencia de ejecuciones anteriores del mismo caso:

```
resources/qa/
├── plans/
│   └── test-plan-<feature>.md              # ./references/test_plan_template.md
├── runbooks/
│   └── qa-runbook-<feature>.md             # ./references/markdown_test_runbook.md
├── TC-01/                                  # una carpeta por caso, creada al ejecutar
│   ├── <runId-1>/video.webm, trace.zip, screenshot-*.png
│   └── <runId-2>/video.webm, trace.zip, screenshot-*.png
├── TC-02/
│   └── <runId-1>/video.webm, trace.zip, screenshot-*.png
├── test-results/<runId>/                   # salida cruda de Playwright (incl. results.json)
├── playwright-report/<runId>/              # reporte HTML de Playwright
└── reports/
    ├── <runId>-manifest.json               # id de caso -> estado, prioridad, rutas de artefactos
    └── <runId>-execution-report.md
```

Esto aplica tanto a lo que escribís vos directamente (plan de pruebas,
runbook) como a lo que producen los scripts (`scripts/organize-evidence.mjs`,
`scripts/generate-execution-report.mjs`, `playwright.config.ts`). Los
scripts y la plantilla de configuración ya vienen apuntando a esta
estructura por defecto — no los redirijas a otra carpeta salvo pedido
explícito del usuario. Los specs automatizados (`e2e/`, `tests/`) NO van
acá: siguen viviendo en el código fuente del proyecto, como cualquier otro
archivo de test.

## Flujo de Trabajo Principal

### 0. Reconocer el Proyecto Antes de Actuar

Nunca apliques los patrones de este skill a ciegas. Antes de escribir un
plan, un runbook o un test, invertí unos minutos en entender el proyecto
real:

1. Leer instrucciones del propio proyecto si existen (`CLAUDE.md`,
   `AGENTS.md`, `README.md`, `CONTRIBUTING.md`) — comandos de build/test,
   convenciones de naming, restricciones explícitas del equipo.
2. Leer `package.json`: framework y versión (`react`, `next`, u otro),
   gestor de paquetes real a partir del lockfile (`package-lock.json` →
   npm, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `bun.lockb` → bun), y
   qué test runner ya está instalado (`jest`, `vitest`, etc.) y qué scripts
   de `"scripts"` ya existen para correrlos — usá esos, no asumas `npm test`.
3. Si ya existe `playwright.config.ts` o `jest.config.*` en el proyecto,
   **no lo sobrescribas con la plantilla completa de este skill**. Leelo
   primero y fusioná solo lo necesario (video/trace/screenshot, `outputDir`
   bajo `resources/qa/`) preservando el resto de su configuración.
4. Si el frontend no es React/Next.js (Vue, Angular, Svelte, etc.), avisale
   al usuario que este skill está afinado para React/Next.js — los patrones
   de selectors, RTL y Page Object Model pueden no aplicar 1:1 — y confirmá
   antes de aplicarlos igual.
5. En proyectos Next.js, identificar si usan App Router (`app/`) o Pages
   Router (`pages/`), porque cambia las rutas de test, el patrón de layouts
   y cómo se mockea el router en pruebas unitarias/integración.

Esto evita el error más común de aplicar este manual como una plantilla
rígida: pisar configuración existente, imponer un test runner que el
proyecto no usa, o generar specs con convenciones que no encajan con las
del repo.

### 0.1 Instalar Dependencias y Herramientas Faltantes

No le pidas al usuario que instale nada a mano. Con el gestor de paquetes
detectado en el Paso 0, corré:

```bash
node scripts/ensure-qa-dependencies.mjs [--with-unit] [--with-msw] [--with-a11y]
```

1. Por defecto garantiza `@playwright/test` y descarga sus navegadores
   (`npx playwright install --with-deps chromium`) — lo mínimo para E2E.
2. Sumá `--with-unit` si el plan requiere pruebas unitarias/integración
   (instala Jest + React Testing Library), `--with-msw` si hay que mockear
   APIs, y `--with-a11y` si el plan incluye pruebas de accesibilidad.
3. El script solo agrega lo que falte como devDependency del proyecto — no
   toca dependencias de producción, no instala nada global (`-g`), y no
   actualiza ni reemplaza una versión ya instalada sin que el usuario lo
   pida explícitamente.
4. Contale al usuario qué se instaló (paquetes + comando usado) — instalar
   en silencio sin dejar rastro no es aceptable, aunque sea automático.
5. Si la instalación falla (sin red, registry privado, permisos), no
   reintentes en loop: mostrale al usuario el error exacto y pedile que
   resuelva el acceso a la registry antes de continuar.
6. En CI con una imagen que ya trae los navegadores de Playwright
   preinstalados (ej. `mcr.microsoft.com/playwright`), usar `--skip-browsers`
   para no perder tiempo reinstalándolos en cada corrida.

Repetir este paso cada vez que el plan/runbook agregue un tipo de prueba
nuevo (por ejemplo, se pasa de solo E2E a sumar pruebas de accesibilidad).

### 1. Definir Primero la Estrategia de Pruebas

1. Clasificar flujos críticos y áreas de riesgo.
2. Aplicar una distribución equilibrada de la pirámide:
   - Unitarias: 50-60%
   - Integración: 25-35%
   - E2E: 10-15%
3. Definir umbrales de cobertura por riesgo, no por métricas vanidosas.
4. Definir quality gates de CI y criterios de fallo.

Referencia: `./references/testing_strategies.md`

### 2. Crear el Plan de Pruebas

1. Definir alcance dentro y fuera (features, páginas, flujos críticos).
2. Definir tipos y prioridades de prueba (smoke, regresión, exploratoria).
3. Definir escenarios con precondiciones, pasos, resultados esperados y etiquetas de riesgo.
4. Definir estrategia de datos (usuarios de prueba por rol, fixtures,
   entornos, estrategia de reseteo) — las credenciales siempre vía
   variables de entorno, nunca en texto plano.
5. Definir criterios de entrada y salida (cobertura, tasa de aprobación, política de bloqueantes).
6. Definir requisitos de evidencia (screenshots, trace, video, logs) — ver
   `./references/video_evidence_guide.md` para la política por defecto de
   "grabar y conservar todo".
7. Producir el plan como un archivo Markdown real en
   `resources/qa/plans/test-plan-<feature>.md` (creando la carpeta si no
   existe) usando `./references/test_plan_template.md`, no solo como un
   resumen en el chat.

Referencia: `./references/testing_strategies.md`, `./references/test_plan_template.md`

### 3. Implementar Pruebas con Patrones Reutilizables

1. Preferir nombres de prueba orientados a comportamiento (`should ... when ...`).
2. Usar la estructura Arrange-Act-Assert.
3. Usar selectores resilientes (role/label/text primero).
4. Encapsular flujos repetidos con:
   - Page Object Model para E2E.
   - Objetos de componente/prueba para pruebas de UI.
   - Factories de datos de prueba y fixtures.
5. Mockear dependencias externas con MSW y resetear handlers en cada prueba.
6. Para specs E2E ligados a un caso del runbook, prefijar el título de la
   prueba con el id del caso (y opcionalmente una etiqueta de prioridad
   entre corchetes), ej.
   `test('TC-01 [critical] - Login con credenciales válidas', ...)` — esto
   es obligatorio para que la organización automática de evidencia (paso 5) funcione.

Referencia: `./references/test_automation_patterns.md`

### 4. Configurar Ejecución y Captura de Video

1. Si el proyecto ya tiene `playwright.config.ts` (ver Paso 0), fusionar en
   él solo lo necesario (`video`, `trace`, `screenshot`, `launchOptions.slowMo`,
   `outputDir`/reporters bajo `resources/qa/`) en vez de reemplazarlo. Si no
   existe, copiar `./scripts/playwright.config.template.ts` como
   `playwright.config.ts` y ajustar `testDir`/`baseURL`.
2. Copiar `./references/env.example` al proyecto como `.env.qa`, completar
   los valores reales ahí, y confirmar que `.env.qa` está en `.gitignore`.
3. Si algún caso requiere un usuario autenticado y las credenciales no
   están en `.env.qa`, correr `node scripts/ensure-test-user.mjs --role user`
   (o `--role admin`) antes de ejecutar — genera y provisiona la cuenta en
   vez de bloquearse pidiéndole la contraseña al usuario.
4. Mantener la política de evidencia por defecto — video, trace y screenshot
   capturados en cada caso, en cada ejecución — a menos que el usuario pida
   explícitamente reducirla (ej. `retain-on-failure` para CI con
   restricciones de espacio).
5. Dejar `QA_SLOWMO_MS` activo (default 300) y dividir cada spec en
   `test.step()` nombrados, para que el video resultante sea legible por una
   persona y no una ráfaga de clics indistinguibles.
6. Confirmar que el título de cada spec automatizado lleva el id del caso
   para que la evidencia se mapee automáticamente contra el runbook.

Referencia: `./references/video_evidence_guide.md`, `./references/test_automation_patterns.md`

### 5. Ejecutar, Organizar Evidencia y Reportar

1. Ejecutar primero las pruebas smoke, luego la suite de regresión/completa,
   en orden de prioridad (crítico/alto antes que medio/bajo).
2. Ejecutar con artefactos habilitados según el paso 4 (trace/video/screenshot).
3. Después de la ejecución, organizar la salida cruda de Playwright en una
   carpeta por caso y generar el reporte de ejecución, todo dentro de
   `resources/qa/` (los scripts crean las carpetas que falten):
   ```bash
   node scripts/organize-evidence.mjs --results resources/qa/test-results/<runId>/results.json --out resources/qa
   node scripts/generate-execution-report.mjs --manifest resources/qa/reports/<runId>-manifest.json --out resources/qa/reports/<runId>-execution-report.md
   ```
   Esto crea (o reutiliza) `resources/qa/<CASE-ID>/<runId>/` para cada caso
   ejecutado, sin pisar la evidencia de ejecuciones anteriores de ese mismo caso.
4. Documentar los fallos con pasos reproducibles, severidad clara, y un
   enlace al `resources/qa/<CASE-ID>/<runId>/video.webm` y `trace.zip` del caso.
5. Re-ejecutar solo los alcances impactados después de los fixes, usando un `runId` nuevo.
6. Publicar el contenido del reporte de ejecución (pasaron/fallaron/bloqueados,
   riesgos, veredicto) al usuario — no digas solo "las pruebas pasaron",
   mostrá la tabla y el veredicto calculado por el script.

Referencia: `./references/qa_best_practices.md`, `./references/video_evidence_guide.md`

### 6. Reforzar Confiabilidad y Mantenibilidad

1. Mantener las pruebas aisladas (sin estado mutable compartido entre pruebas).
2. Eliminar el no-determinismo (semillas aleatorias, red real, condiciones de carrera de timing).
3. Poner en cuarentena y arreglar pruebas inestables con análisis de causa raíz.
4. Medir la salud de la suite: tasa de aprobación, tasa de flakiness, duración, defectos escapados.
5. Refactorizar pruebas con helpers/factories para reducir duplicación.

Referencia: `./references/qa_best_practices.md`

## Guías de Tareas (Playbooks)

### Grabar Pruebas de Navegador (Playwright)

1. Elegir el flujo de negocio a capturar (login, onboarding, checkout, etc.).
2. Grabar un script inicial a partir de interacciones reales:
  - `npx playwright codegen <url>`
3. Refactorizar los pasos generados a locators estables de role/label.
4. Agrupar acciones con pasos de prueba claros y aserciones significativas.
5. Nombrar la prueba con el prefijo del id de caso (`TC-01 [critical] - ...`)
   para que las herramientas de evidencia puedan mapearla contra el runbook.
6. Guardar bajo `tests/` o `e2e/` con nomenclatura basada en el escenario.
7. Confirmar que `playwright.config.ts` tiene video/trace habilitados según
   `./references/video_evidence_guide.md` antes de ejecutar.

### Ejecutar Pruebas desde un Runbook en Markdown

1. Leer el archivo Markdown provisto y extraer objetivo, entorno, precondiciones y lista de casos.
2. Normalizar cada caso en: id de caso, título, pasos, datos de prueba, resultado esperado y prioridad.
3. Si los datos de prueba de algún caso contienen una credencial literal en
   vez de una referencia `${ENV_VAR}`, detenerse y marcarlo antes de ejecutar.
   Si en cambio la variable de entorno referenciada no existe todavía en
   `.env.qa`, correr `node scripts/ensure-test-user.mjs --role <rol>` para
   provisionarla en vez de bloquear la ejecución.
4. Ejecutar los casos en orden de riesgo (crítico/alto primero), registrando el estado pass/fail de cada uno.
5. Ejecutar `scripts/organize-evidence.mjs` y `scripts/generate-execution-report.mjs`
   (ver paso 5 del Flujo de Trabajo Principal) para recolectar evidencia y calcular el veredicto,
   dejando todo bajo `resources/qa/`.
6. Publicar un resumen de ejecución que mapee cada id de caso a su resultado, defectos, evidencia y ruta de video.
7. Si el runbook está incompleto o es ambiguo, detenerse y solicitar los detalles faltantes antes de ejecutar.

Referencia: `./references/markdown_test_runbook.md`

### Grabar el Caso de Prueba Ejecutado

1. Cuando el runbook o el usuario pidan grabación, capturar el flujo real del navegador con Playwright.
2. Empezar con `npx playwright codegen <url>` y realizar exactamente los pasos del runbook.
3. Refactorizar el código generado a locators resilientes de role/label y aserciones claras.
4. Guardar un spec por id de caso (ejemplo de nombre: `checkout-happy-path-TC-01.spec.ts`),
   con el título de la prueba también prefijado por el id de caso.
5. Ejecutarlo con video/trace/screenshot habilitados, y luego correr
   `scripts/organize-evidence.mjs` para adjuntar los artefactos resultantes
   a la carpeta de evidencia del caso.
6. Asegurar que el script grabado sea ejecutable en CI (modo headless, datos determinísticos, sin sleeps duros).

### Crear Plan de Pruebas (Flujo de Plantilla)

Usar `./references/test_plan_template.md` directamente — ya cubre objetivo,
matriz funcional, riesgos, estrategia de datos/entorno (variables de
entorno, nunca secretos literales), estrategia de ejecución, requisitos de
evidencia y criterios de entrada/salida.

Salidas recomendadas (todas dentro de `resources/qa/`, creando las carpetas que falten):
- `resources/qa/plans/test-plan-<feature>.md` — documento de plan de pruebas (Markdown, a partir de la plantilla).
- `resources/qa/runbooks/qa-runbook-<feature>.md` — checklist de escenarios para ejecución (runbook en Markdown, `./references/markdown_test_runbook.md`).
- Registro de defectos con severidad y reproducibilidad (dentro del mismo runbook o del reporte de ejecución).

### Generar Pruebas Unitarias/de Integración

1. Identificar el comportamiento del componente/hook/servicio y sus casos límite.
2. Redactar pruebas alrededor del comportamiento observable por el usuario.
3. Agregar aserciones de caso exitoso, validación y camino de fallo.
4. Agregar mocks de API y esperas asíncronas donde sea necesario.
5. Ejecutar pruebas con cobertura e iterar sobre los huecos encontrados.

### Armar Pruebas E2E (Scaffolding)

1. Seleccionar 3-5 flujos críticos de usuario (login, checkout, dashboard, etc.).
2. Crear specs basados en rutas y page objects, titulados con id de caso.
3. Usar locators robustos y aserciones web-first.
4. Capturar video/trace/screenshots en cada caso (ver paso 4 del Flujo de Trabajo Principal).
5. Agregar la suite smoke al PR y la suite completa a main/release.

### Mejorar Cobertura con Foco en el Negocio

1. Medir la cobertura actual como línea base.
2. Priorizar módulos críticos (auth, pagos, reglas de negocio).
3. Agregar pruebas de rama y camino de error antes que líneas de bajo valor.
4. Aplicar umbrales en CI.
5. Seguir la tendencia en el tiempo, no una foto puntual.

### Ejecutar Plan de Pruebas y Publicar Resultados

1. Ejecutar la suite smoke en el entorno objetivo.
2. Ejecutar las suites de regresión priorizadas.
3. Recolectar artefactos con `scripts/organize-evidence.mjs`:
  - Reporte de Playwright
  - Archivos de trace
  - Videos y screenshots de cada caso
4. Generar el reporte con `scripts/generate-execution-report.mjs`.
5. Publicar el veredicto final de QA exactamente como lo calculó el script:
  - `GO` (listo)
  - `GO with known risks` (listo con riesgos conocidos)
  - `NO-GO` (defectos bloqueantes)

## Cosas a Evitar (Gotchas)

- No optimizar ciegamente para 100% de cobertura. Priorizar el comportamiento crítico.
- No testear detalles de implementación (estado interno, internals privados) cuando alcanza con aserciones de comportamiento.
- No depender de `waitForTimeout`/sleeps duros en pruebas de UI.
- No golpear APIs externas reales en pruebas automatizadas; mockearlas.
- No compartir objetos mutables entre pruebas; crear instancias frescas.
- No usar selectores frágiles como primera opción (`data-testid` es el fallback, no la opción por defecto).
- No ejecutar una regresión completa antes de los checks smoke; fallar rápido primero.
- No cerrar el ciclo de QA sin artefactos de evidencia para cada caso, no solo los que fallaron.
- No ejecutar un runbook en Markdown si faltan pasos, resultados esperados o datos de prueba para casos críticos.
- No grabar scripts generados sin refactorizar locators y aserciones para que sean determinísticos.
- No escribir usuarios/passwords reales en un plan de pruebas, runbook,
  archivo de spec, o en la carpeta `references/` de este skill — usar
  referencias `${ENV_VAR}` y `./references/env.example`. Si encontrás
  credenciales literales en cualquier archivo que estés por leer o editar,
  detenete y marcalo antes de continuar.
- No renumerar un id de caso existente una vez que ya tiene historial de
  ejecución — la evidencia y las herramientas de reporte dependen de ese id.
- No omitir la convención de id de caso en el título de los specs E2E; sin
  eso, la organización de evidencia cae a títulos slugificados y se rompe
  la trazabilidad contra el runbook.
- No bloquearte ni pedirle al usuario una contraseña real cuando falte una
  credencial de prueba — correr `scripts/ensure-test-user.mjs` en su lugar.
- No copiar `playwright.config.template.ts`/`env.example` a ciegas sobre un
  proyecto que ya tiene su propia configuración de testing; leer primero
  (ver Paso 0) y fusionar solo lo necesario.
- No dejar `QA_SLOWMO_MS=0` por defecto en specs que van a grabarse como
  evidencia para revisión humana — sin pacing, el video queda ilegible.
- No le pidas al usuario que instale Playwright/Jest/RTL/MSW ni los
  navegadores a mano — correr `scripts/ensure-qa-dependencies.mjs` (Paso 0.1)
  en su lugar.
- No instalar nada de forma global (`-g`), ni actualizar/reemplazar una
  versión ya instalada de un paquete sin permiso explícito del usuario — el
  auto-instalador solo agrega lo que falte como devDependency.
- No silenciar un fallo de instalación reintentando en loop — mostrar el
  error real (red, permisos, registry privada) y pedir que se resuelva.

## Solución de Problemas

| Problema | Solución |
|---|---|
| Aserciones asíncronas inestables (flaky) | Reemplazar sleeps por `findBy*`, `waitFor`, y mocks determinísticos. |
| Pasa en local, falla en CI | Revisar paridad de entorno, timezone/locale, reintentos, y diferencias de modo headless. |
| Suite lenta | Mover escenarios pesados de E2E a integración/unitarias donde sea posible; paralelizar shards de E2E. |
| Cobertura alta pero se escapan bugs | Agregar pruebas de integración basadas en escenarios y smoke E2E de flujos críticos. |
| Rotura frecuente de selectores | Preferir locators de role/label/text y page objects para abstracción. |
| No se genera video / la evidencia no se agrupa bien | Ver `./references/video_evidence_guide.md#troubleshooting`. |
| El video se ve acelerado, no se distingue qué se probó | Falta `slowMo` o pasos nombrados; ver `./references/video_evidence_guide.md#legibilidad-del-video-por-que-se-ve-acelerado`. |
| El veredicto da `NO-GO` y no está claro por qué | Falló un caso etiquetado `[critical]`; revisar primero la carpeta `resources/qa/<CASE-ID>/<runId>/` de ese caso. |
| Falta un usuario/contraseña de prueba para ejecutar un caso | Correr `node scripts/ensure-test-user.mjs --role user` (o `--role admin`) en vez de bloquear la ejecución. |
| Los specs generados no calzan con las convenciones del proyecto (test runner, estructura de carpetas, router) | Repetir el Paso 0 (leer `CLAUDE.md`/`package.json`/config existente) antes de seguir generando pruebas. |
| `npx playwright test` falla con "Executable doesn't exist" o falta un paquete de testing | Correr `node scripts/ensure-qa-dependencies.mjs` (con `--with-unit`/`--with-msw`/`--with-a11y` según corresponda) para instalar lo que falte, incluidos los navegadores. |
| La instalación automática de dependencias falla | Revisar acceso a la registry de npm/proxy corporativo/permisos de escritura; no reintentar en loop, reportar el error tal cual al usuario. |

## Qué se Espera Producir al Usar Este Skill

- Detectar y resolver por cuenta propia lo que falte para poder ejecutar (dependencias, navegadores, usuarios de prueba) en vez de detenerse a pedirle pasos manuales al usuario.
- Producir o refinar un archivo de plan de pruebas concreto (a partir de `./references/test_plan_template.md`) antes de una ejecución amplia.
- Grabar flujos reproducibles de navegador cuando haya que convertir comportamiento manual en pruebas automatizadas, titulados con su id de caso.
- Leer y ejecutar runbooks de pruebas en Markdown provistos por el usuario, rechazando credenciales literales en los datos de prueba.
- Grabar cada caso ejecutado solicitado y mapearlo a su id de caso más artefactos de evidencia vía `scripts/organize-evidence.mjs`.
- Ejecutar pruebas en fases (smoke -> regresión -> reintento) y reportar evidencia con `scripts/generate-execution-report.mjs`.
- Producir pruebas con intención clara, comportamiento determinístico y estructura mantenible.
- Explicar los trade-offs de cobertura y la priorización basada en riesgo.
- Recomendar gates de CI acordes a la madurez del proyecto.
- Identificar explícitamente huecos en:
  - Cobertura de caminos críticos
  - Manejo de errores
  - Puntos calientes de riesgo de flakiness
  - Ids de caso faltantes en títulos de specs E2E (rompe la trazabilidad de evidencia)

## Referencias

- `./references/testing_strategies.md`
- `./references/test_automation_patterns.md`
- `./references/qa_best_practices.md`
- `./references/markdown_test_runbook.md`
- `./references/test_plan_template.md`
- `./references/video_evidence_guide.md`
- `./references/env.example`

## Scripts

- `./scripts/ensure-qa-dependencies.mjs` — detecta el gestor de paquetes del proyecto e instala automáticamente las devDependencies de QA que falten (`@playwright/test`, `dotenv`, y opcionalmente Jest/RTL, MSW, jest-axe/@axe-core con `--with-unit`/`--with-msw`/`--with-a11y`), más los navegadores de Playwright.
- `./scripts/playwright.config.template.ts` — configuración base con video/trace/screenshot siempre activados, `slowMo` configurable vía `QA_SLOWMO_MS` para videos legibles, y carpetas de salida por ejecución (`runId`) dentro de `resources/qa/`.
- `./scripts/ensure-test-user.mjs` — verifica que existan credenciales de usuario de prueba en `.env.qa`; si faltan, genera un email/password seguros y los crea vía `QA_SEED_API_URL` (si está configurado) o da instrucciones para crearlos por el signup real de la app, persistiéndolos en `.env.qa`.
- `./scripts/organize-evidence.mjs` — crea una carpeta por caso en `resources/qa/<CASE-ID>/<runId>/` con sus adjuntos de Playwright (video/trace/screenshot), creando las carpetas si no existen, y escribe el manifest en `resources/qa/reports/<runId>-manifest.json`.
- `./scripts/generate-execution-report.mjs` — convierte ese manifest en el reporte de ejecución del runbook (`resources/qa/reports/<runId>-execution-report.md`) más el veredicto GO/GO-with-risks/NO-GO.
