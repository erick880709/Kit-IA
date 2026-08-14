---
id: HU-E5-02
type: Historia de Usuario
epic: E5 - Auditoría, Trazabilidad y Cumplimiento
priority: High
points: 3
---

# HU-E5-02: Registro de triaje descargable (normativa colombiana)

## Como
Médico / Auditor

## Quiero
generar el registro de triaje exigido por la normativa, descargable/visualizable

## Para
cumplir el requisito normativo del registro de información de triaje (RF-013, CONTEXTO TRIAJE.txt §10).

## Criterios de Aceptación
- [ ] CA1: Contenido mínimo: paciente anonimizado, fecha/hora, nivel IA vs. humano, signos vitales, motivo de consulta, variables SHAP de mayor peso.
- [ ] CA2: Exportación a PDF.
- [ ] CA3: El documento no incluye identificadores directos del paciente (RNF-006).
- [ ] CA4: Generación queda registrada en auditoría.

## Dependencias
TT-E5-01 + HU-E2-08
