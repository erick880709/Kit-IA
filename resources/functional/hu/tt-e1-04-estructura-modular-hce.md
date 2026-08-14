---
id: TT-E1-04
type: Tarea Técnica
epic: E1 - Fundación del Sistema
priority: Highest
points: 5
---

# TT-E1-04: Crear estructura modular del proyecto y puntos de extensión HCE

## Descripción
Estructura modular por capas (ui / services / data / models) con interfaces que dejen puntos de extensión para la futura integración con Historia Clínica Electrónica (RF-INT-001).

## Criterios de Done
- [ ] Módulo `services/patient_service.py` con interfaz de repositorio desacoplada (RF-001, RF-015).
- [ ] Interfaz `HistoryConnector` con implementación `MockHCE` (autorreporte) lista para reemplazarse por integración real.
- [ ] Separación UI / lógica de negocio / persistencia (la UI no accede a SQL directo).
- [ ] Inyección simple de dependencias documentada.

## Dependencias
TT-E1-01 + TT-E1-02
