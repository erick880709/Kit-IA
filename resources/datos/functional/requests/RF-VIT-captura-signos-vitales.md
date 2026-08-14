# RF-VIT: Captura de Signos Vitales

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 42, Módulo de Captura de Signos Vitales; 03-CATALOGO-DATOS-Y-VARIABLES.md
**Prioridad:** Crítica

## Descripción
El sistema permitirá el registro completo de los signos vitales del paciente durante el proceso de triaje. Estas variables constituyen el núcleo de los datos estructurados que alimentan el modelo de IA y son, según la literatura, los predictores de mayor peso en la clasificación de triaje.

## Actores involucrados
- Enfermera de Triaje (principal)

## Criterios de aceptación

### Variables a capturar (RF-VIT-001 a RF-VIT-008)
| Sub-requerimiento | Variable | Unidad | Tipo |
|---|---|---|---|
| RF-VIT-001 | Temperatura corporal | °C | Decimal |
| RF-VIT-002 | Frecuencia cardíaca | lpm (latidos por minuto) | Entero |
| RF-VIT-003 | Frecuencia respiratoria | rpm (respiraciones por minuto) | Entero |
| RF-VIT-004 | Saturación de O₂ (SpO₂) | % | Entero (0-100) |
| RF-VIT-005 | Presión arterial (sistólica / diastólica) | mmHg | Entero / Entero |
| RF-VIT-006 | Peso | kg | Decimal |
| RF-VIT-007 | Talla | cm | Decimal |
| RF-VIT-008 | IMC | kg/m² (calculado automáticamente) | Decimal |

### Validaciones (RF-VIT-009)
- Todos los signos vitales se validan antes del almacenamiento contra rangos fisiológicamente plausibles.
- La temperatura debe estar entre 30 °C y 45 °C.
- La saturación de O₂ no puede superar el 100%.
- La frecuencia cardíaca y respiratoria no pueden ser negativas.
- La presión arterial sistólica debe ser > diastólica y > 0 mmHg.

### Alertas (RF-VIT-010)
- Valores fuera de rangos fisiológicos generan alertas visuales inmediatas (RNC-004).
- Las variables de mayor peso predictivo (SpO₂, frecuencia respiratoria, temperatura, presión sistólica) reciben indicación visual de criticidad cuando están fuera de rango.
- La alerta no bloquea el flujo, pero requiere confirmación del profesional antes de continuar.

## Dependencias / relacionados
- RF-IA-001: Los signos vitales deben estar registrados antes de ejecutar la inferencia (RNC-003).
- RNC-003: Signos vitales obligatorios antes de inferencia, salvo Nivel I (reanimación inmediata).
- RNC-004: Alertas por valores fuera de rango.
- RNQ-003: Valores fuera de rango generan alertas.
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`: SpO₂, frecuencia respiratoria, temperatura y presión sistólica son las variables de mayor peso predictivo.

## Notas del analista
- El IMC se calcula automáticamente (RF-VIT-008) cuando peso y talla están presentes, no es un campo de entrada manual.
- La prioridad de captura debe reflejar el peso predictivo: SpO₂ y frecuencia respiratoria son más críticas que peso/talla.
