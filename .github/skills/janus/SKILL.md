---
name: janus
description: Extrae requerimientos funcionales, no funcionales, requisitos técnicos, información de diseño y contexto de soporte desde documentos de RFP (PDF, HTML, TXT, Excel, PowerPoint o Markdown), y genera archivos Markdown organizados en resources/functional/requests, resources/architecture/definitions, resources/design/models y resources/summary. Usa esta skill SIEMPRE que el usuario mencione "RFP", "solicitud de propuesta", "términos de referencia", "TDR", "bases de licitación", pida "extraer requerimientos", "analizar una RFP", "sacar requisitos funcionales/no funcionales de un documento", o suba un documento de licitación/propuesta para evaluación como arquitecto de software. También aplica si el usuario pide preparar insumos para iniciar un proyecto de software a partir de un documento de requerimientos de cliente, aunque no use la palabra "RFP" explícitamente.
---

# Janus — RFP Requirements Extractor

Skill para arquitectos de software que reciben documentos de RFP (Request for Proposal) y necesitan
extraer de forma estructurada los requerimientos funcionales, no funcionales, requisitos técnicos,
definiciones de diseño e información de soporte, dejando todo organizado en archivos Markdown listos
para alimentar el arranque de un proyecto de software.

## Cuándo usar esta skill

- El usuario sube un archivo de RFP (PDF, HTML, TXT, XLSX/XLS, PPTX/PPT o MD) y pide evaluarlo,
  analizarlo o extraer requerimientos.
- El usuario pide "sacar los requisitos funcionales y no funcionales" de un documento.
- El usuario pide preparar la base documental (`resources/...`) para iniciar un proyecto de software
  a partir de un documento de cliente.

No uses esta skill para tareas simples de una sola línea que no involucren un documento real (ej.
"dame un ejemplo de requerimiento funcional" sin documento de por medio — eso se responde directo).

## Flujo de trabajo

1. **Leer el documento fuente** según su formato (ver sección "Lectura por formato").
2. **Analizar y clasificar** todo el contenido relevante en 4 categorías (ver "Criterios de
   clasificación").
3. **Asignar IDs** consecutivos por categoría, revisando primero si ya existen archivos previos en las
   carpetas de destino para no duplicar numeración (ver "Numeración y anti-colisión").
4. **Generar un archivo Markdown por cada requerimiento individual** usando las plantillas de la
   sección "Plantillas de salida", guardándolo en la carpeta que corresponda.
5. **Generar el resumen ejecutivo** consolidado en `resources/summary/executive-summary.md`.
6. **Presentar al usuario** un resumen en el chat: cuántos requerimientos de cada tipo se extrajeron,
   dónde quedaron guardados, y cualquier vacío o ambigüedad detectada en el RFP (información faltante,
   requisitos contradictorios, secciones poco claras).

Trabaja siempre sobre una copia editable: crea los archivos directamente bajo el `resources/` del
directorio de trabajo actual del usuario (ruta relativa, no absoluta), creando las carpetas si no
existen.

## Estructura de carpetas de salida

```
resources/
├── functional/
│   └── requests/                  # Requerimientos funcionales (uno por archivo)
├── architecture/
│   └── definitions/                # Requisitos técnicos + requerimientos NO funcionales
├── design/
│   └── models/                     # Información de diseño (UI/UX, modelos de datos, diagramas)
└── summary/
    └── executive-summary.md        # Resumen ejecutivo del RFP (archivo único)
```

> **Nota de criterio:** el usuario definió explícitamente 3 carpetas (funcional, arquitectura, diseño).
> Los requerimientos **no funcionales** (rendimiento, seguridad, disponibilidad, escalabilidad,
> usabilidad, etc.) no tenían carpeta propia asignada; por defecto esta skill los coloca junto con los
> requisitos técnicos en `resources/architecture/definitions/`, ya que normalmente son atributos de
> calidad con impacto arquitectónico. Si el usuario prefiere una carpeta separada (ej.
> `resources/architecture/non-functional/`), ajusta esta skill o dilo explícitamente en la solicitud.

## Lectura por formato

Antes de leer el archivo, consulta la skill correspondiente para hacerlo correctamente:

| Formato | Skill / método a usar |
|---|---|
| `.pdf` | Consulta `/skills/pdf/SKILL.md` (extracción de texto/tablas; rasterizar páginas si es un PDF escaneado) |
| `.docx` | Consulta `/skills/docx/SKILL.md` |
| `.pptx` / `.ppt` | Consulta `/skills/pptx/SKILL.md` (incluye notas del orador, que suelen tener contexto valioso) |
| `.xlsx` / `.xls` / `.csv` | Consulta `/skills/xlsx/SKILL.md` (los RFP en Excel suelen traer matrices de requisitos por fila) |
| `.html` | Lee el archivo directamente con `view` o `bash_tool` (extraer texto ignorando markup, prestando atención a tablas) |
| `.txt` / `.md` | Lee el archivo directamente con `view` |

Si el archivo fue subido, primero revisa `/skills/file-reading/SKILL.md` para decidir la
herramienta correcta según si el contenido ya está o no en el contexto.

Para PDF/PPTX/XLSX presta especial atención a:
- Tablas de requisitos (suelen venir en formato tabular con columnas tipo ID/Descripción/Prioridad).
- Anexos técnicos (infraestructura, integraciones, SLAs).
- Diagramas o wireframes incluidos como imágenes (descríbelos en el archivo de diseño correspondiente).

## Criterios de clasificación

Clasifica cada fragmento de información relevante del RFP en una de estas 4 categorías. Ante duda,
prioriza la categoría más específica (técnico/diseño) sobre la genérica (funcional).

### 1. Requerimiento funcional → `resources/functional/requests/`
Describe **qué debe hacer el sistema** desde la perspectiva del usuario o del negocio: procesos,
reglas de negocio, casos de uso, flujos, roles y permisos, reportes, integraciones funcionales
("el sistema debe permitir...", "el usuario podrá...").

### 2. Requisito técnico o no funcional → `resources/architecture/definitions/`
Incluye:
- **Requisitos técnicos**: stack tecnológico exigido/sugerido, infraestructura, ambientes,
  integraciones a nivel de sistema, estándares, normativas de cumplimiento, requisitos de seguridad,
  arquitectura esperada, restricciones de licenciamiento.
- **Requerimientos no funcionales**: rendimiento, escalabilidad, disponibilidad/SLA, seguridad,
  usabilidad medible, mantenibilidad, portabilidad, capacidad, tiempos de respuesta.

### 3. Información de diseño → `resources/design/models/`
Todo lo relacionado con la forma/presentación del software: lineamientos de UI/UX, identidad visual,
wireframes o mockups mencionados/adjuntos, modelos de datos o entidades si el RFP los define,
diagramas de procesos o de arquitectura visual incluidos como referencia de diseño.

### 4. Información de soporte / contexto → resumen ejecutivo (`resources/summary/executive-summary.md`)
Todo lo que no es un requisito en sí pero es necesario para entender el proyecto: nombre del cliente,
alcance general, objetivos del proyecto, plazos, presupuesto o modelo de contratación, criterios de
evaluación de la propuesta, stakeholders, entregables esperados, supuestos y restricciones generales,
glosario de términos del dominio.

## Numeración y anti-colisión

Antes de crear archivos nuevos, revisa si las carpetas de destino ya tienen archivos de una extracción
previa (`ls resources/functional/requests/`, etc.). Si existen, continúa la numeración desde el máximo
ID existente por prefijo, no reinicies desde 1. Si es la primera vez, comienza en 001.

Prefijos de ID:
- `RF-###` → Requerimiento funcional
- `RNF-###` → Requerimiento no funcional
- `RT-###` → Requisito técnico
- `RD-###` → Información de diseño

## Convención de nombres de archivo

Un archivo por requerimiento, con slug corto y descriptivo derivado del título:

```
{ID}-{slug-corto-en-minusculas}.md
```

Ejemplos:
- `resources/functional/requests/RF-001-gestion-de-usuarios.md`
- `resources/architecture/definitions/RNF-003-tiempo-respuesta-consultas.md`
- `resources/architecture/definitions/RT-002-integracion-erp-sap.md`
- `resources/design/models/RD-001-lineamientos-marca.md`

El slug: minúsculas, sin tildes ni caracteres especiales, palabras separadas por guiones, máximo ~6
palabras.

## Plantillas de salida

Todo el contenido de los archivos .md se redacta **en español**, independientemente del idioma del
documento fuente (traduce si el RFP viene en otro idioma, conservando términos técnicos en inglés
cuando sea el estándar de la industria, ej. "SLA", "API").

### Requerimiento funcional (RF)

```markdown
# RF-{n}: {Título del requerimiento}

**Tipo:** Requerimiento funcional
**Fuente:** {sección/página/anexo del RFP donde aparece}
**Prioridad:** {Alta/Media/Baja — solo si el RFP la especifica; si no, "No especificada"}

## Descripción
{Descripción clara y completa del requerimiento, redactada en tercera persona o como declaración
del sistema. Si el RFP lo redactó de forma ambigua, aclara la interpretación asumida.}

## Actores involucrados
{Roles o usuarios que interactúan con este requerimiento, si se identifican}

## Criterios de aceptación
{Si el RFP los define explícitamente, listarlos. Si no, escribir "No especificados en el RFP —
 definir con el cliente."}

## Dependencias / relacionados
{Otros RF/RNF/RT relacionados, si aplica}

## Notas del analista
{Ambigüedades, vacíos de información, supuestos hechos al interpretar el RFP}
```

### Requerimiento no funcional / requisito técnico (RNF / RT)

```markdown
# {RNF|RT}-{n}: {Título}

**Tipo:** {Requerimiento no funcional | Requisito técnico}
**Categoría:** {Rendimiento/Seguridad/Disponibilidad/Escalabilidad/Stack tecnológico/Infraestructura/
Integración/Cumplimiento normativo/Otro}
**Fuente:** {sección/página/anexo del RFP}

## Descripción
{Descripción del requisito}

## Criterio medible / restricción concreta
{Valores concretos si el RFP los da: ej. "tiempo de respuesta < 2s con 500 usuarios concurrentes",
 "disponibilidad 99.9%", "debe desplegarse en AWS". Si no hay valores concretos, indicarlo.}

## Impacto en la arquitectura
{Breve nota de qué implica este requisito para el diseño de la solución}

## Notas del analista
{Ambigüedades o vacíos detectados}
```

### Información de diseño (RD)

```markdown
# RD-{n}: {Título}

**Tipo:** Información de diseño
**Fuente:** {sección/página/anexo del RFP}

## Descripción
{Lineamiento, modelo o referencia de diseño extraído}

## Elementos de referencia
{Wireframes, mockups, paletas de color, entidades del modelo de datos, diagramas mencionados;
 si el original incluye imágenes, descríbelas aquí}

## Notas del analista
{Ambigüedades o vacíos detectados}
```

### Resumen ejecutivo (`resources/summary/executive-summary.md`, archivo único y consolidado)

```markdown
# Resumen Ejecutivo — {Nombre del proyecto/RFP}

**Cliente:** {si se identifica}
**Fecha del documento:** {si se identifica}
**Documento fuente:** {nombre de archivo original}

## Objetivo y alcance del proyecto
{Síntesis del objetivo general y alcance descrito en el RFP}

## Plazos
{Cronograma, fechas límite de entrega de propuesta, duración estimada del proyecto}

## Presupuesto / modelo de contratación
{Si se especifica: monto, rango, modalidad (fijo, por horas, T&M, etc.)}

## Criterios de evaluación de la propuesta
{Cómo se evaluará la propuesta del proveedor, si el RFP lo indica}

## Stakeholders identificados
{Roles/áreas del cliente involucradas}

## Entregables esperados
{Lista de entregables que pide el RFP}

## Supuestos y restricciones generales
{Supuestos hechos por el analista, restricciones explícitas del RFP}

## Glosario
{Términos de dominio específicos del cliente/industria que aparecen en el RFP}

## Resumen cuantitativo de la extracción
- Requerimientos funcionales extraídos: {n}
- Requerimientos no funcionales extraídos: {n}
- Requisitos técnicos extraídos: {n}
- Información de diseño extraída: {n}

## Vacíos y riesgos detectados
{Información que el RFP no cubre y que normalmente se necesita para arrancar el proyecto: ej. no
 define ambiente de hosting, no define volumetría de datos, no define integraciones existentes, etc.}
```

## Reporte final al usuario

Al terminar, responde en el chat (no solo en archivos) con:
1. Tabla resumen de cantidades por categoría.
2. Rutas de las carpetas generadas.
3. Lista breve (3-6 puntos) de vacíos o ambigüedades más relevantes detectados en el RFP, para que el
   usuario decida cómo resolverlos con el cliente.

No repitas el contenido completo de cada archivo en el chat; el valor está en los archivos generados.
