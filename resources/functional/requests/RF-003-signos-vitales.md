# RF-003: Captura de Signos Vitales

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-VIT-001 a 010) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Alta

## Descripción
El sistema debe permitir el registro de los signos vitales del paciente: temperatura, frecuencia cardíaca, frecuencia respiratoria, saturación de O₂, presión arterial (sistólica/diastólica), peso y talla con cálculo automático de IMC; validar rangos fisiológicos y alertar valores críticos.

Cubre los requerimientos fuente: RF-VIT-001 a RF-VIT-010.

## Actores involucrados
Enfermera (captura), sistema (validación y alertas).

## Criterios de aceptación
- Valores fuera de rango generan alerta visible antes de continuar (RF-VIT-009/010, RNQ-003).
- IMC se calcula automáticamente a partir de peso y talla.
- SpO₂, frecuencia respiratoria, temperatura y presión sistólica reciben prioridad de calidad de captura (variables de mayor peso predictivo según estado del arte).

## Dependencias / relacionados
[[RF-006]], [[RNF-002]], RD-002 (ENT-003 Signos Vitales).

## Notas del analista
Pantalla "Captura de signos vitales" con estado de alerta por valor fuera de rango definido en 04 §3.
