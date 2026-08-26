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
| I | 0.6666666666666666 | 1.0 | 0.8 |
| II | 1.0 | 0.9375 | 0.967741935483871 |
| III | 1.0 | 1.0 | 1.0 |
| IV | 1.0 | 1.0 | 1.0 |
| V | 1.0 | 1.0 | 1.0 |

- **Macro-F1:** 0.9535483870967741 · **AUC-ROC (OVR):**
  1.0

## Intervalos de confianza (bootstrap 1000)
{
  "f1_macro": {
    "metrica": "f1_macro",
    "punto": 0.9391886514684127,
    "ic95": [
      0.7328205039297272,
      1.0
    ],
    "n_bootstrap": 1000
  },
  "accuracy": {
    "metrica": "accuracy",
    "punto": 0.9983316666666666,
    "ic95": [
      0.995,
      1.0
    ],
    "n_bootstrap": 1000
  },
  "recall_i_ii": {
    "metrica": "recall_i_ii",
    "punto": 0.3766000000000001,
    "ic95": [
      0.2,
      0.4
    ],
    "n_bootstrap": 1000
  }
}

## Calibración de probabilidades
- Brier multiclase: 0.025965003925347743 · ECE: 0.047219901634080616

## Auditoría de equidad por subgrupo
{
  "sexo": {
    "Femenino": {
      "n": 341,
      "f1_macro": 0.9504761904761905,
      "recall_i_ii": 0.38181818181818183
    },
    "Masculino": {
      "n": 259,
      "f1_macro": 0.8,
      "recall_i_ii": 0.2
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
      "f1_macro": 0.7904761904761906,
      "recall_i_ii": 0.18181818181818182
    },
    "Remisión": {
      "n": 132,
      "f1_macro": 1.0,
      "recall_i_ii": 0.4
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
