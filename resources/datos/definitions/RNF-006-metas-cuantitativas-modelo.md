# RNF-006: Metas Cuantitativas de Desempeño del Modelo

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento / Calidad del modelo
**Fuente:** 01-CONTEXTO-MAESTRO-CONSOLIDADO.md §4; contexto-tfm.md §4; CONTEXTO_TRIAJE.txt v2.0

## Descripción
El modelo de IA debe alcanzar métricas de desempeño mínimas, evaluadas sobre el conjunto de prueba (10-fold cross-validation), que garanticen su utilidad clínica como herramienta de apoyo a la decisión. Las métricas deben evaluarse por clase (no solo macro-promedio) dado el desbalance natural de los niveles de triaje (IV-V mayoritarios, I crítico pero raro).

## Criterio medible / restricción concreta

| Métrica | Meta mínima | Notas |
|---|---|---|
| F1-Score (macro-promedio) | ≥ 0.82 | Media armónica de precisión y recall |
| Precisión (macro-promedio) | ≥ 0.85 | Fracción de predicciones correctas entre todas las predicciones |
| Recall (macro-promedio) | ≥ 0.80 | Fracción de casos reales correctamente identificados |
| AUC-ROC (macro-promedio) | ≥ 0.87 | Capacidad discriminativa global |

- **Evaluación por clase obligatoria**, no solo macro-promedio. Un F1 global alto puede esconder mal desempeño en Nivel I (el más crítico).
- **AUPRC (Precision-Recall AUC) adicional** para clases minoritarias (Niveles I y II), por ser más informativa que AUC-ROC en presencia de desbalance extremo.
- **Prioridad de Recall sobre Precisión en Niveles I y II:** el costo clínico de un falso negativo (subclasificar a un paciente crítico) es inasumible. La estrategia de umbral por clase está calibrada para maximizar Recall en estos dos niveles.
- **Comparación contra benchmarks de la literatura** (CTAS AUROC 0.882, Raita et al. 2019 AUC 0.87, Hong et al. 2018 AUC 0.93, Ueareekul et al. 2024 AUPRC 0.629) — el modelo debe ser competitivo con el estado del arte.

## Impacto en la arquitectura
- El pipeline de evaluación (10-fold CV) debe calcular y reportar métricas por clase automáticamente.
- El módulo de gestión de modelos (RF-MOD-*) debe almacenar estas métricas junto con cada versión registrada.
- La estrategia de umbral por clase requiere un paso de post-procesamiento después de la predicción de probabilidades (no es un cambio en el modelo, sino en la regla de decisión).

## Notas del analista
- Las metas son consistentes en los 5 documentos del contexto (`01-CONTEXTO-MAESTRO-CONSOLIDADO.md`, `contexto-tfm.md`, `CONTEXTO_TRIAJE.txt`, PDF del TFM, `CONTEXT_TRIA.txt`). No hay ambigüedad.
- Si el modelo no alcanza estas metas con los datos disponibles, debe documentarse como limitación (Cap. 6 del TFM), no ajustarse las metas a la baja sin justificación.
- AUPRC no está definido como meta numérica en los documentos fuente, pero se recomienda reportarlo dada la naturaleza desbalanceada del problema.
