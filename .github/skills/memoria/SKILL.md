---
name: memoria
description: Gestiona la continuidad de contexto entre sesiones de trabajo. Al iniciar una sesión, restaura el estado del proyecto (fase activa, último skill ejecutado, decisiones tomadas, tareas pendientes, riesgos abiertos, aprendizaje acumulado). Al finalizar, guarda el nuevo estado para la siguiente sesión. Úsala SIEMPRE que el usuario inicie una nueva sesión de trabajo sobre un proyecto ya empezado, cuando pregunte "¿en qué quedamos la última vez?", "¿qué sigue?", "¿qué decisiones tomamos?", o cuando termine una sesión y quiera dejar registro del avance. También al inicio de cualquier sesión nueva para que el orquestador sepa qué fase del pipeline está activa sin tener que re-leer todo resources/.
---

# Memoria — Gestión de Contexto entre Sesiones

## Propósito

En un flujo de trabajo que abarca múltiples sesiones de chat (días o semanas), el mayor riesgo no es técnico: es la **pérdida de contexto**. Un agente que empieza una sesión nueva sin saber qué se decidió en la anterior puede: repetir trabajo ya hecho, contradecir decisiones previas, o peor, no detectar que el proyecto ya avanzó y empezar desde cero.

Este skill resuelve eso con un mecanismo simple: al **inicio** de cada sesión, lee el estado guardado de `resources/session/` y lo carga como contexto activo. Al **final** de la sesión (o cuando el usuario lo pida), guarda el nuevo estado. El `orquestador` lo invoca automáticamente al arrancar — el usuario no debería tener que pedirlo manualmente.

## Dónde se guarda la memoria

```
resources/session/
├── estado.json                    # Estado estructurado de la sesión actual (machine-readable)
├── contexto.md                    # Resumen narrativo para consumo humano y del agente
├── bitacora.md                    # Historial cronológico de sesiones (append-only)
└── learning/                      # Lecciones aprendidas y patrones descubiertos
    ├── LNN-<tema>.md              # Una lección por archivo (Learning Number N)
    └── INDEX.md                   # Índice de lecciones por categoría
```

## Al iniciar una sesión

### Paso 1 — Detectar si hay sesión previa

1. Busca `resources/session/estado.json` en la raíz del proyecto. Si no existe, esta es la primera sesión sobre este proyecto → pasa al Paso 4 (inicializar).
2. Si existe, léelo completo (es un JSON pequeño, ~2KB). Extrae:
   - `proyecto`: nombre del proyecto
   - `fase_actual`: fase del pipeline en la que quedó (`negocio`, `arquitectura`, `scaffold`, `ingenieria`, `entrega`)
   - `ultimo_skill_ejecutado`: nombre del skill
   - `hitos_completados`: lista de IDs (ej. `["RF-01..RF-12", "ADR-001", "HU-01..HU-04"]`)
   - `pendientes`: tareas o HU/TT aún no abordadas
   - `decisiones_pendientes`: preguntas abiertas que el usuario aún no respondió
   - `riesgos_abiertos`: riesgos identificados no mitigados
   - `supuestos_activos`: supuestos no validados aún
   - `fecha_ultima_sesion`: ISO 8601
3. Lee también `resources/session/contexto.md` (resumen narrativo) para tener la historia completa.

### Paso 2 — Restaurar contexto

1. **Preséntale al usuario un resumen ejecutivo** de dónde quedó el proyecto (máximo 6 líneas):
   - Proyecto y fase actual
   - Último avance concreto (qué se entregó)
   - Lo que sigue (próximo paso lógico en el pipeline)
   - Decisiones o preguntas que quedaron abiertas
2. **No preguntes "¿qué querés hacer?" a secas** — el usuario ya tomó decisiones en sesiones previas. Decile: "La última vez quedamos en [X]. Lo que sigue naturalmente es [Y]. ¿Avanzamos con eso o preferís otro camino?"
3. **Carga en contexto** los archivos de `resources/` que el `estado.json` indique como relevantes para la fase actual:
   - Fase `negocio` → `resources/functional/requests/`, `resources/summary/`
   - Fase `arquitectura` → `resources/architecture/`, `resources/functional/hu/`
   - Fase `scaffold` → `resources/architecture/`, `resources/functional/hu/`
   - Fase `ingenieria` → `resources/engineering/`, `resources/qa/`
   - Fase `entrega` → `resources/engineering/release/`, `resources/security/`

### Paso 3 — Validar que el estado sigue siendo correcto

El código pudo haber cambiado entre sesiones (commits de otros devs, ramas mergeadas). Antes de confiar ciegamente en el `estado.json`:

1. Si hay un repo Git, revisa `git log --oneline -5` para ver commits recientes desde `fecha_ultima_sesion`.
2. Si hay cambios en archivos que afectan la fase actual (ej. alguien mergeó un PR que resuelve un pendiente), actualiza el estado.
3. Si el proyecto se movió a otra fase (ej. el scaffold ya fue generado por otro medio), detectalo y ajustá.

### Paso 4 — Inicializar (primera sesión)

Si `resources/session/` no existe:

1. Crea la carpeta.
2. Inicializa `estado.json` con estructura vacía pero con `fecha_inicio` y `proyecto` (preguntá el nombre si no es obvio del repo).
3. Crea `contexto.md` con un placeholder inicial.
4. Crea `bitacora.md` con la primera entrada.
5. No asumas fase — dejá que el `orquestador` la determine a partir de lo que exista en `resources/`.

## Al finalizar una sesión

Este skill se invoca **al final de cada sesión** (el `orquestador` lo encadena automáticamente como último paso, o el usuario lo pide con "guardá el estado de la sesión"). No esperes a que el usuario lo pida.

### Qué guardar

Actualiza `resources/session/estado.json`:

```json
{
  "proyecto": "Nombre del Proyecto",
  "fase_actual": "arquitectura",
  "fecha_ultima_sesion": "2026-08-09T18:30:00Z",
  "ultimo_skill_ejecutado": "archi",
  "hitos_completados": ["RF-01..RF-12", "HU-01..HU-04", "Documento_Arquitectura_ProyectoX"],
  "pendientes": ["HU-05: Módulo de notificaciones", "TT-03: Configurar CI/CD"],
  "decisiones_pendientes": ["Elegir entre PostgreSQL y MongoDB para el módulo de analytics"],
  "riesgos_abiertos": ["El equipo no tiene experiencia en Kubernetes"],
  "supuestos_activos": ["Asumimos que el cliente usará Azure (no confirmado)"],
  "archivos_clave": [
    "resources/architecture/Documento_Arquitectura_ProyectoX.md",
    "resources/functional/hu/HU-01.md"
  ],
  "metricas": {
    "total_sesiones": 4,
    "horas_estimadas_invertidas": 12
  }
}
```

Registra en `resources/session/bitacora.md` (append):

```markdown
## Sesión 4 — 2026-08-09

**Objetivo:** Diseñar arquitectura de despliegue en AWS
**Skills ejecutados:** archi (Caso A, con modo multi-nube activo)
**Artefactos generados:**
- `resources/architecture/Despliegue_AWS_ProyectoX.drawio`
- `resources/architecture/Pricing_ProyectoX.md`
- `resources/architecture/adr/ADR-002-base-de-datos.md`

**Decisiones tomadas:**
- PostgreSQL sobre MongoDB para datos transaccionales (ver ADR-002)
- Redis para caché de sesiones

**Pendientes para próxima sesión:**
- Resolver ADR-003: ECS vs EKS para orquestación
- Iniciar `builder` con HU-05

**Riesgos identificados:**
- Cold start de Lambda puede afectar latencia p95 (pendiente de benchmark)
```

Regenera `resources/session/contexto.md` (resumen narrativo completo, no append — reescribilo entero cada vez, máximo 1 página).

## Lecciones aprendidas (Learning Journal)

Cuando durante una sesión se descubre algo que conviene recordar para futuras sesiones (un patrón que funcionó, un error que costó caro, una decisión que resultó acertada o equivocada), este skill lo registra:

1. Crea un archivo `resources/session/learning/LNN-<tema>.md` (numeración secuencial).
2. Usa este formato:

```markdown
---
fecha: 2026-08-09
fase: arquitectura
tags: [base-de-datos, decision, postgresql]
severidad: alta
---

# LNN-003: PostgreSQL JSONB no reemplaza MongoDB para documentos anidados profundos

## Contexto
Evaluando si usar el tipo JSONB de PostgreSQL en vez de MongoDB para la colección de "perfiles de usuario" (documentos con hasta 5 niveles de anidamiento).

## Decisión
Descartamos JSONB porque las consultas con `jsonb_path_query` en 3+ niveles de profundidad eran 8x más lentas que MongoDB y el ORM (Prisma) no las soportaba bien.

## Consecuencia
MongoDB para la colección de perfiles. PostgreSQL para todo lo demás. Dos DBs en vez de una — el costo operativo extra se justifica por la diferencia de performance.

## Revalidación
Revisar en 6 meses si PostgreSQL 18 mejora el soporte de JSONB indexado.
```

## Integración con el orquestador

El `orquestador` debe:

1. **Al inicio de cada sesión**: invocar `memoria` (modo lectura) para restaurar contexto antes de decidir la ruta del pipeline.
2. **Al final de cada sesión**: invocar `memoria` (modo escritura) para guardar el estado antes de cerrar.
3. **Cuando un skill termina**: actualizar `estado.json` con el nuevo hito completado y los pendientes actualizados.

## Reglas de oro

1. **La memoria no reemplaza a `resources/` — lo complementa.** `resources/` guarda los artefactos; `resources/session/` guarda el contexto de qué se hizo, qué falta y qué se aprendió. Uno sin el otro es incompleto.
2. **Sé conciso.** `contexto.md` no es un documento de arquitectura — es un resumen ejecutivo para que un agente (o un humano) en 30 segundos sepa dónde está parado el proyecto.
3. **No asumas que la memoria es perfecta.** Siempre validá contra el estado real del repositorio (git log, archivos existentes en `resources/`).
4. **El usuario puede borrar `resources/session/` en cualquier momento** sin perder artefactos. La memoria es volátil por diseño — los artefactos en `resources/` son la fuente de verdad.
