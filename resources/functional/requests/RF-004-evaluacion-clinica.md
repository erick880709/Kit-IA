# RF-004: Evaluación Clínica

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-EVA-001 a 007) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Alta

## Descripción
El sistema debe permitir registrar la evaluación clínica: motivo de consulta (estructurado y texto libre), escala de dolor (0-10), escala de Glasgow, nivel de conciencia, antecedentes clínicos (comorbilidades, embarazo, medicación relevante), alergias y observaciones en texto libre.

Cubre los requerimientos fuente: RF-EVA-001 a RF-EVA-007.

## Actores involucrados
Enfermera y médico.

## Criterios de aceptación
- El motivo de consulta se captura en dos campos: categoría estructurada (catálogo controlado ENT-004) y texto libre (RF-EVA-001 extendido en 06 §5).
- Los antecedentes se capturan por autorreporte/anamnesis cuando no exista integración con Historia Clínica Electrónica (RF-INT-001 condicionado).
- Texto libre vacío no bloquea el flujo (RF-NLP-004).

## Dependencias / relacionados
[[RF-005]], [[RF-015]], RD-002 (ENT-004, ENT-005, ENT-008).

## Notas del analista
La captura dual estructura/texto libre permite al pipeline continuar solo con variables estructuradas si el NLP no tiene entrada.
