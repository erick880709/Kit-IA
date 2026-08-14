# Contexto de la Aplicación — Motor de Clasificación de Triaje con IA

> Este documento define el "qué" y el "cómo" del sistema de IA que decide si un caso es o no una emergencia (y en qué nivel I-V). Sirve de insumo directo para el Capítulo 4 (Desarrollo de la contribución) del TFM.

## 1. Objetivo funcional de la aplicación

Dado un conjunto de datos de un paciente que llega a urgencias, el sistema debe predecir a cuál de los **5 niveles de la Resolución 5596 de 2015** pertenece, con una salida explicable, para apoyar (no reemplazar) al profesional que hace el triaje.

```
Entrada (datos del paciente) → Modelo multimodal → Nivel I-V + explicación SHAP → Apoyo a decisión humana
```

## 2. Definición operativa de "emergencia" (regla de negocio, no solo modelo)

El sistema no decide "es emergencia sí/no" de forma binaria — clasifica en 5 niveles ordinales, donde I-II se consideran clínicamente críticos (emergencia real) y IV-V son claramente no urgentes. El nivel III es la zona gris que más valor aporta clasificar bien.

| Nivel | Umbral clínico de referencia (a definir con datos reales/protocolo del hospital) | Acción del sistema |
|---|---|---|
| I — Resucitación | Riesgo vital inminente (paro, shock, vía aérea comprometida) | Alerta inmediata, prioridad máxima en cola |
| II — Emergencia | Riesgo vital no inminente pero alto (ej. dolor torácico agudo, alteración de conciencia) | Alerta alta, atención ≤30 min |
| III — Urgencia | Cuadro que requiere atención pero estable | Cola prioritaria, ≤2 h |
| IV — Menor urgencia | Estable, sin riesgo | Cola estándar, ≤4 h |
| V — No urgencia | Remitible a consulta externa | Redirección, ≤24 h |

**Importante:** estos umbrales deben calibrarse contra los datos reales de "Clasificación en Triaje Urgencias" (Min. Salud) y el registro del Hospital San Juan de Dios, no asumirse a priori — es justamente lo que el modelo aprende.

## 3. Variables de entrada (features)

### 3.1 Datos estructurados

| Categoría | Variables | Fuente típica |
|---|---|---|
| Signos vitales | Frecuencia respiratoria, saturación de O₂, presión arterial (sistólica/diastólica), frecuencia cardíaca, temperatura corporal | Toma directa en admisión |
| Dolor | Escala de dolor (0-10) | Reporte del paciente |
| Demográficas | Edad, sexo, régimen de afiliación (BDUA) | BDUA / admisión |
| Antecedentes | Comorbilidades, episodios previos de urgencias, medicación crónica | Historia clínica |
| Administrativas | Vía de llegada (ambulancia, particular, remisión), motivo de consulta estructurado (código) | Sistema de admisión |

> Según el estado del arte revisado (Lee et al. 2022; Casteñeda-Lopera et al. 2024), las variables con mayor peso predictivo consistente son: **saturación de O₂, frecuencia respiratoria, temperatura corporal, presión arterial sistólica, edad y vía de llegada.** Priorizar la calidad de captura de estas.

### 3.2 Datos no estructurados

- **Motivo de consulta en texto libre** (notas de enfermería en admisión).
- **Historia clínica narrativa** (si disponible y autorizada).
- Procesamiento: embeddings tipo BERT (clínico, idealmente afinado en español médico — evaluar BioBERT-es o similar en Cap. 4).

## 4. Arquitectura del modelo

### Opción A — Fusión temprana (early fusion)
Concatenar el vector de features estructuradas + embedding del texto en un único vector de entrada antes del modelo de clasificación (XGBoost/RF sobre vector combinado, o red densa).

### Opción B — Fusión tardía (late fusion)
Dos submodelos independientes:
- Submodelo A: estructurado → XGBoost/Random Forest.
- Submodelo B: texto → BERT + clasificador.
- Combinación de las salidas (promedio ponderado, stacking, o meta-clasificador).

**Recomendación para el TFM:** documentar y comparar ambas (es justamente el objetivo específico 3 y parte de la Fase 3 metodológica) y justificar cuál se usa en la versión final según el AUC-ROC/F1 obtenido.

### Pipeline técnico

```
1. Ingesta (MIMIC-IV-ED + CSV colombianos + registro hospital)
2. Limpieza: imputación de nulos, outliers
3. Normalización de numéricas / one-hot de categóricas
4. Embeddings de texto libre (notas clínicas)
5. Split train/test + 10-fold cross-validation
6. Entrenamiento modelos baseline (unimodal): Regresión Logística, RF, XGBoost
7. Entrenamiento modelo multimodal (early/late fusion)
8. Evaluación: matriz de confusión, precisión, recall, F1, AUC-ROC (macro y por nivel)
9. Explicabilidad: SHAP sobre el modelo ganador
10. Comparación contra benchmarks (CTAS, MTS, literatura)
```

## 5. Métricas objetivo y criterios de éxito

| Métrica | Meta (definida en Cap. 3 del TFM) |
|---|---|
| F1-score | ≥ 0,82 |
| Precisión | ≥ 0,85 |
| Recall | ≥ 0,80 |
| AUC-ROC | ≥ 0,87 |

Consideraciones adicionales para el desbalance de clases (los niveles IV-V suelen ser mayoritarios, I es raro pero crítico):
- Evaluar métricas **por clase**, no solo macro-promedio — un buen F1 global puede esconder mal desempeño en Nivel I (el más crítico de detectar).
- Considerar AUPRC (no solo AUROC) para las clases minoritarias, como hace Ueareekul et al. 2024.
- Técnicas a evaluar: class weights, SMOTE, focal loss (si se usa red neuronal).

## 6. Explicabilidad (XAI) — qué debe responder el sistema

Para cada predicción, el sistema debe poder mostrar al clínico:
1. Nivel predicho + probabilidad/confianza.
2. Top-5 variables que más influyeron (valores SHAP), en lenguaje clínico comprensible (ej. "saturación de O₂ baja (88%) fue el factor de mayor peso").
3. Comparación implícita con el criterio MTS/Manchester cuando coincida, para reforzar confianza clínica (los hallazgos de Lee et al. 2022 muestran convergencia con MTS en frecuencia respiratoria, SpO₂ y temperatura).

## 7. Restricciones y consideraciones de gobernanza

- **El sistema es de apoyo, no de decisión autónoma** — el criterio humano prevalece siempre (esto debe quedar explícito en cualquier interfaz o documento del sistema).
- **Autorización ética pendiente** para datos del Hospital San Juan de Dios (Art. 2.7 Reglamento TFM UNIR) — no se puede entrenar/usar con esos datos reales hasta tenerla.
- **Anonimización obligatoria** conforme a Ley 1581 de 2012 antes de cualquier procesamiento.
- **Sesgo geográfico:** MIMIC-IV-ED es de EE.UU. — el modelo entrenado solo con esa base no es válido para el contexto colombiano sin la fase de adaptación/fine-tuning con datos locales; esto debe quedar como limitación explícita en Cap. 6.
- **Trazabilidad:** cada predicción debería quedar registrada (para auditoría clínica y detección de deriva del modelo en producción).

## 8. Qué falta definir con la directora (Damaris Fuentes Lorenzo)

- Framework definitivo de fusión (early vs. late) a implementar en la versión final.
- Umbral de probabilidad para "alerta" en niveles I-II (¿se prioriza recall sobre precisión ahí, dado el costo clínico de un falso negativo?).
- Alcance real del prototipo: ¿modelo entrenado y evaluado offline, o se construye también una interfaz/demo funcional?
- Confirmación del estado del trámite ético para los datos del Hospital San Juan de Dios.
