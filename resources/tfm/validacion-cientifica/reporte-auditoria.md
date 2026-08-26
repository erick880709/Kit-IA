# Reporte de Auditoría Científica — TriajeIA

- **Fecha:** 2026-08-26 19:33 UTC
- **Modelo:** modelo-latefusion-xgb-text-sjd-v20260826 · **Artefacto:** modelo-latefusion-xgb-text-sjd-v20260826.joblib
- **Semilla:** 42 · **Git:** 6156e95

## Fase 1 · Prevención de fuga de datos
| Severidad | Hallazgo |
|---|---|
| info | Split 70/15/15 estratificado por nivel, sin solape de filas: True |
| info | Escalador/imputación ajustados SOLO con train (corregido en pipeline v3) |
| info | TF-IDF ajustado con textos de train + cohorte SJdD (test solo transformado) |
| info | Matriz de confusión del ganador guardada: confusion_matrix_modelo_ganador_test.json |
| info | Caso SHAP guardado: nivel real III → predicho III |

## Fase 2 · Estrategia de validación cruzada
| Severidad | Hallazgo |
|---|---|
| info | CV estratificado (StratifiedKFold, shuffle, semilla fija) en baselines/early/late |
| info | Pesos balanceados por clase y búsqueda de hiperparámetros con validación |

## Fase 3 · Validación estadística de comparaciones
| Severidad | Hallazgo |
|---|---|
| info | McNemar ganador vs regla mayoritaria: b=1 c=58 p=0.0000 (significativo) |
| info | IC95 macro-F1: [0.5109784996256126, 0.573901372200038] · accuracy: [0.9633333333333334, 0.9866666666666667] · recall I-II: [0.11995454545454545, 0.2] |

## Fase 4 · Calibración de probabilidades
| Severidad | Hallazgo |
|---|---|
| info | Brier multiclase: 0.0304 · ECE: 0.0268 |

## Fase 5 · Auditoría de sesgo y equidad
| Severidad | Hallazgo |
|---|---|
| info | Equidad por sexo: {"Femenino": {"n": 341, "f1_macro": 0.5577004690313909, "recall_i_ii": 0.18181818181818182}, "Masculino": {"n": 259, "f1_macro": 0.5534009083859532, "recall_i_ii": 0.16}} |
| info | Equidad por vía de llegada: {"Ambulancia": {"n": 166, "f1_macro": 0.6, "recall_i_ii": 0.2}, "Particular": {"n": 302, "f1_macro": 0.5455616942909761, "recall_i_ii": 0.16363636363636364}, "Remisión": {"n": 132, "f1_macro": 0.5314285714285714, "recall_i_ii": 0.2}} |
| advertencia | Auditoría de equidad sobre demo SINTÉTICO: los subgrupos son andamiaje metodológico; la auditoría definitiva requiere MIMIC/SJdD con variables demográficas reales (fuente, régimen, sexo, edad). |

## Fase 6 · Trazabilidad y reproducibilidad
| Severidad | Hallazgo |
|---|---|
| info | Semilla 42 · artefacto modelo-latefusion-xgb-text-sjd-v20260826 · git 6156e95 |

## Veredicto
- **Leakage:** SIN EVIDENCIA DE FUGA tras corrección (escalador solo en train,
  holdout SJdD sin contaminación).
- **Estado:** APROBADO con advertencias documentadas — las métricas del demo son válidas como evidencia preliminar; el capítulo de Resultados debe declarar las limitaciones listadas en el model card
