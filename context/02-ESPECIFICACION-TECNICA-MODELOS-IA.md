# Especificación Técnica — Modelos de IA

Insumo directo para el Capítulo 4 del TFM y para el desarrollo del pipeline. Ata las reglas funcionales ya definidas (`RNA-*`, `RF-IA-*`, `RF-NLP-*`, `RF-MOD-*` en `CONTEXT_TRIA.txt`) a las decisiones técnicas cerradas en `01-CONTEXTO-MAESTRO-CONSOLIDADO.md`.

## 1. Features de entrada

### 1.1 Estructuradas (ver `03-CATALOGO-DATOS-Y-VARIABLES.md` para el detalle completo)

Signos vitales (FR, SpO₂, PA sistólica/diastólica, FC, temperatura), escala de dolor, edad, sexo, régimen de afiliación, comorbilidades, episodios previos de urgencias, **vía de llegada**, motivo de consulta estructurado.

> Variables de mayor peso predictivo según estado del arte (priorizar calidad de captura): **SpO₂, frecuencia respiratoria, temperatura corporal, presión sistólica, edad, vía de llegada.**

### 1.2 No estructuradas

Motivo de consulta en texto libre + historia clínica narrativa (si disponible/autorizada). Procesadas vía embeddings tipo BERT clínico — evaluar BioBERT-es o equivalente afinado en español médico (RF-NLP-002).

- Texto vacío → el pipeline continúa solo con variables estructuradas (RF-NLP-004, ya definido — no requiere cambio).

## 2. Arquitectura: ambas estrategias de fusión (decisión cerrada, no elegir una sola)

### Opción A — Early fusion
Vector de features estructuradas + embedding de texto concatenados antes del clasificador (XGBoost/RF sobre vector combinado, o red densa).

### Opción B — Late fusion
- Submodelo A (estructurado) → XGBoost / Random Forest.
- Submodelo B (texto) → BERT clínico + clasificador.
- Combinación: promedio ponderado, stacking o meta-clasificador — a determinar empíricamente en Fase 3.

**Regla de selección del modelo ganador:** mejor **Recall en Niveles I-II**, sin descuidar F1 global. Documentar la comparativa completa (no solo el ganador) en el Capítulo 5 — esto es lo que RF-IA-007 "Comparación de Modelos" y RF-MOD-* "Gestión de Modelos" ya habilitan funcionalmente: ambas arquitecturas coexisten como versiones distintas del modelo (RNA-006) durante la fase de validación.

### Baselines obligatorios (para poder afirmar que el multimodal aporta valor)
Regresión Logística, Random Forest, XGBoost — unimodales, solo datos estructurados.

## 3. Estrategia de umbral por clase (corrige RF-IA-003 del documento funcional)

`RF-IA-003` dice "seleccionará automáticamente la clase con mayor probabilidad". Interpretación correcta y no ambigua para implementación:

> El sistema selecciona la clase con mayor probabilidad **después de aplicar el umbral de decisión optimizado por clase para los Niveles I y II**, calibrado para maximizar Recall aunque implique una ligera caída de Precisión en esas dos clases. Para Niveles III-V se usa el umbral estándar (argmax).

**Justificación clínica (para el TFM):** el costo de un falso negativo en Nivel I-II (subclasificar a un paciente crítico) es inasumible; un falso positivo genera sobrecarga operativa pero no riesgo vital inmediato.

Técnica: threshold tuning sobre la curva ROC/PR por clase, documentando el punto de equilibrio elegido en el capítulo de resultados.

## 4. Manejo de desbalance de clases

Niveles IV-V son mayoritarios; Nivel I es raro pero crítico. Técnicas a evaluar y comparar: class weights, SMOTE, focal loss (si se usa red neuronal). Reportar métricas **por clase** además de macro-promedio, y AUPRC para las clases minoritarias.

## 5. Pipeline técnico (extiende el pipeline ya definido en `CONTEXTO_TRIAJE.txt` §5, sin cambios de fondo)

```
1. Ingesta: MIMIC-IV-ED + CSV colombianos (datos.gov.co, BDUA, Supersalud) + registro Hospital San Juan de Dios
2. Anonimización (Ley 1581/2012) — obligatoria antes de cualquier paso siguiente
3. Limpieza: imputación de nulos, outliers
4. Normalización numéricas / one-hot categóricas
5. Embeddings de texto libre (notas clínicas)
6. Split train/test + 10-fold cross-validation
7. Entrenamiento baselines unimodales (LR, RF, XGBoost)
8. Entrenamiento early fusion Y late fusion en paralelo
9. Threshold tuning por clase (Niveles I-II) sobre el modelo ganador
10. Evaluación: matriz de confusión, precisión/recall/F1/AUC-ROC (macro y por nivel), AUPRC clases minoritarias
11. Explicabilidad: SHAP sobre el modelo ganador
12. Comparación contra benchmarks (CTAS 0.882 AUROC, MTS, literatura — ver contexto-tfm.md §7)
13. Despliegue en demo funcional
```

## 6. Explicabilidad (XAI) — contrato de salida por predicción

Cada predicción debe entregar (mapea 1:1 a RF-XAI-001 a 006, ya definidos funcionalmente):
1. Nivel predicho + probabilidad/confianza + **versión del modelo** (RNA-002, RNA-005).
2. Top-5 a Top-10 variables SHAP con mayor influencia, en lenguaje clínico (ej. "saturación de O₂ baja (88%) fue el factor de mayor peso") — no solo el nombre técnico de la variable.
3. Comparación implícita con criterio MTS/Manchester cuando coincida (refuerza confianza clínica, ya documentado en el estado del arte del TFM).
4. Tiempo de inferencia (RNA-003) — objetivo funcional: **< 3 segundos** (RNP-001, ya definido).

## 7. Trazabilidad y registro (sin cambios — ya bien cubierto por el documento funcional)

Cada predicción queda registrada para auditoría clínica y detección de deriva (RNA-010, RNAU-*). El registro de triaje exigido por normativa colombiana (paciente anonimizado, fecha/hora, nivel IA vs. nivel humano, signos vitales, motivo de consulta, variables SHAP top) se genera como resumen descargable/visualizable en la demo — ya cubierto por RF-REP-* y RF-AUD-006.

## 8. Limitación explícita a documentar en el TFM

MIMIC-IV-ED es de EE.UU. — un modelo entrenado solo con esa base no es válido para el contexto colombiano por sesgo geográfico. El fine-tuning con datos del Hospital San Juan de Dios (ya autorizado) es obligatorio, no opcional, y debe documentarse como estrategia de adaptación en el capítulo de limitaciones (Cap. 6).
