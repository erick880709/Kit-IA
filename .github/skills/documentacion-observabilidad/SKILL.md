---
name: documentacion-observabilidad
description: 'Documenta decisiones arquitectónicas relevantes tomadas durante la implementación (ADRs) y define/agrega instrumentación de logs estructurados, métricas RED y trazas antes de que el código llegue a producción. Úsala cuando `tdd-implementacion`, `revision-calidad` o `seguridad-rendimiento` tomen una decisión de diseño no trivial que merezca quedar registrada, cuando el usuario pida "documentar por qué elegimos X", "escribir un ADR", "agregar logging/métricas a este módulo", o "preparar observabilidad antes de desplegar". Adaptación al español y al contrato de `resources/` de las skills `documentation-and-adrs` y `observability-and-instrumentation` de addyosmani/agent-skills.'
---

# Documentación (ADRs) y Observabilidad

## Resumen

Envuelve `documentation-and-adrs` y `observability-and-instrumentation` del
pack `agent-skills`. Referencia completa (inglés, solo lectura):
`.github/skills-addy/skills/documentation-and-adrs/SKILL.md` y
`.github/skills-addy/skills/observability-and-instrumentation/SKILL.md`, más
`.github/skills-addy/references/observability-checklist.md`.

Los ADRs que produce este skill son el mismo tipo de artefacto que `archi`
menciona en su plantilla de documento de arquitectura — este skill es el que
efectivamente los redacta cuando la decisión surge durante la implementación
(no durante el diseño inicial), y los dos flujos convergen en el mismo lugar.

## Entrada esperada

- La decisión a documentar: puede venir de un slice de `tdd-implementacion`
  ("elegimos X librería de colas en vez de Y"), de un hallazgo de
  `revision-calidad`/`seguridad-rendimiento`, o de una pregunta directa del usuario.
- `resources/architecture/Documento_Arquitectura_<Proyecto>.md` como contexto
  de las decisiones ya tomadas por `archi`, para no contradecirlas sin registrar el cambio.

## Salida

- `resources/engineering/adr/ADR-<n>-<titulo-corto>.md`
- `resources/engineering/observability/plan-<modulo>.md`

## ADRs — qué va adentro

Un ADR corto y honesto vale más que uno largo y genérico. Estructura mínima:

```
# ADR-<n>: <Título en una frase, orientado a la decisión>

## Estado
Propuesto | Aceptado | Reemplazado por ADR-<m>

## Contexto
Qué problema forzó esta decisión. Cita el RNF-###/RT-### si aplica.

## Decisión
Qué se decidió, en una o dos frases directas.

## Alternativas consideradas
Al menos una, con la razón concreta por la que se descartó (no "no nos gustó").

## Consecuencias
Qué se gana y qué se sacrifica. Un ADR sin trade-off explícito es sospechoso.
```

Numerá los ADRs de forma secuencial y nunca reutilices un número, ni siquiera
si el ADR queda obsoleto — marcalo como reemplazado y apuntá al nuevo.

## Observabilidad — instrumentar mientras se construye, no después

La instrumentación no es un paso posterior a "ya funciona", corre en paralelo
a `tdd-implementacion` (igual que en el pack addy, donde
`observability-and-instrumentation` corre en paralelo a la implementación, no
después). Cubrir como mínimo:

- **Logging estructurado** — con contexto suficiente para diagnosticar sin
  tener que reproducir localmente (IDs de correlación, no solo mensajes libres).
- **Métricas RED** — Rate, Errors, Duration por endpoint/operación crítica.
- **Trazas** — al menos en los cruces entre servicios/capas si la arquitectura
  de `archi` los define como componentes separados.
- **Alertas basadas en síntoma**, no en causa — alertar sobre "el usuario ve
  errores" en vez de "la CPU subió", que puede ser ruido sin impacto real.

## Rationalizaciones comunes

| Excusa | Realidad |
|---|---|
| "La decisión es obvia, no hace falta un ADR" | Obvia hoy, no en seis meses ni para quien se sume al equipo — el ADR es barato de escribir ahora. |
| "Agrego logs cuando algo falle en producción" | Para ese momento ya es tarde para diagnosticar sin contexto; instrumentá al construir. |
| "Las métricas las agrega el equipo de infra después" | Si el `RNF` de observabilidad ya está definido por `janus`/`archi`, es parte del criterio de aceptación, no un extra. |

## Red flags

- Un ADR sin alternativas consideradas (parece más una justificación a posteriori que una decisión).
- Logging que solo dice "error" sin contexto suficiente para diagnosticar.
- Alertas configuradas sobre métricas de causa en vez de síntoma visible al usuario.

## Verificación antes de cerrar

- [ ] Cada decisión no trivial de la implementación tiene su ADR correspondiente.
- [ ] El ADR cita el RNF/RT de origen cuando existe, en vez de referenciar la documentación de forma genérica.
- [ ] La instrumentación cubre logging + al menos una métrica RED del componente tocado.
- [ ] Las alertas nuevas (si las hay) están basadas en síntoma, no en causa interna.

Con esto, el flujo converge en `entrega-continua` para el commit, el gate de
CI/CD y el checklist de shipping.
