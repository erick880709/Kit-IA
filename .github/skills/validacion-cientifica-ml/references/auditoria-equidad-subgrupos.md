# Auditoría de Equidad por Subgrupo — Modelo de Triaje

> Un modelo de apoyo clínico que funciona bien "en promedio" pero mal en un subgrupo específico de
> pacientes no es un modelo seguro — es un modelo que oculta su peor desempeño detrás de un
> macro-promedio favorable. Esta guía exige desagregar, no solo promediar.

## 1. Subgrupos obligatorios a auditar en este proyecto

| Subgrupo | Por qué importa aquí específicamente |
|---|---|
| **Fuente del dato: MIMIC-IV-ED (EE. UU.) vs. San Juan de Dios (Colombia)** | Es la comprobación real de si el fine-tuning corrigió el sesgo geográfico que el propio proyecto declara como limitación (`02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §8) — sin esta desagregación, "documentamos el sesgo como limitación" es una frase, no una medición |
| **Régimen de afiliación (contributivo/subsidiado)** | Correlaciona con acceso previo a servicios de salud y calidad de historia clínica disponible — un modelo puede aprender a clasificar mejor a pacientes con historiales más completos (régimen contributivo) |
| **Sexo** | Sesgo documentado en la literatura médica general (síntomas de eventos cardiovasculares se presentan y registran distinto por sexo) |
| **Grupo etario** (al menos: pediátrico si aplica / adulto / adulto mayor) | Los signos vitales normales varían por edad; un modelo mal calibrado por edad puede sub-triar adultos mayores con signos vitales "normales para su edad" pero críticos en términos absolutos |

## 2. Qué medir por subgrupo (no solo accuracy global)

Para cada subgrupo, reportar — específicamente para Niveles I-II, que es donde el costo clínico
del error es mayor:

```python
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix

def audit_subgroup(y_true, y_pred, subgroup_mask, subgroup_name, niveles_criticos=("I", "II")):
    """
    subgroup_mask: array booleano que marca qué filas pertenecen al subgrupo.
    Ejecutar una vez por cada subgrupo definido en la sección 1.
    """
    y_true_sub = y_true[subgroup_mask]
    y_pred_sub = y_pred[subgroup_mask]

    resultado = {
        "subgrupo": subgroup_name,
        "n": int(subgroup_mask.sum()),
        "recall_macro": recall_score(y_true_sub, y_pred_sub, average="macro"),
    }
    for nivel in niveles_criticos:
        mask_nivel = y_true_sub == nivel
        if mask_nivel.sum() == 0:
            resultado[f"recall_nivel_{nivel}"] = None  # sin casos suficientes para medir
            continue
        resultado[f"recall_nivel_{nivel}"] = recall_score(
            y_true_sub, y_pred_sub, labels=[nivel], average="micro"
        )
    return resultado
```

## 3. Umbral de alerta (a definir con criterio clínico, no arbitrariamente)

Este skill **mide y reporta la brecha entre subgrupos** — no decide cuál es "aceptable". Esa
decisión es clínica y debe tomarse con la directora/equipo médico, documentando en el TFM:

- La brecha de Recall en Nivel I-II entre el subgrupo con mejor y peor desempeño.
- Si esa brecha se considera clínicamente relevante o no, y por qué (justificación explícita, no
  un número arbitrario elegido por conveniencia para que el modelo "pase").
- Si la brecha es relevante, qué mitigación se aplicó o se propone como trabajo futuro
  (reponderar el subgrupo subrepresentado, recolectar más datos de ese subgrupo, ajustar el
  umbral por subgrupo — cada opción tiene trade-offs que deben discutirse, no aplicarse
  automáticamente).

## 4. Formato de reporte para el capítulo de Limitaciones del TFM

```
### Auditoría de equidad por subgrupo (Nivel I-II)

| Subgrupo | n (test) | Recall Nivel I | Recall Nivel II | Brecha vs. mejor subgrupo |
|---|---|---|---|---|
| Fuente: MIMIC-IV-ED | | | | referencia |
| Fuente: San Juan de Dios | | | | |
| Régimen contributivo | | | | |
| Régimen subsidiado | | | | |
| ... | | | | |

Hallazgo: [describir la brecha más relevante encontrada, con cifras reales]
Interpretación clínica: [con criterio del equipo/directora, no inventada]
Mitigación aplicada / propuesta: [si aplica]
```

Este bloque, con datos reales, es exactamente el tipo de "limitación con hallazgo real del
proyecto" que `brief_finalizacion_tfm.md` §2.3 pide y que hoy el documento no tiene — reemplaza
una limitación genérica de "sesgo geográfico" por una medición concreta y defendible.
