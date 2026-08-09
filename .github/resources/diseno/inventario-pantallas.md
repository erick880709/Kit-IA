# 📋 Inventario de Pantallas — STriAI Frontend React

**Proyecto:** STriAI — Sistema de Triaje Multimodal IA
**Frontend:** React 19 + TypeScript + Vite + Tailwind CSS
**Fecha auditoría:** 2026-07-21
**Total pantallas:** 14 (13 autenticadas + 1 login)

---

## Pantalla 01 — Login

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/login` |
| **Componente** | `LoginPage.tsx` |
| **Propósito** | Autenticación JWT de profesionales de salud |
| **Estados** | Loading ✅ · Error ✅ · Success ✅ |
| **Navega a** | `/pacientes` |
| **Issues** | Sin enlace "Olvidé mi contraseña" · Sin `autocomplete` · Footer académico no clínico · Botón toggle sin aria-label |

## Pantalla 02 — Registro de Paciente

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/pacientes` |
| **Componente** | `PatientRegistrationPage.tsx` |
| **Propósito** | Registrar nuevo paciente o buscar existente para iniciar triaje |
| **Estados** | Loading ✅ · Error ✅ · Duplicado ✅ · Success ✅ |
| **Navega a** | `/signos-vitales` |
| **Issues** | Clase CSS `.input` inexistente · Tabs sin ARIA · Select departamento sin búsqueda · Validación solo al submit |

## Pantalla 03 — Signos Vitales

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/signos-vitales` |
| **Componente** | `VitalSignsPage.tsx` |
| **Propósito** | Captura de 6 signos vitales con indicadores de normalidad |
| **Estados** | Loading ✅ · Error ✅ · Empty (sin paciente) ✅ · Success ✅ |
| **Navega a** | `/evaluacion-clinica` |
| **Issues** | Clases Tailwind dinámicas rotas · Sin aria-valuemin/max · Sin stepper · Doble PatientSearch |

## Pantalla 04 — Evaluación Clínica

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/evaluacion-clinica` |
| **Componente** | `ClinicalEvaluationPage.tsx` |
| **Propósito** | Evaluación clínica: Glasgow, dolor, conciencia, comorbilidades |
| **Estados** | Loading ✅ · Error ✅ · Empty ✅ · Success ✅ |
| **Navega a** | `/clasificacion-ia` |
| **Issues** | Sin breadcrumb/stepper · Slider dolor sin output · Chips sin aria-pressed · Sin validación Glasgow |

## Pantalla 05 — Clasificación IA

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/clasificacion-ia` |
| **Componente** | `IAClassificationPage.tsx` |
| **Propósito** | Inferencia IA con explicación SHAP |
| **Estados** | Loading ✅ · Error (pred) ✅ · Error (SHAP) ❌ · Success ✅ |
| **Navega a** | `/validacion` |
| **Issues** | 🔴 Datos de signos hardcodeados · SHAP sin manejo de error · Barras sin aria · Feature names sin traducción |

## Pantalla 06 — Validación y Cierre

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/validacion` |
| **Componente** | `TriageValidationPage.tsx` |
| **Propósito** | Validar nivel profesional y cerrar triaje |
| **Estados** | Loading ✅ · Error ✅ · Success ✅ |
| **Navega a** | `/pacientes` |
| **Issues** | Stepper falso · Sin comparativa IA vs Profesional · Sin resumen post-cierre |

## Pantalla 07 — Dashboard

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/dashboard` |
| **Componente** | `DashboardPage.tsx` |
| **Propósito** | KPIs operativos y gráficos de tendencia |
| **Estados** | Loading ✅ · Error (KPIs) ✅ · Error (trend) ❌ · Empty ✅ · Success ✅ |
| **Navega a** | — |
| **Issues** | 🔴 Error en tendencia sin manejo · Gráficos sin aria · Umbral 3s hardcodeado · Sin selector de fechas |

## Pantalla 08 — Gestión Modelos IA

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/modelos` |
| **Componente** | `ModelManagementPage.tsx` |
| **Propósito** | CRUD de modelos ML: serializados, BD, registro |
| **Estados** | Loading ❌ · Error ❌ · Empty (disk) ✅ · Empty (db) ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | 🔴 Sin loading/error · ACTIVO hardcodeado · Tabs sin ARIA · `.input` roto |

## Pantalla 09 — Comparar Modelos

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/comparar-modelos` |
| **Componente** | `ModelComparisonPage.tsx` |
| **Propósito** | Tabla comparativa de métricas entre modelos |
| **Estados** | Loading ✅ · Error ❌ · Empty ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | Sin error/empty · SHAP emoji sin texto · Sin highlight · Tabla no ordenable |

## Pantalla 10 — Auditoría

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/auditoria` |
| **Componente** | `AuditPage.tsx` |
| **Propósito** | Consultar y exportar logs de auditoría |
| **Estados** | Loading ✅ · Error ❌ · Empty ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | Sin error/empty · Tabla sin caption · CSV sin loading · Paginación sin Anterior/Siguiente · Fecha raw |

## Pantalla 11 — Gestión Usuarios

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/usuarios` |
| **Componente** | `UserManagementPage.tsx` |
| **Propósito** | CRUD de usuarios + reset de contraseña |
| **Estados** | Loading ✅ · Error ❌ · Empty ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | 🔴 Contraseña en texto plano · Modal sin role=dialog · Sin confirmación desactivar · `.input` roto |

## Pantalla 12 — Control de Cambios

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/control-cambios` |
| **Componente** | `ControlCambiosPage.tsx` |
| **Propósito** | Historial de cambios en entidades |
| **Estados** | Loading ✅ · Error ❌ · Empty ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | Sin error/empty · Tabla sin caption · Casting unknown frágil · Sin paginación |

## Pantalla 13 — Histórico Paciente

| Atributo | Valor |
|----------|-------|
| **Ruta** | `/historico` |
| **Componente** | `HistoricoPacientePage.tsx` |
| **Propósito** | Buscar paciente y ver historial de triajes |
| **Estados** | Loading ✅ · Error ❌ · Empty ❌ · Success ✅ |
| **Navega a** | — |
| **Issues** | Sin error/empty · Concordancia emoji sin texto · Sin scroll al resultado · Sin botón Limpiar |

---

## Componentes Layout

| Componente | Issues |
|------------|--------|
| **Sidebar** | Sin aria-label en nav · Ítems desaparecen sin indicación · No colapsable · 256px fijo |
| **Header** | Sin breadcrumb · Sin indicador de sede · Badge rol contraste bajo |
| **AppLayout** | 🔴 Sin ErrorBoundary · Sin Suspense/lazy loading · Sin transiciones entre rutas |

---

## Resumen de severidad

| Severidad | Cantidad | Descripción |
|-----------|----------|-------------|
| 🔴 Crítico | 13 | Datos hardcodeados, sin manejo de error en 7 páginas, clases CSS rotas, contraseña expuesta, sin ErrorBoundary |
| 🟠 Medio | 18 | ARIA faltante, validación débil, sin confirmación en acciones destructivas, layout rígido |
| 🟡 Leve | 14 | Tooltips faltantes, formato de fechas, decimales excesivos, sin lazy loading |
