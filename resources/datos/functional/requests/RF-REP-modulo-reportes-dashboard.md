# RF-REP: Módulo de Reportes y Dashboard

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 48, Módulo Reportes; 04-ESPECIFICACION-APLICACION-DEMO.md; 06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md
**Prioridad:** Alta

## Descripción
El sistema proporcionará dashboards y reportes que permitan a los diferentes roles (médicos, coordinadores, auditores, investigadores) monitorear el desempeño operativo del servicio de urgencias, la calidad de las clasificaciones y la concordancia entre la IA y los profesionales. Los indicadores deben ser filtrables por período, nivel de triaje y profesional.

## Actores involucrados
- Coordinador del Servicio / Dirección Médica (dashboard operativo)
- Médico de Urgencias
- Auditor
- Investigador / Científico de Datos

## Criterios de aceptación

### RF-REP-001 — Dashboard General
- Panel de control con indicadores operativos agregados: total de triajes del período, distribución por niveles (I-V), tiempos promedio de clasificación, tasa de reclasificaciones, disponibilidad del modelo IA.

### RF-REP-002 — Distribución de Triaje por Niveles
- Gráfico de barras o torta con la distribución de pacientes clasificados en cada nivel (I-V) para el período seleccionado.
- Comparación con la distribución de referencia nacional ("Clasificación en Triaje Urgencias", datos.gov.co).

### RF-REP-003 — Tiempo Promedio de Clasificación
- Tiempo transcurrido desde la creación del evento de triaje hasta la validación/cierre.
- Desglose por nivel de triaje y por profesional.
- Indicador de cumplimiento del tiempo máximo normativo por nivel (Resolución 5596/2015).

### RF-REP-004 — Desempeño del Modelo IA
- Métricas calculadas sobre los datos de la demo (no confundir con la evaluación offline del modelo): Accuracy, Precision, Recall, F1-Score, AUC-ROC.
- Las métricas se presentan agregadas (macro-promedio) y desglosadas por nivel de triaje.
- AUPRC para clases minoritarias (Niveles I y II).
- Comparación visual contra las metas cuantitativas del proyecto (F1 ≥ 0.82, Precisión ≥ 0.85, Recall ≥ 0.80, AUC-ROC ≥ 0.87).

### RF-REP-005 — Concordancia IA vs. Profesional
- Matriz de confusión IA vs. Profesional (por nivel, no solo accuracy global).
- Porcentaje de concordancia global y desglosado por nivel de triaje.
- Listado filtrable de discrepancias con su motivo registrado, para revisión clínica y detección de patrones de error del modelo.
- **Nota metodológica:** esta concordancia se mide sobre casos reales operados en la demo (con sesgo de anclaje porque el profesional ve primero la sugerencia de IA), y es distinta de la evaluación offline del modelo contra el dataset de prueba (10-fold CV).

### RF-REP-006 — Exportación de Reportes
- Formatos: Excel, PDF, CSV.
- El reporte de triaje descargable por evento incluye: paciente anonimizado, fecha/hora, nivel IA sugerido vs. nivel asignado por el profesional, signos vitales, motivo de consulta, top variables SHAP.

## Dependencias / relacionados
- RF-AUD-005: Los datos para los reportes provienen del módulo de auditoría.
- `04-ESPECIFICACION-APLICACION-DEMO.md`: pantalla de Dashboard Operativo.
- `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §6: reportes habilitados por la comparativa IA vs. profesional.
- Resolución 5596 de 2015: tiempos máximos de atención por nivel.

## Notas del analista
- El indicador de concordancia (RF-REP-005) es una métrica de **utilidad clínica real** (¿el profesional confía en la IA?), no de acuerdo interobservador puro. El sesgo de anclaje debe documentarse como limitación en el Cap. 6 del TFM.
- AUPRC es más informativo que AUC-ROC para clases minoritarias (Nivel I); incluirlo en el dashboard para investigadores.
