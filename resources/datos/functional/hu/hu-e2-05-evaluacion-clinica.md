---
id: HU-E2-05
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 5
---

# HU-E2-05: Evaluación Clínica del Paciente

## Como
Enfermera de Triaje / Médico

## Quiero
Registrar el motivo de consulta (texto libre + categoría), escala de dolor, nivel de conciencia, antecedentes, alergias y observaciones clínicas

## Para
Completar toda la información que el modelo de IA necesita para ejecutar la inferencia multimodal

## Criterios de Aceptación
- [ ] CA1: Campo "Motivo de consulta — Texto libre": textarea para descripción narrativa del paciente
- [ ] CA2: Campo "Motivo de consulta — Categoría": dropdown con catálogo (Dolor torácico, Trauma, Disnea, Dolor abdominal, Fiebre, Cefalea, Convulsiones, Hemorragia, Intoxicación, Otro)
- [ ] CA3: Escala de dolor: slider o input numérico 0-10
- [ ] CA4: Escala de Glasgow: numérico 3-15 (cuando aplique)
- [ ] CA5: Nivel de conciencia: dropdown (Alerta, Somnoliento, Obnubilado, Inconsciente)
- [ ] CA6: Antecedentes: checkboxes (Diabetes, Hipertensión, Enfermedad renal, Embarazo, Cáncer, Cardiopatías, Enfermedad pulmonar, Cirugías recientes) + campo "Medicación relevante"
- [ ] CA7: Campo "Episodios previos de urgencias": numérico (precargado si viene del historial)
- [ ] CA8: Campo "Alergias": texto libre (opcional)
- [ ] CA9: Campo "Observaciones": textarea para notas narrativas de enfermería (alimenta NLP)

## Recurso de datos involucrado
- **Nombre:** EvaluacionClinica (ENT-007) + MotivoConsulta (ENT-004) + AntecedentesClinicos (ENT-005) + TextoClinico (ENT-008)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdEvaluacion | UUID | Sí | Generado automáticamente |
| IdTriaje | UUID | Sí | FK a EventoTriaje |
| MotivoTextoLibre | Texto | No | Alimenta NLP |
| MotivoCategoria | Catálogo | Sí | Dropdown controlado |
| EscalaDolor | Entero | Sí | 0-10 |
| Glasgow | Entero | No | 3-15 |
| NivelConciencia | Catálogo | Sí | Alerta/Somnoliento/Obnubilado/Inconsciente |
| Diabetes | Booleano | No | Default false |
| Hipertension | Booleano | No | Default false |
| EnfermedadRenal | Booleano | No | Default false |
| Embarazo | Booleano | No | Default false |
| Cancer | Booleano | No | Default false |
| Cardiopatias | Booleano | No | Default false |
| EnfermedadPulmonar | Booleano | No | Default false |
| CirugiasRecientes | Booleano | No | Default false |
| MedicacionRelevante | Texto | No | Texto libre |
| EpisodiosPreviosUrgencias | Entero | No | Precargado del historial |
| Alergias | Texto | No | Texto libre |
| Observaciones | Texto | No | Texto libre para NLP |

### Relaciones con otros recursos
- `EventoTriaje` (1:1)
- `Paciente` (N:1): antecedentes pertenecen al paciente

## Subtareas
- [ ] Diseñar pantalla de Evaluación Clínica
- [ ] Implementar catálogo de motivos de consulta
- [ ] Implementar checkboxes de antecedentes
- [ ] Implementar campos de texto libre para NLP
- [ ] Conectar con datos de historial (EpisodiosPrevios)
