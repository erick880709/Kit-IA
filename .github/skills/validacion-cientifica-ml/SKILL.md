---
name: validacion-cientifica-ml
description: 'Audita el rigor científico y la equidad de un pipeline de Machine Learning/IA antes de declarar un modelo como "entrenado" o "ganador". Cubre: prevención de fuga de datos (leakage) en el split train/test, validación estadística de comparaciones entre modelos (McNemar, DeLong), calibración de probabilidades, auditoría de sesgo/equidad por subgrupo demográfico, trazabilidad de experimentos (MLflow/DVC) y generación de model cards. Úsala SIEMPRE que el usuario pida "validar mi modelo", "revisar si el pipeline de ML tiene fuga de datos", "comparar estadísticamente dos modelos", "auditar sesgo del modelo", "generar un model card", "verificar reproducibilidad del experimento", o antes de que `tfm-redactor` redacte el capítulo de Resultados con las métricas como definitivas. También aplica cuando `builder` termine de generar el scaffold de un pipeline de ML y el usuario quiera confirmar que el diseño experimental (no solo el código) es correcto antes de ejecutar el entrenamiento real. No uses esta skill para el diseño de arquitectura del pipeline (eso es `archi`), ni para generar el código/scaffold (eso es `builder`), ni para pruebas de software tradicionales de la app (eso es `qa`, orientado a frontend/backend, no a validez estadística de modelos).'
---

# Validación Científica de Modelos ML — Auditor de Rigor y Equidad

## Resumen

`builder` genera el scaffold del pipeline (`src/data/`, `src/models/`, `src/evaluation/`) y
`archi` documenta la arquitectura, pero ninguno de los dos verifica que el **diseño experimental
en sí sea correcto**. Un pipeline puede estar perfectamente estructurado en código y aun así
producir métricas infladas por fuga de datos, o un modelo "ganador" que no es estadísticamente
distinto del segundo lugar, o un buen desempeño promedio que oculta un mal desempeño en un
subgrupo real de pacientes. Este skill es el que detecta eso, antes de que las cifras lleguen al
capítulo de Resultados del TFM (`tfm-redactor`) o a producción.

Filosofía: **una métrica sin su procedimiento de validación detrás no es evidencia, es una
cifra.** Este skill exige el procedimiento, no solo el número.

## Cuándo se activa

- Después de que `builder` scaffoldeó el pipeline de ML, antes de la primera corrida real de
  entrenamiento — para revisar el diseño del split y la estrategia de validación.
- Después de obtener resultados de varios modelos (baseline, early fusion, late fusion) y antes
  de declarar un "ganador" — para exigir la prueba estadística de la comparación.
- Antes de que `tfm-redactor` cierre el capítulo de Resultados — como gate de calidad.
- Cuando el usuario pregunte si el modelo está "bien entrenado" o "listo para producción/demo".

## Entrada esperada

| Insumo | Obligatorio | De dónde sale |
|---|---|---|
| Script/notebook de split train/test (`src/data/*.py` o notebook 02/03) | Sí | `builder` |
| Métricas por modelo ya calculadas (`artifacts/metrics/`) | Sí, para las fases 3-4 | Pipeline de entrenamiento |
| Identificador de paciente/episodio usado en el split | Sí, para la fase 1 (leakage) | Esquema de datos (`03-CATALOGO-DATOS-Y-VARIABLES.md` o equivalente) |
| Variable(s) demográfica(s) disponibles (régimen de afiliación, sexo, edad, fuente del dato — MIMIC vs. local) | Sí, para la fase 5 (equidad) | Catálogo de entidades del proyecto |
| Predicciones probabilísticas del modelo ganador (no solo la clase predicha) | Sí, para la fase 4 (calibración) | `artifacts/models/*` |

Si un insumo no existe, la fase correspondiente se marca `[NO VERIFICABLE — falta insumo X]` en
vez de omitirse en silencio — la ausencia de una verificación es en sí misma un hallazgo que debe
quedar registrado.

## Salida

- `resources/tfm/validacion-cientifica/reporte-auditoria.md` — hallazgo por fase, con severidad
  (bloqueante / advertencia / informativo) y la evidencia (ruta de archivo, número de filas
  afectadas, valor p, etc.).
- `resources/tfm/validacion-cientifica/model-card-<modelo-ganador>.md` — ver
  `references/plantilla-model-card.md`.
- Si se detecta leakage o una comparación sin soporte estadístico, el reporte se etiqueta como
  **bloqueante para el capítulo de Resultados** — `tfm-redactor` debe leer este reporte antes de
  redactar esa sección.

## Proceso

### Fase 1 — Prevención de fuga de datos (leakage)
Verifica que el split train/test/CV se haga por **unidad de paciente/episodio**, no por fila
suelta. Riesgos específicos de este proyecto:
- Si un mismo paciente tiene múltiples visitas en MIMIC-IV-ED o en San Juan de Dios, todas sus
  filas deben caer en el mismo lado del split (train o test), nunca repartidas.
- La normalización/escalado (`StandardScaler`, imputación) debe **ajustarse solo con train** y
  aplicarse a test — nunca ajustar con el dataset completo antes del split.
- Si se usa oversampling (SMOTE), debe aplicarse **después** del split, solo sobre train — aplicar
  SMOTE antes del split filtra información sintética del test hacia el train.
- Ver `references/checklist-leakage.md` para el detalle completo por etapa del pipeline.

### Fase 2 — Estrategia de validación cruzada apropiada para desbalance
Confirma que el 10-fold CV sea **estratificado** (`StratifiedKFold`, no `KFold` plano) para que
cada fold conserve la proporción real de Niveles I-V — con Nivel I raro, un fold no estratificado
puede quedar sin ningún ejemplo de esa clase.

### Fase 3 — Validación estadística de la comparación entre modelos
No basta con que Early Fusion tenga Recall 0.86 y Late Fusion 0.81 en Nivel I-II — hay que
verificar si la diferencia es estadísticamente significativa dado el tamaño de muestra:
- **Prueba de McNemar** para comparar accuracy/recall de dos clasificadores sobre el mismo
  conjunto de test.
- **Prueba de DeLong** para comparar AUC-ROC entre dos modelos.
- Reportar intervalo de confianza (bootstrap, 1000+ remuestreos) para cada métrica, no solo el
  punto estimado — especialmente importante en Nivel I por el tamaño de muestra pequeño.
- Ver `references/pruebas-estadisticas-comparacion-modelos.md` para el código de referencia.

### Fase 4 — Calibración de probabilidades
El sistema muestra al profesional una "probabilidad/confianza" (RNA-002, RF-XAI-*) — esa cifra
solo es interpretable si el modelo está calibrado. Genera curva de calibración (reliability
diagram) y Brier score para el modelo ganador. Si no está calibrado, documentar la necesidad de
calibración post-hoc (Platt scaling / isotonic regression) como paso adicional del pipeline, no
como nota opcional.

### Fase 5 — Auditoría de sesgo y equidad por subgrupo
Desagrega las métricas del modelo ganador (Recall, F1 por Nivel I-II especialmente) por:
- Fuente del dato (MIMIC vs. San Juan de Dios) — para cuantificar si el fine-tuning realmente
  corrigió el sesgo geográfico que `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §8 declara como
  limitación, en vez de asumirlo corregido sin medirlo.
- Régimen de afiliación (si el campo está disponible).
- Sexo y grupo etario.
Cualquier caída de Recall en Nivel I-II mayor a un umbral relevante clínicamente (a definir con la
directora, no inventado por este skill) en un subgrupo específico es un hallazgo bloqueante, no
una nota al pie — ver `references/auditoria-equidad-subgrupos.md`.

### Fase 6 — Trazabilidad y reproducibilidad
Confirma que cada corrida quede registrada (MLflow/DVC, o al menos una tabla versionada con
commit hash + semilla + hiperparámetros + métrica resultante) y que el notebook/script corra de
principio a fin sin celdas huérfanas o estado oculto (`Restart & Run All` limpio).

### Fase 7 — Model card
Genera `model-card-<modelo>.md` con: datos de entrenamiento (fuente, tamaño, periodo), métricas
por clase con intervalo de confianza, resultado de la auditoría de equidad, casos de uso previstos
y explícitamente NO previstos, y limitaciones conocidas. Ver
`references/plantilla-model-card.md`.

## Integración con el resto del kit

- Se ejecuta **después** de que `builder`/`tdd-implementacion` generen resultados reales, y
  **antes** de que `tfm-redactor` redacte el capítulo de Resultados — es el gate entre ambos.
- Si detecta leakage o falta de significancia estadística, el hallazgo se pasa a
  `tdd-implementacion` para corregir el pipeline (no a `tfm-redactor`, que no debe "redactar
  alrededor" de un problema metodológico).
- Los hallazgos de equidad por subgrupo alimentan directamente la sección de Limitaciones del TFM
  (vía `tfm-redactor`) como hallazgos reales del proyecto, no como limitaciones genéricas copiadas
  de la literatura — exactamente lo que `brief_finalizacion_tfm.md` pide en su sección 2.3.

## Anti-patrones (qué NO debe hacer este skill)

- ❌ Declarar un modelo "ganador" sin prueba estadística solo porque tiene la métrica puntual más
  alta.
- ❌ Asumir que el fine-tuning con datos locales corrigió el sesgo geográfico sin medir el
  desempeño desagregado por fuente de dato.
- ❌ Inventar el umbral de "caída de Recall aceptable" por subgrupo — eso es una decisión clínica
  que corresponde a la directora/equipo médico, este skill solo mide y reporta.
- ❌ Aprobar un capítulo de Resultados que no tenga trazabilidad de la semilla aleatoria y la
  versión de datos usada.
