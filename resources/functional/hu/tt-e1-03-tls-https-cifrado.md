---
id: TT-E1-03
type: Tarea Técnica
epic: E1 - Fundación del Sistema
priority: High
points: 3
---

# TT-E1-03: Implementar TLS/HTTPS y documentar cifrado en reposo

## Descripción
Documentar e implementar la capa de seguridad en transporte para la demo: HTTPS con certificado self-signed en local [SUPUESTO], y documentar el cifrado en reposo de SQLite (datos demo sintéticos, no aplica cifrado real — se deja el diseño para producción).

## Criterios de Done
- [ ] Demo documentada con opción HTTPS local (self-signed).
- [ ] Sección de seguridad en README: TLS, hash de contraseñas, cifrado en reposo para producción.
- [ ] Comunicación app↔servicio de inferencia local sin secretos hardcodeados.

## Dependencias
TT-E1-01
