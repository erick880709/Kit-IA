---
name: seguridad-rendimiento
description: 'Endurece código que maneja input de usuario, autenticación, datos sensibles o integraciones externas contra el OWASP Top 10, y mide/optimiza performance con presupuestos concretos (Core Web Vitals en frontend, latencia/throughput en backend) en vez de optimizar a ciegas. Úsala SIEMPRE que el usuario pida "revisar seguridad de este endpoint/módulo", "hacer un hardening", "auditoría OWASP", "por qué está lento esto", "optimizar performance", o cuando `revision-calidad` detecte un hallazgo de seguridad o performance que requiera un análisis dedicado. Adaptación al español y al contrato de `resources/` de las skills `security-and-hardening` y `performance-optimization` de addyosmani/agent-skills.'
---

# Seguridad y Rendimiento

## Resumen

Envuelve `security-and-hardening` y `performance-optimization` del pack
`agent-skills`. Referencia completa (inglés, solo lectura):
`.github/skills-addy/skills/security-and-hardening/SKILL.md` y
`.github/skills-addy/skills/performance-optimization/SKILL.md`, más los
checklists compartidos `.github/skills-addy/references/security-checklist.md`
y `.github/skills-addy/references/performance-checklist.md`.

Este skill también alimenta y consume `resources/security/` — la misma
carpeta que ya usa `archi` para hallazgos de seguridad de arquitectura — para
que un hallazgo de arquitectura y uno de implementación queden en un solo
lugar consultable.

## Entrada esperada

- El módulo/endpoint a revisar (típicamente recién salido de `tdd-implementacion`).
- `resources/architecture/definitions/` (RNF de seguridad/performance que dejó `janus`).
- Cualquier `RNF-###` o `RT-###` concreto que aplique — citalo por ID, no de forma genérica.

## Salida

- `resources/engineering/security/hardening-<modulo>.md`
- `resources/engineering/perf/budget-<modulo>.md`
- Actualiza `resources/security/` si el hallazgo es relevante para futuras
  corridas de `archi` (Caso C, AS-IS→TO-BE).

## Seguridad — sistema de tres niveles de frontera

Clasificá cada dato que entra al sistema por su nivel de confianza antes de
decidir cuánta validación aplicar:

1. **Frontera externa** (input de usuario, webhooks, API pública) — validación
   estricta, allowlist sobre denylist, nunca confiar en el cliente.
2. **Frontera interna** (entre servicios propios) — validar contratos pero con
   menos paranoia que la frontera externa; el contrato de API ya lo definió `archi`/`builder`.
3. **Dato ya confiable** (post-validación, dentro del mismo proceso) — no
   revalidar en cada capa, eso es ruido, no seguridad.

Repasar contra el OWASP Top 10 vigente (inyección, auth rota, exposición de
datos sensibles, control de acceso, mala configuración, etc.) usando
`.github/skills-addy/references/security-checklist.md` como checklist
operativa. Prestar atención especial a: manejo de secretos (nunca en código
ni en `resources/`, siempre variables de entorno — mismo principio que ya
aplica `qa` para credenciales de QA), auditoría de dependencias, headers
de seguridad, y CORS.

## Performance — medir antes de optimizar

No optimices sin un número de referencia. Flujo:

1. **Medir primero** — perfilar/loggear el estado actual real (no estimado).
2. **Definir el presupuesto** — Core Web Vitals objetivo en frontend (LCP,
   INP, CLS) o latencia p50/p95/p99 y throughput en backend, según aplique.
3. **Optimizar lo que realmente pesa** — el perfil manda, no la intuición de
   "esto se ve lento".
4. **Volver a medir** y dejar constancia del antes/después en `budget-<modulo>.md`.

## Rationalizaciones comunes

| Excusa | Realidad |
|---|---|
| "Es un endpoint interno, no hace falta validar tanto" | Frontera interna igual valida el contrato; "no hace falta validar nada" es la excusa que abre la inyección. |
| "Ya sé que esto es lento, no necesito perfilar" | La intuición sobre qué es lento falla seguido; perfilá antes de tocar código. |
| "Guardé la API key en una variable dentro del código, la voy a mover después" | Nunca — va a variable de entorno ahora, antes de commitear. |
| "El framework ya sanitiza esto" | Verificá la versión y configuración real, no asumas por el nombre del framework. |

## Red flags

- Validación solo del lado del cliente sin espejo en el servidor.
- Optimización de performance sin número de "antes" para comparar.
- Secretos hardcodeados, aunque sea "solo para probar".
- Un hallazgo de seguridad marcado como resuelto sin una prueba que lo confirme.

## Verificación antes de cerrar

- [ ] Cada frontera de confianza tiene la validación que le corresponde (ni de más ni de menos).
- [ ] El checklist OWASP relevante fue repasado explícitamente, no solo "a ojo".
- [ ] Hay una medición de performance de "antes" y "después", no solo la optimización.
- [ ] `hardening-<modulo>.md` y `budget-<modulo>.md` quedaron guardados con evidencia real.

Con esto cerrado, el flujo continúa hacia `documentacion-observabilidad` (si
hubo una decisión que merece ADR) y `entrega-continua`.
