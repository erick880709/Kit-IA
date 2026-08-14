# RF-016: Pipeline de Entrenamiento y Evaluación Offline

**Tipo:** Requerimiento funcional
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §5 · `context/CONTEXTO TRIAJE.txt` §5
**Prioridad:** Alta

## Descripción
El sistema debe incluir un pipeline offline completo: ingesta de las fuentes de datos, anonimización, limpieza (imputación de nulos, outliers), normalización de numéricas y codificación de categóricas, generación de embeddings del texto, split train/test con 10-fold cross-validation, entrenamiento de baselines unimodales (LR, RF, XGBoost), entrenamiento en paralelo de early y late fusion, threshold tuning por clase, evaluación con métricas por nivel, SHAP sobre el ganador y comparación contra benchmarks.

## Actores involucrados
Equipo de investigación (ejecución en entorno Jupyter/VS Code).

## Criterios de aceptación
- La anonimización es obligatoria antes de cualquier paso posterior.
- Ambas arquitecturas de fusión se entrenan y comparan (decisión cerrada, no elegir una sola).
- Se documenta la comparativa completa (no solo el ganador) para el Cap. 5 del TFM.
- Las métricas se reportan por clase y con AUPRC para clases minoritarias.

## Dependencias / relacionados
[[RT-001]], [[RT-002]], [[RT-004]], [[RT-009]], [[RNF-004]], [[RNF-005]], RD-006.

## Notas del analista
Los 13 pasos del pipeline están numerados en 02 §5 y 05 §5 (12 pasos en v2.0); la secuencia es consistente.

**Paso 3 (limpieza) — hallazgos de datos reales:**
- Normalizar REGIMEN: unificar typos (`ESPCIAL`→ESPECIAL, `EXCPECION`/`EXCEPCION`→EXCEPCION, `SUBIDIADO`→SUBSIDIADO, etc.).
- Filtrar AÑO corrupto (~130 filas con 2027-2358 en morbilidad).
- Imputar/marcar fechas de atención faltantes (Hora_Ingre/Hora_Atencion del dataset de triaje vienen con fecha fantasma `01/01/1900`).
