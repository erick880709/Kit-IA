---
name: desglosador
description: >
  Lee una épica de Jira usando el MCP de Jira, la analiza en profundidad y genera
  automáticamente un desglose estructurado en historias de usuario, tareas técnicas
  y subtareas. Usa este skill SIEMPRE que el usuario mencione épicas de Jira, quiera
  descomponer requerimientos en historias, crear user stories desde Jira, hacer
  breakdown de features, generar tareas desde una épica, o diga cosas como "desglosa
  esta épica", "separa en historias", "crea las tareas para la épica X", "analiza
  la épica PROJ-123", "genera historias de usuario desde Jira". También aplica cuando
  el usuario menciona claves de Jira (ej. ABC-42) en el contexto de planificación o
  descomposición de trabajo.
compatibility: "Requiere MCP de Jira (Atlassian MCP o compatible)"
---

# Desglosador — Jira Epic Breakdown

Este skill lee una épica de Jira, la analiza y genera un desglose estructurado en:
- **Historias de usuario** (con criterios de aceptación)
- **Tareas técnicas** (trabajo de ingeniería sin valor de negocio directo)
- **Subtareas** (para historias o tareas complejas)

---

## Paso 0 — Solicitar la fuente de entrada

Al iniciar, pregunta siempre al usuario:

> **¿Cuál es la fuente de la épica a analizar?**
> - **ID de Jira** — ingresa la clave de la épica (ej. `PROJ-123`)
> - **Archivo Markdown** — ingresa el nombre del archivo `.md` (se buscará en `resources/functional/reqs/`)

Si el usuario escribe solo un nombre de archivo (ej. `mi-epica.md` o `mi-epica`), asume la ruta `resources/functional/reqs/<nombre>.md`. Solo usa una ruta distinta si el usuario la escribe explícitamente con `/` o `\`.

Espera la respuesta antes de continuar. Si el usuario ya proporcionó uno de los dos en su mensaje inicial, úsalo directamente sin preguntar.

---

## Paso 1 — Obtener la épica

### Opción A: desde Jira

Usa el MCP de Jira para leer la épica. Busca la herramienta correcta según lo disponible:

```
// Herramientas comunes del MCP de Jira (usa la que esté disponible):
// - get_issue / jira_get_issue
// - search_issues con JQL: "key = EPIC-KEY"
// - get_epic
```

**Qué extraer de la épica:**
- Título / Summary
- Descripción completa
- Labels / componentes
- Sprint o Fix Version asignados
- Issues hijos ya existentes (para no duplicar)
- Campos personalizados relevantes (Story Points, Team, etc.)

### Opción B: desde archivo Markdown

Lee el archivo en `resources/functional/reqs/<nombre>.md` (o la ruta exacta si el usuario la especificó). Extrae de su contenido:
- Título de la épica (primer encabezado `#` o campo `title` en frontmatter)
- Descripción / contexto de negocio
- Roles de usuario mencionados
- Criterios de éxito o restricciones indicadas
- Cualquier listado de funcionalidades o alcance definido

Si el archivo tiene frontmatter YAML, úsalo como fuente principal de metadatos. Si la descripción es muy escueta, aplica el protocolo de épicas ambiguas del Paso 2.

---

## Paso 2 — Verificar ambigüedades

Antes de analizar el alcance, escanea la épica en busca de definiciones incompletas o imprecisas. Clasifícalas en estas categorías:

### 2.1 — Tecnologías sin versión

Detecta cualquier mención de lenguajes, frameworks, librerías, plataformas o servicios sin versión explícita. Ejemplos de señales de alerta:

| Mención ambigua | Pregunta a hacer |
|---|---|
| "Java" | ¿Qué versión de Java? (8, 11, 17, 21…) |
| "Spring Boot" | ¿Qué versión de Spring Boot? |
| "React" | ¿Qué versión de React? (17, 18, 19…) |
| "Node.js" | ¿Qué versión de Node.js? |
| "Python" | ¿Qué versión de Python? (3.10, 3.12…) |
| ".NET" | ¿Qué versión de .NET? (6, 8, 9…) |
| "Angular" | ¿Qué versión de Angular? |
| "PostgreSQL / MySQL" | ¿Qué versión del motor de base de datos? |
| "Docker" | ¿Hay restricción de versión de imagen base? |
| "Kubernetes" | ¿Qué versión del clúster objetivo? |

Aplica el mismo criterio a cualquier otra tecnología mencionada aunque no aparezca en esta tabla.

### 2.2 — Otros campos ambiguos

Además de versiones, detecta:

- **Rendimiento sin métrica:** "debe ser rápido", "baja latencia" → pedir umbral concreto (ej. p95 < 300 ms)
- **Escala sin número:** "soportar muchos usuarios", "alta concurrencia" → pedir cifra estimada
- **Seguridad genérica:** "debe ser seguro", "con autenticación" → ¿qué mecanismo? (JWT, OAuth2, SAML…) ¿qué estándar?
- **Integraciones sin endpoint:** "se conecta con el sistema X" → ¿REST, SOAP, evento? ¿hay contrato disponible?
- **Roles sin definir:** "el usuario admin puede…" → ¿ya existe ese rol en el sistema o hay que crearlo?
- **Criterios de éxito ausentes:** si la épica no tiene ningún criterio medible de "done", señalarlo.

### 2.3 — Presentar hallazgos y preguntar

Si se encontraron ambigüedades, preséntalas de forma clara antes de continuar:

```
⚠️ Encontré las siguientes definiciones incompletas que pueden afectar el desglose:

1. [Tecnología/concepto]: [descripción del problema]
   → Pregunta: [pregunta específica]

2. ...

¿Puedes aclarar estos puntos antes de que genere las historias?
(Si prefieres, puedo continuar con supuestos explícitos.)
```

Agrupa las preguntas en un solo bloque — máximo 5 por ronda. Si el usuario elige continuar con supuestos, documenta cada supuesto al inicio del desglose con el prefijo `[SUPUESTO]`.

Si **no** se encontraron ambigüedades, avanza directamente al Paso 3 sin comentarlo.

---

## Paso 3 — Analizar el alcance

Antes de generar las historias, razona internamente sobre:

1. **¿Cuál es el valor de negocio central de la épica?**
2. **¿Qué tipo de usuarios se benefician y cómo?**
3. **¿Qué partes son funcionalidad de producto vs. trabajo técnico?**
4. **¿Existen dependencias o precondiciones técnicas?**
5. **¿Hay criterios de aceptación implícitos en la descripción?**
6. **¿La épica define o insinúa entidades/recursos de datos?** Para cada HU o TT que implique crear, modificar o exponer una entidad (CRUD, formularios, endpoints), identifica los campos, tipos y relaciones que la épica ya menciona explícitamente. Esto alimenta la sección opcional "Recurso de datos involucrado" del Paso 4 — no inventes campos que la épica no sustente; si un dato es necesario pero no está definido, márcalo como `No especificado en la épica — definir con negocio` en vez de asumirlo.

Este análisis determina cómo dividir el trabajo. Consulta `references/breakdown-guide.md` para heurísticas detalladas.

---

## Paso 4 — Generar el desglose

### Estructura de salida esperada

```
📋 ÉPICA: [CLAVE] — [Título]

## 🧩 Historias de Usuario  (N historias)

### HU-01: [Título corto]
**Como** [rol de usuario]
**Quiero** [acción/funcionalidad]
**Para** [beneficio/objetivo]

**Criterios de Aceptación:**
- [ ] CA1: ...
- [ ] CA2: ...
- [ ] CA3: ...

**Recurso de datos involucrado** *(incluir solo si la historia crea, modifica o expone una entidad/recurso; omitir todo este bloque si no aplica — ej. historias de UI pura, configuración o navegación)*
- **Nombre del recurso:** NombreDelRecurso
- **Capa(s):** backend / frontend / ambas

**Campos del recurso:**
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| ... | ... | ... | ... |

**Relaciones con otros recursos:**
- `NombreEntidad` (cardinalidad): descripción de la relación

**Story Points estimados:** [1 / 2 / 3 / 5 / 8 / 13]
**Prioridad sugerida:** [Alta / Media / Baja]

---

## ⚙️ Tareas Técnicas  (N tareas)

### TT-01: [Título]
**Descripción:** [Qué hay que hacer y por qué]
**Criterios de Done:**
- [ ] ...

**Recurso de datos involucrado** *(incluir solo si la tarea crea o modifica un esquema/entidad — ej. migración de BD, endpoint CRUD base; omitir si no aplica)*
- **Nombre del recurso:** NombreDelRecurso

**Campos del recurso:**
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| ... | ... | ... | ... |

**Dependencias:** [Lista de HU o TT que deben completarse antes]
**Story Points estimados:** [...]

---

## 🔩 Subtareas sugeridas

### Para [HU-01 o TT-01]:
- Subtarea: [descripción breve]
- Subtarea: [descripción breve]
```

---

## Paso 5 — Elegir destino de salida

Tras presentar el desglose completo, pregunta al usuario:

> **¿Cómo deseas guardar estas historias?**
> 1. **Subir a Jira** — crear los issues directamente en Jira usando el MCP
> 2. **Guardar como archivos Markdown** — crear un `.md` por historia en `resources/functional/hu/`
> 3. **Ambas opciones** — subir a Jira y crear los archivos Markdown

Espera la respuesta antes de continuar.

---

## Paso 5a — Subir a Jira

Si el usuario elige opción 1 o 3, pregunta antes de crear:
1. ¿En qué proyecto deben crearse? (si no es el mismo de la épica)
2. ¿Quiere asignar Assignee desde ahora o dejarlos sin asignar?
3. ¿Debe vincular los issues a la épica original?

Luego usa el MCP de Jira para crear cada issue. Herramientas comunes:
```
// create_issue / jira_create_issue
{
  "project": "PROJ",
  "summary": "...",
  "description": "...",
  "issuetype": "Story" | "Task" | "Sub-task",
  "parent": "EPIC-KEY",   // para vincular a la épica
  "customfield_10016": 5  // Story Points (campo puede variar)
}
```

**Orden de creación:** Primero tareas técnicas de infraestructura/setup, luego historias de usuario en orden de prioridad, finalmente subtareas vinculadas a su padre.

Reporta al usuario los links de cada issue creado.

---

## Paso 5b — Guardar como archivos Markdown

Si el usuario elige opción 2 o 3, crea un archivo `.md` por cada historia de usuario y tarea técnica en la carpeta `resources/functional/hu/`.

### Nombre de archivo

Usa el slug del título en kebab-case:
```
resources/functional/hu/hu-01-titulo-corto.md
resources/functional/hu/tt-01-titulo-corto.md
```

### Estructura de cada archivo

```markdown
---
id: HU-01
type: Historia de Usuario | Tarea Técnica
epic: [CLAVE-ÉPICA]
priority: Alta | Media | Baja
points: [1/2/3/5/8/13]
---

# HU-01: [Título corto]

## Como
[rol de usuario]

## Quiero
[acción/funcionalidad]

## Para
[beneficio/objetivo]

## Criterios de Aceptación
- [ ] CA1: ...
- [ ] CA2: ...
- [ ] CA3: ...

## Recurso de datos involucrado
<!-- Incluir esta sección y sus subsecciones solo si la historia/tarea crea, modifica o expone una entidad; eliminar toda la sección si no aplica (ej. UI pura, configuración, navegación). No inventar campos que la épica no sustente: usar "No especificado en la épica — definir con negocio" cuando falte el dato. -->

### Recurso
- **Nombre:** NombreDelRecurso
- **Capa(s):** backend / frontend / ambas

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| ... | ... | ... | ... |

### Relaciones con otros recursos
- `NombreEntidad` (cardinalidad): descripción de la relación

## Subtareas
- [ ] [descripción breve]
- [ ] [descripción breve]
```

Crea la carpeta `resources/functional/hu/` si no existe. Al finalizar, lista los archivos creados con sus rutas relativas.

---

## Reglas de calidad

- **Historias de usuario:** Deben ser independientes, estimables, pequeñas (completable en 1 sprint), valiosas para el usuario y verificables (criterio INVEST).
- **Tareas técnicas:** No mezclar con historias de usuario. Son habilitadores técnicos (setup CI/CD, migración BD, crear API base, etc.).
- **Subtareas:** Solo para issues > 5 Story Points que se pueden dividir lógicamente. Máximo 5 subtareas por issue.
- **No duplicar:** Verificar siempre los issues hijos ya existentes en la épica antes de proponer nuevos.
- **Idioma:** Generar siempre los issues en español, sin importar el idioma en que esté escrita la épica original.
- **Recurso de datos involucrado:** Completar esta sección solo con información que la épica sustente explícita o implícitamente. No inventar campos, tipos ni relaciones — si un dato es necesario para el scaffold pero la épica no lo define, escribir `No especificado en la épica — definir con negocio` en vez de asumirlo. Esta sección existe para que `builder` pueda generar el scaffold del recurso sin tener que re-preguntar lo que ya se resolvió en el desglose.

---

## Manejo de épicas incompletas

Si la descripción de la épica es muy escueta o ambigua:
1. Informa al usuario qué información falta.
2. Haz preguntas específicas para completar el análisis (máximo 3 preguntas a la vez).
3. Genera un borrador preliminar con los supuestos que hagas explícitos.

Consulta `references/breakdown-guide.md` → sección "Épicas ambiguas" para más detalles.
