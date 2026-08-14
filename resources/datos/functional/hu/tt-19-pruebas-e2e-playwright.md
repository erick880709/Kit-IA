---
id: TT-19
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Media
points: 5
dependencies: "TT-18"
---

# TT-19: Pruebas E2E con Playwright

## Descripción

Crear tests end-to-end con Playwright que cubran los flujos críticos del sistema. Estos tests garantizan que la migración no rompió ninguna funcionalidad existente y sirven como red de seguridad para futuros cambios.

## Criterios de Done

- [ ] Playwright instalado y configurado (`playwright.config.ts`).
- [ ] **Test: Flujo completo de triaje** (`tests/triage-flow.spec.ts`):
  - Login con credenciales válidas.
  - Registrar nuevo paciente.
  - Iniciar triaje.
  - Ingresar signos vitales.
  - Ingresar evaluación clínica.
  - Ejecutar clasificación IA (esperar resultado).
  - Cerrar triaje.
  - Verificar que aparece animación de confirmación.
  - Descargar informe.
- [ ] **Test: Login fallido** (`tests/auth.spec.ts`):
  - Credenciales inválidas → mensaje de error.
  - Acceso a ruta protegida sin token → redirigir a login.
- [ ] **Test: Búsqueda de paciente** (`tests/patient-search.spec.ts`):
  - Buscar paciente existente por documento.
  - Verificar que aparece en resultados.
  - Buscar paciente inexistente → mensaje "No encontrado".
- [ ] **Test: Dashboard** (`tests/dashboard.spec.ts`):
  - Verificar que los KPIs cargan.
  - Verificar que los gráficos se renderizan.
- [ ] **Test: Navegación role-based** (`tests/navigation.spec.ts`):
  - Login como Administrador → ver todas las opciones.
  - Login como Enfermera → solo opciones de su rol.
- [ ] Tests configurados para correr en CI (GitHub Actions opcional).

## Recurso de datos involucrado

No aplica — es infraestructura de calidad.

## Subtareas

- [ ] Instalar y configurar Playwright
- [ ] Crear test de flujo completo de triaje
- [ ] Crear tests de autenticación
- [ ] Crear test de búsqueda de paciente
- [ ] Crear test de dashboard
- [ ] Crear test de navegación role-based
- [ ] Configurar para CI (opcional)
