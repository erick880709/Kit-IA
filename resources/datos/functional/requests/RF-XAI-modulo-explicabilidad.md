# RF-XAI: Módulo de Explicabilidad (XAI)

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 46, Módulo Explicabilidad; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §6
**Prioridad:** Alta

## Descripción
Toda predicción generada por el modelo de IA deberá ir acompañada de una explicación interpretable que muestre qué variables influyeron más en la decisión, en qué dirección (aumentaron o disminuyeron la probabilidad de cada nivel) y con qué magnitud. La explicabilidad es un requisito no negociable del sistema: sin ella, el profesional no puede confiar en la recomendación ni ejercer un juicio clínico informado.

## Actores involucrados
- Médico de Urgencias (consulta la explicación)
- Enfermera de Triaje
- Auditor (revisa explicaciones históricas)

## Criterios de aceptación

### RF-XAI-001 — Generar Explicación SHAP
- Toda predicción debe generar automáticamente una explicación utilizando SHAP (SHapley Additive exPlanations).
- La explicación se genera como parte del pipeline de inferencia, no como un paso aparte.
- La explicación queda asociada a la predicción y se almacena para auditoría (RNX-005).

### RF-XAI-002 — Top Variables Más Influyentes
- Mostrar el ranking de las top-5 a top-10 variables con mayor influencia en la predicción.
- Las variables deben presentarse en **lenguaje clínico comprensible** (ej. "Saturación de O₂ baja (88%) fue el factor de mayor peso para clasificar como Nivel II"), no solo con el nombre técnico de la columna.
- Cada variable muestra su valor SHAP (magnitud y dirección del impacto).

### RF-XAI-003 — Impacto Positivo (a favor del nivel predicho)
- Identificar y mostrar las variables que incrementaron la probabilidad del nivel asignado.
- Representación visual con código de color (ej. rojo = aumenta probabilidad).

### RF-XAI-004 — Impacto Negativo (en contra del nivel predicho)
- Identificar y mostrar las variables que disminuyeron la probabilidad del nivel asignado.
- Representación visual con código de color diferenciado (ej. azul = disminuye probabilidad).

### RF-XAI-005 — Visualización Gráfica Interpretable
- Gráficos de barras horizontales con el ranking de variables SHAP.
- Waterfall plot o force plot para visualizar cómo cada variable contribuye a la predicción final.
- Comparación implícita con criterios MTS/Manchester cuando las variables coincidan, para reforzar la confianza clínica.

### RF-XAI-006 — Exportar Explicación
- Permitir exportar la explicación en formato descargable (parte del resumen de triaje, RF-REP-006).
- Formatos: visualización en pantalla, PDF en el registro de triaje descargable.

## Dependencias / relacionados
- RF-IA-001: La explicación se genera junto con la inferencia.
- RNX-001 a 006: Reglas de Explicabilidad.
- RNP-004: La generación de SHAP no debe impedir la continuidad asistencial.
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §6: contrato de salida por predicción (4 elementos obligatorios).
- `04-ESPECIFICACION-APLICACION-DEMO.md`: pantalla de Explicación SHAP.

## Notas del analista
- El contrato de salida definido en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §6 requiere 4 elementos: (1) nivel predicho + probabilidad + versión del modelo, (2) top variables SHAP en lenguaje clínico, (3) comparación con MTS/Manchester cuando coincida, (4) tiempo de inferencia.
- La generación de SHAP puede ser computacionalmente costosa; RNP-004 establece que no debe bloquear el flujo asistencial. Evaluar SHAP aproximado (KernelExplainer con submuestreo) vs. exacto (TreeExplainer para XGBoost/RF).
