# Checklist de Prevención de Fuga de Datos (Leakage) — Pipeline de Triaje Multimodal

> Recorre cada etapa del pipeline definido en `guia-implementacion-triaje-multimodal.md` de
> `builder` y verifica el punto correspondiente. Cualquier ítem marcado ❌ es bloqueante: las
> métricas obtenidas con ese pipeline no son confiables hasta corregirlo.

## 1. Split train/test/validación

- [ ] El split se hace por **identificador de paciente/episodio** (`stay_id` en MIMIC, el
      identificador anonimizado equivalente en San Juan de Dios), no por fila.
- [ ] Si un mismo paciente tiene múltiples visitas, todas caen en el mismo lado del split.
- [ ] El split es **estratificado** por nivel de triaje (`StratifiedKFold` / `train_test_split(...,
      stratify=y)`), no aleatorio simple — con Nivel I raro, un split no estratificado puede dejar
      folds sin ningún ejemplo de esa clase.
- [ ] Si se mezclan MIMIC + San Juan de Dios, decidir explícitamente si el split respeta la fuente
      (para poder medir el efecto del fine-tuning, fase 5 de `validacion-cientifica-ml`) o si se
      mezcla — documentar la decisión, no dejarla implícita.

## 2. Preprocesamiento (imputación, escalado, codificación)

- [ ] `SimpleImputer`, `StandardScaler`, `OneHotEncoder` (o equivalentes) se **ajustan (`fit`) solo
      con el conjunto de entrenamiento**.
- [ ] El conjunto de test/validación solo usa `transform`, nunca `fit_transform`.
- [ ] Si se usa un `ColumnTransformer`/`Pipeline` de sklearn (patrón ya definido en
      `guia-implementacion-triaje-multimodal.md` §3), confirmar que todo el pipeline se ajuste
      dentro de cada fold de CV, no una sola vez sobre el dataset completo antes del CV.

## 3. Balanceo de clases (SMOTE / class weights / focal loss)

- [ ] SMOTE (o cualquier técnica de oversampling) se aplica **después** del split, solo sobre
      train — nunca antes, porque generaría muestras sintéticas correlacionadas entre train y test.
- [ ] Si se usa SMOTE dentro de CV, se aplica dentro de cada fold (`imblearn.pipeline.Pipeline`,
      no `sklearn.pipeline.Pipeline`, para que el paso de resampling entre en el `fit` por fold).
- [ ] `class_weight='balanced'` (si se usa en vez de SMOTE) no tiene riesgo de leakage — se puede
      calcular con el fold de entrenamiento directamente.

## 4. Embeddings de texto libre (BERT/BioBERT-es)

- [ ] Si se hace *fine-tuning* del modelo de lenguaje (no solo inferencia con pesos preentrenados),
      el fine-tuning se hace solo con train.
- [ ] Si se usa un modelo preentrenado sin fine-tuning adicional (uso más común y más seguro para
      este alcance de TFM), no hay leakage en este paso — documentar explícitamente cuál de las dos
      rutas se tomó.

## 5. Selección de features / selección de modelo

- [ ] Si se hace selección de variables (`SelectKBest`, importancia de features, etc.), se hace
      dentro de cada fold de CV, no una sola vez sobre el dataset completo antes de dividir.
- [ ] La búsqueda de hiperparámetros (`GridSearchCV`/`RandomizedSearchCV`/Optuna) usa un split
      anidado (nested CV) o al menos un conjunto de validación separado del test final — el test
      final se toca **una sola vez**, al final, para el número que va al TFM.

## 6. Umbral de decisión por clase (Niveles I-II)

- [ ] El umbral óptimo por clase (threshold tuning descrito en
      `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §3) se calibra usando un conjunto de validación
      distinto del test final — si se calibra directamente sobre el test, la métrica de Recall
      reportada está inflada porque el umbral "ya sabía" el resultado que buscaba producir.

## 7. Fuente MIMIC vs. San Juan de Dios

- [ ] Si el fine-tuning con San Juan de Dios ocurre después de preentrenar con MIMIC, confirmar
      que ningún paciente de San Juan de Dios haya sido usado (aunque sea indirectamente, vía un
      dataset combinado mal particionado) en el conjunto de entrenamiento de MIMIC.
- [ ] El conjunto de test final para reportar las métricas del TFM debe incluir una porción real de
      datos colombianos (San Juan de Dios) — un modelo evaluado solo contra el test de MIMIC no
      demuestra la adaptación al contexto colombiano que es el objetivo específico del proyecto.
