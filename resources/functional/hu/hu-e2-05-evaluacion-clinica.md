---
id: HU-E2-05
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 5
---

# HU-E2-05: Evaluación clínica

## Como
Enfermera / Médico

## Quiero
registrar motivo de consulta, dolor, Glasgow, conciencia, antecedentes, alergias y texto libre

## Para
completar los features del modelo (RF-004, RF-EVA-001 a 007).

## Criterios de Aceptación
- [ ] CA1: Motivo de consulta en doble captura: catálogo estructurado (ENT-004) + texto libre.
- [ ] CA2: Escala de dolor 0-10, Glasgow y nivel de conciencia con catálogos.
- [ ] CA3: Antecedentes por autorreporte si no hay integración HCE (RF-INT-001 condicionado).
- [ ] CA4: Texto libre vacío no bloquea el flujo (RF-NLP-004).

## Recurso de datos involucrado
### Recurso
- **Nombre:** EvaluacionClinica
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| MotivoConsultaCodigo | catálogo CIE-10 | Sí | Sembrado con los top-10 reales (RD-002) |
| MotivoConsultaTexto | texto libre | No | Alimenta NLP |
| EscalaDolor | entero 0-10 | Sí | — |
| Glasgow, NivelConciencia | entero/catálogo | Sí | — |
| Antecedentes, Alergias | texto/catálogo | No | Autorreporte |
| Observaciones | texto libre | No | — |

### Relaciones con otros recursos
- `EventoTriaje` (N:1) · `Paciente` (N:1)

## Dependencias
HU-E2-04
