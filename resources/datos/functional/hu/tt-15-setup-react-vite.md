---
id: TT-15
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "TT-06 (API backend disponible)"
---

# TT-15: Setup proyecto React + TypeScript + Vite

## Descripción

Crear el proyecto frontend desde cero con Vite, TypeScript, y todas las dependencias del stack definido en el ADR-002. Configurar la estructura de carpetas, el tema visual y las variables de entorno.

## Criterios de Done

- [ ] Proyecto creado con `npm create vite@latest frontend -- --template react-ts`.
- [ ] Dependencias instaladas:
  - `react-router-dom` (ruteo)
  - `@tanstack/react-query` (data fetching)
  - `axios` (HTTP client)
  - `react-hook-form` + `@hookform/resolvers` + `zod` (formularios)
  - `recharts` (gráficos dashboard)
  - `lucide-react` (iconos)
  - `ag-grid-react` + `ag-grid-community` (tablas de datos)
  - `tailwindcss` + `@tailwindcss/vite` (estilos)
  - `shadcn/ui` (componentes base — init con `npx shadcn@latest init`)
- [ ] `tailwind.config.ts` con tema clínico: colores de alerta (rojo para Nivel I, naranja II, amarillo III, verde IV, azul V).
- [ ] `vite.config.ts` con proxy de desarrollo: `/api` → `http://localhost:8000`.
- [ ] Variables de entorno (`.env`): `VITE_API_BASE_URL=http://localhost:8000`.
- [ ] Estructura de carpetas creada según documento TO-BE sección 7.2.
- [ ] `npm run dev` arranca en `http://localhost:5173`.

## Recurso de datos involucrado

No aplica — es infraestructura del proyecto.

## Subtareas

- [ ] Crear proyecto Vite + React + TS
- [ ] Instalar y configurar dependencias
- [ ] Configurar Tailwind CSS con tema clínico
- [ ] Inicializar shadcn/ui
- [ ] Configurar proxy de Vite para API
- [ ] Crear estructura de carpetas
- [ ] Verificar arranque
