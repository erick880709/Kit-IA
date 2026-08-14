---
id: HU-E2-04
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 5
---

# HU-E2-04: Captura de 8 signos vitales con validación de rangos

## Como
Enfermera

## Quiero
registrar los signos vitales con validación y alertas automáticas

## Para
alimentar el modelo con datos de calidad (RF-003, RF-VIT-001 a 010).

## Criterios de Aceptación
- [ ] CA1: Captura los 8 signos: temperatura, FC, FR, SpO₂, PA sistólica/diastólica, peso, talla (IMC auto).
- [ ] CA2: Valores fuera de rango fisiológico → alerta visible y confirmación antes de continuar (RNQ-003).
- [ ] CA3: SpO₂, FR, temperatura y PA sistólica marcadas como prioritarias en la UI.
- [ ] CA4: Estado "alerta por valor fuera de rango" diseñado (RD-004).

## Recurso de datos involucrado
### Recurso
- **Nombre:** SignosVitales
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Temperatura | decimal | Sí | 34-43 °C |
| FrecuenciaCardiaca | entero | Sí | 20-300 lpm |
| FrecuenciaRespiratoria | entero | Sí | 4-60 rpm |
| SaturacionO2 | entero | Sí | 50-100 % |
| PresionSistolica / Diastolica | entero | Sí | 40-300 / 20-200 mmHg |
| Peso, Talla, IMC | decimal | Sí | IMC calculado |

### Relaciones con otros recursos
- `EventoTriaje` (N:1): los signos pertenecen a un evento.

## Dependencias
HU-E2-01 + TT-E1-02
