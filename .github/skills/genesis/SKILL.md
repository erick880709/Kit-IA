---
name: genesis
description: >
  Inicializa desde cero el repositorio de código de un proyecto greenfield a partir de la
  arquitectura propuesta por `archi` en Caso A (sin código previo). Lee
  `resources/architecture/Documento_Arquitectura_<Proyecto>.md`, extrae las decisiones de
  stack/patrón/despliegue, completa las convenciones de código que `archi` no define, e
  inicializa el repositorio real (manifiestos, esqueleto de capas según el patrón elegido,
  plomería base — configuración, conexión a datos, contenedor de inyección de dependencias,
  manejo de errores, logging, endpoint de salud — y los documentos vivos en
  `resources/architecture/` y `resources/design/`) para que `builder` pueda operar
  normalmente sobre el repo a partir de la primera historia de usuario real. Usa esta skill
  SIEMPRE que el usuario tenga un `Documento_Arquitectura_*.md` de un proyecto nuevo
  (greenfield) sin código todavía y pida "inicializar el repo", "crear el proyecto base",
  "arrancar el codebase", "hacer el bootstrap del proyecto", o quiera pasar de la
  arquitectura propuesta a un scaffold ejecutable antes de generar el primer módulo de
  negocio con `builder`. No uses esta skill si el proyecto ya tiene código real (Casos B/C
  de `archi`) — ahí `builder` ya puede detectar el ecosistema directamente sin este puente.
---

# Genesis — Bootstrap de Repositorio Greenfield

## Por qué existe esta skill

`archi` en Caso A produce una **propuesta de arquitectura en papel**: un
`Documento_Arquitectura_<Proyecto>.md` con el estilo arquitectónico, el stack y los
contenedores decididos, más sus diagramas. `builder`, en cambio, **asume que ya existe un
repositorio real**: su Fase 0.2 detecta lenguaje/framework/ORM/patrón leyendo manifiestos
(`package.json`, `pom.xml`, etc.) y busca un módulo CRUD completo para usarlo como plantilla
viva (`builder/SKILL.md` §D). En un proyecto greenfield recién salido de `archi` no existe
ninguna de las dos cosas — no hay manifiesto que detectar ni módulo que imitar.

`genesis` es el puente entre ambos: toma la decisión arquitectónica de `archi` y la convierte
en un repositorio real, ejecutable, con la plomería base conectada de punta a punta. No
genera módulos de negocio (eso lo sigue haciendo `builder`) — solo dejar el terreno listo
para que la primera corrida de `builder` encuentre algo real que detectar.

## Cuándo usar esta skill

- El usuario tiene un `Documento_Arquitectura_*.md` de Caso A (greenfield) y pide
  inicializar/arrancar/hacer el bootstrap del repositorio de código.
- Se acaba de terminar una corrida de `archi` en Caso A y el usuario quiere pasar de la
  propuesta al primer commit de código real.
- El repositorio destino está vacío o solo tiene artefactos no funcionales (README,
  licencia, `.gitignore`) — sin código de aplicación.

## Cuándo NO usarla

- El proyecto ya tiene código real (Casos B/C de `archi`, o cualquier repo con manifiestos y
  módulos existentes): ahí `builder` ya puede ejecutar su Fase 0 de detección directamente,
  sin pasar por `genesis`.
- Se quiere agregar un módulo de negocio a un proyecto ya inicializado (con o sin `genesis`
  de por medio): eso es trabajo de `builder`, no de `genesis`.

## Relación con el resto del pipeline

```
janus / refinador / desglosador → archi (Caso A) → genesis → builder (primera HU real) → qa
                                                  ↑
                                    también invocable a demanda, apuntando
                                    directamente a un Documento_Arquitectura_*.md
                                    de una sesión anterior de archi.
```

`genesis` puede invocarse encadenado (justo después de que `archi` cierra un Caso A en la
misma conversación) o a demanda en cualquier momento posterior, siempre que exista un
`Documento_Arquitectura_*.md` de Caso A para leer.

---

## FASE 0 — Resolución de entrada

### 0.1 Determinar el documento de arquitectura fuente

Si el usuario no indicó ningún argumento:
1. Busca en `resources/architecture/` archivos `Documento_Arquitectura_*.md`.
2. Si hay uno solo, confírmalo con el usuario antes de continuar (no asumas en silencio).
3. Si hay varios, list a los encontrados (nombre + fecha si el frontmatter/encabezado lo
   trae) y pide al usuario cuál usar.
4. Si no hay ninguno, informa que `genesis` necesita un documento de arquitectura de `archi`
   (Caso A) para trabajar, y ofrece invocar `archi` primero si el usuario todavía no lo tiene.

Si el usuario dio una ruta explícita, úsala tal cual.

### 0.2 Validar que el documento es Caso A (greenfield)

Lee el campo **Tipo de documento** del encabezado (`Arquitectura propuesta` / `AS-IS` /
`TO-BE`, según la plantilla de `archi`).

- Si es `Arquitectura propuesta` (Caso A): continúa.
- Si es `AS-IS` o `TO-BE`: detente e informa al usuario que ese documento describe o evoluciona
  un sistema que **ya tiene código** — en ese caso corresponde usar `builder` directamente
  sobre el repo existente, no `genesis`.

### 0.3 Verificar el estado real del repositorio destino

Antes de inicializar nada, confirma que el repositorio destino (directorio de trabajo actual)
está efectivamente vacío de código de aplicación:

1. Lista el árbol de archivos de la raíz del proyecto.
2. Si encuentras manifiestos de lenguaje (`package.json`, `pom.xml`, `*.csproj`,
   `pyproject.toml`, `go.mod`, etc.) o carpetas de código con contenido real, **detente**:
   informa al usuario que el repo ya no está vacío y pregunta si de verdad quiere que
   `genesis` inicialice sobre él (riesgo de sobrescribir trabajo existente) o si en realidad
   lo que necesita es `builder` (que sí está diseñado para operar sobre código existente).
3. Artefactos no funcionales presentes (README, LICENSE, `.gitignore`, `.git/`,
   `resources/`) no cuentan como "código existente" — no bloquean el arranque.

---

## FASE 1 — Extracción de decisiones arquitectónicas

Lee el `Documento_Arquitectura_*.md` completo y extrae, por cada contenedor de la Vista de
Contenedores (sección 5, C4 Nivel 2):

| Dato a extraer | Sección del documento |
|---|---|
| Lenguaje y versión | 1.3 (atributos de calidad puede mencionar restricciones), Restricciones (2), texto de cada contenedor en sección 5 |
| Framework / tecnología del contenedor | Sección 5 (columna "Tecnología" de cada `Container(...)`) |
| Patrón arquitectónico | Sección 4 (Estrategia de Solución) |
| ORM / motor de base de datos | Sección 5 (contenedores `ContainerDb`), Sección 9 (Modelo de Datos) |
| Autenticación / autorización | Sección 10 (Conceptos Transversales) |
| Manejo de errores / logging / configuración | Sección 10 (Conceptos Transversales) |
| Proveedor de nube y forma de despliegue | Sección 12 (Vista de Despliegue) — si hubo modo multi-nube, revisa también la recomendación final de `Pricing_<Proyecto>.md` |
| CI/CD, IaC, ambientes | `Linea_Base_<Proyecto>.md` si existe (bloque "DevOps y ciclo de entrega") |
| Supuestos ya declarados | Sección 16 (Supuestos) — no los repreguntes, ya son la fuente de verdad |

Si el proyecto tiene más de un contenedor con tecnología propia (ej. backend + frontend +
worker), arma una tabla interna `contenedor → stack → patrón` — cada contenedor se
inicializa como una unidad independiente en la Fase 4.

Muestra un resumen al usuario antes de continuar:

```
Arquitectura resuelta desde: resources/architecture/Documento_Arquitectura_<Proyecto>.md

Contenedores a inicializar:
  - api           → Java 21 / Spring Boot 3, Hexagonal, PostgreSQL (JPA)
  - webApp        → React 18 / Vite, sin patrón backend aplicable
  - workerNotif   → Java 21 / Spring Boot 3 (batch), comparte patrón con "api"

Proveedor de despliegue: AWS (ECS Fargate + RDS)

Continuando con la resolución de convenciones de código...
```

---

## FASE 2 — Completar convenciones de código

`archi` decide arquitectura macro, no micro-convenciones de código — esas normalmente las
deriva `builder` de un módulo existente (`builder/SKILL.md` §E "Convenciones de código"), que
en greenfield todavía no existe. `genesis` debe fijarlas explícitamente para que el
repositorio nazca consistente.

### 2.1 Buscar primero si ya están decididas

Antes de preguntar o de aplicar un default, revisa si el dato ya está en el
`Documento_Arquitectura_*.md` o en `Linea_Base_<Proyecto>.md` (ej. un ADR que fije el estilo
de manejo de errores, o el bloque de stack que ya mencione un ORM con su convención estándar).

### 2.2 Completar lo que falte

Para cada dimensión de la tabla siguiente: si no está decidida en ningún documento, aplica el
default idiomático del stack detectado (ver
[references/convenciones-default.md](./references/convenciones-default.md)) y regístralo como
supuesto — **no lo preguntes**, salvo que sea una decisión de alto impacto y bajo costo de
pregunta (ver 2.3):

| Dimensión | Ejemplo de default si no está decidido |
|---|---|
| Nombrado de archivos/clases | El estándar del lenguaje (`PascalCase.java`, `snake_case.py`, `kebab-case.ts`, etc.) |
| Estilo de inyección de dependencias | El nativo del framework (constructor + `@Autowired`/anotaciones de Spring, DI container de NestJS, `Depends()` de FastAPI, etc.) |
| Manejo de errores | Middleware/handler centralizado con formato de error consistente (ver plantilla en `plomeria-base.md`) |
| Validación de entrada | En el límite de entrada (DTO/schema), nunca en el dominio |
| Logging | La librería estándar del ecosistema (SLF4J+Logback, Winston/Pino, `logging` de Python, Serilog) |
| Formato de respuesta / paginación / prefijo de rutas | `/api/v1`, envoltorio `{ data, meta }` para listas paginadas, salvo que el documento ya defina otro formato |
| Formato de ID | UUID v4 por defecto, salvo que el motor de datos elegido sugiera otro (ej. autoincrement si es SQL simple y no hay requisito de exponerlo públicamente) |

### 2.3 Preguntar solo lo de alto impacto

Pregunta explícitamente (agrupado en un solo bloque, máximo la lista de abajo) únicamente lo
que es costoso de revertir después y que ni el documento ni la línea base resuelven:

- **Monorepo vs. polyrepo**, si hay más de un contenedor con stack propio y no está decidido
  (ver Fase 3).
- **Gestor de paquetes** cuando el ecosistema admite más de uno con convenciones distintas
  (ej. npm vs. pnpm vs. yarn; Maven vs. Gradle) y no hay preferencia declarada.
- **Estrategia real de autenticación** si la sección 10 la menciona en abstracto ("JWT") pero
  no dice si hay un proveedor de identidad externo (Auth0, Cognito, Keycloak) o si se
  implementa localmente — cambia materialmente qué se inicializa.

Todo lo demás se decide con el default documentado y se lista en el reporte final como
supuesto, sin bloquear el arranque.

---

## FASE 3 — Resolver topología del repositorio

Con los contenedores de la Fase 1 y las respuestas de la Fase 2:

1. Si hay un solo contenedor con lenguaje propio (backend puro, o backend+frontend en el
   mismo lenguaje de forma trivial): un solo repositorio, estructura plana.
2. Si hay varios contenedores con stacks distintos (ej. backend Java + frontend React): por
   defecto usa **monorepo** con carpetas `apps/<contenedor>/` (o `services/<contenedor>/` si
   el documento ya usa ese término) — es la opción de menor fricción para un proyecto que
   recién arranca y no tiene aún equipos separados por repo. Solo usa polyrepo si el
   documento de arquitectura o la línea base ya lo determinan explícitamente, o si el usuario
   lo pidió en la Fase 2.3.
3. Deja explícita la topología elegida en el resumen antes de pasar a inicializar.

---

## FASE 4 — Inicializar cada contenedor

### 4.1 Generación en paralelo cuando hay más de un contenedor independiente

Si la Fase 1 resolvió más de un contenedor con stack propio (ej. backend + frontend),
inicialízalos **en paralelo**, con el mismo mecanismo que usa `builder` §2.0: lanzar un
sub-agente (tool `Agent`) por contenedor en el mismo mensaje, cada uno autocontenido con:

- El stack, patrón y convenciones resueltos en las Fases 1–2 para ese contenedor específico.
- La topología de repositorio de la Fase 3 (ruta exacta donde debe inicializar sus archivos).
- Las secciones 4.2, 5 y 6 de esta skill (comandos de init, esqueleto de capas, plomería base)
  filtradas a lo que ese contenedor necesita.
- Instrucción explícita de **no tocar** archivos de otro contenedor ni los documentos vivos
  de `resources/` (esos los escribe el orquestador una sola vez al final, Fase 7).

Si solo hay un contenedor, sáltate el paralelismo y ejecútalo directamente.

### 4.2 Comando de inicialización por stack

Usa [references/comandos-init-por-stack.md](./references/comandos-init-por-stack.md) para
obtener el comando de arranque real del ecosistema/framework detectado (equivalente al `npm
init`/`dotnet new`/`django-admin startproject` correspondiente), más el linter/formatter y
test runner por defecto de ese stack si el documento no especificó otros.

No inventes un comando si el stack detectado no está en la tabla de referencia: busca el
comando de inicialización oficial del framework (documentación oficial) antes de asumir uno.

---

## FASE 5 — Generar el esqueleto de capas por patrón arquitectónico

Reutiliza las tablas de `builder/SKILL.md` §2.1 ("Capas a generar por patrón arquitectónico")
para crear la **estructura de carpetas vacía** correspondiente al patrón resuelto en la Fase 1
(Hexagonal/Clean, Layered/MVC, Modular, CQRS, MVC Convencional, Vertical Slice) — mismos
nombres de carpeta que usaría `builder` al agregar un módulo, para que la primera corrida real
de `builder` sobre este repo encuentre la convención ya establecida.

`genesis` **no genera archivos específicos de un recurso de negocio** en esta fase (eso sigue
siendo exclusivo de `builder`) — solo el andamiaje de carpetas y los archivos de plomería
transversal de la Fase 6.

---

## FASE 6 — Plomería base

Dentro del esqueleto de la Fase 5, genera la plomería mínima que hace que el proyecto sea un
programa real que arranca, no solo carpetas vacías. Sigue
[references/plomeria-base.md](./references/plomeria-base.md) para el detalle por patrón:

- Carga de configuración/variables de entorno (`.env.example` incluido).
- Conexión a la base de datos con el ORM/driver decidido (sin modelos de negocio todavía).
- Contenedor de inyección de dependencias / bootstrap de la aplicación.
- Manejo de errores centralizado con el formato de la Fase 2.
- Logging configurado con la librería resuelta.
- Un **endpoint/comando de salud** (`GET /health` o equivalente) que verifica que la app
  levantó y que la conexión a datos responde — este es el único "recurso" funcional que
  `genesis` entrega, y sirve como prueba end-to-end de que la plomería quedó bien conectada.
- Un test trivial que ejercita ese endpoint de salud, usando el test runner resuelto en la
  Fase 4.2.

Si la Fase 1 resolvió infraestructura containerizada (Docker/Kubernetes en la Vista de
Despliegue), agrega también `Dockerfile` y, si hay más de un contenedor en el mismo repo,
`docker-compose.yml` para levantar todo el stack localmente (app + base de datos + cache si
aplica). Si la línea base definió una herramienta de CI/CD, agrega el archivo de pipeline
mínimo (install → lint → test → build) sin inventar pasos que el documento no pidió.

Genera también un `README.md` en español con instrucciones reales de puesta en marcha local
(requisitos, comando de instalación, comando de arranque, cómo correr los tests, variables de
entorno necesarias).

---

## FASE 7 — Poblar los documentos vivos de `resources/`

Escribe (o crea si no existen) estos archivos siguiendo **exactamente** las plantillas que ya
usa `builder/SKILL.md` §0.3, para que sean el mismo formato que `builder` espera encontrar en
sus corridas siguientes:

- `resources/architecture/overview.md`
- `resources/architecture/stack.md`
- `resources/design/data-model.md` — normalmente sin entidades todavía (estructura lista para
  que `builder` agregue la primera al generar el primer recurso). **Excepción:** si la Sección
  9 (Modelo de Datos) del `Documento_Arquitectura_*.md` ya trae entidades con campos/tipos/
  relaciones concretos (porque `archi` los tomó de un desglose de `desglosador` ya resuelto — ver
  `archi/SKILL.md` Paso 0.6 —, no un ER conceptual de alto nivel), transcribe esas entidades tal
  cual en vez de dejar el archivo vacío: son datos ya validados con negocio, no un supuesto de
  `genesis`. La primera corrida de `builder` para esas entidades las completa/implementa, no
  las vuelve a diseñar.
- `resources/design/api.md` (con las convenciones de formato de respuesta/error/paginación/
  autenticación resueltas en la Fase 2 — esto sí puede poblarse desde ya, aunque no exista
  ningún endpoint de negocio, porque son convenciones de proyecto, no de un recurso puntual)
- `resources/design/openapi.yaml` — el envoltorio base del contrato de API vivo que
  `builder/SKILL.md` §1.6 irá acumulando recurso a recurso: `openapi: 3.1.0`, `info.title`
  (del proyecto) e `info.version: "0.1.0"`, `servers` (con el prefijo de rutas de la Fase 2),
  `components.securitySchemes` (el mecanismo de autenticación resuelto en la Fase 2),
  `components.schemas.Error` y `components.schemas.PaginationMeta` (mismo formato que
  `api.md`), y `components.responses` para 400/401/403/404/409/500 referenciando `Error`.
  `paths: {}` vacío — el primer path lo agrega la primera corrida real de `builder`.

Deja explícita la procedencia en cada archivo (ej. `> Generado por genesis a partir de
Documento_Arquitectura_<Proyecto>.md — builder debe actualizar este archivo
incrementalmente, no regenerarlo desde cero`), para que quede trazable a las decisiones de
`archi` y para que `builder` no lo pise sin necesidad en su primera corrida.

Si se generó en paralelo por contenedor (§4.1), estos archivos los escribe el orquestador una
única vez con la información consolidada de todos los contenedores — nunca cada sub-agente
por separado, para evitar que se pisen entre sí.

---

## FASE 8 — Verificación antes de entregar

Antes de reportar como terminado:

- [ ] El proyecto instala sus dependencias sin error con el gestor de paquetes resuelto.
- [ ] El proyecto arranca (`build`/`start` según el comando del framework) sin error.
- [ ] El endpoint/comando de salud responde correctamente.
- [ ] El test trivial de salud pasa.
- [ ] Si se generó en paralelo por contenedor, cada uno arranca de forma independiente.
- [ ] `resources/architecture/overview.md`, `stack.md`, `resources/design/data-model.md` y
      `api.md` reflejan el stack y las convenciones reales inicializadas (no las genéricas de
      la plantilla).
- [ ] `resources/design/openapi.yaml` es YAML válido, con `paths: {}` vacío y los schemas/
      responses compartidos (`Error`, `PaginationMeta`, 400/401/403/404/409/500) ya resueltos
      según las convenciones de la Fase 2 — listo para que la primera corrida de `builder`
      le agregue su primer recurso (§1.6 de `builder/SKILL.md`).
- [ ] El `README.md` generado permite levantar el proyecto siguiendo sus propios pasos, sin
      información tácita que solo tenga esta conversación.

Si algo falla, corrígelo antes de reportar — no entregues un scaffold que no compila o no
levanta.

---

## Reporte final al usuario

Al terminar, resume en el chat (no solo en archivos):

1. Contenedores inicializados, con stack y patrón de cada uno.
2. Topología de repositorio elegida (monorepo/polyrepo) y por qué.
3. Supuestos aplicados en la Fase 2 (convenciones no decididas por `archi`, con su default).
4. Rutas de los documentos vivos actualizados en `resources/`.
5. Cómo levantar el proyecto localmente (comando concreto).
6. Cierre explícito: **"El repositorio está listo — la siguiente historia de usuario ya puede
   generarse con `builder` sobre este proyecto."**

---

## Reglas transversales

- **No sobrescribas código existente.** Si la Fase 0.3 detecta que el repo no está vacío,
  detente y confirma con el usuario antes de continuar.
- **No inventes decisiones de alto impacto** (monorepo/polyrepo, proveedor de identidad,
  gestor de paquetes cuando hay ambigüedad real) sin preguntar — todo lo demás se resuelve
  con default documentado, sin bloquear.
- **No generes módulos de negocio.** El único "recurso" funcional que entrega `genesis` es el
  endpoint de salud de la Fase 6 — cualquier entidad de dominio real es responsabilidad de
  `builder`.
- **Idioma:** documentación y comentarios en español; identificadores de código (nombres de
  clases, variables, rutas) en las convenciones idiomáticas normales del lenguaje/framework,
  igual que hace `builder`.
- **Ubicación:** todo el código se crea en la raíz del repositorio destino (el directorio de
  trabajo actual del usuario), nunca dentro de `resources/` — `resources/` sigue siendo solo
  para los documentos vivos de arquitectura/diseño.
- **Trazabilidad:** cada supuesto o default aplicado en la Fase 2 debe quedar registrado en el
  reporte final y, cuando aplique, como comentario/nota en el archivo de configuración
  correspondiente (ej. una nota en `.env.example` explicando por qué se eligió tal proveedor
  por defecto).

## Referencias

- [references/comandos-init-por-stack.md](./references/comandos-init-por-stack.md)
- [references/plomeria-base.md](./references/plomeria-base.md)
- [references/convenciones-default.md](./references/convenciones-default.md)
