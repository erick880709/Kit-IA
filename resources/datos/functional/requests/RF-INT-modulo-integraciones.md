# RF-INT: Módulo de Integraciones

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 51, Módulo Integraciones; 03-CATALOGO-DATOS-Y-VARIABLES.md
**Prioridad:** Media

## Descripción
El sistema se diseñará con una arquitectura de integración desacoplada que permita la interoperabilidad futura con la Historia Clínica Electrónica (HCE) institucional y otros sistemas hospitalarios. Para el alcance inmediato de la demo, se prioriza la exportación de datos en formatos estándar (FHIR/JSON/CSV) y la generación de datasets anonimizados para entrenamiento.

## Actores involucrados
- Arquitecto de Software
- Científico de Datos
- Administrador del Sistema

## Criterios de aceptación

### RF-INT-001 — Integración con Historia Clínica Electrónica
- Integración mediante API REST desacoplada cuando exista disponibilidad institucional.
- La integración es opcional para el funcionamiento del sistema (RNO-006: el sistema funciona sin IA; aplica mismo principio a HCE).
- Si está disponible: permite consultar antecedentes del paciente, eventos previos y notas clínicas sin re-captura manual.
- Si no está disponible: los datos se capturan manualmente mediante los formularios del sistema (RF-EVA-005, RF-PAC-003).

### RF-INT-002 — Integración con Sistemas Hospitalarios
- Arquitectura desacoplada basada en APIs (REST/HL7 FHIR como referencia futura).
- La integración no debe acoplar el sistema de triaje a la implementación específica del HIS (Hospital Information System).
- Sincronización de la clasificación validada con la HCE cuando exista integración (RNO-005).

### RF-INT-003 — Exportación en Formatos Estándar
- Formatos de exportación para interoperabilidad: FHIR (JSON), JSON plano, CSV.
- Aplica a: datos de pacientes (anonimizados), resultados de inferencia, registros de auditoría, reportes.

### RF-INT-004 — Exportación de Dataset de Entrenamiento
- Generación de datasets anonimizados para reentrenamiento del modelo.
- Cumplimiento obligatorio de anonimización antes de la exportación (Ley 1581 de 2012, RNS-009, RNS-010).
- El dataset exportado debe incluir todas las variables utilizadas como features por el modelo, con las mismas transformaciones aplicadas.
- Los identificadores directos (nombre, documento, dirección) se eliminan; los identificadores indirectos (fecha de nacimiento → edad, municipio → categoría regional) se transforman según la política de anonimización institucional.

## Dependencias / relacionados
- RNO-005: Sincronización con HCE cuando exista integración.
- RNS-009, RNS-010: Anonimización obligatoria.
- RNA-009: Datos de entrenamiento anonimizados.
- `03-CATALOGO-DATOS-Y-VARIABLES.md`: mapeo de entidades a fuentes de datos reales.
- DF-008: Integración con HCE desacoplada mediante APIs.

## Notas del analista
- Para el alcance de la demo (TFM), la integración con HCE no se implementa — los datos se capturan mediante formularios. La arquitectura debe dejar el punto de extensión documentado para futura integración real.
- FHIR se menciona como referencia futura; no es obligatorio implementarlo en la demo, pero sí diseñar los esquemas de datos de forma compatible con el modelo FHIR Patient/Observation/Encounter.
