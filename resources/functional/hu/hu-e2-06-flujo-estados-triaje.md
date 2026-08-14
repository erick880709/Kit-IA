---
id: HU-E2-06
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 5
---

# HU-E2-06: Flujo de 7 estados del triaje

## Como
Sistema / Enfermera / Médico

## Quiero
que cada evento de triaje avance por una máquina de 7 estados controlada

## Para
garantizar integridad del proceso clínico (RF-002).

## Criterios de Aceptación
- [ ] CA1: Estados: Registrado → SignosVitales → EvaluaciónClínica → ClasificaciónIA → ValidaciónProfesional → Cierre (más estado de Reclasificación).
- [ ] CA2: Solo transiciones válidas permitidas (validación backend).
- [ ] CA3: Cambio de estado queda en auditoría con usuario y timestamp.
- [ ] CA4: Sin estado "ClasificaciónIA" completado no se permite el cierre.

## Dependencias
HU-E2-01 + HU-E2-05

## Subtareas
- [ ] Definición de la máquina de estados
- [ ] Guard de transiciones en backend
- [ ] Indicador de estado en la UI
