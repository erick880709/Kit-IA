# ADR-006 — Aislamiento entre pruebas y evidencia de producción (artifacts/)

- **Estado:** Aceptado · **Fecha:** 2026-08-14
- **Contexto:** los tests de entrenamiento sobrescribían `artifacts/metrics/`
  reales (métricas del pipeline reemplazadas por métricas de prueba con
  k_folds=3), hallazgo detectado en la auditoría de trazabilidad del TFM.

## Decisión

Las funciones de entrenamiento siguen escribiendo vía `guardar_metricas`, pero
**las pruebas redirigen `ARTIFACTS_METRICS` a un directorio temporal**
(`monkeypatch` + `tmp_path`). La evidencia de producción solo la genera el
orquestador `ml/pipeline.py` y la auditoría `ml/validacion.py`.

## Alternativas consideradas

1. Agregar un parámetro `destino` a todas las funciones de entrenamiento:
   desechada — dispersa la responsabilidad de salida por toda la API pública.
2. Omitir persistencia en funciones de entrenamiento: desechada — la
   trazabilidad del pipeline exige que cada corrida deje JSON con nombre de
   modelo y k_folds.

## Consecuencias

- `pytest` nunca vuelve a tocar la evidencia real (regresión cubierta con
  asserts sobre `tmp_path` en los 3 tests afectados).
- La trazabilidad del capítulo de Resultados quedó restaurada: CV de 5 folds
  con valores distintos por modelo (early 0.578, late promedio 0.555,
  stacking 0.560).

## Evidencia

`tests/test_ml_pipeline.py`: `test_baselines_cv_completo`,
`test_early_fusion_metricas`, `test_late_fusion_combinadores` — todos
verifican que la salida quedó en `tmp_path`.
