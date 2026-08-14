# RF-EVA: Evaluación Clínica

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 43, Módulo de Evaluación Clínica; 06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md
**Prioridad:** Crítica

## Descripción
El sistema permitirá registrar toda la información de la evaluación clínica inicial del paciente, incluyendo motivo de consulta (estructurado y texto libre), escala de dolor, nivel de conciencia, antecedentes, alergias y observaciones. Estos datos, combinados con los signos vitales, constituyen la entrada completa al modelo multimodal de IA.

## Actores involucrados
- Enfermera de Triaje (principal)
- Médico de Urgencias

## Criterios de aceptación

### Sub-requerimientos

**RF-EVA-001 — Registrar Motivo de Consulta:**
- Captura en dos modalidades simultáneas: (1) texto libre (campo abierto, alimenta el módulo NLP) y (2) categoría estructurada (catálogo controlado: dolor torácico, trauma, disnea, dolor abdominal, fiebre, etc.).
- Ambos se envían juntos al modelo; el pipeline de fusión decide cómo combinarlos.

**RF-EVA-002 — Registrar Escala del Dolor:**
- Valor entero de 0 a 10 (RNC-005).
- Campo obligatorio.

**RF-EVA-003 — Registrar Escala de Glasgow:**
- Cuando aplique clínicamente.
- Valores según escala estándar (3-15).

**RF-EVA-004 — Registrar Nivel de Conciencia:**
- Catálogo controlado: Alerta, Somnoliento, Obnubilado, Inconsciente.

**RF-EVA-005 — Registrar Antecedentes Clínicos:**
- Diabetes, hipertensión, enfermedad renal, embarazo, cáncer, cardiopatías, enfermedad pulmonar, cirugías recientes, medicación relevante.
- Incluye `EpisodiosPreviosUrgencias` (variable añadida, ver Notas).
- Cuando no exista integración con HCE (RF-INT-001), se capturan por autorreporte/anamnesis.

**RF-EVA-006 — Registrar Alergias:**
- Campo opcional de texto libre.

**RF-EVA-007 — Registrar Observaciones (Texto Clínico):**
- Campo de texto libre para notas narrativas de enfermería/médico.
- Este texto alimenta el pipeline NLP (embeddings BERT/BioBERT-es).
- Si el texto está vacío, el pipeline continúa solo con variables estructuradas (RF-NLP-004).

## Dependencias / relacionados
- RF-NLP-001 a 005: Procesamiento de texto libre.
- RF-IA-001: La evaluación clínica es precondición para ejecutar la inferencia.
- RNC-006: El motivo de consulta debe registrarse antes de finalizar el triaje.
- RNC-007: Los antecedentes se registran si están disponibles, sin bloquear el proceso.
- `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md`: detalle de la pantalla de captura de síntomas.

## Notas del analista
- `EpisodiosPreviosUrgencias` fue añadido como campo en `03-CATALOGO-DATOS-Y-VARIABLES.md` por ser variable de alto peso predictivo. Este requerimiento es el que le da soporte funcional de captura.
- La estrategia de doble captura (texto libre + categoría) para el motivo de consulta asegura que el modelo siempre tenga al menos la categoría estructurada aunque el texto libre esté vacío (RF-NLP-004).
