# RT-008: Benchmarks de Comparación de la Literatura

**Tipo:** Requisito técnico
**Categoría:** Evaluación
**Fuente:** `context/contexto-tfm.md` §7 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §5 (paso 12)

## Descripción
Los resultados propios deben contrastarse contra los benchmarks publicados de la literatura de triaje con IA.

## Criterio medible / restricción concreta
| Estudio | Modelo | Métrica de referencia |
|---|---|---|
| Raita et al. 2019 | RF / RL / árboles | AUC-ROC 0.87 |
| Hong et al. 2018 | DNN (972.756 admisiones) | AUC-ROC 0.93 |
| Ueareekul et al. 2024 | XGBoost multimodal | AUROC 0.917 · AUPRC 0.629 |
| CTAS (estándar canadiense) | — | AUROC 0.882 |
| Levin et al. 2021 | Estructurado + BERT | F1 0.81 |
| Lee, Lee & Shin 2022 | SHAP sobre triaje | Prec 0.91 · Recall 0.83 · F1 0.87 |
| Lidal et al. 2017 | Acuerdo interobservador | Kappa 0.43 |

## Impacto en la arquitectura
Define la sección de comparación del módulo de evaluación; las mismas métricas (AUC-ROC/F1) deben calcularse para hacer comparables los resultados.

## Notas del analista
El Kappa 0.43 de profesionales es el contraste natural para la concordancia IA-profesional de la demo (RF-010), con la salvedad del sesgo de anclaje documentada.
