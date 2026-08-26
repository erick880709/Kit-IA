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
| III | 0.9962406015037594 | 1.0 | 0.9981167608286252 |
| IV | 0.9387755102040817 | 0.9387755102040817 | 0.9387755102040817 |
| V | 0.0 | 0.0 | 0.0 |

- **Macro-F1:** 0.5623784542065413 · **AUC-ROC (OVR):**
  0.8901472923726237

## Intervalos de confianza (bootstrap 1000)
{
  "f1_macro": {
    "metrica": "f1_macro",
    "punto": 0.5608244684694804,
    "ic95": [
      0.5297042813110486,
      0.5838143344969465
    ],
    "n_bootstrap": 1000
  },
  "accuracy": {
    "metrica": "accuracy",
    "punto": 0.9830083333333334,
    "ic95": [
      0.9716666666666667,
      0.9916666666666667
    ],
    "n_bootstrap": 1000
  },
  "recall_i_ii": {
    "metrica": "recall_i_ii",
    "punto": 0.17406462076411647,
    "ic95": [
      0.1375,
      0.2
    ],
    "n_bootstrap": 1000
  }
}

## Calibración de probabilidades
- Brier multiclase: 0.03001544019613944 · ECE: 0.03528887623058358

## Auditoría de equidad por subgrupo
{
  "sexo": {
    "Femenino": {
      "n": 341,
      "f1_macro": 0.5643427156736377,
      "recall_i_ii": 0.18181818181818182
    },
    "Masculino": {
      "n": 259,
      "f1_macro": 0.5591731266149871,
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
      "f1_macro": 0.5570424836601308,
      "recall_i_ii": 0.16363636363636364
    },
    "Remisión": {
      "n": 132,
      "f1_macro": 0.5418181818181818,
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
