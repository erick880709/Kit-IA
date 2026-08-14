---
name: orquestador
description: 'Meta-skill de enrutamiento. SIEMPRE se consulta primero, antes de invocar cualquier otro skill, para decidir qué skill(s) aplican a la tarea actual y en qué orden. Combina el pipeline de negocio-a-arquitectura-a-scaffold (janus, refinador, desglosador, figma-prd-mockups, archi, genesis, builder, qa) con la disciplina de ingeniería de implementación tomada de addyosmani/agent-skills (tdd-implementacion, validacion-cientifica-ml, revision-calidad, seguridad-rendimiento, entrega-continua, documentacion-observabilidad, y los 24 skills fuente en .github/skills-addy/skills/). Incluye gestión de memoria entre sesiones (memoria), exportación a Obsidian (obsidian) y cierre académico (tfm-redactor). Úsala cuando el usuario inicie una sesión, cuando no quede claro qué skill corresponde, cuando la tarea cruce más de una fase (p. ej. "de la RFP al código funcionando"), o cuando termine un skill y haga falta decidir cuál sigue. Extensiones: validacion-cientifica-ml y tfm-redactor según references/extension-tfm-ml.md.'
---

# Orquestador — Router del Kit Agéntico Unificado

## Por qué existe

Este repositorio combina dos familias de skills que resuelven problemas distintos y complementarios:

1. **Kit de negocio→arquitectura→scaffold** (`.github/skills/janus`, `refinador`, `desglosador`,
   `figma-prd-mockups`, `archi`, `genesis`, `builder`, `qa`, `front`): responde **"¿QUÉ
   hay que construir y con qué forma?"**. Es fuerte en RFP, elicitación, Jira, arquitectura
   C4/ADR/ML, mockups y scaffolding inicial de un módulo o repo greenfield. Su salida son
   documentos y código base bajo `resources/`.
2. **Kit de disciplina de ingeniería** (`.github/skills-addy/skills/*`, adaptado aquí en
   `tdd-implementacion`, `revision-calidad`, `seguridad-rendimiento`, `entrega-continua`,
   `documentacion-observabilidad`): responde **"¿CÓMO se construye bien, se prueba, se
   revisa, se asegura y se despliega ese código?"**. Es fuerte en TDD, code review de
   cinco ejes, seguridad OWASP, performance, git/CI-CD, observabilidad y shipping.

Ninguno de los dos kits es completo por sí solo: el primero se detiene apenas el código
existe (scaffold + QA de alto nivel); el segundo asume que ya hay un spec y no sabe de
dónde salió. El orquestador cierra ese hueco enrutando siempre hacia el skill correcto
y garantizando que **la salida de un skill sea literalmente la entrada del siguiente**
(mismos archivos bajo `resources/`, mismos IDs de HU/TT/RF/RNF, sin recrear contexto).

## ⚡ Pre-arranque: memoria de sesión

**Antes de ejecutar cualquier skill** en una sesión nueva, el orquestador invoca `memoria` (modo lectura) para:

1. Restaurar el contexto de la sesión anterior desde `resources/session/estado.json` y `contexto.md`.
2. Presentar al usuario un resumen ejecutivo de dónde quedó el proyecto.
3. Validar que el estado guardado sigue siendo consistente con el código actual (git log, archivos en `resources/`).
4. Si no hay sesión previa, inicializar `resources/session/` como primera sesión.

Si `memoria` detecta que el proyecto ya está en una fase avanzada (ej. `fase_actual: ingenieria`), el orquestador **no** debe sugerir volver a fases tempranas del pipeline a menos que el usuario lo pida explícitamente. La memoria es la brújula que evita repetir trabajo.

## Regla de oro: contrato de carpetas `resources/`

Todos los skills — de ambos kits — leen y escriben bajo `resources/` en la raíz del
proyecto destino. Antes de correr cualquier skill, verifica qué existe ya en:

```
resources/
├── functional/requests/     # RF de janus            → entrada de refinador, desglosador
├── functional/reqs/         # necesidades refinadas   → refinador escribe, desglosador lee
├── architecture/definitions/# RNF/RT de janus         → entrada de archi, genesis
├── design/models/           # RD de janus             → entrada de figma-prd-mockups, archi
├── summary/                 # resumen ejecutivo janus → contexto para archi Caso A
├── functional/hu/           # HU/TT de desglosador    → entrada de figma-prd-mockups, builder
├── diseno/                  # mockups/handoff figma    → entrada de builder (UI) y front
├── architecture/            # documento + diagramas archi → entrada de genesis, builder
├── qa/                      # planes/evidencia qa      → entrada de revision-calidad, entrega-continua
├── security/                # hallazgos seguridad      → entrada de entrega-continua (gate)
├── engineering/             # evidencia de disciplina  → usado por los skills de ingeniería
└── session/                 # NUEVO — memoria entre sesiones (memoria) + fuente para vault Obsidian (obsidian)
    ├── estado.json          # estado actual del proyecto (machine-readable)
    ├── contexto.md          # resumen narrativo para agentes y humanos
    ├── bitacora.md          # historial cronológico de sesiones
    └── learning/            # lecciones aprendidas (LNN-*.md)
```

Se agrega una carpeta nueva, **`resources/engineering/`**, como contrato de salida de la
capa de disciplina de ingeniería (no existía en el kit original de Erick porque ese kit
no bajaba hasta ese nivel):

```
resources/engineering/
├── plans/plan-<slice>.md        # tdd-implementacion: plan de slices verticales
├── tests/coverage-<modulo>.md   # tdd-implementacion: evidencia red-green-refactor
├── reviews/review-<PR>.md       # revision-calidad: hallazgos de 5 ejes + severidad
├── security/hardening-<modulo>.md # seguridad-rendimiento
├── perf/budget-<modulo>.md      # seguridad-rendimiento (Core Web Vitals / backend)
├── adr/ADR-<n>-<titulo>.md      # documentacion-observabilidad
├── observability/plan-<modulo>.md
└── release/checklist-<version>.md # entrega-continua
```

Cada skill nuevo referenciado abajo declara explícitamente qué lee de esa estructura y
qué escribe, siguiendo el mismo estilo que `janus`/`archi`/`builder` ya usan.

## Árbol de decisión (fusionado)

```
Llega una tarea
│
├── ¿Hay un documento de RFP / TDR / requerimientos de cliente sin procesar?
│     └──→ janus  (extrae RF/RNF/RT/RD a resources/)
│
├── ¿Hay una necesidad de negocio ambigua en texto libre, o un RF de janus
│    que necesita afinarse antes de poder actuar sobre él?
│     └──→ refinador  (eliciación iterativa → especificación verificable)
│         (si la ambigüedad es sobre todo de PRODUCTO/alcance más que de
│          requisito puntual, complementa con `interview-me` o `idea-refine`
│          de .github/skills-addy/skills/ — ver "Cuándo usar el kit addy en
│          fase Define" más abajo)
│
├── ¿Hay una épica de Jira (o un RF ya elicitado) para descomponer en
│    historias de usuario / tareas técnicas?
│     └──→ desglosador  (desglose HU/TT/subtareas, sube a Jira o guarda .md)
│
├── ¿Hay HU/RF listas y se necesitan pantallas/mockups antes de programar?
│     └──→ figma-prd-mockups  (Figma o Excalidraw, un mockup por pantalla)
│
├── ¿Se necesita dirección visual/distintiva para la UI (paleta de colores,
│    tipografía, layout, diseño intencional que no lea como template genérico)?
│     └──→ front  (guía de diseño visual: paleta, tipografía, espaciado,
│           dirección estética — complementa a figma-prd-mockups, no lo reemplaza)
│
├── ¿Hace falta diseñar, documentar, auditar o modernizar la arquitectura
│    (Caso A nuevo / Caso B AS-IS / Caso C AS-IS→TO-BE), incluyendo ML/IA
│    o comparativas multi-nube?
│     └──→ archi  (documento de arquitectura, C4, ADRs iniciales, costos)
│
├── ¿El documento de archi es Caso A (greenfield) y el repo aún no existe
│    o está vacío?
│     └──→ genesis  (bootstrap del repositorio real: manifiestos, capas,
│                     plomería base, documentos vivos de resources/)
│
├── ¿Hay una HU/TT/Épica de Jira (o .md en resources/functional/hu/) y se
│    necesita el scaffold de un módulo de dominio nuevo?
│     └──→ builder  (CRUD o pipeline ML, agnóstico de stack)
│         └── Salida de builder = ENTRADA de la capa de disciplina ↓↓↓
│
├── ── A partir de aquí el código ya existe (por builder, genesis, o ya
│      preexistía en el repo). Aplica la capa de disciplina de ingeniería: ──
│
│  ├── ¿Se va a escribir/modificar lógica dentro del scaffold?
│  │     └──→ tdd-implementacion  (slices verticales + red-green-refactor;
│  │           envuelve incremental-implementation + test-driven-development)
│  │
│  ├── ¿`builder` activó el modo "Pipeline de Machine Learning" y
│  │    `tdd-implementacion` acaba de producir artifacts/metrics/ nuevos
│  │    (un modelo entrenado, baseline o candidato)?
│  │     └──→ validacion-cientifica-ml  (leakage, McNemar/DeLong, calibración,
│  │           equidad por subgrupo, model card)
│  │         ├── ❌ hallazgo bloqueante → vuelve a tdd-implementacion a corregir
│  │         │      el pipeline, NO continúa a qa/entrega-continua
│  │         └── ✅ sin bloqueantes → continúa el flujo normal
│  │
│  ├── ¿El usuario pide "desplegar la demo" o cerrar el modelo como definitivo?
│  │     └──→ GATE: validacion-cientifica-ml sin bloqueantes pendientes para ESE
│  │           modelo antes de entrega-continua (re-ejecutar si el modelo cambió)
│  │
│  ├── ¿Se necesita contexto de librería/framework verificado contra fuentes
│  │    oficiales antes de codear, o cargar el contexto correcto de sesión?
│  │     └──→ usar directamente .github/skills-addy/skills/source-driven-development
│  │           y .github/skills-addy/skills/context-engineering
│  │
│  ├── ¿La decisión es de alto riesgo, en código desconocido, o irreversible?
│  │     └──→ usar directamente .github/skills-addy/skills/doubt-driven-development
│  │
│  ├── ¿Hay que grabar/ejecutar pruebas E2E de UI, generar evidencia en video,
│  │    o correr un runbook de QA en Markdown?
│  │     └──→ qa  (complementa con browser-testing-with-devtools de addy
│  │           para inspección en vivo del DOM/consola/red durante la grabación)
│  │
│  ├── ¿Hay artefactos de documentación nuevos o actualizados en resources/ y
│  │    el usuario quiere navegarlos como grafo de conocimiento?
│  │     └──→ obsidian  (exporta/actualiza el vault de Obsidian con los artefactos
│  │           de la fase actual: convierte a notas con frontmatter, wikilinks,
│  │           tags y genera/actualiza Mapas de Contenido)
│  │
│  ├── ¿Algo falló (test, build, comportamiento inesperado)?
│  │     └──→ usar directamente .github/skills-addy/skills/debugging-and-error-recovery
│  │
│  ├── ¿Hay un cambio listo para revisar antes de mergear?
│  │     └──→ revision-calidad  (envuelve code-review-and-quality +
│  │           code-simplification, cinco ejes + Chesterton's Fence)
│  │
│  ├── ¿Maneja input de usuario, auth, datos sensibles, o hay que medir/optimizar
│  │    performance (Core Web Vitals / backend)?
│  │     └──→ seguridad-rendimiento  (envuelve security-and-hardening +
│  │           performance-optimization)
│  │
│  ├── ¿Hay que commitear, versionar, armar el pipeline de CI/CD, desplegar,
│  │    o retirar código/features viejos?
│  │     └──→ entrega-continua  (envuelve git-workflow-and-versioning +
│  │           ci-cd-and-automation + shipping-and-launch +
│  │           deprecation-and-migration)
│  │
│  ├── ¿Hay que documentar una decisión arquitectónica (ADR) o instrumentar
│  │    logs/métricas/trazas/alertas?
│  │     └──→ documentacion-observabilidad  (envuelve documentation-and-adrs +
│  │           observability-and-instrumentation; alimenta también
│  │           resources/architecture/adr/ para que `archi` lo reutilice en
│  │           la próxima corrida de Caso C)
│  │
│  └── ¿Terminó la sesión de trabajo?
│        └──→ memoria (modo escritura) — guarda estado.json, actualiza
│              contexto.md y bitacora.md, registra lecciones aprendidas.
│              Si el usuario quiere exportar el estado final al vault:
│              obsidian (para sesiones/ y learning/)
│
│  └── ¿El proyecto es un TFM/TFG (brief_finalizacion_tfm.md o pedido
│       explícito) y hay que redactar capítulos, revisar cumplimiento
│       normativo o preparar el depósito?
│        └──→ tfm-redactor  (precondición: validacion-cientifica-ml sin
│              bloqueantes para los artefactos citados; auditoría UNIR +
│              redacción con evidencia trazable → resources/tfm/capitulos/)
│              → docx (maquetación final: portada, numeración, TOC)
```

## Secuencia completa de referencia (ciclo de vida end-to-end)

Para una iniciativa completa, de "llegó una RFP" a "está en producción":

```
 0. memoria (lectura)             restaurar contexto de sesión anterior
 1. janus                         RFP → RF/RNF/RT/RD estructurados
 2. refinador                     afina cada RF ambiguo → especificación verificable
 3. desglosador                   épica/RF → HU + TT + subtareas (Jira o .md)
    obsidian (exportar HU/TT)     convierte RF y HU a notas del vault
 4. figma-prd-mockups             HU → mockups/wireframes por pantalla
 5. archi                         RF/RNF/RD/HU → documento de arquitectura + C4 + ADRs
    obsidian (exportar arquit.)   convierte doc, ADRs, diagramas a notas del vault
 6. genesis                       (solo Caso A) documento de arquitectura → repo bootstrapeado
 7. builder                       HU/TT → scaffold del módulo (capas, modelo, API)
 8. context-engineering/          carga el contexto correcto antes de programar
    source-driven-development     (addy, uso directo)
 9. tdd-implementacion            scaffold → código con lógica real, slice a slice, TDD

 9.5 validacion-cientifica-ml     leakage → CV estratificado → McNemar/DeLong →
      ★ NUEVO (extension-tfm-ml)  calibración → equidad → trazabilidad → model card
      │                            ❌ bloqueante → vuelve a 9 · ✅ → continúa
10. doubt-driven-development      (addy, uso directo) — solo si el slice es de alto riesgo
11. qa + browser-testing-         pruebas E2E, evidencia, inspección en vivo del navegador
    with-devtools (addy)
    obsidian (exportar QA)        convierte planes y evidencia a notas del vault
12. revision-calidad              review de 5 ejes + simplificación antes de mergear
13. seguridad-rendimiento         hardening OWASP + presupuesto de performance
    obsidian (exportar hallazgos) convierte hallazgos de seguridad a notas del vault
14. documentacion-observabilidad  ADRs de decisiones tomadas en 9–13 + instrumentación

 GATE validacion-cientifica-ml   re-chequeo si el modelo cambió desde 9.5
      ★ NUEVO (extension-tfm-ml)  (nuevo hiperparámetro/split/datos → re-ejecutar)

15. entrega-continua              commit atómico, pipeline CI/CD, checklist de shipping
    obsidian (exportar release)   convierte checklist de release a nota del vault
16. memoria (escritura)           guarda estado final de la sesión, lecciones aprendidas
    obsidian (exportar sesión)    convierte bitácora y learning a notas del vault
17. tfm-redactor                  solo si hay entregable académico (TFM/TFG) ★ NUEVO
      ★ NUEVO (extension-tfm-ml)  auditoría normativa UNIR + capítulos con evidencia
                                  trazable → resources/tfm/capitulos/ → docx
```

No toda tarea recorre las 15 fases. Una corrección de bug puntual, por ejemplo, puede
resolverse solo con `debugging-and-error-recovery → tdd-implementacion →
revision-calidad → entrega-continua`.

## Reglas transversales (aplican a ambos kits, siempre)

1. **Nunca dupliques el descubrimiento.** Antes de invocar un skill, revisa si otro
   skill ya dejó la respuesta bajo `resources/`. `archi` ya define esto para su propio
   Paso 0.5/0.6; esta regla lo generaliza a todo el pipeline.
2. **Superficie de supuestos.** Antes de generar cualquier artefacto no trivial, declara
   los supuestos explícitamente (tomado del "Core Operating Behavior #1" del kit addy) y
   dale al usuario la oportunidad de corregirlos antes de continuar.
3. **No mezcles fases.** `builder` no debe "adelantarse" a escribir lógica de negocio
   compleja directamente (eso es trabajo de `tdd-implementacion`); `archi` no debe
   generar código; `tdd-implementacion` no debe rediseñar la arquitectura que ya definió
   `archi` — si detecta que la arquitectura no sirve, para y señala la inconsistencia en
   vez de improvisar un cambio silencioso.
4. **Verificación no negociable.** Cada skill de la capa de disciplina termina con
   evidencia real (tests corridos, build, salida de linter/scanner) — "parece correcto"
   nunca es suficiente. Esto es una importación directa del pack addy y se adopta para
   todo el kit unificado, no solo para esa capa.
5. **Idioma.** Los skills de negocio→arquitectura (janus…qa) producen artefactos en
   español, salvo que el proyecto destino ya esté en inglés. Los skills de disciplina
   (tdd-implementacion…entrega-continua) pueden producir código/comentarios en el idioma
   del proyecto, pero sus documentos de proceso (planes, reviews, ADRs) siguen la misma
   convención que el resto de `resources/`.

## Cuándo usar el kit addy directamente, sin wrapper en español

Los siguientes skills de `.github/skills-addy/skills/` se usan **tal cual, en inglés**,
sin un bridge dedicado, porque no chocan con el contrato de `resources/` de Erick y
traducirlos no agrega valor real:

- `interview-me`, `idea-refine` — técnicas de elicitación de producto, complementarias a
  `refinador` (que es más formal/verificable); útiles cuando la ambigüedad es de visión de
  producto y no de un requisito puntual.
- `context-engineering`, `source-driven-development` — se consultan antes de que
  `tdd-implementacion` empiece a escribir código.
- `doubt-driven-development` — revisión adversarial puntual sobre una decisión ya tomada.
- `debugging-and-error-recovery`, `browser-testing-with-devtools` — troubleshooting y
  verificación en vivo, complementan a `qa`.
- `frontend-ui-engineering`, `api-and-interface-design` — guía de calidad de UI/API que
  `tdd-implementacion` invoca cuando el slice que está implementando es de UI o de API
  pública, respectivamente.

## Qué producir al terminar de orquestar

Al decidir la ruta, deja constancia breve (2-4 líneas) de: qué skill(s) vas a invocar, en
qué orden, y qué archivo(s) de `resources/` estás leyendo como entrada — antes de invocar
el primer skill. Esto reemplaza cualquier necesidad de volver a preguntarle al usuario
"¿qué querés que haga?" cuando la respuesta ya está en el árbol de decisión de arriba.
