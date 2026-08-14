---
id: HU-E4-01
type: Historia de Usuario
epic: E4 - Motor de IA y Explicabilidad
priority: Highest
points: 8
---

# HU-E4-01: Ejecutar inferencia y ver probabilidades por nivel

## Como
Médico / Enfermera

## Quiero
ejecutar la clasificación IA y ver el nivel sugerido con las probabilidades de los 5 niveles

## Para
disponer de la sugerencia clínica en el flujo de triaje (RF-006, RF-007).

## Criterios de Aceptación
- [ ] CA1: Inferencia asíncrona, sin bloquear la UI (RF-IA-010), con estado "Cargando" y manejo de error.
- [ ] CA2: Tiempo objetivo < 3 s incluyendo SHAP (RNP-001); se registra el tiempo real (RF-IA-005).
- [ ] CA3: Muestra probabilidades de los 5 niveles + nivel sugerido tras umbral optimizado por clase (RF-007, no argmax puro).
- [ ] CA4: Se registran versión, algoritmo, fecha, id y confianza (RF-IA-004/006).

## Dependencias
TT-E4-01 + HU-E2-06

## Subtareas
- [ ] Endpoint/componente de inferencia asíncrona
- [ ] Aplicación del vector de umbrales por clase
- [ ] Registro de metadatos de inferencia
