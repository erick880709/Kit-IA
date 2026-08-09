---
name: obsidian
description: Gestiona vaults de Obsidian (https://obsidian.md) como destino de documentación del kit. Convierte artefactos de resources/ (documentos de arquitectura, ADRs, HU/TT, planes de QA, lecciones aprendidas) en notas de Obsidian con frontmatter YAML, wikilinks [[...]], tags, backlinks y Mapas de Contenido (MOC). Úsala cuando el usuario pida "exportar a Obsidian", "crear vault del proyecto", "generar notas de la arquitectura", "vincular los ADRs en Obsidian", "sincronizar con mi vault", o cuando quiera navegar la documentación del proyecto como un grafo de notas interconectadas estilo Zettelkasten.
---

# Obsidian — Integración con Vaults de Conocimiento

## Propósito

El kit genera documentación rica bajo `resources/`: documentos de arquitectura, ADRs, historias de usuario, planes de prueba, lecciones aprendidas. Pero esa documentación está en Markdown plano — no tiene links bidireccionales, ni tags consistentes, ni una forma de navegarla como un grafo de conocimiento.

Este skill convierte los artefactos de `resources/` en **notas de Obsidian** — archivos Markdown con frontmatter YAML, wikilinks `[[...]]`, tags jerárquicos (`#arquitectura/adr`), y Mapas de Contenido (MOC) que permiten navegar el proyecto como un segundo cerebro digital.

## Cuándo usarlo

- **Al iniciar un proyecto**: crear la estructura base del vault en paralelo a `resources/`.
- **Al finalizar una fase**: exportar los artefactos generados (ej. después de `archi`, exportar documento + ADRs + diagramas).
- **Para navegación**: generar o actualizar MOCs que vinculen todas las notas relacionadas.
- **Para el equipo**: el vault se puede compartir por Git (es solo una carpeta de archivos `.md`) y cada miembro lo abre con Obsidian.

## Estructura del vault generado

```
vault-proyecto/
├── .obsidian/                        # Configuración de Obsidian (no tocar si usás un vault existente)
├── 000-Inicio.md                     # Nota de entrada: qué es este vault, cómo navegarlo
├── 010-MOC-Proyecto.md               # Mapa de Contenido raíz
├── arquitectura/
│   ├── Documento_Arquitectura.md     # El documento completo, seccionado o linkeado
│   ├── ADR/
│   │   ├── ADR-001-seleccion-cloud.md
│   │   └── ADR-002-base-de-datos.md
│   ├── diagramas/
│   │   └── (referencias a los .drawio y .png exportados)
│   └── C4/
│       ├── Contexto.md
│       ├── Contenedores.md
│       └── Componentes.md
├── requerimientos/
│   ├── RF/
│   │   └── RF-001.md .. RF-NNN.md
│   ├── RNF/
│   │   └── RNF-001.md .. RNF-NNN.md
│   └── HU/
│       ├── HU-001.md .. HU-NNN.md
│       └── TT-001.md .. TT-NNN.md
├── ingenieria/
│   ├── planes/
│   ├── reviews/
│   ├── seguridad/
│   └── releases/
├── sesiones/
│   ├── contexto.md
│   ├── bitacora.md
│   └── learning/
│       └── LNN-001.md .. LNN-NNN.md
├── templates/                        # Plantillas de notas para nuevos artefactos
│   ├── tpl-arquitectura.md
│   ├── tpl-adr.md
│   ├── tpl-hu.md
│   └── tpl-learning.md
└── assets/                           # Imágenes, diagramas exportados como PNG
    └── (capturas de .drawio exportadas)
```

## Paso 1 — Detectar el vault destino

1. Pregunta al usuario si ya tiene un vault de Obsidian para este proyecto:
   - **"¿Ya tenés un vault de Obsidian para este proyecto, o querés que cree uno nuevo?"**
2. Si ya existe:
   - Pregunta la ruta absoluta al vault (ej. `C:\Users\...\vault-proyecto` o `~/Documents/obsidian/proyecto`).
   - **Nunca sobrescribas** archivos `.md` existentes sin preguntar. Si un archivo ya existe, ofrecé: sobrescribir, mergear (agregar secciones nuevas al final), o saltar.
   - No toques la carpeta `.obsidian/` a menos que el usuario pida explícitamente configurar plugins/themes.
3. Si no existe o el usuario pide uno nuevo:
   - Crea la carpeta `vault-proyecto/` en la raíz del repositorio o donde el usuario indique.
   - Inicializa `.obsidian/` solo si el usuario quiere (recomendado: no lo hagas automáticamente; Obsidian lo genera al abrir la carpeta como vault).

## Paso 2 — Convertir artefactos de resources/ a notas de Obsidian

### Formato de nota estándar

Toda nota generada por este skill usa este esqueleto:

```markdown
---
fecha: 2026-08-09
tags:
  - arquitectura
  - adr
  - base-de-datos
aliases:
  - "ADR 002"
  - "Decisión de base de datos"
proyecto: "Nombre del Proyecto"
fase: arquitectura
origen: "[[Documento_Arquitectura]]"
---

# ADR-002: Selección de Base de Datos

## Contexto
...

## Decisión
...

## Consecuencias
...

## Relacionado
- [[ADR-001-seleccion-cloud|ADR-001: Selección de Nube]]
- [[RF-005|RF-005: Persistencia de datos de usuario]]
- [[Documento_Arquitectura|Documento de Arquitectura §9: Modelo de Datos]]
```

### Reglas de conversión

1. **Frontmatter YAML**: todo archivo lo tiene. Campos mínimos: `fecha`, `tags`, `proyecto`.
2. **Wikilinks**: cada referencia a otro artefacto del proyecto USA `[[...]]`:
   - `[[ADR-001-seleccion-cloud]]` — link a nota existente
   - `[[ADR-001-seleccion-cloud|ADR-001: Selección de Nube]]` — con alias descriptivo
   - `[[Documento_Arquitectura#seccion-9-modelo-de-datos|Modelo de Datos]]` — link a heading específico
3. **Tags**: jerárquicos con `#` y `/` como separador:
   - `#arquitectura/adr` para ADRs
   - `#requerimientos/funcional` para RF
   - `#ingenieria/qa` para planes de prueba
   - `#sesion/learning` para lecciones aprendidas
4. **Aliases**: nombres alternativos para búsqueda (ej. el ID corto y el título largo).
5. **Sección "Relacionado"**: al final de cada nota, lista de wikilinks a notas relacionadas (backlinks manuales — Obsidian también genera backlinks automáticos, pero los explícitos son más confiables).

### Qué convertir y cuándo

| Artefacto en `resources/` | Nota(s) en vault | Cuándo |
|---|---|---|
| `architecture/Documento_Arquitectura_*.md` | `arquitectura/Documento_Arquitectura.md` + secciones como notas separadas si son muy largas | Después de `archi` |
| `architecture/adr/ADR-*.md` | `arquitectura/ADR/ADR-*.md` | Después de `documentacion-observabilidad` |
| `functional/requests/RF-*.md` | `requerimientos/RF/RF-*.md` | Después de `janus` |
| `functional/hu/HU-*.md` y `TT-*.md` | `requerimientos/HU/HU-*.md` y `TT-*.md` | Después de `desglosador` |
| `qa/*.md` | `ingenieria/qa/*.md` | Después de `qa` |
| `engineering/reviews/*.md` | `ingenieria/reviews/*.md` | Después de `revision-calidad` |
| `engineering/security/*.md` | `ingenieria/seguridad/*.md` | Después de `seguridad-rendimiento` |
| `engineering/release/*.md` | `ingenieria/releases/*.md` | Después de `entrega-continua` |
| `session/contexto.md`, `learning/*.md` | `sesiones/` (espejo directo) | Al final de cada sesión (`memoria`) |
| Diagramas `.drawio` | `arquitectura/diagramas/` (el `.drawio`) + export PNG a `assets/` | Después de `archi` |

## Paso 3 — Generar Mapas de Contenido (MOC)

Un MOC es una nota cuyo único propósito es **vincular otras notas** sobre un mismo tema. Es el índice navegable del vault.

### MOC raíz (`010-MOC-Proyecto.md`)

```markdown
---
fecha: 2026-08-09
tags: [moc, indice]
proyecto: "Nombre del Proyecto"
---

# 🗺️ Mapa de Contenido — Nombre del Proyecto

## Arquitectura
- [[Documento_Arquitectura|Documento de Arquitectura]]
- **ADRs**: [[ADR-001-seleccion-cloud]], [[ADR-002-base-de-datos]]
- **Diagramas**: [[C4-Contexto]], [[C4-Contenedores]], [[Despliegue-AWS]]

## Requerimientos
- **Funcionales**: [[MOC-Requerimientos-Funcionales]]
- **No Funcionales**: [[MOC-Requerimientos-No-Funcionales]]
- **Historias de Usuario**: [[MOC-HU]]

## Ingeniería
- **Planes**: ...
- **QA**: [[Plan-Pruebas-HU-01]]
- **Seguridad**: [[Hardening-API-Auth]]
- **Releases**: [[Checklist-v1.0.0]]

## Sesiones
- [[Contexto|Estado actual del proyecto]]
- **Lecciones**: [[MOC-Lecciones-Aprendidas]]
```

### MOCs temáticos

Genera un MOC para cada agrupación lógica cuando haya más de 5 notas sobre el mismo tema:
- `MOC-HU.md`: índice de todas las historias de usuario, agrupadas por épica
- `MOC-ADRs.md`: índice cronológico de ADRs con decisión resumida en una línea
- `MOC-Lecciones-Aprendidas.md`: índice de lecciones por categoría y severidad

## Paso 4 — Plantillas (templates/)

Crea templates reutilizables en `templates/` para que el equipo pueda generar nuevas notas consistentes desde Obsidian (`Ctrl+N` → elegir template):

- **`tpl-adr.md`**: esqueleto de ADR con secciones Contexto/Decisión/Alternativas/Consecuencias
- **`tpl-hu.md`**: esqueleto de historia de usuario con criterios de aceptación
- **`tpl-learning.md`**: esqueleto de lección aprendida
- **`tpl-sesion.md`**: esqueleto de nota de sesión (para bitácora manual)

## Paso 5 — Integración con graphify

Si `graphify` está instalado en el proyecto (como lo está en este kit), ofrecé generar un grafo complementario:

```bash
/graphify . --obsidian --obsidian-dir vault-proyecto
```

Esto genera `graphify-out/` dentro del vault con `graph.json`, `graph.html` y `GRAPH_REPORT.md`, permitiendo navegar el vault como grafo interactivo además de como notas interconectadas.

**Pero ojo**: `--obsidian` de graphify escribe en la raíz del vault. Si el vault ya tiene contenido, los archivos generados no pisan nada existente (graphify escribe en `graphify-out/`), pero los nodos del grafo incluirán TODO el vault. Si el vault es grande, el grafo puede ser pesado — avisale al usuario.

## Integración con el orquestador

El `orquestador` invoca este skill:
- **Al final de cada fase del pipeline** (después de `archi`, después de `desglosador`, etc.) para exportar los artefactos generados.
- **Cuando el usuario lo pide explícitamente**: "exportá todo a Obsidian", "actualizá el vault".
- **Al final del proyecto** (`entrega-continua`): exportación completa y generación de MOC final.

## Convivencia con resources/

| `resources/` | Vault Obsidian |
|---|---|
| Fuente de verdad canónica | Vista navegable, enriquecida con links y tags |
| Estructura plana por tipo de artefacto | Estructura navegable con MOCs y wikilinks |
| Consumido por los skills del kit | Consumido por humanos explorando el proyecto |
| Un solo archivo por artefacto | Mismo contenido, reformateado con frontmatter + links |
| Se versiona en Git | Se versiona en Git (son archivos `.md`) |

**Regla de oro**: `resources/` es la fuente de verdad. El vault es un **espejo enriquecido**, no un reemplazo. Si hay conflicto, `resources/` gana. Nunca edites un artefacto en el vault y esperes que `resources/` se actualice solo — el flujo es unidireccional: `resources/` → vault.

## Anti-patrones

1. **No crees un vault sin preguntar la ruta.** El usuario puede tener su vault en cualquier lado (Documents, Nextcloud, iCloud, Git repo separado).
2. **No generes notas vacías "por si acaso".** Solo creá notas para artefactos que realmente existen en `resources/`.
3. **No dupliques contenido.** Si una nota ya existe, actualizala (mergeá secciones nuevas) en vez de crear una segunda nota con sufijo `-1`.
4. **No asumas que el usuario usa Obsidian.** Preguntá primero. Algunos usan Logseq, Notion, o nada. Este skill es específico para Obsidian — no intentes adaptarlo a otras herramientas.
