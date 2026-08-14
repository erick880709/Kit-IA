---
id: HU-E1-03
type: Historia de Usuario
epic: E1 - Fundación del Sistema
priority: Medium
points: 2
---

# HU-E1-03: Recuperación de contraseña por email

## Como
Usuario registrado

## Quiero
recuperar mi contraseña por email

## Para
no quedar bloqueado del sistema (RF-SEC-003).

## Criterios de Aceptación
- [ ] CA1: Solicitud con usuario registrado → genera token temporal y "envía" email (simulado en demo [SUPUESTO: sin SMTP real]).
- [ ] CA2: Token de un solo uso con expiración (15 min).
- [ ] CA3: La nueva contraseña cumple política mínima (≥8 caracteres).

## Dependencias
TT-E1-02 + HU-E1-01
