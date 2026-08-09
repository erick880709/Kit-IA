# 🤝 Handoff de Diseño — STriAI Frontend React

**Fecha:** 2026-07-21
**Herramienta:** Excalidraw MCP (Path B)

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
