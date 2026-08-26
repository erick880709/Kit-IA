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
| I | 0.16666666666666666 | 0.5 | 0.25 |
| II | 0.9166666666666666 | 0.6875 | 0.7857142857142857 |
| III | 0.9962406015037594 | 1.0 | 0.9981167608286252 |
| IV | 0.94 | 0.9591836734693877 | 0.9494949494949495 |
| V | 0.0 | 0.0 | 0.0 |

- **Macro-F1:** 0.5966651992075721 · **AUC-ROC (OVR):**
  0.9873722302712544

## Intervalos de confianza (bootstrap 1000)
{
  "f1_macro": {
    "metrica": "f1_macro",
    "punto": 0.5700882834241897,
    "ic95": [
      0.5427264747402532,
      0.589353720329188
    ],
    "n_bootstrap": 1000
  },
  "accuracy": {
    "metrica": "accuracy",
    "punto": 0.9863533333333332,
    "ic95": [
      0.975,
      0.995
    ],
    "n_bootstrap": 1000
  },
  "recall_i_ii": {
    "metrica": "recall_i_ii",
    "punto": 0.18668218399910963,
    "ic95": [
      0.15384615384615385,
      0.2
    ],
    "n_bootstrap": 1000
  }
}

## Calibración de probabilidades
- Brier multiclase: 0.026531151859762913 · ECE: 0.030610862043095554

## Auditoría de equidad por subgrupo
{
  "sexo": {
    "Femenino": {
      "n": 341,
      "f1_macro": 0.6202665020322067,
      "recall_i_ii": 0.24545454545454545
    },
    "Masculino": {
      "n": 259,
      "f1_macro": 0.5313953488372093,
      "recall_i_ii": 0.12
    }
  },
  "via_llegada": {
    "Ambulancia": {
      "n": 166,
      "f1_macro": 0.4,
      "recall_i_ii": 0.0
    },
    "Particular": {
      "n": 302,
      "f1_macro": 0.5325980392156863,
      "recall_i_ii": 0.12727272727272726
    },
    "Remisión": {
      "n": 132,
      "f1_macro": 0.702415458937198,
      "recall_i_ii": 0.3
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
