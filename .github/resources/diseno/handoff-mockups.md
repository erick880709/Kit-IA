# Handoff de Mockups — TriajeIA (builder / genesis)

**Fecha:** 2026-08-13 · **Skill:** figma-prd-mockups
**Stack objetivo:** Python 3.12 + Streamlit (decisión refinador)

## Herramienta usada

**Path B — Excalidraw** (Figma MCP no conectado en esta sesión). 9 vistas renderizadas: 8 wireframes de pantalla + 1 diagrama de flujo.

## Mockups HTML + JPG (2026-08-13)

Además de las vistas Excalidraw, se generaron mockups estáticos editables y exportaciones de imagen:

- **HTML:** `mockups/triajeia-mockups.html` — las 9 vistas en una galería HTML estilizada con el design system TriajeIA (paleta cyan-salud + Fira Sans/Code). Referencia visual directa para `genesis`/`builder`.
- **JPG:** `mockups/jpg/01-login.jpg` … `09-flujo-clinico.jpg` — exportes por sección (quality 90) para presentaciones/entregables del TFM.
- **Guía:** `mockups/README.md` — cómo se generaron y cómo regenerarlos.

## Mapeo pantalla → vista

| Pantalla | Vista Excalidraw | Checkpoint ID | Ref. |
|---|---|---|---|
| 1 Login | "TriajeIA · Acceso clínico" | `94bf80065d6a4dc8b4` | `excalidraw/01-login.md` |
| 2 Registro de paciente | "Registro de paciente" | `9bd8e837eb4e464fad` | `excalidraw/02-registro-paciente.md` |
| 3 Captura de signos vitales | "Captura de signos vitales" | `4dbfe99b0bdb4ebea3` | `excalidraw/03-signos-vitales.md` |
| 4 Evaluación clínica | "Evaluación clínica" | `7f43bdba4f274c11b6` | `excalidraw/04-evaluacion-clinica.md` |
| 5 Clasificación IA | "Ejecutar clasificación IA" | `3b8da5b846da457c99` | `excalidraw/05-clasificacion-ia.md` |
| 6 Explicación SHAP | "Explicación SHAP" | `ee0c01ad72d14c63ba` | `excalidraw/06-explicacion-shap.md` |
| 7 Validación (discrepancia) | "Validación de triaje — discrepancia" | `4c5ae301e2b348f885` | `excalidraw/07-validacion-discrepancia.md` |
| 8 Cierre del evento | "Cierre del evento de triaje" | `67afce8580bc4109b1` | `excalidraw/08-cierre-evento.md` |
| Flujo completo | "Flujo clínico principal" | `1c4392b150924a6bb8` | `excalidraw/09-flujo-clinico.md` |

## Design system

- Origen: `design-system/triajeia/MASTER.md` (ui-ux-pro-max, query "healthcare clinical triage dashboard", densidad 8)
- Resumen: `.github/resources/diseno/design-system.md` — paleta cyan-salud (`#0891B2`) + Fira Sans/Code

## Diferido explícitamente

- 4 pantallas de soporte (Comparación de modelos, Gestión de modelos, Dashboard, Auditoría) — fase 2.
- Estados cargando/error de inferencia: solo etiquetados en pantalla 5.
- Prototipo navegable real: se obtiene al implementar en Streamlit (builder).

## Para el siguiente skill (archi → genesis → builder)

Leer este archivo primero. Derivar estilos de `design-system.md`, no improvisar. El builder de Streamlit debe implementar las 8 pantallas en este orden.

---

## Anexo histórico — Handoff React STriAI (2026-07-21)

**Fecha:** 2026-07-21
**Herramienta:** Excalidraw MCP (Path B) — 4 wireframes de mejora sobre frontend React (auditoría de accesibilidad/estados). Superado por la iteración Streamlit actual; sus hallazgos aplican como checklist de calidad.

---

## 1. Resumen ejecutivo

Se auditó el frontend React de STriAI (14 pantallas) identificando **13 issues críticos**, **18 medios** y **14 leves**. Los hallazgos se documentaron en `inventario-pantallas.md` y se generaron 4 wireframes de mejora en Excalidraw.

---

## 2. Tool usado

**Excalidraw MCP** — 4 vistas de wireframe generadas:

| Vista | Tema | Prioridad |
|-------|------|-----------|
| `e84da1c47b33450eb9` | Dashboard — manejo de errores, accesibilidad gráficos, selector de fechas | 🔴 ALTA |
| `8eb1af9c24134ee9bc` | Flujo Clínico — Stepper real con estados de BD | 🟠 MEDIA |
| `9b9303181f544a6da7` | Tablas — Patrón Loading/Error/Empty para 7 páginas | 🔴 ALTA |
| `b5d085df4e014e86bb` | Login + Seguridad — Autocomplete, contraseñas, JWT | 🔴 CRÍTICA |

---

## 3. Screen → Wireframe mapping

| Pantalla | Wireframe(s) aplicable(s) |
|----------|---------------------------|
| LoginPage | `b5d085df` (Login + Seguridad) |
| DashboardPage | `e84da1c4` (Dashboard) + `9b930318` (Estados) |
| AuditPage | `9b930318` (Estados) |
| ClinicalEvaluationPage | `8eb1af9c` (Stepper) |
| ControlCambiosPage | `9b930318` (Estados) |
| HistoricoPacientePage | `9b930318` (Estados) |
| IAClassificationPage | `8eb1af9c` (Stepper) + `9b930318` (SHAP error) |
| ModelComparisonPage | `9b930318` (Estados) |
| ModelManagementPage | `9b930318` (Estados, 3 queries) |
| PatientRegistrationPage | `8eb1af9c` (Stepper inicio) |
| TriageValidationPage | `8eb1af9c` (Stepper real) |
| UserManagementPage | `9b930318` (Estados) + `b5d085df` (Seguridad) |
| VitalSignsPage | `8eb1af9c` (Stepper) + Clases Tailwind |

---

## 4. Design system source

- **Colores:** Tailwind CSS slate/gray palette (slate-50 a slate-900)
- **Tipografía:** System font stack (Inter / SF Pro)
- **No se ejecutó `ui-ux-pro-max`** porque el proyecto ya tiene un design system implementado vía Tailwind
- Las mejoras sugeridas mantienen la paleta y tipografía existentes

---

## 5. Top 5 acciones prioritarias para builder

| # | Acción | Severidad | Esfuerzo |
|---|--------|-----------|----------|
| 1 | **Corregir datos hardcodeados en `IAClassificationPage`** — Leer signos vitales reales de la API antes de llamar a `/inference/predict` | 🔴 Bug funcional | Medio |
| 2 | **Eliminar exposición de contraseña en `UserManagementPage`** — Mostrar modal "contraseña reseteada" con botón copiar, no texto plano | 🔴 Seguridad | Bajo |
| 3 | **Agregar Loading/Error/Empty states en 7 páginas** — Usar componentes `LoadingSpinner`, `ErrorAlert`, `EmptyState` de `shared/index.tsx` | 🔴 UX | Bajo |
| 4 | **Agregar `ErrorBoundary` en `AppLayout`** — Un solo componente wrapper para evitar crashes catastróficos | 🔴 Estabilidad | Bajo |
| 5 | **Definir clase CSS `.input` en `index.css`** — Todas las páginas la usan pero no existe. Agregar estilos base para inputs | 🔴 Visual | Bajo |

---

## 6. Artefactos

| Artefacto | Ruta |
|-----------|------|
| Inventario de pantallas | `.github/resources/diseno/inventario-pantallas.md` |
| Design system (existente) | Tailwind CSS + `frontend/src/index.css` |
| Handoff (este archivo) | `.github/resources/diseno/handoff-mockups.md` |
| Wireframe Dashboard | Excalidraw checkpoint `e84da1c47b33450eb9` |
| Wireframe Stepper | Excalidraw checkpoint `8eb1af9c24134ee9bc` |
| Wireframe Estados | Excalidraw checkpoint `9b9303181f544a6da7` |
| Wireframe Seguridad | Excalidraw checkpoint `b5d085df4e014e86bb` |

---

## 7. Deferred / Open Questions

- **ui-ux-pro-max design system:** No se ejecutó porque los estilos ya están definidos vía Tailwind. Si se quiere un refresh visual completo, ejecutar Step 2 del skill.
- **Migración a httpOnly cookies:** Recomendada para entorno clínico, pero requiere cambios en backend (CORS + cookie settings). Dejado como backlog.
- **Sidebar colapsable:** No incluido en wireframes por ser un cambio de layout mayor. Evaluar en siguiente iteración.
- **Lazy loading de páginas (React.lazy + Suspense):** No incluido. El bundle actual pesa 749KB. Si crece más, implementar code splitting por ruta.
- **Gráficos con alternativas textuales:** Los gráficos de Recharts necesitan `aria-label` y un `table` oculto con los mismos datos para lectores de pantalla. Evaluar librería `recharts-accessibility` o similar.

---

**Próximo paso para builder:** Leer `.github/resources/diseno/handoff-mockups.md` como entrada, priorizar las 5 acciones de la sección 5, y ejecutar correcciones en orden de severidad.
