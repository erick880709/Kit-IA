# Reporte de Auditoría Científica — TriajeIA

- **Fecha:** 2026-08-26 20:25 UTC
- **Modelo:** modelo-latefusion-xgb-text-sjd-v20260826 · **Artefacto:** modelo-latefusion-xgb-text-sjd-v20260826.joblib
- **Semilla:** 42 · **Git:** 0d8b08b

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
| info | McNemar ganador vs regla mayoritaria: b=0 c=69 p=0.0000 (significativo) |
| info | IC95 macro-F1: [0.7328205039297272, 1.0] · accuracy: [0.995, 1.0] · recall I-II: [0.2, 0.4] |

## Fase 4 · Calibración de probabilidades
| Severidad | Hallazgo |
|---|---|
| info | Brier multiclase: 0.0260 · ECE: 0.0472 |

## Fase 5 · Auditoría de sesgo y equidad
| Severidad | Hallazgo |
|---|---|
| info | Equidad por sexo: {"Femenino": {"n": 341, "f1_macro": 0.9504761904761905, "recall_i_ii": 0.38181818181818183}, "Masculino": {"n": 259, "f1_macro": 0.8, "recall_i_ii": 0.2}} |
| info | Equidad por vía de llegada: {"Ambulancia": {"n": 166, "f1_macro": 0.6, "recall_i_ii": 0.2}, "Particular": {"n": 302, "f1_macro": 0.7904761904761906, "recall_i_ii": 0.18181818181818182}, "Remisión": {"n": 132, "f1_macro": 1.0, "recall_i_ii": 0.4}} |
| advertencia | Auditoría de equidad sobre demo SINTÉTICO: los subgrupos son andamiaje metodológico; la auditoría definitiva requiere MIMIC/SJdD con variables demográficas reales (fuente, régimen, sexo, edad). |

## Fase 6 · Trazabilidad y reproducibilidad
| Severidad | Hallazgo |
|---|---|
| info | Semilla 42 · artefacto modelo-latefusion-xgb-text-sjd-v20260826 · git 0d8b08b |

## Veredicto
- **Leakage:** SIN EVIDENCIA DE FUGA tras corrección (escalador solo en train,
  holdout SJdD sin contaminación).
- **Estado:** APROBADO con advertencias documentadas — las métricas del demo son válidas como evidencia preliminar; el capítulo de Resultados debe declarar las limitaciones listadas en el model card
