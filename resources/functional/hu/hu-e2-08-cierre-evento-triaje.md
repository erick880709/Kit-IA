---
id: HU-E2-08
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 3
---

# HU-E2-08: Cierre del evento de triaje con validación de concordancia

## Como
Médico

## Quiero
cerrar el evento con la validación final registrando concordancia IA vs. profesional

## Para
dejar evidencia completa del triaje (RF-002, RF-010).

## Criterios de Aceptación
- [ ] CA1: El cierre exige NivelSugeridoIA y NivelAsignadoProfesional presentes (RD-003).
- [ ] CA2: Concordancia calculada por el sistema (`NivelSugeridoIA == NivelAsignadoProfesional`).
- [ ] CA3: Si difieren → MotivoDiscrepancia obligatorio.
- [ ] CA4: Ambos valores y la versión del modelo quedan persistidos de forma permanente.

## Dependencias
HU-E2-06
