# Plantilla de Plan de Pruebas

Plantilla concreta de Markdown, para completar, que hay que producir cuando
un usuario pide un plan de pruebas. Usá `./testing_strategies.md` para el
razonamiento detrás de la distribución de la pirámide y los umbrales;
usá este archivo para la forma real del documento a entregar.

Instanciá siempre esta plantilla como un archivo real en
`resources/qa/plans/test-plan-<feature>.md` (creando la carpeta si no
existe) en vez de solo describirla en el chat, salvo que el usuario pida
explícitamente un resumen verbal.

## Encabezado Obligatorio

```markdown
# Plan de Pruebas: <Nombre de la Feature / Release>

- Autor: <nombre o "Claude Code (skill QA)">
- Fecha: <YYYY-MM-DD>
- Entorno(s): <staging | preprod | prod-like>
- Historia relacionada: <id de Jira (ej. PROJ-123) o id local (ej. HU-01) — "N/A" si el plan no nace de una historia puntual>
- Estado en Jira al momento de planear: <ej. "Ready for QA", "In Review" — "N/A" si no aplica. Si no es un estado listo para QA, dejarlo señalado acá y pasarlo también a `generate-execution-report.mjs --story-status` (ver ./video_evidence_guide.md)>
- Runbook relacionado: <ruta al runbook en Markdown que producirá este plan, ej. resources/qa/runbooks/qa-runbook-<feature>.md>
```

Si el plan nace de una historia técnica (ver `../SKILL.md` Paso 0), cada fila
de la Matriz Funcional (sección 4) debe trazarse a un criterio de aceptación
de esa historia — marcar con `[SUPUESTO]` cualquier escenario que la
historia no sustente explícitamente.

## 1. Objetivo

Un párrafo: qué se está validando y por qué (feature nueva, guarda de
regresión, gate de release, seguimiento de un incidente).

## 2. Alcance

**Dentro del alcance**
- Feature/página/flujo 1
- Feature/página/flujo 2

**Fuera del alcance**
- Áreas explícitamente excluidas y por qué (dueño de otro equipo, código
  sin cambios, ya cubierto por una suite existente, etc.)

## 3. Evaluación de Riesgo

| Área | Impacto de negocio si falla | Probabilidad | Prioridad |
|---|---|---|---|
| Login / auth | Alto | Bajo | Critical |
| Checkout | Alto | Medio | Critical |
| Configuración de perfil | Bajo | Bajo | Medium |

La prioridad define el orden de ejecución (crítico/alto primero) y qué
casos requieren grabación de video — ver `./video_evidence_guide.md`.

## 4. Matriz Funcional

| Feature | Escenario | Resultado esperado | Prioridad | Tipo de prueba |
|---|---|---|---|---|
| Login | Credenciales válidas | Redirige a /dashboard | Critical | E2E |
| Login | Credenciales inválidas | Error inline, sin redirección | High | E2E |
| Login | Campos vacíos | Errores de validación por campo | Medium | Integración |

Esta matriz es la fuente para generar los casos de prueba individuales en
el runbook de Markdown (`./markdown_test_runbook.md`).

## 5. Estrategia de Datos y Entorno

- Cuentas de prueba necesarias (roles, no credenciales).
- Fixtures/datos semilla y cómo se resetean entre ejecuciones.
- **Política de credenciales: nunca escribir usuarios/passwords reales en
  este documento ni en el runbook.** Referenciar variables de entorno en
  su lugar (ver `./env.example`), ej. "Datos de prueba: `${QA_USER_EMAIL}` /
  `${QA_USER_PASSWORD}`".
- Dependencias/integraciones externas que necesitan mockearse (handlers de
  MSW, APIs de sandbox, feature flags).

## 6. Estrategia de Ejecución

1. Suite smoke (solo flujos críticos) en el entorno objetivo.
2. Suite completa/de regresión en orden de prioridad (crítico → alto → medio → bajo).
3. Reintento dirigido de los casos impactados solamente, después de que los fixes estén desplegados.

## 7. Requisitos de Evidencia

- Cada caso: trace de Playwright + al menos un screenshot.
- Video: grabado y conservado para cada caso (ver
  `./video_evidence_guide.md` para la política de retención y el layout de
  almacenamiento del proyecto).
- Reporte de ejecución generado con
  `../scripts/generate-execution-report.mjs` después de cada corrida.

## 8. Criterios de Entrada

- Entorno objetivo desplegado y estable.
- Datos de prueba/fixtures sembrados.
- Suite smoke automatizada en verde sobre el build bajo prueba.

## 9. Criterios de Salida

- Sin defectos abiertos de prioridad crítica.
- Umbral de tasa de aprobación acordado alcanzado (indicar el número, ej.
  ≥95% de los casos de prioridad alta+ pasaron).
- Todos los riesgos conocidos documentados con dueño y mitigación/aceptación.

## 10. Entregables

Todos dentro de `resources/qa/` (creando las carpetas que falten):

- Este plan de pruebas (`resources/qa/plans/test-plan-<feature>.md`).
- Runbook en Markdown con los casos de prueba individuales (`resources/qa/runbooks/qa-runbook-<feature>.md`, formato de `./markdown_test_runbook.md`).
- Reporte de ejecución por corrida (`resources/qa/reports/<runId>-execution-report.md`).
- Una carpeta de evidencia por caso ejecutado (`resources/qa/<CASE-ID>/<runId>/`), con historial entre corridas.
- Veredicto final: `GO` / `GO with known risks` / `NO-GO`.
