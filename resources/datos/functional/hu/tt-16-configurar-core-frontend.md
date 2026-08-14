---
id: TT-16
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "TT-15"
---

# TT-16: Configurar TanStack Query, Axios y React Router

## Descripción

Configurar las bibliotecas core del frontend: el cliente HTTP con interceptor JWT, el proveedor de React Query para caching de datos del servidor, y el enrutador con rutas protegidas por rol.

## Criterios de Done

- [ ] `api/client.ts` creado:
  - Instancia de Axios con `baseURL` desde variable de entorno.
  - Interceptor de request: añade header `Authorization: Bearer <token>` desde `localStorage`.
  - Interceptor de response: si recibe 401, limpia token y redirige a `/login`.
  - Timeout configurable.
- [ ] `App.tsx` envuelto en `QueryClientProvider` (TanStack Query):
  - `defaultOptions`: `staleTime: 30_000` (30s), `retry: 1`.
- [ ] `App.tsx` envuelto en `AuthProvider` (React Context):
  - Estado: `user`, `token`, `isAuthenticated`, `isAdmin`.
  - Métodos: `login()`, `logout()`.
  - Persistencia en `localStorage`.
- [ ] React Router configurado:
  - `createBrowserRouter` con rutas anidadas.
  - `ProtectedRoute` wrapper que verifica autenticación y rol.
  - Ruta `*` → `NotFoundPage`.
- [ ] Tipos TypeScript para respuestas de API (`types/api.ts`): `ApiResponse<T>`, `PaginatedResponse<T>`.

## Recurso de datos involucrado

No aplica — es infraestructura del frontend.

## Subtareas

- [ ] Crear `api/client.ts` con interceptores Axios
- [ ] Crear `AuthContext` + `AuthProvider`
- [ ] Configurar `QueryClientProvider`
- [ ] Configurar React Router con rutas protegidas
- [ ] Crear tipos genéricos para API
