# RT-005: Pipeline Técnico de Entrenamiento y Evaluación

**Tipo:** Requisito técnico
**Categoría:** Infraestructura / MLOps
**Fuente:** 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §5; contexto-tfm.md §6; CONTEXTO_TRIAJE.txt v2.0 §5

## Descripción
El pipeline técnico abarca desde la ingesta de datos crudos hasta la evaluación del modelo entrenado y la generación de artefactos para la demo. El pipeline está definido como una secuencia de 13 pasos que garantizan reproducibilidad, trazabilidad y calidad en cada etapa.

## Pipeline completo (13 pasos)

```
Paso  1. Ingesta de datos: MIMIC-IV-ED + CSV colombianos (datos.gov.co, BDUA, Supersalud) + registro Hospital San Juan de Dios.
Paso  2. Anonimización (Ley 1581/2012) — OBLIGATORIO antes de cualquier paso siguiente. Eliminación de identificadores directos e indirectos.
Paso  3. Limpieza: imputación de valores nulos (mediana/moda para numéricas, categoría "Desconocido" para categóricas), detección y tratamiento de outliers (rango intercuartílico o límites fisiológicos).
Paso  4. Normalización de variables numéricas (StandardScaler o MinMaxScaler) y codificación one-hot de variables categóricas.
Paso  5. Embeddings de texto libre (notas clínicas): tokenización + inferencia con BERT clínico (BioBERT-es o BETO) → vector de embeddings.
Paso  6. Split train/test (80/20 estratificado por nivel de triaje) + 10-fold cross-validation sobre el conjunto de entrenamiento.
Paso  7. Entrenamiento de baselines unimodales: Regresión Logística, Random Forest, XGBoost (solo datos estructurados, sin embeddings de texto).
Paso  8. Entrenamiento de early fusion Y late fusion en paralelo (ver RT-001).
Paso  9. Threshold tuning por clase (Niveles I-II) sobre el conjunto de validación para el modelo con mejor desempeño preliminar.
Paso 10. Evaluación final sobre el conjunto de test: matriz de confusión 5×5, Precision/Recall/F1/AUC-ROC (macro y por nivel), AUPRC para clases minoritarias.
Paso 11. Explicabilidad: cálculo de valores SHAP sobre el conjunto de test para el modelo ganador.
Paso 12. Comparación contra benchmarks de la literatura (CTAS AUROC 0.882, Raita et al. 2019, Hong et al. 2018, Ueareekul et al. 2024, Levin et al. 2021).
Paso 13. Serialización del modelo ganador + metadatos para despliegue en la demo funcional.
```

## Criterio medible / restricción concreta
- Cada paso debe ser ejecutable de forma independiente y reproducible (scripts Python, no celdas de notebook ejecutadas manualmente en orden arbitrario).
- El split train/test debe ser estratificado por nivel de triaje para garantizar que todas las clases estén representadas en ambas particiones.
- La semilla aleatoria debe fijarse para reproducibilidad (random_state=42 o similar).
- Las transformaciones (scaler, one-hot encoder) se ajustan sobre el conjunto de entrenamiento y se aplican al conjunto de test (nunca al revés, para evitar data leakage).
- Los embeddings de texto pueden precomputarse offline (para acelerar experimentos) pero el pipeline debe documentar cómo se generarían en producción (inferencia en tiempo real).

## Impacto en la arquitectura
- El pipeline es offline (no se ejecuta en la demo). El artefacto de salida es el modelo serializado + metadatos.
- La demo carga el modelo serializado y aplica las mismas transformaciones (scaler, encoder, tokenizador) que se guardaron junto con el modelo.
- La separación estricta entre entrenamiento (offline) e inferencia (online en la demo) es un principio arquitectónico fundamental.

## Notas del analista
- Los pasos 3 y 5 (limpieza + embeddings) son los más costosos computacionalmente. Planificar tiempo suficiente de ejecución.
- Para la demo TFM, el pipeline puede ejecutarse en una máquina local con CPU (no requiere GPU, aunque acelera significativamente los embeddings BERT). Si no se dispone de GPU, evaluar modelos más ligeros (distilBERT, BETO-small) o limitar el tamaño del dataset de entrenamiento.
