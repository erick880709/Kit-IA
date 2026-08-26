# Model Card — modelo-latefusion-xgb-text-sjd-v20260826

- **Algoritmo:** latefusion-xgb-text-sjd · **Fecha de entrenamiento:** 2026-08-26
- **Clases:** I · II · III · IV · V (triaje I–V, Res. 5596/2015)

## Datos de entrenamiento
{
  "fuente_demo": "demo sintético 4000 registros calibrado con distribución nacional real",
  "fuente_sjd": "cohorte San Juan de Dios (43.594 eventos) — submodelo de texto",
  "periodo": "sintético; SJdD 2023",
  "split": "70/15/15 estratificado, escalador solo en train"
}

## Métricas por clase
| Nivel | Precisión | Recall | F1 |
|---|---|---|---|
| I | 0.0 | 0.0 | 0.0 |
| II | 0.875 | 0.875 | 0.875 |
| III | 0.9962335216572504 | 0.9981132075471698 | 0.9971724787935909 |
| IV | 0.9166666666666666 | 0.8979591836734694 | 0.9072164948453608 |
| V | 0.0 | 0.0 | 0.0 |

- **Macro-F1:** 0.5558777947277903 · **AUC-ROC (OVR):**
  0.9863644336729707

## Intervalos de confianza (bootstrap 1000)
{
  "f1_macro": {
    "metrica": "f1_macro",
    "punto": 0.5471201109979015,
    "ic95": [
      0.5109784996256126,
      0.573901372200038
    ],
    "n_bootstrap": 1000
  },
  "accuracy": {
    "metrica": "accuracy",
    "punto": 0.9763483333333334,
    "ic95": [
      0.9633333333333334,
      0.9866666666666667
    ],
    "n_bootstrap": 1000
  },
  "recall_i_ii": {
    "metrica": "recall_i_ii",
    "punto": 0.16240330497993205,
    "ic95": [
      0.11995454545454545,
      0.2
    ],
    "n_bootstrap": 1000
  }
}

## Calibración de probabilidades
- Brier multiclase: 0.030411665916027043 · ECE: 0.026762923305606364

## Auditoría de equidad por subgrupo
{
  "sexo": {
    "Femenino": {
      "n": 341,
      "f1_macro": 0.5577004690313909,
      "recall_i_ii": 0.18181818181818182
    },
    "Masculino": {
      "n": 259,
      "f1_macro": 0.5534009083859532,
      "recall_i_ii": 0.16
    }
  },
  "via_llegada": {
    "Ambulancia": {
      "n": 166,
      "f1_macro": 0.6,
      "recall_i_ii": 0.2
    },
    "Particular": {
      "n": 302,
      "f1_macro": 0.5455616942909761,
      "recall_i_ii": 0.16363636363636364
    },
    "Remisión": {
      "n": 132,
      "f1_macro": 0.5314285714285714,
      "recall_i_ii": 0.2
    }
  }
}

## Casos de uso previstos
- Apoyo a la decisión de triaje en urgencias (no autónomo).
- Monitoreo de concordancia IA vs profesional.

## Casos de uso NO previstos
- Decisión clínica sin validación profesional.
- Poblaciones fuera del contexto colombiano / datos sintéticos de demo.

## Limitaciones conocidas
- El demo sintético genera CIE-10 condicionado al nivel: AUC sobre demo-test es optimista.
- Macro-F1 limitado por clases raras (I/V) en un demo de 4000 registros.
- El submodelo de texto puro en SJdD es débil (F1 ≈ 0.10): su valor es complementario.
- MIMIC-IV-ED (signos vitales reales) pendiente de credenciales PhysioNet.
- Sistema de apoyo a la decisión — nunca autónomo (validación profesional obligatoria).
