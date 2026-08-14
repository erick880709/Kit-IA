# 🧠 Kit IA — Pipeline de Desarrollo Spec-Driven con Agentes de IA

<p align="center">
  <a href="https://github.com/erick880709/Kit-IA/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/erick880709/Kit-IA"><img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version 1.0.0"></a>
  <a href="https://github.com/erick880709/Kit-IA/stargazers"><img src="https://img.shields.io/github/stars/erick880709/Kit-IA?style=flat" alt="Stars"></a>
  <a href="https://github.com/erick880709/Kit-IA/blob/main/CONTRIBUTING.md"><img src="https://img.shields.io/badge/contribuciones-bienvenidas-brightgreen.svg" alt="Contribuciones bienvenidas"></a>
  <a href="https://github.com/erick880709/Kit-IA/blob/main/SECURITY.md"><img src="https://img.shields.io/badge/security-policy-blue.svg" alt="Security Policy"></a>
</p>

> **De RFP a producción, sin perder contexto entre sesiones.**
> 22 skills de IA orquestados que cubren el ciclo completo de desarrollo de software:
> desde la extracción de requerimientos hasta el despliegue continuo, pasando por
> arquitectura, scaffold, TDD, QA, seguridad, documentación y memoria entre sesiones.

---

## ¿Qué es Kit IA?

Kit IA es un **sistema de habilidades (skills) para asistentes de IA** como GitHub Copilot, Claude Code o Cursor. Cada skill es una instrucción especializada que guía al asistente en una fase específica del desarrollo de software. El `orquestador` — un meta-skill — decide automáticamente qué skill ejecutar según la tarea que describas en lenguaje natural.

**No necesitás saber qué skill invocar.** Decí "necesito diseñar la arquitectura de este proyecto" y el `orquestador` enruta a `archi`. Decí "revisame este PR" y va a `revision-calidad`. El kit resuelve la ruta por vos.

## 🚀 Instalación (30 segundos)

```bash
# 1. Copiá la carpeta .github/ a la raíz de tu proyecto
cp -r kit-ia/.github/ tu-proyecto/

# 2. (Opcional) Instalá el grafo de conocimiento para navegar el codebase
pip install graphifyy
graphify install --project

# 3. Abrí tu asistente de IA y describí tu tarea en lenguaje natural
```

**Requisitos previos:**
- GitHub Copilot, Claude Code, Cursor, o cualquier asistente compatible con skills en Markdown
- Python 3.10+ (solo para `graphify`; el resto del kit funciona sin dependencias)

---

## 🗺️ Pipeline SDD completo

El kit cubre las **5 fases** del desarrollo Spec-Driven, con **16 pasos** orquestados automáticamente:

```
 PRE-ARRANQUE → NEGOCIO → ARQUITECTURA → SCAFFOLD → INGENIERÍA → CIERRE
┌────────┐ ┌───────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ ┌──────┐ ┌────────┐ ┌────────┐   ┌───────┐ ┌────┐ ┌────┐ ┌────────┐ ┌───────┐ ┌──────┐ ┌────────┐ ┌────────┐
│memoria │▶│ janus │▶│refinador│▶│desglos.│▶│ figma- │▶│ front │▶│archi │▶│genesis │▶│builder │──▶│  tdd-  │▶│ qa │▶│rev.│▶│seguridad│▶│ docs+ │▶│entrega │▶│memoria │
│(lect.) │ │ RFP→  │ │ afina   │ │ épica→ │ │ prd-   │ │(visual)│ │Caso  │ │bootstrap│ │scaffold│   │implemen│ │E2E │▶│cal.│▶│+perf.   │▶│ obs.  │▶│contin. │ │(escr.) │
│        │ │ RF/RNF│ │ RF      │ │HU/TT   │ │mockups │ │        │ │A/B/C │ │repo    │ │módulo  │   │tación  │ │    │ │5ej │ │OWASP    │ │ADRs   │ │git+CI  │ │        │
└────────┘ └───────┘ └────────┘ └────────┘ └────────┘ └───────┘ └──────┘ └────────┘ └────────┘   └────────┘ └────┘ └────┘ └────────┘ └───────┘ └──────┘ └────────┘ └────────┘
                                                                                  ┌──────────┐
                                                                                  │ obsidian │  exporta artefactos al vault de conocimiento
                                                                                  └──────────┘
```

### Fase 0 — Pre-arranque
| Skill | Función |
|---|---|
| `memoria` (lectura) | Restaura el contexto de la sesión anterior: fase activa, hitos, pendientes, decisiones abiertas |

### Fase 1 — Negocio (RFP → Requerimientos)
| # | Skill | Entrada → Salida |
|---|---|---|
| 1 | `janus` | Documento RFP (PDF, HTML, TXT, Excel, Markdown) → RF, RNF, RT, RD estructurados |
| 2 | `refinador` | RF ambiguo → especificación verificable (IA ≤ 15%) |
| 3 | `desglosador` | Épica Jira / RF refinado → Historias de Usuario + Tareas Técnicas + Subtareas |

### Fase 2 — Arquitectura (HU → Diseño)
| # | Skill | Entrada → Salida |
|---|---|---|
| 4 | `figma-prd-mockups` | HU + RD → mockups Figma/Excalidraw (una pantalla por HU) |
| 5 | `front` | Mockups → dirección visual (paleta, tipografía, espaciado, jerarquía) |
| 6 | `archi` | RF + RNF + HU + mockups → Documento de Arquitectura (C4, ADRs, multi-nube, ML/IA) |

### Fase 3 — Scaffold (Arquitectura → Código base)
| # | Skill | Entrada → Salida |
|---|---|---|
| 7 | `genesis` | Documento de Arquitectura (Caso A greenfield) → Repositorio bootstrapeado |
| 8 | `builder` | HU/TT → Scaffold del módulo (Java/Spring, C#/.NET, Python/FastAPI, Node.js, Angular) |

### Fase 4 — Ingeniería (Código → Producción)
| # | Skill | Entrada → Salida |
|---|---|---|
| 9 | `tdd-implementacion` | Scaffold → Código con lógica real (Red-Green-Refactor, slices verticales) |
| 10 | `qa` | Código → Pruebas E2E + evidencia en video (Playwright, runbooks Markdown) |
| 11 | `revision-calidad` | PR → Code review 5 ejes + simplificación |
| 12 | `seguridad-rendimiento` | Código → Hardening OWASP + presupuestos de performance |
| 13 | `documentacion-observabilidad` | Decisiones → ADRs + logs/métricas/trazas |
| 14 | `entrega-continua` | Código aprobado → Commit atómico + CI/CD + release checklist |

### Fase 5 — Cierre
| Skill | Función |
|---|---|
| `memoria` (escritura) | Guarda el estado de la sesión para la próxima: hitos, pendientes, lecciones aprendidas |
| `obsidian` | Exporta todos los artefactos a un vault de Obsidian con wikilinks, tags y MOCs |

---

## 🎯 Capacidades del kit

### 🏗️ Arquitectura de software
- **Casos A/B/C**: greenfield, AS-IS (documentación de legacy), TO-BE (evolución con gap analysis)
- **C4 Model**: Contexto, Contenedores, Componentes (Mermaid) + Código (opcional)
- **Multi-nube**: Diagramas `.drawio` con iconografía oficial AWS 2025/Q3, Azure 2025/Q2, GCP
- **Pricing**: Estimación de costos comparativa con reporte HTML
- **ML/IA**: Arquitectura de pipelines de datos, entrenamiento, inferencia, explicabilidad (SHAP/XAI)
- **Bases de datos**: Árbol de decisión SQL vs NoSQL, 6 tipos de DB, matriz ponderada, servicios cloud
- **Arquitecturas candidatas**: Evaluación con matriz de decisión antes de comprometerse a un diseño
- **Patrones**: 14 patrones de software + 12 patrones de solución + anti-patrones documentados

### 💻 Desarrollo (nivel senior)
- **Java 21 + Spring Boot 3**: Clean Architecture, MapStruct, Flyway, Testcontainers
- **C# 12 + .NET 8**: Minimal API, MediatR, FluentValidation, EF Core Fluent API
- **Python 3.12 + FastAPI**: SQLAlchemy async, Pydantic v2, Alembic, pytest
- **Node.js 22 + TypeScript 5**: Zod, Prisma, Vitest, Express 5 error handler tipado
- **Angular 18+**: Signals, standalone components, control flow syntax, lazy loading

### 🧪 Calidad
- **TDD**: Red-Green-Refactor obligatorio, slices verticales
- **QA**: Playwright E2E, evidencia en video, runbooks Markdown
- **Code Review**: 5 ejes (corrección, diseño, mantenibilidad, consistencia, testing)
- **Seguridad**: OWASP Top 10, auditoría de dependencias, gestión de secretos
- **Performance**: Core Web Vitals (frontend) + latencia/throughput (backend)

### 📋 Entregables formales
- Documentos Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`), PDF
- Documentos de arquitectura profesionales con diagramas C4, secuencia, despliegue
- ADRs (Architecture Decision Records) trazables

### 🧠 Memoria y conocimiento
- **Continuidad entre sesiones**: El `orquestador` + `memoria` recuerdan dónde quedó el proyecto
- **Obsidian**: Exportación automática a vault con wikilinks `[[...]]`, tags, Mapas de Contenido
- **Graphify**: Grafo de conocimiento del codebase consultable con lenguaje natural

---

## 📁 Contrato de datos: `resources/`

Todos los skills leen y escriben bajo `resources/` en la raíz del proyecto destino. Esto garantiza que **la salida de un skill sea literalmente la entrada del siguiente**, sin depender de la memoria del chat.

| Carpeta | La llena | La consume |
|---|---|---|
| `resources/functional/requests/` (RF) | `janus` | `refinador`, `desglosador`, `archi` |
| `resources/functional/reqs/` (refinadas) | `refinador` | `desglosador` |
| `resources/functional/hu/` (HU/TT) | `desglosador` | `figma-prd-mockups`, `builder`, `tdd-implementacion` |
| `resources/architecture/definitions/` (RNF/RT) | `janus` | `archi`, `genesis`, `seguridad-rendimiento` |
| `resources/architecture/` (documento, C4, ADRs) | `archi` | `genesis`, `builder`, `tdd-implementacion` |
| `resources/architecture/adr/` | `archi`, `documentacion-observabilidad` | `orquestador`, `obsidian` |
| `resources/design/models/` (RD) | `janus` | `figma-prd-mockups`, `archi` |
| `resources/diseno/` (mockups) | `figma-prd-mockups` | `builder`, `front` |
| `resources/qa/` (planes, evidencia) | `qa` | `revision-calidad`, `entrega-continua` |
| `resources/security/` | `archi`, `seguridad-rendimiento` | `entrega-continua` |
| `resources/engineering/` | `tdd-implementacion`, `revision-calidad`, `seguridad-rendimiento`, `documentacion-observabilidad`, `entrega-continua` | skills siguientes en la cadena |
| `resources/session/` | `memoria` | `orquestador`, `obsidian` |
| `resources/summary/` | `janus` | `archi` (Caso A) |

---

## 🛠️ Skills incluidos (24)

### Pipeline principal (19 skills en español)

| Skill | Categoría | Trigger |
|---|---|---|
| `orquestador` | Meta | *Siempre primero* — decide la ruta automáticamente |
| `memoria` | Sesión | "¿en qué quedamos?", inicio/fin de sesión |
| `janus` | Negocio | "RFP", "solicitud de propuesta", "TDR", "bases de licitación" |
| `refinador` | Negocio | Necesidad ambigua, "afinar requerimiento", "elicitar" |
| `desglosador` | Negocio | "desglosa esta épica", "crear user stories", "breakdown" |
| `figma-prd-mockups` | Diseño | "mockups", "wireframes", "diseña las pantallas" |
| `front` | Diseño | "diseño visual", "paleta de colores", "tipografía", "look and feel" |
| `archi` | Arquitectura | "diseñar arquitectura", "diagrama C4", "documentar arquitectura", "AS-IS", "TO-BE" |
| `genesis` | Scaffold | "inicializar el repo", "crear proyecto base", "bootstrap" |
| `builder` | Scaffold | "generar scaffold", "crear módulo CRUD", "scaffold de HU" |
| `tdd-implementacion` | Ingeniería | "implementar la lógica de", "hacer TDD de", "escribir código" |
| `validacion-cientifica-ml` | ML | "validar mi modelo", "¿hay fuga de datos?", "McNemar", "model card", "auditar sesgo" |
| `qa` | Ingeniería | "pruebas E2E", "grabar evidencia", "runbook de QA" |
| `revision-calidad` | Ingeniería | "revisar PR", "code review", "¿está listo para mergear?" |
| `seguridad-rendimiento` | Ingeniería | "revisar seguridad", "OWASP", "optimizar performance", "por qué está lento" |
| `documentacion-observabilidad` | Ingeniería | "escribir ADR", "agregar logging", "métricas", "trazas" |
| `entrega-continua` | Ingeniería | "commitear", "pipeline CI/CD", "preparar release", "desplegar" |
| `tfm-redactor` | Académico | "redactar capítulo del TFM", "preparar depósito", "checklist UNIR" |
| `obsidian` | Conocimiento | "exportar a Obsidian", "crear vault", "vincular notas" |

### Skills de utilidad (5 en inglés)

| Skill | Propósito |
|---|---|
| `mcp-builder` | Construir servidores MCP (Python/TypeScript) para integrar APIs externas |
| `docx` | Crear/editar documentos Word profesionales |
| `pptx` | Crear/editar presentaciones PowerPoint |
| `xlsx` | Crear/editar hojas de cálculo Excel |
| `pdf` | Leer/extraer/crear/manipular archivos PDF |

---

## 🧭 Ejemplo: de RFP a producción en un solo flujo

```
Usuario: "Acá está la RFP de un cliente nuevo. Quiero llegar a producción."

┌─ orquestador detecta RFP sin procesar ─────────────────────────────────────┐
│                                                                            │
│  memoria (lectura)     → restaura contexto de sesión anterior              │
│  janus                 → RFP → RF-01..RF-12, RNF-01..RNF-06               │
│  refinador             → afina RF-03 (ambiguo en criterios de aceptación)  │
│  desglosador           → RF-03 → HU-01..HU-04, TT-01..TT-02 (Jira o .md)  │
│  figma-prd-mockups     → HU → mockups en Figma/Excalidraw                  │
│  front                 → refinamiento visual de los mockups                │
│  archi                 → Caso A: Documento Arquitectura + C4 + ADR-001     │
│  genesis               → bootstrap del repo (Java 21 + Spring Boot 3)      │
│  builder               → HU-01 → scaffold del módulo (Clean Architecture)  │
│  tdd-implementacion    → HU-01 → lógica real, slice a slice, TDD           │
│  qa                    → pruebas E2E con Playwright + evidencia en video   │
│  revision-calidad      → code review 5 ejes: ✅ corrección, ✅ diseño...    │
│  seguridad-rendimiento → hardening OWASP + presupuesto Core Web Vitals     │
│  doc-observabilidad    → ADR-002 + logs estructurados + métricas RED       │
│  entrega-continua      → commit atómico + CI/CD pipeline + release checklist│
│  memoria (escritura)   → guarda estado: hitos ✓, pendientes, lecciones     │
│  obsidian              → exporta todo al vault: docs, ADRs, HU, diagramas   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

Resultado: Documento de arquitectura profesional + Repositorio con código
funcional y testeado + Pipeline CI/CD + Vault Obsidian navegable.
```

---

## 🔌 Integración con herramientas existentes

| Herramienta | Integración |
|---|---|
| **GitHub Copilot** | Skills en `.github/skills/` + `.github/copilot-instructions.md` |
| **Claude Code** | Skills en `.claude/skills/` + hooks PreToolUse |
| **Jira** | `desglosador` y `builder` usan MCP de Jira para leer/generar issues |
| **Figma** | `figma-prd-mockups` genera mockups vía MCP de Figma (o Excalidraw como fallback) |
| **draw.io** | `archi` genera `.drawio` con iconografía oficial AWS/Azure/GCP |
| **Obsidian** | `obsidian` exporta `resources/` a vault con wikilinks y MOCs |
| **Graphify** | Grafo de conocimiento del codebase consultable en lenguaje natural |

---

## 📊 Roadmap

- [x] Pipeline SDD completo (RFP → producción)
- [x] Memoria entre sesiones (`memoria`)
- [x] Exportación a Obsidian (`obsidian`)
- [x] Arquitecturas candidatas con matriz de decisión (`archi`)
- [x] Competencias de bases de datos relacionales y no relacionales (`archi`)
- [x] Guías senior de desarrollo: Java/Spring, C#/.NET, Python/FastAPI, Node.js, Angular (`builder`)
- [x] Grafo de conocimiento con Graphify
- [x] Construcción de servidores MCP (`mcp-builder`)
- [ ] Migración de datos (skill dedicado)
- [ ] Dashboards y alertas post-deploy
- [ ] Aprobación formal de stakeholders (sign-off gates)
- [ ] QA para stacks no React (Angular, Vue, mobile)

---

## 🤝 Contribuir

Este kit está diseñado para ser extendido. Cada skill es un archivo Markdown con instrucciones para el asistente de IA — no requiere código compilado ni dependencias de runtime.

1. **Agregar un skill nuevo:** Creá una carpeta en `.github/skills/` con un `SKILL.md` que tenga frontmatter YAML (`name`, `description`) y el cuerpo con las instrucciones.
2. **Registrarlo en el orquestador:** Agregá una rama en el árbol de decisión de `.github/skills/orquestador/SKILL.md`.
3. **Documentarlo en el README:** Agregá una fila en la tabla de skills y en el `resources/` si corresponde.

---

## ⚙️ Requisitos del sistema

| Componente | Requisito |
|---|---|
| Asistente de IA | GitHub Copilot, Claude Code, Cursor, Codex, o compatible |
| Python | 3.10+ (solo para graphify; el kit funciona sin Python) |
| Graphify | `pip install graphifyy` (opcional, para grafo de conocimiento) |
| Git | Para versionado de artefactos y CI/CD |
| Jira (opcional) | MCP de Jira configurado para `desglosador` y `builder` |
| Figma (opcional) | MCP de Figma configurado para `figma-prd-mockups` |

---

<p align="center">
  <b>Kit IA</b> — Un sistema de habilidades para asistentes de IA que cubre el ciclo completo de desarrollo de software.<br>
  Construido con ❤️ para equipos que quieren desarrollar con velocidad, calidad y trazabilidad.
</p>
