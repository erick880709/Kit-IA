---
id: HU-E1-03
type: Historia de Usuario
epic: 001-fundacion-del-sistema
priority: Media
points: 2
---

# HU-E1-03: Recuperación de Contraseña

## Como
Usuario del sistema

## Quiero
Recuperar mi contraseña si la olvido

## Para
No quedar bloqueado del sistema y mantener la continuidad operativa

## Criterios de Aceptación
- [ ] CA1: En la pantalla de login existe un enlace "¿Olvidó su contraseña?"
- [ ] CA2: El usuario ingresa su nombre de usuario o correo y recibe un enlace de restablecimiento
- [ ] CA3: El enlace de restablecimiento expira en 30 minutos
- [ ] CA4: La nueva contraseña debe cumplir políticas: mínimo 8 caracteres, al menos 1 mayúscula, 1 número
- [ ] CA5: La contraseña anterior no puede reutilizarse (últimas 3 contraseñas)

## Recurso de datos involucrado
- **Nombre:** Usuario (extensión)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Email | Texto | Sí | Para envío de enlace de restablecimiento |
| TokenRestablecimiento | Texto | No | UUID generado, expira en 30 min |
| FechaExpiracionToken | DateTime | No | Automático |
| HistorialPasswords | JSON | Sí | Últimos 3 hashes (no se puede reutilizar) |

## Subtareas
- [ ] Diseñar pantalla de "Olvidó su contraseña"
- [ ] Implementar generación de token y envío por email
- [ ] Implementar validación de políticas de contraseña
- [ ] Implementar historial de contraseñas (no reutilización)
