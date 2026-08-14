---
id: HU-06
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 8
---

# HU-06: Clasificación IA con explicación SHAP

## Como
Profesional de enfermería o médico

## Quiero
Ejecutar la clasificación automática del nivel de triaje mediante IA, ver las probabilidades para cada nivel, y entender qué factores influyeron más en la predicción mediante una explicación visual

## Para
Tomar una decisión informada sobre el nivel de triaje del paciente, usando la IA como apoyo — no como reemplazo — de mi juicio clínico

## Criterios de Aceptación

- [ ] CA1: La página muestra un resumen de los datos clínicos ingresados (signos vitales + evaluación) en un panel lateral o superior.
- [ ] CA2: Botón prominente "🧠 Clasificar con IA" que inicia la inferencia.
- [ ] CA3: Durante la inferencia (3-5s), se muestra un spinner con texto "Analizando datos clínicos..." y una barra de progreso indeterminada.
- [ ] CA4: Al completar, se muestra el resultado en un layout de 2-3 columnas:
  - **Columna 1 — Nivel Predicho**: badge grande con el nivel (I-V), color codificado (rojo para I, naranja II, amarillo III, verde IV, azul V), y texto descriptivo del nivel.
  - **Columna 2 — Probabilidades**: barras horizontales para cada nivel I-V con porcentaje y color. El nivel predicho se resalta.
  - **Columna 3 — Clasificación del Profesional**: select para que el profesional asigne su propio nivel (independiente de la IA).
- [ ] CA5: Botón "🔍 Ver Explicación SHAP" que despliega un panel con:
  - Top 10 features que más influyeron en la predicción.
  - Cada feature muestra: nombre legible en español, valor del paciente, importancia (barra horizontal), y dirección (➕ aumentó el riesgo / ➖ disminuyó el riesgo).
  - Tooltip con descripción de qué significa cada feature.
- [ ] CA6: Si SHAP no está disponible (fallback), se muestran las feature_importances_ de XGBoost con una nota "Explicación basada en importancia de features del modelo".
- [ ] CA7: Botón "Guardar y Continuar a Validación" que persiste la predicción y navega al siguiente paso.
- [ ] CA8: La predicción se almacena en el servidor (via `POST /api/inference/predict`) y se asocia al triaje activo. No se pierde al recargar la página (se recupera con `GET /api/triages/{id}`).

## Recurso de datos involucrado

- **Nombre del recurso:** Prediccion
- **Capa(s):** frontend (consume POST /api/inference/predict y POST /api/inference/explain)

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| nivel_predicho | string | Sí | "I", "II", "III", "IV", "V" |
| nivel_codigo | number | Sí | 0-4 |
| probabilidades | object | Sí | `{I: 0.01, II: 0.15, III: 0.70, IV: 0.10, V: 0.04}` |
| shap_explicacion | array | No | Top 10 `{feature, importancia, direccion, valor_paciente}` |
| tiempo_inferencia_ms | number | Sí | |
| modelo_version | string | Sí | |

## Subtareas

- [ ] Crear `pages/IAClassificationPage.tsx`
- [ ] Crear `components/ia/ClassificationResult.tsx` (badge + barras)
- [ ] Crear `components/ia/ShapExplanation.tsx` (top 10 features)
- [ ] Crear `api/inference.ts` (predict, explain, status)
- [ ] Implementar spinner durante inferencia
- [ ] Implementar select de clasificación del profesional
- [ ] Manejar fallback si SHAP no disponible
- [ ] Probar con diferentes escenarios clínicos
