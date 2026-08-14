---
id: HU-E4-03
type: Historia de Usuario
epic: 004-motor-ia-explicabilidad-demo
priority: Alta
points: 5
---

# HU-E4-03: Validar Clasificación y Registrar Concordancia

## Como
Médico de Urgencias / Enfermera de Triaje

## Quiero
Ver la sugerencia de la IA, evaluar su explicación, y registrar MI propia clasificación en un campo independiente, quedando registrada la concordancia o discrepancia entre ambas

## Para
Ejercer mi criterio clínico y generar datos para la comparativa IA vs. profesional (métrica de utilidad clínica real)

## Criterios de Aceptación
- [ ] CA1: Después de ver la sugerencia de la IA y la explicación SHAP, el profesional ve un selector de nivel (I-V) para registrar SU clasificación
- [ ] CA2: El campo `NivelAsignadoProfesional` NUNCA se autocompleta con el valor de la IA — el profesional debe seleccionar activamente
- [ ] CA3: Al seleccionar su nivel, el sistema calcula automáticamente `Concordancia = (NivelSugeridoIA == NivelAsignadoProfesional)`
- [ ] CA4: Si Concordancia = No, el sistema EXIGE el campo `MotivoDiscrepancia` (texto obligatorio) antes de permitir continuar
- [ ] CA5: Si Concordancia = Sí, el sistema muestra confirmación visual (check verde) y permite continuar sin exigir motivo
- [ ] CA6: Ambos valores (IA + profesional) se guardan juntos de forma permanente

## Recurso de datos involucrado
- **Nombre:** EventoTriaje (campos de validación)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| NivelSugeridoIA | Catálogo | Sí (si hubo inferencia) | I-V |
| ProbabilidadesIA | JSON | Sí | {I: p1, II: p2, III: p3, IV: p4, V: p5} |
| NivelAsignadoProfesional | Catálogo | Sí | I-V, NUNCA autocompletado |
| Concordancia | Booleano | Sí | Calculado automáticamente |
| MotivoDiscrepancia | Texto/Catálogo | Condicional (si Concordancia = No) | Obligatorio cuando hay discrepancia |
| VersionModeloUsado | Texto | Sí | Referencia a ENT-009 |

## Subtareas
- [ ] Diseñar sección de validación del profesional
- [ ] Implementar campo independiente NivelAsignadoProfesional
- [ ] Implementar cálculo automático de concordancia
- [ ] Implementar exigencia de MotivoDiscrepancia
- [ ] Conectar con flujo de cierre del evento (HU-E2-08)
