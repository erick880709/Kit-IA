# Contexto del TFM — Sistema de Triaje Multimodal basado en IA (Colombia)

> Documento de contexto para retomar el trabajo en cualquier sesión futura, sin necesidad de releer el PDF completo. Última actualización: 13 de julio de 2026.

## 1. Ficha del proyecto

| Campo | Valor |
|---|---|
| Título | Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia |
| Programa | Máster Universitario en Inteligencia Artificial — UNIR |
| Modalidad | TFM grupal (3 integrantes) |
| Autores (orden alfabético requerido) | Medina Betancur, Diego Andrés · Rivera Villanueva, Leyniker · Soto Díaz, Erick Duván |
| Directora | Damaris Fuentes Lorenzo |
| Ciudad | Armenia, Colombia |
| Fecha del borrador actual | Mayo de 2026 |
| Tipología del trabajo | Tipo 2 (Desarrollo software) combinado con Tipo 3 (Piloto experimental / comparativa) |

## 2. Problema que resuelve

Los servicios de urgencias en Colombia están saturados: +30 millones de consultas/año, 30-40% de casos no urgentes (niveles IV-V) desplazando la atención de pacientes críticos. El 74% de las instituciones usa esquemas de triaje sin validación internacional (solo interpretación básica de la Resolución 5596 de 2015), y un 13% no tiene claro qué sistema aplica. Esto genera alta variabilidad, subjetividad y riesgo clínico.

## 3. Propuesta de solución

Un sistema de apoyo a la decisión clínica (no reemplaza el criterio médico) que:
1. Integra datos **multimodales**: signos vitales, escala de dolor, variables demográficas, antecedentes clínicos estructurados + notas clínicas en texto libre.
2. Clasifica automáticamente al paciente en los **5 niveles de la Resolución 5596 de 2015**.
3. Incorpora **explicabilidad (XAI)** vía SHAP para generar confianza clínica.
4. Está **adaptado al marco regulatorio y epidemiológico colombiano** (a diferencia de la literatura existente, que casi no cubre LATAM).

### Niveles de triaje (Resolución 5596/2015)

| Nivel | Descripción | Tiempo máx. de atención |
|---|---|---|
| I | Resucitación (máxima urgencia) | Inmediata |
| II | Emergencia (riesgo vital) | 30 min |
| III | Urgencia | 2 horas |
| IV | Menor urgencia | 4 horas |
| V | No urgencia (consulta externa) | 24 horas |

## 4. Objetivos

**General:** Diseñar y validar un sistema inteligente de triaje multimodal que optimice precisión y consistencia en la clasificación, con metas cuantitativas:
- F1-score ≥ 0,82
- Precisión ≥ 0,85
- Recall ≥ 0,80
- AUC-ROC ≥ 0,87

**Específicos:**
1. Diagnosticar limitaciones actuales del triaje en Colombia.
2. Seleccionar/preprocesar variables clínicas determinantes.
3. Diseñar arquitectura multimodal (fusión de datos estructurados + texto libre).
4. Evaluar rendimiento vs. benchmarks unimodales/multimodales de la literatura.
5. Incorporar módulo de explicabilidad SHAP.
6. Analizar viabilidad de despliegue e impacto en gestión hospitalaria.

## 5. Fuentes de datos

| Fuente | Tipo | Rol |
|---|---|---|
| MIMIC-IV-ED v2.2 (PhysioNet) | Internacional, 422.500 admisiones | Entrenamiento base / preentrenamiento |
| Registro clínico Hospital San Juan de Dios | Local, datos sanitarios reales | Adaptación al contexto colombiano — **requiere autorización del Comité de Ética (Art. 2.7 Reglamento UNIR)** |
| "Clasificación en Triaje Urgencias" (Min. Salud, datos.gov.co) | CSV público | Distribución real de niveles I-V en Colombia |
| BDUA (ADRES) | CSV público | Variables demográficas, régimen de afiliación, perfil socioeconómico |
| Datos abiertos Supersalud | CSV público | Desempeño operativo de EPS/IPS |

Cumplimiento: Ley 1581 de 2012 (protección de datos personales, Colombia).

## 6. Modelos y arquitectura técnica

- **Baseline unimodal:** Regresión Logística, Random Forest, XGBoost.
- **Arquitectura multimodal propuesta:** fusión temprana (early fusion, a nivel de características) vs. fusión tardía (late fusion, a nivel de decisiones).
- **Texto libre (notas clínicas):** embeddings tipo BERT (referencia: Levin et al. 2021, F1 0.81, +12% vs. unimodal).
- **Explicabilidad:** SHAP — predictores más relevantes según literatura: frecuencia respiratoria, saturación de oxígeno, temperatura corporal, presión arterial sistólica, edad, vía de llegada.
- **Stack:** Python, pandas, scikit-learn, TensorFlow/Keras, cloud-native.
- **Validación:** 10-fold cross-validation, matrices de confusión, comparación contra CTAS (AUROC 0.882) y otros estándares internacionales.

## 7. Benchmarks de la literatura (para contrastar resultados propios)

| Estudio | Modelo | Métrica |
|---|---|---|
| Raita et al. 2019 | RF / regresión logística / árboles | AUC-ROC 0.87 |
| Hong, Haimovich & Taylor 2018 | DNN (972.756 admisiones) | AUC-ROC 0.93 |
| Ueareekul et al. 2024 | XGBoost multimodal (163.452 consultas) | AUROC 0.917, AUPRC 0.629 |
| CTAS (estándar canadiense) | — | AUROC 0.882 |
| Levin et al. 2021 | Estructurado + BERT | F1 0.81 |
| Lee, Lee & Shin 2022 | SHAP sobre modelo de triaje | Precisión 0.91, Recall 0.83, F1 0.87 |

## 8. Estado del documento (a la fecha)

- ✅ Resumen / Abstract
- ✅ Cap. 1 Introducción
- ✅ Cap. 2 Contexto y Estado del Arte
- ✅ Cap. 3 Objetivos y Metodología
- ❌ Cap. 4 Desarrollo de la contribución — **pendiente**
- ❌ Cap. 5 Resultados y discusión — **pendiente**
- ❌ Cap. 6 Conclusiones y trabajo futuro — **pendiente**
- ❌ Apéndices — solo título, sin contenido
- ❌ Sección "Organización del trabajo en grupo" (obligatoria antes de la Introducción) — **falta agregarla**

## 9. Pendientes críticos de cumplimiento normativo

1. Insertar sección "Organización del trabajo en grupo" antes del Cap. 1, avalada por Damaris Fuentes Lorenzo.
2. Corregir orden alfabético de autores en portada (Medina → Rivera → Soto).
3. Confirmar/tramitar autorización del Comité de Ética para el uso de datos del Hospital San Juan de Dios (Art. 2.7 del Reglamento) — bloqueante para depósito y defensa si no se resuelve.
4. Pasar el trabajo por la herramienta anti-plagio de UNIR antes de solicitar autorización de depósito a la directora.

## 10. Próximos pasos sugeridos

1. Redactar Cap. 4 (arquitectura, preprocesamiento final, entrenamiento de modelos base y multimodal).
2. Redactar Cap. 5 (resultados, matrices de confusión, comparación con benchmarks, análisis SHAP).
3. Redactar Cap. 6 (conclusiones, limitaciones, trabajo futuro).
4. Cerrar apéndices (código relevante, tablas extendidas).
5. Preparar la plantilla de defensa (repartida equitativamente entre los 3 integrantes).
