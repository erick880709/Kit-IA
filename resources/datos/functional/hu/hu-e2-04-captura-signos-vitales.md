---
id: HU-E2-04
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 5
---

# HU-E2-04: Captura de Signos Vitales con Validación

## Como
Enfermera de Triaje

## Quiero
Registrar los 8 signos vitales del paciente con validación automática de rangos fisiológicos y alertas visuales

## Para
Alimentar el modelo de IA con datos válidos y detectar valores críticos que requieran atención inmediata

## Criterios de Aceptación
- [ ] CA1: Formulario con 8 campos: Temperatura (°C), Frecuencia Cardíaca (lpm), Frecuencia Respiratoria (rpm), Saturación O₂ (%), Presión Sistólica (mmHg), Presión Diastólica (mmHg), Peso (kg), Talla (cm)
- [ ] CA2: IMC se calcula automáticamente al ingresar peso y talla
- [ ] CA3: Validación de rangos fisiológicos en tiempo real:
  - Temperatura: 30-45 °C
  - SpO₂: 0-100%
  - FC/FR: > 0
  - Presión Sistólica > Diastólica y > 0
- [ ] CA4: Valores fuera de rango muestran alerta visual (borde rojo + icono ⚠️) y requieren confirmación del profesional
- [ ] CA5: Las variables de mayor peso predictivo (SpO₂, FR, Temperatura, PA sistólica) tienen indicación visual de criticidad cuando están en rangos de alerta clínica

## Recurso de datos involucrado
- **Nombre:** SignosVitales (ENT-003)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdSignosVitales | UUID | Sí | Generado automáticamente |
| IdTriaje | UUID | Sí | FK a EventoTriaje |
| Temperatura | Decimal | Sí | °C, rango 30-45 |
| FrecuenciaCardiaca | Entero | Sí | lpm, > 0 |
| FrecuenciaRespiratoria | Entero | Sí | rpm, > 0 |
| SaturacionO2 | Entero | Sí | %, 0-100 |
| PresionSistolica | Entero | Sí | mmHg, > Diastólica, > 0 |
| PresionDiastolica | Entero | Sí | mmHg, > 0 |
| Peso | Decimal | No | kg |
| Talla | Decimal | No | cm |
| IMC | Decimal | No | Calculado: peso/(talla/100)² |

### Relaciones con otros recursos
- `EventoTriaje` (1:1): cada triaje tiene un único registro de signos vitales

## Subtareas
- [ ] Diseñar formulario de signos vitales con distribución visual por peso predictivo
- [ ] Implementar validación de rangos fisiológicos en frontend y backend
- [ ] Implementar alertas visuales para valores críticos
- [ ] Implementar cálculo automático de IMC
- [ ] Priorizar visualmente SpO₂, FR, Temperatura, PA sistólica
