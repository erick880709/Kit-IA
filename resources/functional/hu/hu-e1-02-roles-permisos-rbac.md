---
id: HU-E1-02
type: Historia de Usuario
epic: E1 - Fundación del Sistema
priority: Highest
points: 5
---

# HU-E1-02: Gestión de roles y permisos RBAC (5 roles)

## Como
Administrador

## Quiero
gestionar los 5 roles y sus permisos por pantalla

## Para
garantizar que cada usuario ve solo lo que le corresponde (RF-014, RF-SEC-002).

## Criterios de Aceptación
- [ ] CA1: Roles definidos: Administrador, Médico, Enfermera, Investigador, Auditor.
- [ ] CA2: Cada pantalla del inventario RD-004 declara qué roles la usan y el acceso se valida en backend (no solo UI).
- [ ] CA3: Un usuario sin permiso no puede acceder ni por URL directa.
- [ ] CA4: Cambios de rol/permiso quedan en auditoría.

## Dependencias
TT-E1-02 + HU-E1-01

## Subtareas
- [ ] Modelo de permisos por pantalla
- [ ] Decorador/middleware de autorización
- [ ] Pantalla de administración de roles
