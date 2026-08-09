# Formato de Runbook de Pruebas en Markdown

Usá este formato cuando la ejecución de pruebas esté dirigida por un documento Markdown.

## Secciones Obligatorias

1. Objetivo
- Qué se está validando y por qué.

2. Entorno
- URL base, nombre del entorno, navegador objetivo, y requisitos de seed/reseteo.
- **Roles** de cuentas de prueba únicamente (ej. "usuario estándar", "admin")
  — nunca usuarios/passwords reales. Apuntar a `./env.example` y a las
  variables de entorno que necesita la ejecución (`QA_BASE_URL`,
  `QA_USER_EMAIL`, `QA_USER_PASSWORD`, etc.).
- Si esas variables no están definidas todavía, no es un bloqueante: correr
  `../scripts/ensure-test-user.mjs --role <rol>` genera credenciales de
  prueba nuevas y las provisiona (por API si hay `QA_SEED_API_URL`, o por
  el signup real de la app) antes de ejecutar el runbook.

3. Precondiciones
- Estado requerido de la aplicación antes de la ejecución.

4. Casos de Prueba
- Cada caso debe incluir:
  - Id de Caso (estable, único, patrón `TC-\d+`; nunca renumerar un caso
    existente una vez que ya tiene historial de ejecución)
  - Título
  - Prioridad (critical/high/medium/low)
  - Pasos
  - Resultado esperado
  - Datos de prueba (referencias a variables de entorno, ej.
    `${QA_USER_EMAIL}` — no secretos literales)
  - Grabación requerida (sí/no) — ver `./video_evidence_guide.md` para la
    política por defecto del proyecto (este skill usa "sí" por defecto para
    todos los casos)
  - Ruta del spec automatizado (se completa después de grabar, ej.
    `e2e/checkout-happy-path-TC-01.spec.ts`)

5. Reglas de Evidencia
- Qué artefactos son obligatorios para pass/fail (screenshots, trace, video, logs).
- Por defecto: video + trace + screenshot obligatorios para cada caso, no
  solo para los que fallan (ver `./video_evidence_guide.md`).

6. Criterios de Salida
- Condiciones para marcar GO, GO con riesgos, o NO-GO.

## Plantilla Recomendada de Caso

```markdown
## Caso de Prueba TC-01 - Login con credenciales válidas

- Prioridad: critical
- Grabación requerida: sí
- Ruta del spec automatizado: e2e/login-TC-01.spec.ts
- Datos de prueba:
  - Usuario: ${QA_USER_EMAIL} / ${QA_USER_PASSWORD}

### Pasos
1. Abrir /login.
2. Ingresar credenciales válidas.
3. Hacer clic en Ingresar.

### Resultado esperado
- El usuario es redirigido a /dashboard.
- El nombre del usuario es visible en el header.

### Evidencia
- Video del flujo completo (obligatorio, en cada ejecución).
- Screenshot después del login exitoso.
- Trace de Playwright.
```

## Reglas de Parseo para la Ejecución

- Parsear los encabezados como límites de caso cuando contienen un patrón de id de caso tipo "TC-".
- Si dos casos del runbook usan el mismo id `TC-xxx` por error (copy-paste sin
  actualizar), corregirlo antes de ejecutar — no dejar que se resuelva solo en
  la evidencia. `../scripts/organize-evidence.mjs` lo detecta después del
  hecho (carpeta `__DUP2`) pero es mejor prevenirlo en el runbook.
- Si un caso no tiene resultado esperado, marcarlo como inválido y pedir aclaración.
- Si los datos de prueba de un caso parecen contener una credencial real
  (no una referencia `${ENV_VAR}`), detenerse y marcarlo en vez de ejecutar
  — no seguir adelante silenciosamente con un secreto filtrado.
- Si un caso está marcado como grabación requerida, crear o actualizar un
  spec de Playwright vinculado al mismo id de caso, con el id de caso (y
  opcionalmente una etiqueta `[prioridad]`) como prefijo literal del título
  de la prueba — ver `./video_evidence_guide.md#case-id-convention`. Esto es
  lo que permite que `../scripts/organize-evidence.mjs` mapee el video
  resultante contra este caso automáticamente.
- Ejecutar los casos críticos antes que los medium/low cuando el tiempo es limitado.
- Cada caso ejecutado obtiene su propia carpeta directamente en
  `resources/qa/<CASE-ID>/`, con una subcarpeta por `runId` adentro para no
  perder la evidencia de ejecuciones anteriores del mismo caso. Generar un
  `runId` por ejecución (timestamp o id de build de CI), compartido entre
  `resources/qa/test-results/<runId>`, `resources/qa/<CASE-ID>/<runId>` de
  cada caso tocado, y el nombre del manifest/reporte.
- Este runbook en sí mismo se guarda como
  `resources/qa/runbooks/qa-runbook-<feature>.md` (creando la carpeta si no existe).

## Esquema del Reporte Final de Ejecución

Se genera automáticamente con
`../scripts/generate-execution-report.mjs --manifest resources/qa/reports/<runId>-manifest.json --out resources/qa/reports/<runId>-execution-report.md`.
Si este runbook nace de una historia de Jira/HU (ver `../SKILL.md` Paso 0),
sumar `--story-key <ID> --story-status "<estado>"` para que el reporte deje
constancia del estado de la historia al momento de probar. En CI, sumar
`--fail-on-no-go` (o `--fail-on-risk`) para que el veredicto bloquee el
pipeline en vez de quedar solo como texto informativo.

Para cada id de caso, incluye:
- Estado: passed, failed, blocked, o not-run
- Resumen del defecto (primera línea del error de fallo, si falló o fue bloqueado)
- Rutas de los artefactos de evidencia (nombres de archivo de video/trace/screenshot)
- Ruta de la grabación (`resources/qa/<CASE-ID>/<runId>/video.webm`)
- Marca `⚠️dup` si el id de caso quedó duplicado por otro título de prueba (ver `../scripts/organize-evidence.mjs`)

Más un veredicto a nivel de ejecución: `GO`, `GO with known risks`, o
`NO-GO` (cualquier caso etiquetado `[critical]` que falle fuerza `NO-GO`).
