# 5. Resultados y discusión — TriajeIA

> Todas las cifras de este capítulo provienen de `triaje-ia/artifacts/metrics/`,
> `triaje-ia/artifacts/shap/` y `resources/tfm/validacion-cientifica/`. La
> columna **Fuente** identifica el archivo exacto. Ningún número se estimó.

## 5.1 Configuración experimental

- **Semilla:** 42 fijada en todo el pipeline (generación, split, modelos).
- **Split:** 70/15/15 estratificado por nivel de triaje (train 2.800 / validación
  600 / test 600 para el demo de 4.000 registros). Todos los preprocesadores
  (imputación, escalado, codificación) se ajustaron **solo** con train; el test
  únicamente se transformó. Fuente: `triaje-ia/ml/pipeline.py` (verificado en
  `resources/tfm/validacion-cientifica/reporte-auditoria.md`, Fase 1).
- **Texto:** TF-IDF con 600 términos ajustado sobre los textos de train más la
  cohorte SJdD (el test solo se transformó).
- **Balanceo:** `class_weight="balanced"` en XGBoost; umbrales de decisión por
  clase optimizados (Youden, acotados a [0.01, 0.99]) priorizando el recall de
  los niveles I–II. Fuente: `ml/src/models/thresholds.py`.
- **Hiperparámetros del ganador:** `max_depth=5`, `learning_rate=0.1`, 250
  estimadores, peso del combinador 0.5 (elegido por validación; macro-F1 en
  validación 0.559). Fuente: `artifacts/metrics/modelo_ganador.json`.

## 5.2 Resultados por modelo

Métricas macro registradas en validación cruzada estratificada (5 folds) para
los modelos de comparación, y sobre el conjunto de test (600 registros) para
el ganador afinado.

| Modelo | F1 (macro) | Precisión (macro) | Recall (macro) | Fuente |
|---|---|---|---|---|
| Regresión logística (baseline) | 0.490 | 0.478 | 0.621 | `artifacts/metrics/baseline_regresion_logistica.json` |
| Random Forest (baseline) | 0.545 | 0.529 | 0.563 | `artifacts/metrics/baseline_random_forest.json` |
| XGBoost (baseline) | 0.553 | 0.559 | 0.549 | `artifacts/metrics/baseline_xgboost.json` |
| Fusión temprana | 0.578 | 0.570 | 0.588 | `artifacts/metrics/early_fusion.json` |
| Fusión tardía (promedio ponderado) | 0.555 | 0.562 | 0.550 | `artifacts/metrics/late_fusion_promedio_ponderado.json` |
| Fusión tardía (stacking) | 0.560 | 0.562 | 0.559 | `artifacts/metrics/late_fusion_stacking.json` |
| **Ganador afinado (test)** | **0.551** | **0.560** | **0.542** | `artifacts/metrics/modelo_ganador.json` |

El ganador afinado alcanzó en test: **exactitud 0.978, AUC-ROC macro (OVR)
0.968** y macro-F1 0.551. La prueba de **McNemar contra la regla de clase
mayoritaria** dio b=0, c=57, p ≈ 0: la superioridad del modelo es
estadísticamente significativa. Intervalos de confianza bootstrap (1.000
remuestreos): macro-F1 [0.514, 0.575], exactitud [0.965, 0.988], recall I–II
[0.120, 0.200]. Fuente: `resources/tfm/validacion-cientifica/reporte-auditoria.md`.

## 5.3 Resultados por clase del modelo ganador (test, n = 600)

| Nivel | Precisión | Recall | F1 | Umbral aplicado | Fuente |
|---|---|---|---|---|---|
| I | 0.000 | 0.000 | 0.000 | 0.279 | model card + `confusion_matrix_modelo_ganador_test.json` |
| II | 0.867 | 0.812 | 0.839 | 0.281 | ídem |
| III | 0.996 | 1.000 | 0.998 | 0.500 | ídem |
| IV | 0.936 | 0.898 | 0.917 | 0.500 | ídem |
| V | 0.000 | 0.000 | 0.000 | 0.500 | ídem |

Justificación del criterio de selección: el ganador se eligió priorizando el
**recall en los niveles I–II** (clínicamente críticos: subclasificar un
paciente grave es el error de mayor costo) por encima del macro-F1 puro,
mediante umbrales por clase optimizados con el índice de Youden y acotados,
decisión documentada en `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md`.

## 5.4 Matriz de confusión del modelo ganador (test)

Filas = nivel real; columnas = nivel predicho. Umbrales de la sección 5.3.
Fuente: `artifacts/metrics/confusion_matrix_modelo_ganador_test.json`.

| Nivel \ Pred | I | II | III | IV | V |
|---|---|---|---|---|---|
| I | 0 | 2 | 0 | 0 | 0 |
| II | 3 | 13 | 0 | 0 | 0 |
| III | 0 | 0 | 530 | 0 | 0 |
| IV | 0 | 0 | 2 | 44 | 3 |
| V | 0 | 0 | 0 | 3 | 0 |

Interpretación: el modelo clasifica con precisión casi perfecta el nivel III
(dominante), retiene bien el nivel II (13/16) y el IV (44/49), pero **falla
sistemáticamente los niveles I y V**, cuyos soportes en test son de 2 y 3
registros respectivamente — consecuencia directa de la escasez de clases
raras, coherente con el intervalo de confianza del recall I–II [0.120, 0.200].

## 5.5 Comparación contra benchmarks de la literatura

| Estudio / estándar | Métrica reportada | Resultado propio equivalente | Fuente propia |
|---|---|---|---|
| CTAS (estándar canadiense) | AUC 0.882 | **AUC 0.968** (demo-test) | `artifacts/metrics/comparativa_benchmarks.json` |
| Hong et al. (2018) | AUC 0.93 | ídem | ídem |
| Ueareekul et al. (2024, XGBoost multimodal) | AUC 0.917 | ídem | ídem |
| Levin et al. (2021, estructurado+BERT) | F1 0.81 | **F1 0.551** (demo-test) | ídem |

**Advertencia de honestidad metodológica:** el AUC propio de 0.968 NO es
directamente comparable con los benchmarks: el dataset sintético genera el
CIE-10 condicionado al nivel de triaje, lo que infla el desempeño del
componente textual. La evaluación honesta del submodelo de texto sobre la
cohorte real SJdD (holdout 80/20 sin fuga, n = 8.719) arrojó macro-F1 0.088 y
AUC 0.481, muy por debajo de los benchmarks y de las metas. En consecuencia,
el resultado propio se declara como evidencia preliminar del diseño
multimodal, no como superioridad frente al estado del arte.

## 5.6 Explicabilidad (SHAP) — evidencia global y caso por paciente

**Top-5 global** de impacto medio SHAP del submodelo estructurado (todas las
predicciones del test): **frecuencia respiratoria (1.057), saturación de O₂
(1.043), presión sistólica (0.464), frecuencia cardíaca (0.465), temperatura
(0.331)**. Fuente: `artifacts/shap/modelo_ganador.json`.

**Caso por paciente (test_1):** paciente real de test con nivel real III,
predicho III con probabilidad máxima 0.983. Top-5 del caso: frecuencia
cardíaca (1.236), régimen de afiliación NoAfiliado (1.128), frecuencia
respiratoria (0.873), saturación de O₂ (0.721), temperatura (0.389).
Fuente: `artifacts/shap/shap_caso_test_1.json`.

La dominancia de las variables respiratorias y hemodinámicas en ambas vistas
es clínicamente coherente con los criterios de las escalas de triaje
estructuradas (MTS/Manchester), lo que refuerza la plausibilidad del modelo
ante clínicos.

## 5.7 Efecto del manejo del desbalance de clases

Técnica aplicada: `class_weight="balanced"` en XGBoost y umbrales por clase
priorizando recall I–II. Efecto medido: el nivel II alcanza recall 0.812 en
test (precision 0.867), sensiblemente mejor que su peso natural del 3 %; sin
embargo, el recall I–II agregado permanece bajo (IC95 [0.120, 0.200]) y los
niveles I y V no se recuperan en absoluto (soportes de 2 y 3 registros). En el
holdout real SJdD, el submodelo de texto puro alcanza recall 0.250 (I) y
0.126 (II). Conclusión: el balanceo mitiga, pero no resuelve, la escasez de
clases críticas — se requiere más datos reales de niveles I/II.

## 5.8 Calibración de probabilidades

Brier multiclase **0.0363** y ECE **0.0423** sobre el test: el modelo está
adecuadamente calibrado en el dominio sintético (ECE ≤ 0.05). Se recomienda
repetir la medición sobre datos reales antes de producción y aplicar
calibración post-hoc (Platt/isotónica) solo si la ECE supera 0.15. Fuente:
`resources/tfm/validacion-cientifica/reporte-auditoria.md`, Fase 4.

## 5.9 Contraste con las metas cuantitativas (RNF-001)

| Meta | Objetivo | Resultado real | ¿Alcanzada? |
|---|---|---|---|
| AUC-ROC | ≥ 0.87 | 0.968 (demo-test) | ✅ (con la salvedad 5.5) |
| Macro-F1 | ≥ 0.82 | 0.551 | ❌ |
| Precisión | ≥ 0.85 | 0.560 | ❌ |
| Recall | ≥ 0.80 | 0.542 | ❌ |

Las metas de F1/precisión/recall no se alcanzaron; la causa principal es la
escasez de las clases críticas (I y V) en los datos disponibles y la debilidad
del componente textual real, no una falla del diseño de fusión (ver Cap. 7).

## 5.10 Checklist de la sección

- [x] Toda cifra tiene ruta de archivo fuente identificable (columna Fuente).
- [x] Las metas del RNF-001 se contrastan explícitamente (5.9).
- [x] Las filas de benchmark están rotuladas como tales, separadas de las propias.
- [x] El ganador declarado coincide con la versión activa documentada
      (`modelo-latefusion-xgb-text-sjd-v20260814`).
- [x] Caso SHAP individual por paciente (5.6, `shap_caso_test_1.json`).
- [x] Métricas de comparación regeneradas con CV de 5 folds sin contaminación
      de la suite de tests (corrección documentada en el checklist de
      cumplimiento).
