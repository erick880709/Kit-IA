# Comparativa de Kits: Erick Soto × addyosmani/agent-skills

> ⚠️ Documento pendiente de redacción. Ver `README.md` para el contexto de la fusión.

## Resumen

Este documento analiza skill por skill la fusión entre:

1. **Kit de Erick Duvan Soto Díaz** — Pipeline de negocio→arquitectura→scaffold (janus,
   refinador, desglosador, figma-prd-mockups, archi, genesis, builder, qa, front)
2. **Kit de addyosmani/agent-skills** — Disciplina de ingeniería (TDD, code review,
   seguridad, performance, CI/CD, observabilidad)

La fusión se materializa en 7 skills wrapper en español que adaptan los skills de addy
al contrato de `resources/` del kit de Erick, y un `orquestador` que enruta entre ambos.

## Skills wrapper (bridge)

| Skill wrapper (español) | Skill addy (inglés) | Adaptación |
|---|---|---|
| `tdd-implementacion` | `incremental-implementation` + `test-driven-development` | Lee HU de `resources/functional/hu/`, escribe en `resources/engineering/` |
| `revision-calidad` | `code-review-and-quality` + `code-simplification` | 5 ejes adaptados al español, escribe en `resources/engineering/reviews/` |
| `seguridad-rendimiento` | `security-and-hardening` + `performance-optimization` | OWASP Top 10 + Core Web Vitals, escribe en `resources/engineering/security/` y `perf/` |
| `documentacion-observabilidad` | `documentation-and-adrs` + `observability-and-instrumentation` | ADRs en `resources/architecture/adr/`, logs/métricas/trazas en `resources/engineering/observability/` |
| `entrega-continua` | `git-workflow-and-versioning` + `ci-cd-and-automation` + `shipping-and-launch` + `deprecation-and-migration` | Checkout de release en `resources/engineering/release/` |

## Uso directo (sin wrapper)

Los siguientes skills de addy se usan tal cual, en inglés, sin adaptación:
- `context-engineering`, `source-driven-development`
- `doubt-driven-development`
- `debugging-and-error-recovery`, `browser-testing-with-devtools`
- `frontend-ui-engineering`, `api-and-interface-design`
- `interview-me`, `idea-refine`

---

*Para el análisis skill-por-skill detallado, consultar el historial de commits o los
issues del repositorio.*
