---
id: HU-02
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 2
---

# HU-02: Layout principal con navegación role-based

## Como
Profesional sanitario autenticado

## Quiero
Ver una interfaz con menú de navegación lateral que me muestre solo las opciones que corresponden a mi rol

## Para
Navegar eficientemente entre las distintas secciones del sistema sin perderme ni ver opciones que no me corresponden

## Criterios de Aceptación

- [ ] CA1: Después del login, se muestra un layout de 2 columnas: sidebar izquierdo + área de contenido principal.
- [ ] CA2: El sidebar muestra dos grupos de navegación: "📋 Flujo Clínico" (Registrar Paciente, Signos Vitales, Evaluación Clínica, Clasificación IA, Validación y Cierre) y "📊 Soporte" (Dashboard, Gestión Modelos, Comparar Modelos, Auditoría, Gestión Usuarios, Control de Cambios, Histórico del Paciente).
- [ ] CA3: Las opciones del sidebar se filtran según el rol del usuario (usa `GET /api/auth/permissions`).
  - Administrador: ve todas las opciones.
  - Médico/Enfermera: ve Flujo Clínico + Dashboard + Histórico. No ve Gestión Usuarios ni Auditoría.
  - Investigador: ve Dashboard + Modelos + Comparación + Auditoría (solo lectura). No ve flujo clínico.
  - Auditor: ve solo Auditoría + Dashboard + Histórico.
- [ ] CA4: La opción activa se resalta visualmente en el sidebar.
- [ ] CA5: El header muestra: nombre de usuario, rol (badge), y botón de cerrar sesión.
- [ ] CA6: En tablet (768px), el sidebar es colapsable (toggle con icono hamburguesa).
- [ ] CA7: La navegación entre páginas es instantánea (React Router, sin recarga de página).

## Recurso de datos involucrado

No aplica — es navegación y layout.

## Subtareas

- [ ] Crear `AppLayout.tsx` con sidebar + header + main
- [ ] Implementar filtrado de opciones por rol
- [ ] Implementar resaltado de opción activa
- [ ] Implementar sidebar colapsable en tablet
- [ ] Probar con todos los roles
