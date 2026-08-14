---
id: TT-17
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 2
dependencies: "TT-15"
---

# TT-17: Implementar componentes compartidos del frontend

## Descripción

Crear los componentes reutilizables que usarán todas las páginas: layout principal, sidebar de navegación, header, indicadores de carga, manejo de errores, y diálogo de confirmación. También los catálogos clínicos como constantes TypeScript.

## Criterios de Done

- [ ] `components/layout/AppLayout.tsx`: estructura de 2 columnas (sidebar + main), responsive.
- [ ] `components/layout/Sidebar.tsx`:
  - Muestra opciones de navegación según el rol del usuario (usa `permissions` del contexto de auth).
  - Agrupado en "Flujo Clínico" y "Soporte" (igual que Streamlit).
  - Colapsable en mobile/tablet.
  - Botón de "Cerrar Sesión".
- [ ] `components/layout/Header.tsx`: muestra nombre de usuario, rol, badge de sesión activa.
- [ ] `components/shared/LoadingSpinner.tsx`: spinner con mensaje opcional.
- [ ] `components/shared/ErrorAlert.tsx`: alerta de error con botón de reintentar.
- [ ] `components/shared/EmptyState.tsx`: mensaje para cuando no hay datos.
- [ ] `components/shared/ConfirmDialog.tsx`: diálogo modal de confirmación (usar shadcn/ui AlertDialog).
- [ ] `lib/constants.ts`: catálogos clínicos exportados como arrays/objetos TypeScript (TIPOS_DOCUMENTO, EPS_COLOMBIA, GRUPOS_SANGUINEOS, DEPARTAMENTOS_COLOMBIA, NIVELES_TRIAGE, ESTADOS_TRIAGE, etc.).

## Recurso de datos involucrado

No aplica — son componentes de infraestructura UI.

## Subtareas

- [ ] Crear `AppLayout` + `Sidebar` + `Header`
- [ ] Crear `LoadingSpinner`, `ErrorAlert`, `EmptyState`
- [ ] Crear `ConfirmDialog`
- [ ] Exportar catálogos clínicos a `lib/constants.ts`
- [ ] Verificar responsive en viewport tablet (768px)
