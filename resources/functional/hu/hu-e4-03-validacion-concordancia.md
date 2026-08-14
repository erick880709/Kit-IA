---
id: HU-E4-03
type: Historia de Usuario
epic: E4 - Motor de IA y Explicabilidad
priority: Highest
points: 5
---

# HU-E4-03: Validar clasificación del profesional y registrar concordancia

## Como
Médico / Enfermera

## Quiero
registrar mi propia clasificación tras ver la sugerencia de la IA y que el sistema calcule la concordancia

## Para
habilitar la comparativa IA vs. profesional (RF-010, RF-011).

## Criterios de Aceptación
- [ ] CA1: `NivelAsignadoProfesional` es campo propio, obligatorio, nunca autocompletado con el valor de la IA.
- [ ] CA2: Concordancia calculada automáticamente (`NivelSugeridoIA == NivelAsignadoProfesional`).
- [ ] CA3: Discrepancia → `MotivoDiscrepancia` obligatorio (catálogo o texto corto).
- [ ] CA4: Ambos niveles + probabilidades + `VersionModeloUsado` persistidos permanentemente (RD-003).

## Recurso de datos involucrado
### Recurso
- **Nombre:** EventoTriaje (registro dual)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| NivelSugeridoIA | catálogo I-V | Sí | Escrito por el sistema |
| ProbabilidadesIA | JSON | Sí | {nivel: prob} |
| NivelAsignadoProfesional | catálogo I-V | Sí | Escrito por el profesional |
| Concordancia | booleano | Sí | Calculado |
| MotivoDiscrepancia | texto/catálogo | Condicional | Solo si Concordancia = No |
| VersionModeloUsado | texto | Sí | Ref. ENT-009 |

### Relaciones con otros recursos
- `Paciente` (N:1) · `Modelo` (N:1)

## Dependencias
HU-E4-02
