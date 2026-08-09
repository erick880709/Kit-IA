---
name: builder
description: >
  Genera el scaffold completo de un nuevo módulo de dominio (CRUD tradicional
  o pipeline de Machine Learning/IA) para cualquier proyecto, en cualquier
  lenguaje y stack, con patrones de nivel senior. Cubre backend (Java/Spring Boot,
  C#/.NET, Python/FastAPI/Django, Node.js/Express/NestJS) y frontend (Angular 18+,
  React/Next.js, Vue). Recibe como entrada un ID de historia de usuario o tarea
  técnica de Jira, un ID de Épica de Jira (en cuyo caso resuelve y recorre
  todas sus historias hijas), o la ruta a un archivo Markdown en
  resources/functional/hu/. Detecta automáticamente el lenguaje, framework,
  ORM y patrón arquitectónico del proyecto — o, si el recurso es de tipo
  Machine Learning/IA, el stack de ciencia de datos (pandas, scikit-learn,
  XGBoost, TensorFlow/PyTorch, notebooks). Si no existe línea base de
  arquitectura ni de requerimientos (ni documentación en resources/architecture,
  resources/architecture/definitions, resources/design/models ni
  resources/design), y el proyecto es realmente greenfield (sin codebase que
  analizar), aprovisiona la línea base invocando primero `janus` (requerimientos
  RNF/RT/RD) y luego `archi` (arquitectura/línea base) antes de generar nada.
  Si sí existe codebase, analiza el codebase y crea la documentación. Luego
  genera el scaffold respetando los patrones reales del proyecto, aplicando
  guías de referencia para cada stack con buenas prácticas de nivel senior
  (Clean Architecture, testing, manejo de errores, seguridad, performance).
---

# Skill: Scaffold de Módulo — Agnóstico de Stack (Nivel Senior)

Genera un módulo completo siguiendo los patrones arquitectónicos y el lenguaje
reales del proyecto. Opera en cuatro fases secuenciales: resolución de entrada,
descubrimiento de arquitectura, análisis del recurso y generación.

La skill **no asume ningún lenguaje ni framework**. Todo lo que genera deriva
del análisis del codebase y del requerimiento funcional provisto, nunca de
suposiciones externas. Para cada stack detectado, aplica las guías de referencia
con patrones de nivel senior (Clean Architecture, CQRS, TDD, Domain-Driven Design,
manejo de errores tipado, validación declarativa, observabilidad).

---

## Guías de referencia por stack

Antes de generar código para un stack específico, carga la guía correspondiente
de `references/` como fuente de convenciones, anti-patrones y checklist de
calidad. Estas guías cubren lo que la detección automática (FASE 0) no puede
inferir de un codebase existente: patrones de diseño, estructura de carpetas
ideal, testing, Dockerfile y stack recomendado.

| Stack detectado | Guía de referencia |
|---|---|
| **Java + Spring Boot** | `references/guia-backend-java-spring.md` |
| **C# / .NET** | `references/guia-backend-csharp-dotnet.md` |
| **Python + FastAPI/Django/Flask** | `references/guia-backend-python.md` |
| **Node.js + Express/Fastify/NestJS** | `references/guia-backend-nodejs.md` |
| **Angular 17+ (frontend)** | `references/guia-frontend-angular.md` |
| **Machine Learning / IA** | `references/guia-notebooks-python.md` (local) + `archi/references/guia-ml-arquitectura.md` |

Para frontend React/Next.js, el skill `qa` tiene patrones de testing E2E
(Playwright) — `builder` genera componentes, servicios y hooks siguiendo las
convenciones detectadas en el codebase.

Si el proyecto es greenfield (sin codebase de referencia), la guía correspondiente
se usa como **fuente de verdad** para estructura de carpetas, convenciones y stack recomendado.

---

## FASE E — RESOLUCIÓN DE ENTRADA

Esta es la primera fase. Antes de analizar el codebase, resolver la fuente
de requerimientos del módulo a construir.

### E.1 Determinar la fuente de entrada

El usuario invoca la skill con uno de estos formatos:

```
/builder PROJ-123                              (historia o tarea individual)
/builder PROJ-100                               (épica → recorre sus HUs hijas, ver §E.2bis)
/builder resources/functional/hu/nombre-del-archivo.md
```

Si el usuario no proveyó ningún argumento, preguntar:

> ¿Cuál es la fuente de requerimientos? Puedes indicar:
> - Un ID de Jira de una historia/tarea (ej: `PROJ-123`)
> - Un ID de Jira de una épica, para desarrollar todas sus historias (ej: `PROJ-100`)
> - La ruta a un archivo en `resources/functional/hu/` (ej: `hu-crear-proveedor.md`)

---

### E.2 Entrada desde Jira

Si el input es un ID de Jira (patrón `[A-Z]+-[0-9]+`):

1. **Leer el issue** usando las herramientas MCP de Jira disponibles en la
   sesión. Buscar herramientas con nombres como `get_issue`, `jira_get_issue`,
   `mcp__jira__get_issue` o similares según lo que esté disponible.

2. **Determinar el tipo de issue (`issuetype`) antes de extraer campos** —
   el flujo se bifurca entre Épica y HU/Tarea:

   - **Si `issuetype` es `Epic`:** este issue no se scaffoldea directamente
     (una épica no es un recurso único). Sigue §E.2bis para resolver sus
     historias hijas.
   - **Si `issuetype` es `Story`, `Task` o `Sub-task`:** continúa con el
     resto de §E.2 normalmente.

3. **Extraer del issue** los siguientes campos:

   | Campo Jira | Qué extraer |
   |---|---|
   | `summary` / título | Nombre del recurso a crear |
   | `description` | Descripción funcional, campos del recurso, reglas de negocio |
   | Criterios de aceptación | Restricciones, validaciones, casos borde |
   | `components` / etiquetas | Capa afectada (backend, frontend, ambas) |
   | Subtareas | Si tiene subtareas técnicas, usarlas para entender el alcance |
   | `issuetype` | Historia de usuario (`Story`) o tarea técnica (`Task`) |

4. **Si es una historia de usuario (`Story`):** extraer el recurso y sus
   reglas de negocio desde la descripción y los criterios de aceptación.

5. **Si es una tarea técnica (`Task` o `Sub-task`):** leer además la historia
   padre para obtener el contexto funcional completo.

6. **Guardar el issue leído** en `resources/functional/hu/` como archivo
   Markdown usando el ID como nombre de archivo (`PROJ-123.md`), con la
   estructura definida en §E.4. Esto permite reutilizarlo en el futuro sin
   volver a consultar Jira.

---

### E.2bis Entrada desde una Épica de Jira (recorrido de HUs hijas)

Cuando el ID resuelto en §E.2 es una `Epic`, el objetivo no es generar un
único recurso sino **recorrer y desarrollar cada punto de la épica**.

1. **Listar las historias hijas.** Usa la herramienta MCP de Jira disponible
   para buscar issues cuyo `Epic Link` (o campo equivalente, p. ej.
   `parent` en proyectos next-gen) apunte a esta épica — herramientas
   típicas: `search_issues`, `jira_search`, `mcp__jira__search` con una
   JQL del estilo `"Epic Link" = PROJ-100` o `parent = PROJ-100`. Si el
   servidor MCP expone una herramienta específica para hijos de épica
   (`get_epic_children` o similar), prefiérela sobre construir la JQL a mano.

2. **Mostrar el plan de desarrollo antes de tocar nada:**

   ```
   Épica resuelta: PROJ-100 — [título de la épica]
   Historias hijas encontradas (N):
     1. PROJ-101 — [título]     [Story]  → backend + frontend
     2. PROJ-102 — [título]     [Story]  → backend
     3. PROJ-103 — [título]     [Task]   → ML: entrenamiento de modelo
     ...

   ¿Genero el scaffold de todas en orden, o prefieres indicarme cuáles
   (o en qué orden)?
   ```

   No asumas "todas, en el orden que las devolvió Jira" sin confirmación —
   el orden puede importar (p. ej. una HU que crea una entidad de la que
   otra depende, o en un proyecto de ML: primero el pipeline de datos, luego
   el de entrenamiento). Si el usuario no tiene preferencia, ordénalas
   respetando dependencias obvias entre recursos (una HU que menciona una
   entidad ya creada por otra HU de la misma épica va después) y, si el
   proyecto tiene componente ML, con el pipeline de datos antes que el de
   entrenamiento y este antes que el de servicio/inferencia (ver §1.2bis).

3. **Ejecutar el resto del skill (Fase -1 en adelante) una vez por cada HU
   hija confirmada, en el orden acordado**, guardando cada una en
   `resources/functional/hu/` (§E.2 paso 6) según se van resolviendo — así
   una corrida interrumpida puede reanudarse sin perder lo ya procesado.
   Antes de generar la HU N+1, verifica rápidamente si algo de lo generado
   en la HU N cambia el contexto de arquitectura (nueva entidad, nuevo
   endpoint) relevante para la siguiente — no repitas todo el descubrimiento
   de la Fase 0, solo confirma que sigue vigente.

4. **Al terminar todas las HUs de la épica**, muestra un resumen consolidado
   (una fila por HU: recurso generado, capas, estado del checklist) en vez
   de solo el checklist de la última HU procesada.

5. Si la épica no tiene historias hijas encontrables, informa al usuario en
   vez de continuar — puede que estén sin vincular en Jira o que la épica
   use un campo de vinculación no estándar; pide confirmación de cómo están
   relacionadas antes de asumir que la épica está vacía.

---

### E.3 Entrada desde archivo Markdown

Si el input es una ruta a un archivo Markdown:

1. Verificar que el archivo existe en `resources/functional/hu/`.
2. Si no existe, informar al usuario y detener la ejecución.
3. Leer el archivo y extraer los datos según la estructura del §E.4.

---

### E.4 Estructura esperada del archivo Markdown de HU

Los archivos en `resources/functional/hu/` deben seguir esta estructura.
La skill la usa para extraer información y también la produce cuando guarda
un issue de Jira.

```markdown
# [ID] Título del recurso / historia

## Descripción funcional
<!-- Qué necesita el negocio. Como [actor], quiero [acción], para [beneficio]. -->

## Recurso a crear
- **Nombre:** NombreDelRecurso (en el naming convention del proyecto)
- **Capa(s):** backend / frontend / ambas
- **Tipo de recurso:** CRUD tradicional / Pipeline de Machine Learning-IA
  <!-- Si no está explícito, infiérelo por el contenido (ver §1.2bis) -->

## Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| nombre | string | sí | Mínimo 3 caracteres |
| ... | | | |

## Relaciones con otros recursos
- `NombreEntidad` (cardinalidad): descripción de la relación

## Reglas de negocio
- Regla 1: descripción
- Regla 2: descripción

## Criterios de aceptación
- [ ] Criterio 1
- [ ] Criterio 2

## Notas técnicas (opcional)
<!-- Restricciones de implementación, decisiones técnicas previas, etc. -->
```

Si el archivo tiene una estructura diferente (distinto orden, secciones con
otros nombres, formato libre), extraer igualmente la información por
interpretación semántica. No rechazar el archivo por formato inesperado.

Para historias/tareas de tipo **Pipeline de Machine Learning-IA**, "Campos
del recurso" no siempre aplica igual que en un CRUD (puede no haber una
entidad con columnas) — en su lugar, extrae de la descripción y criterios de
aceptación lo que §1.2bis necesita: qué etapa del pipeline es (datos,
entrenamiento, evaluación, servicio/inferencia), qué fuente(s) de datos usa,
qué métrica(s) objetivo debe cumplir, y si requiere explicabilidad. No
inventes estos datos si la HU no los trae — pasan a §1.3 como ambigüedad a
confirmar con el usuario, igual que un campo sin tipo definido en un CRUD.

---

### E.5 Resultado de la Fase E

Al finalizar esta fase, tener resueltos:

- **Nombre del recurso** (crudo, para derivar variantes en FASE 1)
- **Lista de campos** con tipo y restricciones
- **Relaciones** con entidades existentes
- **Reglas de negocio** que el dominio debe capturar
- **Capa(s) a generar** (backend, frontend o ambas)
- **Criterios de aceptación** para guiar la generación y el checklist final

Mostrar un resumen al usuario antes de continuar:

```
Requerimiento resuelto:
  Fuente:   PROJ-123 / resources/functional/hu/archivo.md
  Recurso:  NombreDelRecurso
  Campos:   campo1 (tipo), campo2 (tipo), ...
  Capas:    backend + frontend
  Reglas:   [N reglas de negocio identificadas]

Continuando con el descubrimiento de arquitectura...
```

---

## FASE -1 — VERIFICAR Y APROVISIONAR LA LÍNEA BASE (`archi` / `janus`)

Antes de intentar descubrir la arquitectura por tu cuenta (FASE 0), verifica
si la línea base de requerimientos y arquitectura ya fue definida por las
skills responsables de producirla — `builder` **no** debe reinventar
decisiones de arquitectura ni de requerimientos que le corresponden a
`archi` (arquitectura) y `janus` (requerimientos no funcionales/técnicos y
modelo de datos de negocio). Este paso corre una vez por proyecto, no una
vez por HU.

### -1.1 Verificar qué línea base existe

Revisa estas cuatro rutas (relativas a la raíz del proyecto):

| Ruta | La produce | Contiene |
|---|---|---|
| `resources/architecture/definitions/` | `janus` | RNF-###/RT-### (requerimientos no funcionales y técnicos) |
| `resources/design/models/` | `janus` | RD-### (modelo de datos/dominio de negocio) |
| `resources/architecture/` (`overview.md`, `stack.md`, o un `Documento_Arquitectura_*.md`) | `archi` (o `builder` mismo, ver §0.3) | Stack, patrón arquitectónico, decisiones de nube/despliegue |
| `resources/design/` (`data-model.md`, `api.md`, `openapi.yaml`) | `archi`/`builder` | Contrato de API y modelo de datos ya materializados |

### -1.2 Decidir si hace falta aprovisionar

- **Si hay codebase real** (el repositorio tiene código funcional, aunque
  falte documentación): no aprovisiones nada aquí. Falta de documentación
  con código existente se resuelve reverse-engineering el código en §0.2/0.3
  como ya hace este skill — no tiene sentido invocar `archi`/`janus` para
  inventar requerimientos de un sistema que ya está construido.
- **Si el proyecto es realmente greenfield** (repositorio vacío o solo
  scaffold inicial, sin módulos implementados) **y** además
  `resources/architecture/definitions/`, `resources/design/models/` y
  `resources/architecture/` están vacíos o no existen: no hay nada de qué
  partir. Este es el caso a resolver en §-1.3 — típicamente un proyecto
  nuevo (incluyendo uno de Machine Learning/IA, ej. un TFM o una tesis que
  arranca desde cero) donde builder es la primera skill que se invoca sin
  haber corrido antes `janus`/`archi`.
- **Si hay una mezcla** (p. ej. `resources/architecture/` tiene contenido
  pero `resources/design/models/` está vacío, o viceversa): aprovisiona
  solo lo que falta, no regeneres lo que ya existe.

### -1.3 Aprovisionar invocando `janus` y luego `archi`

Cuando §-1.2 determina que hace falta aprovisionar:

1. **Informa al usuario antes de proceder**, no lo hagas en silencio:

   ```
   No encontré línea base de requerimientos ni de arquitectura para este
   proyecto (resources/architecture y resources/design están vacíos o no
   existen), y el repositorio no tiene código para inferirla.

   Antes de generar el scaffold de <recurso>, voy a aprovisionar la línea
   base:
     1. janus  → requerimientos no funcionales/técnicos y modelo de datos
     2. archi  → documento de arquitectura (usando la línea base de janus
                 y, si falta algo, el cuestionario de línea base de archi)

   ¿Continúo?
   ```

2. **Invoca `janus`** primero (si esa skill está disponible en la sesión) con
   el mismo `.md` de especificaciones o la épica/HU de origen que disparó a
   `builder` — `janus` es quien produce los `RNF-###`/`RT-###` en
   `resources/architecture/definitions/` y los `RD-###` en
   `resources/design/models/`. Si `janus` no está disponible como skill
   invocable en el entorno actual, no la simules: dile al usuario que instale
   o habilite `janus`, o pídele directamente las respuestas al bloque de
   preguntas que `janus` normalmente resolvería (usa como referencia los
   bloques 1-11 de `cuestionario-linea-base.md` de `archi`, que cubren el
   mismo tipo de preguntas de negocio/stack/nube/datos/seguridad).
3. **Invoca `archi`** a continuación, con la salida de `janus` ya disponible
   — `archi` la usará como fuente de verdad en su propio Paso 0.5 (línea
   base) en vez de volver a preguntar lo que `janus` ya resolvió. Si el
   proyecto tiene componente de Machine Learning/IA (ver §1.2bis), confirma
   que `archi` active su modo ML (produce `guia-ml-arquitectura.md` y usa
   `plantilla-documento-arquitectura-ml.md`) para que la línea base cubra
   también pipeline de datos, entrenamiento, métricas objetivo y gobernanza
   — sin esto, `builder` no tiene de dónde tomar las convenciones de
   estructura de un módulo ML (ver §2.1 "Pipeline de Machine Learning").
   Si `archi` tampoco está disponible como skill invocable, informa al
   usuario y ofrece continuar solo con lo que él mismo pueda confirmarte
   manualmente (documentado igual como supuesto en Notas Técnicas de la HU),
   dejando explícito que la línea base no fue validada por `archi`.
4. **Solo después de que exista al menos**: el stack tecnológico definido
   (por `archi` o por el usuario) y, si aplica, el modo ML activo con sus
   métricas objetivo — continúa a FASE 0. FASE 0 ahora encontrará contenido
   real en `resources/architecture/` y podrá saltar directo a FASE 1 (ver
   §0.1) en vez de intentar inferir de un codebase que no existe.
5. Si el usuario prefiere no aprovisionar la línea base y pide "generar
   igual" sobre supuestos propios, respeta la decisión pero dilo
   explícitamente en el resumen de la Fase E y en "Notas técnicas" del
   archivo de HU guardado — no dejes que parezca que la línea base fue
   validada cuando en realidad se saltó a pedido del usuario.

---

## FASE 0 — DESCUBRIMIENTO DE ARQUITECTURA

### 0.1 Verificar recursos existentes

Buscar en este orden:

```
resources/
  design/           → Diagramas ER, C4, modelo de entidades, API contracts
    openapi.yaml    → Contrato de API vivo y acumulado (ver §1.6) — léelo
                       completo si existe, es la fuente de verdad de todos
                       los endpoints/schemas ya registrados por corridas
                       anteriores de este skill (o inicializado por `genesis`)
  architecture/     → Stack, patrón arquitectónico, convenciones
```

**Si ambas carpetas existen y tienen contenido relevante:** leerlas y usarlas
como fuente de verdad. Saltar a la FASE 1.

**Si falta alguna carpeta o está vacía:** esto ya fue evaluado en FASE -1.
Si llegaste aquí es porque, o bien hay codebase real del que inferir (sigue
con §0.2 y §0.3 normalmente), o bien el usuario decidió explícitamente
generar sobre supuestos propios sin aprovisionar la línea base (§-1.3 paso
5) — en ese caso, sigue también §0.2/§0.3 pero documentando cada supuesto.

---

### 0.2 Detección del ecosistema (análisis del codebase)

Ejecutar los análisis A–F en paralelo.

---

#### A. Detección del lenguaje principal

Buscar los archivos de manifiesto o configuración que identifican el ecosistema.
Verificar en la raíz y en subdirectorios de paquetes:

| Archivo encontrado | Lenguaje / Ecosistema |
|---|---|
| `pom.xml` | Java / Kotlin (Maven) |
| `build.gradle`, `build.gradle.kts` | Java / Kotlin / Groovy (Gradle) |
| `*.csproj`, `*.sln`, `global.json` | C# / F# (.NET) |
| `pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py` | Python |
| `go.mod`, `go.sum` | Go |
| `Gemfile`, `Gemfile.lock` | Ruby |
| `composer.json`, `composer.lock` | PHP |
| `package.json` | JavaScript / TypeScript (Node.js o frontend) |
| `Cargo.toml` | Rust |
| `mix.exs` | Elixir |
| `pubspec.yaml` | Dart / Flutter |
| `build.sbt` | Scala |

Si hay `package.json`, distinguir entre Node.js (backend) y framework frontend
leyendo el campo `main`, `scripts.start`, y dependencias clave.

Si hay varios lenguajes (monorepo polígota), documentar cada paquete por separado.

---

#### B. Detección del framework y stack por ecosistema

Leer el archivo de manifiesto del lenguaje detectado y buscar las dependencias:

**Java / Kotlin**

| Dependencia / Plugin | Framework |
|---|---|
| `spring-boot-starter-web` | Spring Boot (MVC) |
| `spring-boot-starter-webflux` | Spring WebFlux (reactivo) |
| `quarkus-resteasy` | Quarkus |
| `io.micronaut` | Micronaut |
| `spring-data-jpa`, `hibernate` | JPA / Hibernate (ORM) |
| `spring-data-r2dbc` | R2DBC (reactivo) |
| `jooq` | jOOQ |
| `mybatis` | MyBatis |
| `liquibase`, `flyway` | Migraciones DB |
| `spring-security` | Seguridad |
| `lombok` | Lombok |
| `mapstruct` | MapStruct |

**C# / .NET**

| Dependencia / Paquete NuGet | Framework |
|---|---|
| `Microsoft.AspNetCore.Mvc` | ASP.NET Core MVC |
| `Microsoft.AspNetCore.OpenApi` | Minimal API |
| `Microsoft.EntityFrameworkCore` | Entity Framework Core |
| `Dapper` | Dapper |
| `MediatR` | CQRS con MediatR |
| `FluentValidation` | Validación |
| `AutoMapper` | Mapeo de objetos |
| `Serilog`, `NLog` | Logging |

**Python**

| Dependencia | Framework |
|---|---|
| `django` | Django |
| `djangorestframework` | Django REST Framework |
| `fastapi` | FastAPI |
| `flask` | Flask |
| `sqlalchemy` | SQLAlchemy (ORM) |
| `tortoise-orm` | Tortoise ORM |
| `pydantic` | Validación (FastAPI) |
| `marshmallow` | Serialización (Flask) |
| `alembic` | Migraciones |
| `celery` | Tareas asíncronas |

**Go**

| Import / Módulo | Framework |
|---|---|
| `github.com/gin-gonic/gin` | Gin |
| `github.com/labstack/echo` | Echo |
| `github.com/go-chi/chi` | Chi |
| `github.com/gofiber/fiber` | Fiber |
| `gorm.io/gorm` | GORM |
| `github.com/jmoiron/sqlx` | sqlx |
| `database/sql` | stdlib SQL |
| `github.com/golang-migrate` | Migraciones |

**Ruby**

| Gem | Framework |
|---|---|
| `rails` | Ruby on Rails |
| `sinatra` | Sinatra |
| `grape` | Grape API |
| `active_record` | ActiveRecord ORM |
| `sequel` | Sequel |
| `dry-rb` | Dry::RB (arquitectura funcional) |

**PHP**

| Dependencia composer | Framework |
|---|---|
| `laravel/framework` | Laravel |
| `symfony/framework-bundle` | Symfony |
| `slim/slim` | Slim |
| `doctrine/orm` | Doctrine ORM |
| `doctrine/dbal` | Doctrine DBAL |
| `illuminate/database` | Eloquent (Laravel) |

**JavaScript / TypeScript (Node.js backend)**

| Dependencia npm | Framework |
|---|---|
| `express` | Express |
| `fastify` | Fastify |
| `@nestjs/core` | NestJS |
| `hono` | Hono |
| `koa` | Koa |
| `prisma` | Prisma ORM |
| `typeorm` | TypeORM |
| `drizzle-orm` | Drizzle |
| `mongoose` | Mongoose (MongoDB) |
| `zod` | Validación Zod |
| `class-validator` | Validación NestJS |

**JavaScript / TypeScript (Frontend)**

| Dependencia npm | Framework |
|---|---|
| `react` | React |
| `@angular/core` | Angular |
| `vue` | Vue.js |
| `svelte` | Svelte |
| `solid-js` | SolidJS |
| `@tanstack/react-query` | TanStack Query |
| `swr` | SWR |
| `zustand`, `pinia` | Estado global |
| `react-hook-form` | Formularios React |
| `@angular/forms` | Formularios Angular |

**Machine Learning / Ciencia de Datos (independiente del framework web — puede
coexistir con Python/FastAPI o Django si el proyecto sirve el modelo vía API)**

Revisa esta tabla siempre que el manifiesto sea Python (`requirements.txt`,
`pyproject.toml`) — no asumas que un proyecto Python es solo un backend web:
comprueba primero si trae estas dependencias, porque cambian por completo el
patrón de generación (§2.1 "Pipeline de Machine Learning", no CRUD).

| Dependencia | Rol |
|---|---|
| `pandas`, `numpy` | Manipulación de datos |
| `scikit-learn` | Modelos clásicos, pipelines de preprocesamiento, métricas |
| `xgboost`, `lightgbm`, `catboost` | Gradient boosting |
| `imbalanced-learn` | Balanceo de clases (SMOTE y variantes) |
| `tensorflow`, `keras` | Deep learning |
| `torch` | Deep learning (PyTorch) |
| `transformers` | Modelos preentrenados tipo BERT (NLP) |
| `shap` | Explicabilidad (XAI) |
| `mlflow` | Tracking de experimentos y registro de modelos |
| `dvc` | Versionado de datos y pipelines |
| Carpeta `notebooks/` con archivos `.ipynb` | Señal fuerte de proyecto con componente de ML, aunque el manifiesto no lo deje claro por sí solo |

Si detectas cualquiera de estas dependencias (o la carpeta `notebooks/`),
activa el **modo ML** para este proyecto: en §0.2 C usa la estructura de
carpetas de `references/guia-notebooks-python.md`/`guia-ml-arquitectura.md`
de `archi` (si `resources/architecture/` ya las referencia) como patrón
esperado, y en §0.2 D busca un pipeline existente en vez de un CRUD (ver
abajo). Si el proyecto mezcla ambos (una API web que sirve un modelo ML),
documenta las dos detecciones por separado — no son excluyentes.

---

#### C. Detección del patrón arquitectónico

Inspeccionar la estructura de directorios del paquete backend / principal.
Buscar los nombres de carpeta más representativos:

| Estructura de carpetas encontrada | Patrón arquitectónico |
|---|---|
| `domain/`, `application/`, `infrastructure/` | Hexagonal / Ports & Adapters |
| `domain/`, `application/`, `infrastructure/`, `presentation/` | Clean Architecture |
| `controllers/` + `services/` + `repositories/` | Layered / N-Tier |
| `modules/` con subcarpetas propias (NestJS, Spring Modular) | Modular |
| `features/` o `slices/` por feature | Feature-based / Vertical Slice |
| `handlers/`, `commands/`, `queries/` | CQRS |
| Estructura Rails/Django plana (`models/`, `views/`, `controllers/`) | MVC convencional |
| `data/`, `notebooks/`, `src/{data,features,models,evaluation}/` | Pipeline de Machine Learning / Ciencia de Datos (ver §2.1) |
| `src/` plana sin subcarpetas específicas | Sin patrón explícito — detectar por archivos |

Para Java/Spring: buscar además el uso de `@Service`, `@Repository`,
`@Component` vs. interfaces de puerto y sus implementaciones.

Para .NET: buscar carpetas `Commands/`, `Queries/` (CQRS con MediatR) o
`Application/`, `Domain/`, `Infrastructure/` (Clean Architecture).

---

#### D. Módulo de referencia

**Este es el paso más importante de la fase de análisis.**

Si el modo ML **no** está activo, buscar en el proyecto un módulo CRUD
existente y completo para usarlo como plantilla viva. Criterios de búsqueda:

1. Buscar un controlador o handler que tenga al menos GET (lista), GET (por ID),
   POST (crear), PUT/PATCH (actualizar) y DELETE.
2. Preferir el módulo más completo y representativo (no un ejemplo simplificado).
3. Leer todos sus archivos: entidad, repositorio, servicio/caso de uso,
   controlador, DTOs/schemas, tests si existen, y el modelo de base de datos.

Este módulo de referencia define:
- Los nombres de archivos y su ubicación exacta
- Las convenciones de código (clases vs. funciones, async/await vs. promesas,
  try/catch vs. Result, anotaciones, decoradores, etc.)
- La estructura interna de cada archivo
- El formato de las respuestas HTTP
- El manejo de errores

**Si no existe ningún módulo CRUD completo**, leer los archivos más
representativos de cada capa para inferir el patrón.

**Si el modo ML está activo**, el "módulo de referencia" equivalente es un
notebook o script de pipeline ya existente (ej. `notebooks/03_entrenamiento_baseline.ipynb`
o un módulo bajo `src/models/`). Léelo completo para extraer las mismas
convenciones que en el caso CRUD, adaptadas: cómo se cargan los datos, qué
librería de preprocesamiento usa (`sklearn.pipeline.Pipeline`,
`ColumnTransformer`), convención de nombres de variables/artefactos
(`X_train`/`y_train`, nombres de archivos de modelo guardado), cómo se
registran las métricas (¿hay tracking con MLflow o solo prints/celdas de
notebook?), y si hay separación entre lógica reutilizable (`src/`) y
exploración (`notebooks/`) — ver `references/guia-notebooks-python.md` de
`archi` para el criterio de qué debería ir en cada uno si el proyecto aún no
lo separa. **Si no existe ningún pipeline previo** (proyecto ML greenfield,
típico de un TFM que arranca desde cero), no hay módulo de referencia que
imitar — usa directamente la estructura de `references/guia-notebooks-python.md`
de `archi` como convención por defecto (asumiendo que `archi` ya corrió en
FASE -1 y dejó esa referencia disponible en `resources/architecture/`).

---

#### E. Convenciones de código

A partir del módulo de referencia, documentar:

- **Nombrado de archivos:** `PascalCase`, `kebab-case`, `snake_case`,
  `camelCase`, con o sin sufijo (`Controller`, `Service`, `Repository`, `Handler`)
- **Nombrado de clases / structs / tipos:** convención del lenguaje
- **Nombrado de métodos:** `camelCase`, `snake_case`, `PascalCase` (Go)
- **Imports / requires / uses:** estilo de import del proyecto
- **Inyección de dependencias:** constructor, anotaciones (`@Autowired`, `@Inject`),
  contenedor manual, sin DI
- **Manejo de errores:** `throw`, `Result<T, E>`, `Either`, excepciones tipadas,
  middleware centralizado
- **Validación de entrada:** dónde ocurre (DTO con anotaciones, middleware,
  schema en el handler, service layer)
- **Logging:** librería usada y estilo de log
- **Transacciones:** cómo se manejan (anotación `@Transactional`, Unit of Work,
  transacción explícita)

---

#### F. Modelo de datos existente

Leer el schema o los modelos del ORM según el stack detectado:

| Stack | Dónde buscar |
|---|---|
| Prisma | `prisma/schema.prisma` |
| TypeORM | Archivos `*.entity.ts` con `@Entity()` |
| Hibernate/JPA | Clases `@Entity` en `domain/` o `model/` |
| Entity Framework | Clases en `Domain/` + `*DbContext.cs` |
| SQLAlchemy | Clases que heredan de `Base` o `DeclarativeBase` |
| Django ORM | `models.py` en cada app |
| GORM | Structs con tags `gorm:` |
| ActiveRecord / Rails | Migraciones en `db/migrate/` + modelos en `app/models/` |
| Eloquent / Laravel | Modelos en `app/Models/`, migraciones en `database/migrations/` |
| Doctrine | Entidades con `@ORM\Entity` o configuración YAML/XML |
| Sin ORM | Migraciones SQL o scripts de DDL |

Extraer de cada entidad existente:
- Nombre de la entidad / tabla
- Campos con tipo de dato
- Relaciones (FK, ManyToOne, OneToMany, ManyToMany)
- Campos de auditoría (`created_at`, `updated_at`, `deleted_at`)
- Enums y sus valores
- Índices y restricciones relevantes

---

#### G. Patrones de API existentes

Leer los handlers / controllers existentes y documentar:
- Prefijo de rutas (`/api/v1`, `/api`, sin prefijo)
- Estructura exacta de respuesta exitosa
- Estructura exacta de respuesta de error
- Manejo de paginación (page/limit, offset/take, cursor, sin paginación)
- Autenticación (header, middleware, decorador)
- Formato de IDs en URLs (UUID, CUID, autoincrement)

---

#### H. Cargar guía de referencia del stack detectado

Una vez identificado el stack (lenguaje + framework + ORM), carga la guía de
referencia correspondiente de `references/` según la tabla de §Guías de referencia
por stack. Esta guía proporciona:

- **Estructura de proyecto recomendada** — si el proyecto es greenfield o el
  codebase existente no sigue un patrón claro, la guía es la fuente de verdad.
- **Anti-patrones a evitar** — errores comunes en ese stack que un desarrollador
  senior no cometería (ej. mezclar domain model con JPA entities en Java, usar
  `*ngIf` en Angular 17+, no validar variables de entorno con Zod en Node.js).
- **Convenciones de testing** — frameworks, naming, estructura de tests unitarios
  vs. integración vs. API.
- **Stack recomendado** — si el proyecto es greenfield, la guía incluye una tabla
  de "Stack recomendado por defecto" con versiones actualizadas.
- **Dockerfile canónico** — listo para producción, con healthcheck, usuario no
  root, y multi-stage build cuando aplica.

Si el stack detectado no tiene guía específica en `references/` (ej. Go, Ruby,
PHP, Rust), usa el módulo de referencia del codebase (§0.2 D) como única fuente
de verdad. Si además es greenfield sin codebase, aplica principios universales:
Clean Architecture, separación domain/infrastructure/presentation, testing
unitario del dominio, manejo de errores tipado, validación de entrada declarativa.

---

### 0.3 Crear archivos de documentación

Crear o actualizar con contenido real del análisis. Sin placeholders.

#### `resources/architecture/overview.md`

```markdown
# Arquitectura del Proyecto

## Lenguaje principal y versión
<!-- Java 21, Python 3.12, C# 12 / .NET 8, Go 1.22, Node.js 20, etc. -->

## Tipo de proyecto
<!-- Backend API, Frontend SPA, Fullstack monorepo, Microservicio, etc. -->

## Estructura de paquetes / módulos
<!-- Árbol real de paquetes con su rol -->

## Patrón arquitectónico
<!-- Hexagonal / Layered / Clean / Modular / MVC — con evidencia observada -->

## Convenciones de código
- Nombrado de archivos:
- Nombrado de clases / tipos:
- Inyección de dependencias:
- Manejo de errores:
- Validación de entrada:
- Logging:

## Módulo de referencia usado para scaffold
<!-- Nombre del módulo, rutas de sus archivos -->
```

#### `resources/architecture/stack.md`

```markdown
# Stack Tecnológico

## Lenguaje
<!-- Java 21 / Python 3.12 / C# 12 / etc. -->

## Backend
| Rol | Tecnología | Versión |
|---|---|---|
| Framework HTTP | | |
| ORM / acceso a datos | | |
| Validación | | |
| Autenticación | | |
| Migraciones | | |
| Testing | | |
| Build / empaquetado | | |

## Frontend (si aplica)
| Rol | Tecnología | Versión |
|---|---|---|
| Framework | | |
| Estado / data fetching | | |
| Formularios | | |
| Estilos | | |
| Testing | | |

## Base de datos
<!-- Motor (PostgreSQL / MySQL / MongoDB / SQLite), hosting, version -->

## Infraestructura y despliegue (si es visible en el código)
<!-- Docker, Kubernetes, serverless, scripts CI/CD -->
```

#### `resources/design/data-model.md`

```markdown
# Modelo de Datos

## Entidades existentes

### NombreEntidad
- **Tabla / Colección:** `nombre_real`
- **Tipo de ID:** UUID / CUID / autoincrement / ObjectId / etc.
- **Campos:** lista con tipo de dato real
- **Relaciones:** lista con cardinalidad
- **Auditoría:** campos de auditoría presentes
- **Soft delete:** sí/no (campo usado)
- **Enums:** nombre → valores

<!-- Repetir por cada entidad -->

## Relaciones entre entidades
<!-- Descripción textual o diagrama ASCII de las relaciones -->
```

#### `resources/design/api.md`

```markdown
# Patrones de API

## Endpoint de referencia (módulo existente)
<!-- Copiar un ejemplo real: método + ruta + request + response -->

## Estructura de respuesta exitosa
<!-- Ejemplo real de JSON / formato de respuesta -->

## Estructura de respuesta de error
<!-- Ejemplo real de JSON / formato de error -->

## Paginación
<!-- Parámetros y estructura de respuesta paginada real -->

## Autenticación
<!-- Header, formato del token, middleware / decorador usado -->

## Historial de cambios del contrato
<!-- Una línea por corrida de builder que agregó o modificó el contrato de
     resources/design/openapi.yaml. Ver §1.6.3. Ejemplo:
     - v0.2.0 (2026-07-16): agregado recurso PaymentMethod — aditivo.
     - v1.0.0 (2026-07-20): Order.status — enum reducido (breaking change),
       confirmado por el usuario. -->
```

`resources/design/openapi.yaml` es el equivalente máquina-legible de este archivo: mientras
`api.md` documenta las convenciones en prosa, `openapi.yaml` es el contrato real (OpenAPI 3.1)
que se va acumulando recurso a recurso — ver §1.6.

---

## FASE 1 — ANÁLISIS DEL RECURSO A CREAR

Con la arquitectura documentada (FASE 0) y el requerimiento resuelto (FASE E),
consolidar la información definitiva del recurso a generar.

### 1.1 Pre-población desde la Fase E

Los siguientes datos ya fueron extraídos en la Fase E y no deben volver a
pedirse al usuario salvo que estén incompletos o sean ambiguos:

- Nombre del recurso
- Campos con tipo y restricciones
- Relaciones con entidades existentes
- Reglas de negocio
- Capas a generar

### 1.2 Adaptación al stack detectado

Con los datos de la Fase E, aplicar el contexto técnico de la Fase 0:

- **Tipos de dato:** traducir los tipos del requerimiento funcional al tipo
  equivalente en el lenguaje del proyecto.
  Ej: "texto corto" → `String` (Java), `str` (Python), `string` (TS), `VARCHAR` (SQL)

- **Nombre del recurso:** adaptar al naming convention detectado.
  Ej: si el proyecto usa `snake_case` para archivos, `PaymentMethod` se
  convierte en `payment_method.py`.

- **Relaciones:** verificar contra el modelo de datos en
  `resources/design/data-model.md` que las entidades relacionadas existen
  y que la cardinalidad es correcta.

- **Campos nuevos vs. campos de entidades existentes:** si el requerimiento
  menciona datos que pertenecen a otra entidad ya existente, no duplicarlos —
  modelar como relación.

### 1.2bis Detectar si el recurso es un Pipeline de Machine Learning / IA

Antes de continuar a §1.3, decide si este recurso sigue el flujo CRUD normal
(§2.1 patrones tradicionales) o el patrón de Pipeline de ML (§2.1 "Pipeline
de Machine Learning"). Señales para activarlo:

- El campo "Tipo de recurso" de la HU (§E.4) dice explícitamente ML/IA.
- La descripción/criterios de aceptación mencionan: entrenar, dataset,
  modelo, predicción, clasificación, embeddings, notebook, métricas tipo
  F1/AUC-ROC/precisión-recall, explicabilidad/SHAP.
- El modo ML ya estaba activo desde §0.2 B (el proyecto tiene
  pandas/scikit-learn/TensorFlow/PyTorch en su manifiesto o carpeta
  `notebooks/`).

Si se activa, clasifica además **qué etapa del pipeline** cubre esta HU
específica — una HU rara vez cubre el pipeline completo de punta a punta:

| Etapa | Qué genera §2.1 |
|---|---|
| Ingesta / pipeline de datos | Scripts de carga, limpieza, validación, feature engineering |
| Entrenamiento | Script(s)/notebook de entrenamiento, baseline y candidato(s), tracking de experimento |
| Evaluación / explicabilidad | Script de métricas (por clase, matriz de confusión), SHAP |
| Servicio / inferencia | Endpoint o job de predicción que carga el modelo versionado |

Si la HU no dice a qué etapa pertenece y no es inferible del título/
descripción, pregúntalo en §1.3 como una ambigüedad más — no asumas la
etapa. Si viene de una épica (§E.2bis), usa el orden ya acordado ahí como
pista, pero igual confirma la etapa concreta de esta HU puntual.

Para las convenciones exactas de estructura (dónde va cada script, qué
librerías usar, cómo versionar modelos y datos), usa como fuente de verdad
lo que `archi` haya dejado en `resources/architecture/` (secciones 5.1-5.4/
9.1 del documento si usó `plantilla-documento-arquitectura-ml.md`) y, si el
proyecto lo trae, `references/guia-ml-arquitectura.md` /
`references/guia-notebooks-python.md`. Si ninguno está disponible porque
FASE -1 no pudo invocar `archi`, usa la estructura por defecto de §2.1
"Pipeline de Machine Learning" y documenta la falta de línea base validada
en Supuestos.

### 1.3 Confirmar con el usuario si hay ambigüedades

Solo preguntar al usuario si hay puntos que la Fase E no dejó claros:

- Campos sin tipo definido
- Reglas de negocio que implican múltiples interpretaciones de implementación
- Relaciones con entidades cuya existencia no está confirmada en el modelo
- Si generar solo backend, solo frontend, o ambas (cuando no está explícito)
- Si el modo ML está activo: a qué etapa del pipeline pertenece esta HU, qué
  fuente(s) de datos usa, si hay métrica(s) objetivo definidas, y si requiere
  explicabilidad — cuando la HU no lo deja claro (§1.2bis)

### 1.4 Derivar variantes de nombre

Derivar automáticamente todas las variantes según el lenguaje:

| Variante | Ejemplo Java/TS | Ejemplo Python/Go/Ruby |
|---|---|---|
| PascalCase (clase) | `PaymentMethod` | `PaymentMethod` |
| camelCase (variable) | `paymentMethod` | — |
| snake_case | — | `payment_method` |
| kebab-case (ruta URL) | `payment-methods` | `payment-methods` |
| SCREAMING_SNAKE | `PAYMENT_METHOD` | `PAYMENT_METHOD` |
| Plural | según idioma | según idioma |

---

### 1.5 Congelar el contrato de API (obligatorio si se generan ambas capas)

> Si el modo ML está activo (§1.2bis): este paso y §1.6 aplican **solo** a
> la etapa "Servicio / inferencia" (expone un endpoint HTTP real). Las
> etapas de ingesta, entrenamiento y evaluación/explicabilidad no exponen
> API — son scripts/notebooks offline — así que no tienen contrato que
> congelar ni registrar en `openapi.yaml`. Sáltalos para esas etapas y ve
> directo a FASE 2.

**Este paso es un requisito duro antes de pasar a Fase 2 cuando `Capas: backend + frontend`.**
Su objetivo es eliminar cualquier ambigüedad de interfaz antes de que backend y
frontend se generen por separado, para que ninguno de los dos tenga que
"inventar" o inferir el contrato por su cuenta.

Producir un bloque de contrato explícito, combinando `resources/design/api.md`
(formato general del proyecto) con los campos del recurso resueltos en 1.1–1.4:

```markdown
## Contrato de API — {NombreRecurso}

### Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | /api/.../{recursos} | Listar (paginado) |
| GET | /api/.../{recursos}/:id | Obtener por ID |
| POST | /api/.../{recursos} | Crear |
| PUT/PATCH | /api/.../{recursos}/:id | Actualizar |
| DELETE | /api/.../{recursos}/:id | Eliminar |

### Request — Crear (POST)
| Campo | Tipo | Requerido | Notas |
|---|---|---|---|
| ... | ... | ... | ... |

### Request — Actualizar (PUT/PATCH)
<!-- Mismos campos que crear, marcando cuáles son opcionales -->

### Response — Recurso (usado en GET/POST/PUT)
| Campo | Tipo | Notas |
|---|---|---|
| ... | ... | ... |

### Response — Error
<!-- Formato exacto de error del proyecto, tomado de resources/design/api.md -->

### Paginación
<!-- Parámetros y forma de la respuesta paginada, exacto -->

### Autenticación
<!-- Header, formato de token -->

### Códigos de estado HTTP
| Caso | Código |
|---|---|
| Éxito lectura | 200 |
| Éxito creación | 201 |
| Error de validación | 400/422 (según convención del proyecto) |
| No encontrado | 404 |
| ... | ... |
```

Reglas de este contrato:

- **Nombres de campos idénticos** entre lo que backend expone y lo que frontend
  consume — literal, sin transformar casing entre capas salvo que el proyecto
  ya tenga esa convención documentada (ej. backend `snake_case` en DB pero
  `camelCase` en JSON de respuesta: dejarlo explícito en el contrato).
- Si algún campo, tipo o regla de negocio no está claro para definir el
  contrato, **preguntar al usuario aquí**, no dejarlo para que cada capa lo
  resuelva de forma distinta en Fase 2.
- Este contrato se guarda como sección temporal (no persiste como archivo
  nuevo) y se pasa **completo y literal** a los dos flujos de generación de la
  Fase 2 — es la única fuente de verdad de la interfaz entre capas.
- Si `Capas` es solo backend o solo frontend, este paso no aplica (no hay
  segunda capa con la que desincronizarse).

---

## 1.6 — Registrar contra el contrato de API vivo (`resources/design/openapi.yaml`)

Aplica siempre que `Capas` incluya backend — a diferencia de §1.5 (que solo aplica para
sincronizar dos capas generadas en paralelo), esto corre también en corridas de un solo
recurso backend sin frontend.

`resources/design/openapi.yaml` es el contrato de API **acumulado** de todo el proyecto: cada
corrida de `builder` le agrega o actualiza los `paths`/`schemas` de su recurso, nunca lo
reemplaza ni lo regenera desde cero. Si el archivo no existe todavía (proyecto sin `genesis`,
o de antes de que existiera este archivo), créalo primero con el envoltorio base a partir de
`resources/design/api.md` (título del proyecto, prefijo de rutas, esquema de error, esquema
de paginación, esquema de seguridad) antes de agregar el primer recurso.

### 1.6.1 — Verificar colisiones antes de escribir

Antes de agregar el recurso nuevo al contrato:
- **Colisión de ruta:** ¿ya existe un `path` + método igual perteneciente a otro recurso? Si
  sí, detente e informa al usuario — no se sobrescribe en silencio el endpoint de otro recurso.
- **Reutilización de schemas:** si el recurso tiene una relación con una entidad ya registrada
  en `components.schemas`, referencia ese schema con `$ref` en vez de redefinirlo — mantiene el
  contrato consistente y evita definiciones duplicadas que diverjan con el tiempo.
- **Reutilización de componentes compartidos:** el schema de error, el de paginación y las
  respuestas comunes (400/401/403/404/409/500) se definen una sola vez en `components/` y se
  referencian desde cada operación — no las repitas inline por recurso.

### 1.6.2 — Detectar breaking changes si el recurso ya existía

Si el recurso que se está generando **ya tiene** entradas en `resources/design/openapi.yaml`
(esta corrida modifica/extiende un recurso de una corrida anterior, no lo crea desde cero),
compara el contrato anterior contra el nuevo antes de aplicar el cambio:

| Tipo de cambio | ¿Rompe el contrato? |
|---|---|
| Campo nuevo opcional en request/response | No |
| Endpoint nuevo | No |
| Parámetro de query opcional nuevo | No |
| Valor nuevo agregado a un enum | No (salvo que el consumidor haga match exhaustivo — adviértelo igual) |
| Campo eliminado de un response | **Sí** |
| Campo que pasa de opcional a requerido | **Sí** |
| Cambio de tipo de un campo existente | **Sí** |
| Ruta o método eliminado/renombrado | **Sí** |
| Código de estado de respuesta eliminado | **Sí** |

Si se detecta al menos un cambio de la columna "Sí": **detente antes de generar el scaffold** y
presenta la lista de cambios incompatibles al usuario, con esta pregunta explícita:

> ¿Confirmas este cambio incompatible en `<recurso>` (rompe a cualquier consumidor actual del
> endpoint), o prefieres versionar el endpoint (ej. `/api/v2/<recurso>`) para no romper el
> contrato ya publicado?

No asumas la respuesta — es una decisión de producto/negocio, no técnica. Continúa recién con
la confirmación del usuario, y registra la decisión en el historial de cambios (§1.6.3).

### 1.6.3 — Persistir el cambio

Al final de la Fase 2 (junto con "ACTUALIZAR resources/ TRAS LA GENERACIÓN"), fusiona los
`paths`/`schemas` del recurso en `resources/design/openapi.yaml` y agrega una entrada al
historial de cambios en `resources/design/api.md` (sección "Historial de cambios del
contrato", ver plantilla en §0.3).

Incrementa `info.version` de `resources/design/openapi.yaml` siguiendo semver: **minor** para
cambios aditivos, **major** para cualquier corrida donde se confirmó un breaking change.

---

## FASE 2 — GENERACIÓN DEL SCAFFOLD

### Principio fundamental

**No usar templates predefinidos. Generar imitando el módulo de referencia.**

El proceso es:
1. Tomar cada archivo del módulo de referencia
2. Entender su propósito y estructura
3. Replicar ese mismo archivo para el nuevo recurso, adaptando:
   - Nombre de la entidad y sus variantes
   - Campos y tipos del nuevo recurso
   - Relaciones con otras entidades
4. Mantener todo lo demás igual: imports, anotaciones, manejo de errores,
   formato de respuesta, estilo de código

---

### 2.0 Generación en paralelo cuando aplican ambas capas

Si `Capas: backend + frontend`, backend y frontend se generan **en paralelo**,
no secuencialmente. Son independientes entre sí una vez que el contrato de
API quedó congelado en §1.5 — ninguno necesita esperar al otro porque ninguno
tiene que inferir la interfaz del otro.

**Precondición dura:** el contrato de §1.5 debe existir y estar libre de
ambigüedad antes de disparar esta fase. Si algo del contrato quedó pendiente
de confirmar con el usuario, resolverlo antes de continuar — no arrancar la
generación en paralelo con un contrato incompleto.

**Mecanismo:** lanzar dos sub-agentes (tool `Agent`) en el mismo mensaje,
uno por capa, para que corran de forma concurrente. Cada prompt debe incluir,
de forma autocontenida (el sub-agente no tiene el resto de esta conversación):

- El contrato de API congelado de §1.5, completo y sin reinterpretar.
- El spec del recurso (campos, tipos, variantes de nombre, reglas de negocio)
  resuelto en Fase 1, filtrado a lo que esa capa necesita.
- La sección de arquitectura/convenciones de esa capa (`resources/architecture/`)
  y su módulo de referencia correspondiente (backend o frontend).
- Las secciones de esta skill relevantes a su capa: §2.1 (bloque de capas del
  patrón detectado), §2.2 (principios universales), y su parte de §2.3
  (archivos de registro propios de esa capa).
- Instrucción explícita: **no modificar nombres de campos, tipos, rutas ni
  formato de request/response del contrato congelado.** Si el sub-agente
  detecta un problema real con el contrato, debe reportarlo en su respuesta
  en vez de resolverlo unilateralmente con una interpretación propia.
- Instrucción de **no tocar** `resources/design/data-model.md` ni
  `resources/architecture/overview.md` — esos los actualiza el orquestador
  una sola vez al final (§ACTUALIZAR resources/), para evitar que ambos
  sub-agentes escriban el mismo archivo a la vez.

**Al recibir ambos resultados:** ejecutar el paso de reconciliación de §2.4
antes de continuar al checklist.

---

### 2.1 Capas a generar por patrón arquitectónico

Independientemente del lenguaje, generar las capas equivalentes al patrón detectado.

#### Hexagonal / Clean Architecture
```
[shared o types]
  → DTOs / contratos de interfaz del recurso

[dominio]
  → Entidad de dominio con lógica de negocio
  → Interfaz / puerto del repositorio
  → Value Objects si el módulo de referencia los usa

[aplicación]
  → Casos de uso: Crear, ObtenerPorId, ObtenerTodos, Actualizar, Eliminar
  → DTOs de comando/query si el patrón los usa

[infraestructura / adaptadores]
  → Implementación del repositorio con el ORM detectado
  → Controller / Handler / Resource HTTP
  → Router / registro de rutas
  → Registro en el contenedor de DI

[frontend, si aplica]
  → Entidad o modelo de presentación
  → Puerto / interfaz del cliente HTTP
  → Adaptador del cliente HTTP
  → Hooks o servicios de data fetching
  → Componentes de lista y formulario
  → Página principal del recurso
```

#### Layered / MVC
```
[modelo / entidad]
  → Clase de modelo con el ORM detectado
  → Schema de validación si existe

[repositorio]
  → Clase repositorio con métodos CRUD

[servicio]
  → Clase servicio con lógica de negocio

[controller / handler]
  → Controller con endpoints CRUD

[rutas]
  → Registro de rutas en el router principal

[DTOs / schemas]
  → Schemas de entrada (create, update) y salida (response)
```

#### Modular (NestJS, Spring Modular, etc.)
```
[módulo]
  → Archivo de definición del módulo
  → Controller o Resource
  → Service
  → Repository (si el módulo no usa el repositorio del framework directamente)
  → Entity / Model
  → DTOs de entrada y salida

[registro]
  → Importar el módulo en el módulo raíz de la aplicación
```

#### CQRS (con o sin Event Sourcing)
```
[commands]
  → Command: Create{Resource}Command, Update{Resource}Command,
              Delete{Resource}Command
  → Command Handler por cada command
  → Validadores si los usa el módulo de referencia

[queries]
  → Query: Get{Resource}Query, GetAll{Resource}sQuery
  → Query Handler por cada query

[read model / projections, si aplica]
  → Read model específico para las queries

[domain]
  → Entidad / Aggregate Root
  → Domain Events si el módulo de referencia los usa

[infrastructure]
  → Repositorio de escritura
  → Repositorio de lectura (si read model separado)
  → Controller que despacha commands y queries
```

#### MVC Convencional (Rails, Django, Laravel)
```
[modelo]
  → Clase de modelo con validaciones del framework

[migración]
  → Archivo de migración con la tabla y columnas

[controller]
  → Controller con acciones CRUD (index, show, create, update, destroy)

[rutas]
  → Entrada en el archivo de rutas del framework

[serializer / presenter, si el módulo de referencia los usa]
  → Serializer del recurso

[tests, si el módulo de referencia tiene tests]
  → Tests del modelo
  → Tests del controller (request specs / feature specs)
```

#### Vertical Slice / Feature-based
```
[feature/{resource}]
  → Todos los archivos del recurso dentro de su propia carpeta
  → Handler(s) o Controller
  → Modelo o entidad
  → Repositorio o acceso a datos
  → Schemas de validación
  → Registro en el router central
```

#### Pipeline de Machine Learning / Ciencia de Datos

Se usa cuando §1.2bis determinó que el recurso es de tipo ML/IA, en vez de
cualquiera de los patrones anteriores. La estructura de carpetas sigue
`references/guia-notebooks-python.md` de `archi` cuando está disponible
(`data/`, `notebooks/`, `src/{data,features,models,evaluation}/`, `models/`);
si no está disponible, usa esa misma estructura como convención por defecto.
Genera solo lo que corresponde a la etapa detectada en §1.2bis — no generes
las cuatro etapas de una vez si la HU solo cubre una:

```
[Etapa: Ingesta / pipeline de datos]
  → src/data/ingesta.py (o equivalente) — carga desde la(s) fuente(s) de la HU
  → src/data/limpieza.py — validación, imputación, deduplicación
  → src/data/anonimizacion.py — si la HU/línea base marca datos sensibles
  → src/features/feature_engineering.py — transformación a features de entrada
  → notebooks/0N_exploracion_<recurso>.ipynb — exploración/visual, referenciando
    las funciones de src/ (no reimplementarlas dentro del notebook)

[Etapa: Entrenamiento]
  → src/models/train_baseline.py — modelo(s) baseline simple(s)
  → src/models/train_<nombre_modelo>.py — modelo candidato de la HU
  → notebooks/0N_entrenamiento_<recurso>.ipynb — corrida documentada, con
    semilla aleatoria fijada y parámetros registrados (tracking si el
    proyecto ya usa MLflow/W&B; si no, al menos un log estructurado)
  → models/ (o la ruta que la línea base defina) — artefacto de salida
    versionado con un nombre que incluya fecha/hash, nunca sobrescribir el
    modelo anterior en silencio

[Etapa: Evaluación / explicabilidad]
  → src/evaluation/metrics.py — métricas globales y por clase, matriz de confusión
  → src/evaluation/shap_explain.py — si la HU pide explicabilidad
  → notebooks/0N_evaluacion_<recurso>.ipynb — reporta contra las métricas
    objetivo de la línea base (no solo el número obtenido, también si cumple
    la meta)

[Etapa: Servicio / inferencia — sí expone API, aplica §1.5/§1.6]
  → src/serving/predict.py (o el contenedor de servicio detectado en la
    línea base: FastAPI, Flask, TF Serving) — carga el modelo versionado y
    expone el endpoint de predicción
  → Reutiliza el mismo código de src/data y src/features para el
    preprocesamiento — nunca lo reimplementes en el servicio (evita
    training-serving skew, ver references/guia-ml-arquitectura.md de archi)
  → Sigue el patrón de generación normal (§2.1 patrón detectado para la
    capa web del proyecto) para el controller/endpoint que envuelve la
    predicción — el pipeline ML no reemplaza el patrón de la API, solo el
    contenido de negocio detrás de ese endpoint
```

---

### 2.2 Principios universales de generación

Aplicar en cualquier lenguaje y patrón:

**Entidad de dominio**
- Encapsular la lógica de negocio del recurso en la entidad, no en el servicio
- Los métodos que cambian estado retornan una nueva instancia (inmutabilidad) o
  mutan con validación interna, según lo que hace el módulo de referencia
- Validar invariantes del dominio al construir la entidad
- Sin dependencias de infraestructura (base de datos, HTTP, I/O)

**Repositorio**
- Implementar exactamente la interfaz / contrato del puerto
- Mapear entre el modelo de base de datos y la entidad de dominio
- El repositorio conoce el ORM; la entidad no lo conoce
- Paginación con el mismo patrón que el módulo de referencia

**Servicio o caso de uso**
- Un caso de uso / método de servicio por operación de negocio
- Orquestar: obtener del repositorio → aplicar lógica → persistir → retornar DTO
- No contener lógica de presentación (eso va en el controller)

**Controller / Handler / Resource**
- Delegar toda la lógica al servicio o caso de uso
- Transformar: request HTTP → DTO de entrada → servicio → DTO de salida → response HTTP
- Capturar errores del dominio y mapearlos a códigos HTTP correctos
- Usar el mismo formato de respuesta que el resto del proyecto

**DTOs / Schemas de validación**
- Validar en el límite de entrada (controller o middleware, según el patrón)
- Campos opcionales en update claramente marcados como opcionales
- No reutilizar el mismo schema para create y update si tienen campos distintos

**Tests (si el módulo de referencia tiene tests)**
- Replicar la misma estrategia de tests que existe en el proyecto
- Si hay unit tests del servicio/caso de uso: crear los equivalentes
- Si hay integration/request tests: crear los equivalentes
- Si hay tests de repositorio con DB real: crear los equivalentes

**Pipeline de Machine Learning (si el modo ML está activo, §1.2bis)**
- Cualquier función reutilizable (limpieza, feature engineering,
  entrenamiento parametrizado) va en `src/`, nunca copiada entre celdas de
  distintos notebooks — el notebook la importa, no la reimplementa.
- Fija semillas aleatorias (`random_state`, `numpy.random.seed`,
  `torch.manual_seed`/`tf.random.set_seed`) en cualquier paso estocástico
  (split de datos, inicialización de pesos, SMOTE, shuffle).
- Fija versiones exactas en `requirements.txt`/`pyproject.toml` de cualquier
  librería nueva que agregues (`pandas==2.2.1`, no `pandas`).
- El código de preprocesamiento usado en entrenamiento y el usado en el
  endpoint de servicio deben ser el mismo módulo importado, no dos
  implementaciones paralelas.
- No sobrescribas en silencio un modelo/artefacto ya versionado — genera uno
  nuevo con su propia versión/tag y deja explícito en el notebook o script
  cuál es el vigente.
- Si la HU pide una métrica objetivo, el script/notebook de evaluación debe
  reportar explícitamente si la cumple o no — no solo el valor crudo.

---

### 2.3 Archivos de registro a actualizar

Además de los archivos nuevos, actualizar los archivos de registro existentes
según lo detectado. Los candidatos más comunes son:

| Archivo de registro | Qué agregar |
|---|---|
| Router principal / archivo de rutas | Montar las rutas del nuevo recurso |
| Contenedor de DI / módulo de DI | Registrar repositorio, servicio, controller |
| Módulo raíz (NestJS / Spring Modular) | Importar el nuevo módulo |
| Schema del ORM (Prisma, etc.) | Agregar el modelo |
| Registro de módulos Django (`INSTALLED_APPS`) | Agregar la nueva app |
| `AppModule` o similar | Registrar el nuevo módulo |
| Navegación / sidebar del frontend | Agregar enlace al nuevo recurso |
| Router del frontend | Agregar la nueva ruta |

Cuando backend y frontend se generan en paralelo (§2.0), cada sub-agente solo
toca los archivos de registro de su propia capa (backend no toca navegación ni
router del frontend, y viceversa) — no hay archivos de esta tabla compartidos
entre ambos, así que no hay condición de carrera entre los dos sub-agentes.

---

### 2.4 Reconciliación post-generación (solo si se generó en paralelo)

Al recibir los resultados de ambos sub-agentes de §2.0, antes de pasar al
checklist, verificar que no haya divergido nada del contrato congelado en §1.5:

- **Rutas:** las rutas que el cliente HTTP del frontend llama coinciden
  exactamente (método + path) con las rutas montadas en el backend.
- **Nombres de campos:** los campos que el frontend espera en request/response
  coinciden literalmente con los que el backend expone (mismo casing, mismos
  nombres — sin variantes tipo `paymentMethod` vs `payment_method` no
  contempladas en el contrato).
- **Formato de error y paginación:** el manejo de error/paginación del cliente
  frontend asume la misma forma que realmente devuelve el backend.
- **Reporte de problemas:** si alguno de los dos sub-agentes reportó un
  problema con el contrato (ver §2.0), resolverlo ahora — puede requerir
  regenerar solo la capa afectada, no ambas.

Si se encuentra una divergencia, corregirla directamente (es más barato un
ajuste puntual aquí que descubrirlo en el checklist de verificación final).
Si todo coincide, continuar al checklist normalmente.

---

## CHECKLIST POST-GENERACIÓN

Adaptar según el stack detectado. Los criterios de aceptación extraídos en
la Fase E deben aparecer aquí como ítems de verificación adicionales.

### Trazabilidad
- [ ] El archivo `resources/functional/hu/` contiene el requerimiento fuente
      (guardado desde Jira o provisto por el usuario)
- [ ] Los criterios de aceptación del requerimiento están cubiertos por el scaffold generado
- [ ] `resources/design/data-model.md` refleja la nueva entidad y sus relaciones (no aplica a etapas ML offline sin entidad operacional nueva)
- [ ] Si FASE -1 tuvo que aprovisionar la línea base con `archi`/`janus`, o si se saltó a pedido del usuario, quedó explícito en "Notas técnicas" de la HU

### Base de datos
- [ ] Agregar el modelo / schema / entidad en el ORM
- [ ] Generar y ejecutar la migración
- [ ] Verificar que los tipos de datos y restricciones son correctos

### Backend
- [ ] Completar el mapeo ORM → entidad con los campos reales
- [ ] Registrar en el contenedor / módulo de DI
- [ ] Montar las rutas en el router / servidor principal
- [ ] Verificar que la validación de entrada está activa
- [ ] Verificar que el manejo de errores responde con el formato correcto

### Frontend (si aplica)
- [ ] Completar los campos del formulario
- [ ] Completar las columnas de la lista / tabla
- [ ] Registrar el adaptador de API en el DI del frontend
- [ ] Agregar la ruta en el router del frontend
- [ ] Agregar el link en la navegación

### Machine Learning / IA (si el modo ML está activo, §1.2bis)
- [ ] Semillas aleatorias fijadas en todo paso estocástico del script/notebook generado
- [ ] Dependencias nuevas agregadas con versión fijada en `requirements.txt`/`pyproject.toml`
- [ ] Ninguna función reutilizable quedó copiada entre celdas de notebooks — vive en `src/`
- [ ] Si la etapa es de entrenamiento: el modelo resultante quedó versionado (no sobrescribió uno anterior en silencio) y las métricas obtenidas se compararon explícitamente contra la(s) meta(s) de la línea base
- [ ] Si la etapa es de evaluación: se reportaron métricas por clase (no solo macro-promedio) cuando hay desbalance, y matriz de confusión
- [ ] Si la etapa es de servicio/inferencia: el preprocesamiento reutiliza el mismo código de `src/data`/`src/features` que el pipeline de entrenamiento (sin reimplementación paralela)
- [ ] Si la HU pedía explicabilidad: el script/notebook de SHAP (u otra técnica) está generado y su salida es interpretable por un no-técnico

### Consistencia backend-frontend (si se generó en paralelo, §2.0/§2.4)
- [ ] Rutas, métodos y nombres de campos coinciden entre lo que el frontend
      llama y lo que el backend expone, sin desviarse del contrato de §1.5
- [ ] El formato de error y de paginación asumido en el frontend coincide con
      el que realmente devuelve el backend
- [ ] Ningún sub-agente reportó un problema de contrato sin resolver

### Contrato de API vivo (§1.6, `resources/design/openapi.yaml`)
- [ ] El recurso quedó registrado en `resources/design/openapi.yaml` sin
      colisión de rutas ni de `operationId` con recursos ya existentes
      (aplica al endpoint de servicio/inferencia en recursos ML; no aplica a
      etapas offline de datos/entrenamiento/evaluación)
- [ ] Los schemas compartidos (error, paginación, entidades relacionadas) se
      referenciaron con `$ref` en vez de redefinirse
- [ ] Si hubo cambios incompatibles sobre un recurso existente, el usuario los
      confirmó explícitamente y quedaron en el historial de cambios de
      `resources/design/api.md`
- [ ] `info.version` de `resources/design/openapi.yaml` se incrementó según
      semver (minor si fue aditivo, major si hubo un breaking change confirmado)

### Tests (si el proyecto tiene tests)
- [ ] Generar tests siguiendo la estrategia del módulo de referencia
- [ ] Todos los tests pasan

### Verificación final
- [ ] Build sin errores
- [ ] El endpoint responde en la ruta esperada (o, en etapas ML offline: el
      script/notebook corre de principio a fin sin errores, `Restart & Run
      All` incluido si es notebook)
- [ ] El frontend muestra la nueva página (si aplica)
- [ ] Si el input fue una épica (§E.2bis): todas las HUs confirmadas quedaron
      procesadas, y el resumen consolidado se mostró al usuario

---

## ACTUALIZAR resources/ TRAS LA GENERACIÓN

Después de crear el módulo, actualizar:

- **`resources/design/data-model.md`** → agregar la nueva entidad con sus
  campos y relaciones reales (no aplica a etapas ML offline sin entidad
  operacional nueva)
- **`resources/design/openapi.yaml`** → fusionar los `paths`/`schemas` del
  recurso siguiendo §1.6 (nunca reemplazar el archivo completo) — solo para
  la etapa de servicio/inferencia en recursos ML
- **`resources/design/api.md`** → agregar la entrada correspondiente en
  "Historial de cambios del contrato" (§1.6.3)
- **`resources/architecture/overview.md`** → documentar cualquier excepción o
  variación al patrón general introducida por este módulo
- **Si el modo ML está activo:** deja constancia del modelo/artefacto
  generado (versión, métrica obtenida, ruta) en el lugar que la línea base de
  `archi` haya definido para esto (p. ej. la sección de entrenamiento del
  `Documento_Arquitectura_*.md`, o un registro de experimentos si el proyecto
  usa MLflow/DVC) — no lo dejes solo implícito en el notebook.

Si se generó en paralelo por capas (§2.0), estos archivos los actualiza el orquestador una
única vez con la información consolidada — nunca cada sub-agente por separado (mismo criterio
que ya aplica §2.0 para evitar condiciones de carrera al escribir `resources/`).
