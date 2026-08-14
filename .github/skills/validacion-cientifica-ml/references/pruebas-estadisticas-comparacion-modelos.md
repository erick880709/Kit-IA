# Pruebas Estadísticas para Comparar Modelos (Early vs. Late Fusion vs. Baselines)

> Objetivo: que "el modelo ganador" en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §2 no sea solo
> el de mayor cifra puntual, sino el que gana con soporte estadístico — esto es lo que un tribunal
> de TFM espera ver en el Capítulo 5.

## 1. Prueba de McNemar (comparar accuracy/recall de dos clasificadores en el mismo test set)

Se usa cuando dos modelos se evalúan sobre exactamente las mismas observaciones de test — es el
caso típico de comparar Early Fusion vs. Late Fusion vs. baseline.

```python
from statsmodels.stats.contingency_tables import mcnemar
import numpy as np

def mcnemar_test(y_true, y_pred_model_a, y_pred_model_b):
    """
    Compara si dos modelos difieren significativamente en su tasa de acierto
    sobre el mismo conjunto de test. Útil para decidir si Early Fusion
    realmente supera a Late Fusion, o si la diferencia es ruido de muestra.
    """
    correct_a = (y_pred_model_a == y_true)
    correct_b = (y_pred_model_b == y_true)

    # Tabla de contingencia 2x2: ambos aciertan / solo A / solo B / ambos fallan
    both_correct = np.sum(correct_a & correct_b)
    only_a = np.sum(correct_a & ~correct_b)
    only_b = np.sum(~correct_a & correct_b)
    both_wrong = np.sum(~correct_a & ~correct_b)

    table = [[both_correct, only_a], [only_b, both_wrong]]
    result = mcnemar(table, exact=(only_a + only_b) < 25, correction=True)

    return {
        "statistic": result.statistic,
        "p_value": result.pvalue,
        "significativo_al_5pct": result.pvalue < 0.05,
        "solo_modelo_a_acierta": int(only_a),
        "solo_modelo_b_acierta": int(only_b),
    }
```

**Para el capítulo de Resultados:** reportar el valor p, no solo "el modelo A ganó". Si p ≥ 0.05,
la conclusión honesta es "no hay evidencia suficiente de que un modelo supere al otro con este
tamaño de muestra" — que también es un resultado válido y defendible en un TFM, mucho más que
afirmar una superioridad que la evidencia no respalda.

## 2. Prueba de DeLong (comparar AUC-ROC entre dos modelos)

McNemar compara decisiones (clase predicha); DeLong compara las curvas ROC completas —
recomendado además de McNemar cuando la meta cuantitativa del proyecto es AUC-ROC ≥ 0.87.

```python
# Requiere: pip install scikit-learn scipy
# Implementación de referencia (no incluida por defecto en sklearn):
# usar la librería `delongtest` o el código de referencia de Sun & Xu (2014),
# disponible en: https://github.com/yandexdataschool/roc_comparison

from scipy import stats

def bootstrap_auc_ci(y_true, y_scores, n_bootstrap=1000, ci=0.95, random_state=42):
    """
    Alternativa más simple a DeLong cuando no se quiere agregar una dependencia
    externa: bootstrap del AUC-ROC para obtener intervalo de confianza.
    Repetir para cada modelo y comparar si los intervalos se solapan.
    """
    from sklearn.metrics import roc_auc_score
    rng = np.random.RandomState(random_state)
    n = len(y_true)
    aucs = []
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, n)
        if len(np.unique(np.array(y_true)[idx])) < 2:
            continue  # evitar folds sin ambas clases (relevante para Nivel I raro)
        aucs.append(roc_auc_score(np.array(y_true)[idx], np.array(y_scores)[idx]))
    lower = np.percentile(aucs, (1 - ci) / 2 * 100)
    upper = np.percentile(aucs, (1 + ci) / 2 * 100)
    return {"auc_mean": np.mean(aucs), "ci_lower": lower, "ci_upper": upper}
```

**Regla de reporte:** si los intervalos de confianza del AUC-ROC de dos modelos se solapan
sustancialmente, no se puede afirmar que uno es mejor que el otro — reportar ambos intervalos en
la tabla del Capítulo 5, no solo el punto estimado.

## 3. Intervalo de confianza por bootstrap para métricas por clase (Nivel I especialmente)

Con Nivel I raro, el Recall puntual (ej. "0.86") puede estar calculado sobre muy pocos casos
positivos reales. Reportar siempre el intervalo, no solo el punto:

```python
def bootstrap_metric_ci(y_true, y_pred, metric_fn, n_bootstrap=1000, ci=0.95, random_state=42):
    """
    metric_fn: función tipo sklearn.metrics.recall_score(y_true, y_pred, ...)
    Útil para Recall/F1/Precisión por clase con muestra pequeña (Nivel I-II).
    """
    rng = np.random.RandomState(random_state)
    n = len(y_true)
    scores = []
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, n)
        scores.append(metric_fn(np.array(y_true)[idx], np.array(y_pred)[idx]))
    lower = np.percentile(scores, (1 - ci) / 2 * 100)
    upper = np.percentile(scores, (1 + ci) / 2 * 100)
    return {"mean": np.mean(scores), "ci_lower": lower, "ci_upper": upper}
```

## 4. Qué va en la tabla del Capítulo 5 (Resultados)

No basta con la tabla de §5.2 de `plantilla-capitulo-resultados.md` (de `tfm-redactor`) con un
solo número por celda. Esta skill exige extenderla así:

| Modelo | Recall Nivel I (IC 95%) | Recall Nivel II (IC 95%) | ¿Diferencia vs. 2º lugar es significativa (McNemar, p) |
|---|---|---|---|
| Early Fusion | 0.86 (0.79–0.92) | 0.81 (0.76–0.85) | p = 0.03 (sí) |
| Late Fusion | 0.79 (0.70–0.87) | 0.78 (0.73–0.83) | referencia |

Esta es la diferencia entre una tabla de métricas y una tabla de evidencia.
