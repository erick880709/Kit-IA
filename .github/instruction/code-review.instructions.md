---
description: "Reglas base de revisión de código del kit — 5 ejes, severidades y formato de comentario. Se aplican siempre que se genera o modifica código; el agente `Centinela` y la skill `centinela` las ejecutan como flujo formal antes de merge."
applyTo: "**/*.{ts,tsx,js,jsx,py,java,kt,cs,go,rb,php,sql}"
---

# Revisión de Código — Reglas Base del Kit

Este archivo es la vara mínima que cualquier código generado o editado por una
skill de este kit (`builder`, `genesis`, o el propio desarrollador) debe
cumplir. Es el equivalente para código de lo que
`markdown.instructions.md` es para los `.md`: una regla ambiental, siempre
activa, independiente de si se invoca formalmente a `Centinela`.

La skill `centinela` (ver `skills/centinela/SKILL.md`) es el flujo **formal**
de revisión de 5 ejes con reporte y quality gate antes de merge — se invoca
explícitamente. Este archivo es la base que aplica en todo momento, incluso
sin invocar esa skill.

## Los 5 ejes (en orden de prioridad de bloqueo)

1. **Seguridad** — sin secretos en código, sin inyección (SQL/comandos/paths),
   validación de todo input externo, autenticación/autorización explícitas
   antes de acceder a un recurso.
2. **Correctitud** — la lógica hace lo que la historia de usuario pide; sin
   condiciones de carrera obvias; sin riesgo de pérdida/corrupción de datos.
3. **Pruebas** — el código nuevo o modificado tiene prueba que lo cubre;
   nombres de prueba descriptivos; sin pruebas que siempre pasan.
4. **Arquitectura** — respeta el patrón y las capas definidas por `archi`
   para este proyecto; sin dependencias en la dirección incorrecta.
5. **Legibilidad** — nombres claros, funciones pequeñas y con una sola
   responsabilidad, sin duplicación evidente, sin anidamiento excesivo
   (máx. 3-4 niveles).

## Severidades

- 🔴 **CRÍTICO** — bloquea merge. Seguridad, correctitud grave, breaking
  change sin versionar, riesgo real de pérdida de datos.
- 🟡 **IMPORTANTE** — requiere decisión explícita antes de mergear (arreglar
  o asumir el riesgo por escrito). Cobertura de pruebas faltante en ruta
  crítica, violación seria de arquitectura, duplicación severa.
- 🟢 **SUGERENCIA** — no bloquea. Legibilidad, optimización sin impacto
  funcional, mejoras de documentación.

## Principios de cómo comentar

- Sé específico: archivo, línea, ejemplo concreto — nunca "esto está mal"
  sin decir qué ni por qué.
- Explica el impacto real, no solo la regla que se rompe.
- Propón la corrección, no solo señales el problema.
- Reconoce explícitamente lo que está bien hecho — no todo comentario es una
  corrección.
- Agrupa comentarios sobre el mismo tema en vez de repetirlos línea por
  línea.

## Formato de comentario

```markdown
**[SEVERIDAD] Eje: título breve**

Descripción concreta del problema o la sugerencia.

**Por qué importa:**
Impacto real si no se corrige.

**Corrección sugerida:**
[ejemplo de código si aplica]
```

## Referencias específicas por stack

Este archivo es agnóstico de lenguaje a propósito, porque `builder` opera en
cualquier stack. Cuando el proyecto tiene reglas propias más específicas
(p. ej. `architecture.instructions.md` o `backend.instructions.md` para
proyectos Java/Kotlin con Clean Architecture, o
`security-and-owasp.instructions.md` para el detalle OWASP completo), esas
reglas se suman a estas — nunca las reemplazan. Ante conflicto de detalle
técnico específico de stack, gana la instrucción más específica del proyecto;
ante conflicto de proceso de revisión (severidades, formato de comentario),
gana este archivo.
