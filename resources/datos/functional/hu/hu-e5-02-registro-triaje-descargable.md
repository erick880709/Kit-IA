---
id: HU-E5-02
type: Historia de Usuario
epic: 005-auditoria-trazabilidad-cumplimiento
priority: Media
points: 3
---

# HU-E5-02: Generar Registro de Triaje Descargable

## Como
Médico / Auditor

## Quiero
Generar un resumen descargable (PDF) del evento de triaje que cumpla con los requisitos de la normativa colombiana

## Para
Adjuntarlo a la historia clínica del paciente y cumplir con los requisitos de trazabilidad de la Resolución 5596/2015

## Criterios de Aceptación
- [ ] CA1: Desde un evento de triaje cerrado, el profesional puede generar un "Registro de Triaje" en PDF
- [ ] CA2: El PDF incluye: paciente anonimizado (sin nombre ni documento), fecha/hora de ingreso, fecha/hora de clasificación, nivel sugerido por IA, nivel asignado por el profesional, concordancia, signos vitales, motivo de consulta, top 5 variables SHAP con sus valores
- [ ] CA3: Si hubo discrepancia, se incluye el motivo registrado
- [ ] CA4: El PDF tiene formato profesional con membrete del sistema, numeración de página y fecha de generación
- [ ] CA5: El PDF se genera en < 5 segundos

## Recurso de datos involucrado
- **Nombre:** EventoTriaje + SignosVitales + EvaluacionClinica + PrediccionIA + ExplicacionSHAP (lectura agregada)
- **Capa(s):** backend

## Subtareas
- [ ] Diseñar plantilla PDF del registro de triaje
- [ ] Implementar generación de PDF con los datos del evento
- [ ] Implementar anonimización en el PDF
- [ ] Probar con evento real
