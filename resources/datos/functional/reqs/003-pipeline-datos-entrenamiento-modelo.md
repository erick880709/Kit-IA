---
id: 003
slug: pipeline-datos-entrenamiento-modelo
tipo: epica
prioridad: Must-Have
orden: 2
dependencias: E1
ejecuta_en_paralelo_con: E2
alimenta_a: E4
fecha: 2026-07-19
---

# ÉPICA 3 — Pipeline de Datos y Entrenamiento del Modelo

## Necesidad de Negocio

Construir el pipeline offline que entrena, evalúa y serializa el modelo de IA multimodal. Este pipeline toma datos clínicos crudos de múltiples fuentes (MIMIC-IV-ED, Hospital San Juan de Dios, BDUA, datos.gov.co, Supersalud), los anonimiza, los transforma en features de entrenamiento, entrena ambas arquitecturas (early fusion y late fusion), aplica optimización de umbral por clase para Niveles I-II, y genera el artefacto serializado que la demo cargará en la Épica 4.

## Justificación

Sin un modelo entrenado, el sistema es solo un formulario de captura de datos. El valor diferencial del TFM reside en el modelo multimodal con datos colombianos. Esta épica produce el activo más importante del proyecto: el modelo entrenado con métricas que demuestren su utilidad clínica (F1 ≥ 0.82, Recall en Niveles I-II maximizado).

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Científico de Datos | Ejecutor | Ejecutar y validar el pipeline de entrenamiento |
| Investigador | Beneficiario | Consumir las métricas y artefactos para el Cap. 5 del TFM |
| Administrador IA | Aprobador | Validar que el modelo cumple las metas antes de serializarlo para la demo |

## Alcance

- ✅ IN SCOPE:
  - Ingesta de 5 fuentes de datos (MIMIC-IV-ED, San Juan de Dios, BDUA, datos.gov.co, Supersalud)
  - Anonimización obligatoria (Ley 1581/2012) como paso explícito del pipeline
  - Limpieza: imputación de nulos, detección de outliers
  - Normalización (StandardScaler) y codificación one-hot
  - Embeddings de texto libre con BERT clínico en español (BioBERT-es / BETO)
  - Split train/test estratificado por nivel + 10-fold CV
  - Entrenamiento de 3 baselines unimodales (LR, RF, XGBoost)
  - Entrenamiento de early fusion y late fusion en paralelo
  - Manejo de desbalance: class weights, SMOTE, focal loss (a evaluar)
  - Threshold tuning por clase para Niveles I-II (maximizar Recall)
  - Evaluación con métricas por clase + macro-promedio + AUPRC
  - Explicabilidad SHAP sobre el modelo ganador
  - Comparación contra benchmarks de la literatura
  - Serialización del modelo ganador + transformadores (scaler, encoder) para la demo

- ❌ OUT OF SCOPE:
  - Reentrenamiento automático (MLOps productivo)
  - Servicio de inferencia online (es Épica 4)
  - Monitoreo de deriva en producción
  - Pipelines CI/CD para despliegue continuo

## Criterios de Aceptación

```
DADO que existen datos crudos de las 5 fuentes
CUANDO se ejecuta el paso de anonimización
ENTONCES ningún identificador directo (nombre, documento, dirección) persiste en los datos de entrenamiento

DADO que el pipeline de entrenamiento se ejecuta hasta el final
CUANDO se evalúa el modelo sobre el conjunto de test
ENTONCES F1-score macro-promedio ≥ 0.82, Precisión ≥ 0.85, Recall ≥ 0.80, AUC-ROC ≥ 0.87

DADO que el modelo ganador fue seleccionado (early o late fusion)
CUANDO se aplica el umbral optimizado para Niveles I-II
ENTONCES el Recall en Nivel I y Nivel II es superior al que se obtendría con argmax puro

DADO que el pipeline se ejecuta en una máquina sin GPU
CUANDO se generan los embeddings de texto
ENTONCES el tiempo total de entrenamiento no excede 8 horas para el dataset completo

DADO que el modelo ganador está serializado
CUANDO se carga en un entorno Python limpio con las mismas versiones de librerías
ENTONCES produce exactamente la misma predicción para un mismo vector de entrada (reproducibilidad)
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| F1-score (macro-promedio) | 0 (sin modelo) | ≥ 0.82 | Cierre de E3 |
| Recall Nivel I | 0 (sin modelo) | Máximo alcanzable sin degradar F1 global >10% | Cierre de E3 |
| Recall Nivel II | 0 (sin modelo) | Máximo alcanzable sin degradar F1 global >10% | Cierre de E3 |
| AUC-ROC (macro) | 0 (sin modelo) | ≥ 0.87 | Cierre de E3 |
| Comparativa multimodal vs. unimodal | No existe | Mejora demostrable (ΔF1 ≥ 0.03 sobre mejor baseline) | Cierre de E3 |
| Reproducibilidad | No existe | 100% (mismo seed → mismos resultados) | Cierre de E3 |

## Prioridad (MoSCoW)

- **Must Have:** Pipeline de 13 pasos completo, ambas arquitecturas, baselines unimodales, umbral por clase, métricas por clase, serialización del modelo
- **Should Have:** AUPRC para clases minoritarias, comparación detallada contra benchmarks de literatura, visualizaciones del pipeline
- **Could Have:** Experimentos adicionales con arquitecturas alternativas (redes neuronales), datos sintéticos aumentados
- **Won't Have (en este alcance):** AutoML, búsqueda automática de hiperparámetros, MLOps productivo

## Dependencias

- **E1 (Fundación):** Stack tecnológico definido, acceso a fuentes de datos
- **Se ejecuta en paralelo con E2 (Flujo Clínico):** no hay dependencia mutua — el equipo de datos entrena el modelo mientras el equipo de frontend construye la UI
- **E4 (Motor IA):** E3 produce el artefacto (modelo serializado) que E4 carga en la demo

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RT-003-fuentes-datos-entrenamiento.md` | Técnico |
| `RT-004-desbalance-clases-umbral.md` | Técnico |
| `RT-005-pipeline-tecnico-entrenamiento.md` | Técnico |
| `RF-NLP-procesamiento-lenguaje-natural.md` | Funcional |
| `RT-001-arquitectura-multimodal-fusion.md` | Técnico |
| `RNF-006-metas-cuantitativas-modelo.md` | No funcional |
