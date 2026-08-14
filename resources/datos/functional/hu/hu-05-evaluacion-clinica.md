---
id: HU-05
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 5
---

# HU-05: Evaluación clínica

## Como
Profesional de enfermería o médico

## Quiero
Registrar la evaluación clínica del paciente: motivo de consulta, nivel de conciencia (Glasgow), escala de dolor, y comorbilidades relevantes

## Para
Complementar los signos vitales con información clínica cualitativa que el modelo de IA utiliza para predecir el nivel de triaje

## Criterios de Aceptación

- [ ] CA1: Se muestra el paciente activo y el triaje en curso en un banner superior.
- [ ] CA2: **Motivo de consulta**: textarea para texto libre (lo que el paciente refiere). Placeholder: "Describa el motivo de consulta del paciente...". Este texto se usa para los embeddings NLP.
- [ ] CA3: **Categoría del motivo**: select con opciones clínicas predefinidas (Dolor torácico, Dificultad respiratoria, Trauma, Dolor abdominal, Cefalea, Fiebre, Otro).
- [ ] CA4: **Escala de Glasgow** (`GlasgowInput`):
  - 3 sub-campos: Apertura Ocular (1-4), Respuesta Verbal (1-5), Respuesta Motora (1-6).
  - Total automático (3-15) con indicador de severidad: ≤8 (grave, rojo), 9-12 (moderado, amarillo), 13-15 (leve, verde).
- [ ] CA5: **Escala de dolor** (`PainScale`):
  - Slider visual de 0 (sin dolor) a 10 (dolor máximo).
  - Labels: 0-2 (Leve), 3-6 (Moderado), 7-10 (Severo).
  - Emoji/icono que cambia según intensidad.
- [ ] CA6: **Nivel de conciencia**: select (Alerta, Confuso, Somnoliento, Estuporoso, Coma).
- [ ] CA7: **Comorbilidades** (`ComorbidityChecklist`): 8 checkboxes:
  - Hipertensión, Diabetes, EPOC, Cardiopatía, IRC, Cáncer, Inmunosupresión, Obesidad.
  - Checkbox "Ninguna" que desmarca las demás.
- [ ] CA8: Al guardar (`PUT /api/triages/{id}/clinical-eval`), navegación al siguiente paso: "Continuar a Clasificación IA".
- [ ] CA9: Prevención de pérdida de datos: confirmación si se intenta navegar sin guardar.

## Recurso de datos involucrado

- **Nombre del recurso:** EvaluacionClinica
- **Capa(s):** frontend (consume PUT/GET /api/triages/{id}/clinical-eval)

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| motivo_consulta | string | Sí | Texto libre para NLP |
| categoria_motivo | select | Sí | Catálogo predefinido |
| glasgow_ocular | number | Sí | 1-4 |
| glasgow_verbal | number | Sí | 1-5 |
| glasgow_motora | number | Sí | 1-6 |
| glasgow_total | number | Sí | 3-15 (calculado) |
| escala_dolor | number | Sí | 0-10 |
| nivel_conciencia | select | Sí | Catálogo: Alerta, Confuso, Somnoliento, Estuporoso, Coma |
| comorbilidades | list | No | Lista de strings seleccionados |

## Subtareas

- [ ] Crear `pages/ClinicalEvaluationPage.tsx`
- [ ] Crear `components/clinical/GlasgowInput.tsx`
- [ ] Crear `components/clinical/PainScale.tsx` (slider con emojis)
- [ ] Crear `components/clinical/ComorbidityChecklist.tsx`
- [ ] Implementar cálculo automático de Glasgow total
- [ ] Implementar dirty state guard
- [ ] Probar con diferentes combinaciones clínicas
