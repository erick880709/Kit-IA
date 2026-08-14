---
id: HU-E1-04
type: Historia de Usuario
epic: E1 - Fundación del Sistema
priority: Highest
points: 2
---

# HU-E1-04: Cierre automático de sesión por inactividad

## Como
Sistema

## Quiero
cerrar la sesión automáticamente tras un período de inactividad

## Para
proteger datos clínicos en terminales compartidos (RF-SEC-004).

## Criterios de Aceptación
- [ ] CA1: Inactividad de 5 minutos → cierre de sesión y aviso.
- [ ] CA2: El cierre queda registrado en auditoría.
- [ ] CA3: El timeout es configurable sin re-desplegar.

## Dependencias
HU-E1-01
