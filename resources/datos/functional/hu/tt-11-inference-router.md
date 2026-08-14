---
id: TT-11
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "TT-07"
---

# TT-11: Implementar InferenceRouter

## Descripción

Crear el router de inferencia que expone el `InferenceService` como endpoints REST. Es crítico que el modelo se inicialice una sola vez en el `lifespan` de FastAPI y que las predicciones se ejecuten de forma síncrona (el tiempo de 3-5s es aceptable para la demo).

## Criterios de Done

- [ ] `routers/inference.py` creado con endpoints:
  - `POST /api/inference/predict` — recibe datos clínicos + texto motivo, retorna nivel predicho + probabilidades por clase. Body: `PredictRequest` con campos clínicos y `motivo_texto`.
  - `POST /api/inference/explain` — recibe los mismos datos, retorna explicación SHAP (o fallback feature_importances_). Body: igual que predict.
  - `GET /api/inference/status` — retorna estado del servicio: modelo cargado, versión, features, umbrales, SHAP disponible.
  - `POST /api/inference/reload` — (admin) recarga el modelo desde disco sin reiniciar el servidor.
- [ ] `InferenceService` se inicializa en `lifespan` de FastAPI (no con singleton de módulo).
- [ ] Las predicciones incluyen `tiempo_inferencia_ms` en la respuesta.
- [ ] Manejo de errores: modelo no cargado → 503 Service Unavailable.
- [ ] La respuesta de `predict` incluye el nivel en formato legible (I, II, III, IV, V) + probabilidades numéricas.
- [ ] La respuesta de `explain` incluye top 10 features con importancia y nombre legible.

## Recurso de datos involucrado

- **Nombre del recurso:** Prediccion
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| nivel_predicho | str | Sí | "I", "II", "III", "IV", "V" |
| nivel_codigo | int | Sí | 0-4 mapeado a I-V |
| probabilidades | dict | Sí | `{"I": 0.01, "II": 0.15, ...}` |
| tiempo_inferencia_ms | float | Sí | Tiempo total de la predicción |
| modelo_version | str | Sí | Versión del modelo usado |
| shap_disponible | bool | Sí | |

## Subtareas

- [ ] Crear `routers/inference.py` con 4 endpoints
- [ ] Ajustar inicialización de `InferenceService` en `lifespan`
- [ ] Implementar `POST /predict` con validación de campos requeridos
- [ ] Implementar `POST /explain` con serialización de SHAP a JSON
- [ ] Probar inferencia con Swagger UI
