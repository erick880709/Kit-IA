# Plantilla — Capítulo de Resultados (basada en evidencia de `artifacts/`)

> Esta plantilla es específica para TFM de tipo "modelo de ML con comparación de arquitecturas"
> (p. ej. early vs. late fusion), pero es reutilizable para cualquier TFM que compare modelos.
> Cada tabla exige una columna de trazabilidad (`Fuente`) — si esa columna no se puede llenar con
> una ruta real de `artifacts/`, la fila no se escribe con un número: se deja `[PENDIENTE]`.

## 5.1 Configuración experimental

- Semilla aleatoria fijada (`RANDOM_STATE`), esquema de validación (p. ej. 10-fold CV), split
  train/test, técnica de balanceo de clases usada finalmente (no solo las evaluadas).
- Fuente: `src/models/*.py` (hiperparámetros reales usados), `artifacts/models/*` (versión/tag).

## 5.2 Resultados por modelo — tabla obligatoria

| Modelo | F1 (macro) | Precisión (macro) | Recall (macro) | AUC-ROC (macro) | AUPRC (clases minoritarias) | Fuente |
|---|---|---|---|---|---|---|
| Regresión Logística (baseline) | | | | | | `artifacts/metrics/...` |
| Random Forest (baseline) | | | | | | |
| XGBoost (baseline) | | | | | | |
| Early Fusion | | | | | | |
| Late Fusion | | | | | | |

## 5.3 Resultados por clase (obligatorio para Niveles I y II — prioridad clínica)

| Nivel | Modelo ganador — Precisión | Recall | F1 | Umbral aplicado | Fuente |
|---|---|---|---|---|---|
| I | | | | | |
| II | | | | | |
| III | | | | | |
| IV | | | | | |
| V | | | | | |

Nota obligatoria: justificar por qué el modelo ganador se eligió por Recall en I-II y no por F1
global puro, enlazando con la decisión de umbral documentada en la especificación técnica del
proyecto (si existe un documento tipo `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`, citarlo).

## 5.4 Matriz de confusión del modelo ganador

- Insertar matriz de confusión real (imagen o tabla) — fuente: `artifacts/metrics/confusion_matrix_*`.
- Leyenda obligatoria: qué modelo, qué versión, sobre qué conjunto (test/hold-out), tamaño de muestra.

## 5.5 Comparación contra benchmarks de la literatura

| Estudio / estándar | Modelo | Métrica reportada | Resultado propio equivalente | Fuente propia |
|---|---|---|---|---|
| CTAS (estándar canadiense) | — | AUROC 0.882 | | |
| Raita et al. 2019 | RF/regresión logística/árboles | AUC-ROC 0.87 | | |
| Hong, Haimovich & Taylor 2018 | DNN | AUC-ROC 0.93 | | |
| Ueareekul et al. 2024 | XGBoost multimodal | AUROC 0.917, AUPRC 0.629 | | |
| Levin et al. 2021 | Estructurado + BERT | F1 0.81 | | |

Regla: la columna "Resultado propio equivalente" solo se llena con datos de `artifacts/metrics`.
La comparación debe ser honesta — si el resultado propio es inferior al benchmark, decirlo y
discutir por qué (tamaño de muestra, datos locales vs. internacionales, etc.) en vez de omitirlo.

## 5.6 Explicabilidad (SHAP) — caso clínico ilustrativo

- Al menos un caso real con: nivel predicho, probabilidad, top-5 variables SHAP en lenguaje
  clínico (no solo el nombre técnico de la variable).
- Fuente: `artifacts/shap/*`.
- Comparación implícita con criterio MTS/Manchester si coincide con lo reportado en el estado del
  arte (Cap. 2).

## 5.7 Efecto del manejo de desbalance de clases

- Qué técnica se aplicó finalmente (class weights / SMOTE / focal loss) y su efecto medible,
  específicamente en las clases minoritarias (I y II) antes/después.
- Fuente: `artifacts/metrics/` (comparar corridas con y sin la técnica, si existen ambas).

## 5.8 Checklist de esta sección antes de darla por cerrada

- [ ] Toda cifra tiene una ruta de archivo fuente identificable.
- [ ] Las metas cuantitativas del Cap. 3 se contrastan explícitamente contra estos resultados
      (alcanzadas / no alcanzadas, sin ambigüedad).
- [ ] Ninguna fila de benchmark se confunde visualmente con una fila de resultado propio.
- [ ] El modelo "ganador" declarado aquí coincide con el que se documenta como versión activa en
      `artifacts/models/` (o en el módulo de gestión de modelos, si el proyecto lo tiene).
