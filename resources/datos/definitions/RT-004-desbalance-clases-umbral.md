# RT-004: Estrategia de Manejo de Desbalance de Clases y Umbral por Clase

**Tipo:** Requisito técnico
**Categoría:** Modelado / Optimización
**Fuente:** 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §3, §4; 01-CONTEXTO-MAESTRO-CONSOLIDADO.md §4

## Descripción
Los niveles de triaje presentan un desbalance natural severo: Niveles IV-V son mayoritarios mientras que Nivel I es clínicamente crítico pero estadísticamente raro. El sistema debe implementar técnicas de manejo de desbalance durante el entrenamiento y una estrategia de umbral de decisión por clase que priorice Recall sobre Precisión en los Niveles I y II.

## Criterio medible / restricción concreta

### Técnicas de manejo de desbalance (a evaluar y comparar)
1. **Class weights:** ponderación inversamente proporcional a la frecuencia de cada clase en la función de pérdida (disponible en scikit-learn, XGBoost, TensorFlow/Keras).
2. **SMOTE (Synthetic Minority Over-sampling Technique):** generación de ejemplos sintéticos para clases minoritarias (biblioteca `imbalanced-learn`). Cuidado: SMOTE en datos clínicos puede generar combinaciones no fisiológicamente plausibles.
3. **Focal loss:** función de pérdida que reduce el peso de ejemplos bien clasificados y enfoca el entrenamiento en los difíciles (si se usa red neuronal).
4. **Submuestreo de clases mayoritarias:** alternativa simple pero con riesgo de pérdida de información.

Se debe reportar cuál técnica se usó y su impacto en las métricas por clase.

### Estrategia de umbral por clase (corrige RF-IA-003)
- **Niveles I y II:** umbral de decisión optimizado para maximizar Recall, calibrado sobre la curva ROC/PR por clase. NO se usa argmax puro (clase con mayor probabilidad).
- **Niveles III-V:** umbral estándar (argmax).
- **Justificación clínica:** el costo de un falso negativo en Nivel I-II (subclasificar a un paciente crítico) es un riesgo vital inasumible. Un falso positivo (sobreclasificar) genera sobrecarga operativa pero no pone en peligro la vida del paciente.
- **Técnica:** threshold tuning sobre el conjunto de validación, documentando el punto de equilibrio elegido (trade-off Precision vs. Recall) para cada nivel.

### Métricas obligatorias a reportar
- Por cada nivel (I, II, III, IV, V): Precision, Recall, F1-Score, AUC-ROC.
- Macro-promedio y weighted-promedio de todas las métricas.
- AUPRC (Precision-Recall AUC) para clases minoritarias (Niveles I y II).
- Matriz de confusión completa (5×5).

## Impacto en la arquitectura
- El umbral tuning es un paso de post-procesamiento (no modifica el modelo entrenado, solo la regla de decisión).
- Los umbrales por clase deben almacenarse como metadatos del modelo (junto con RNA-002: versión, hiperparámetros, métricas) para reproducibilidad.
- La UI debe reflejar que la predicción no es simplemente "la clase más probable", sino que aplica una regla de decisión clínica calibrada.

## Notas del analista
- **RF-IA-003 en `CONTEXT_TRIA.txt` es contradictorio con esta estrategia** (dice "selecciona la clase con mayor probabilidad" — argmax puro). La versión corregida está en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` y debe reflejarse en el documento maestro funcional (`05-PENDIENTES-PARA-DIRECTORA.md` #3).
- SMOTE en datos clínicos requiere validación clínica: un paciente sintético con SpO₂ 88% + frecuencia respiratoria 30 + temperatura 39°C puede ser clínicamente plausible, pero uno con SpO₂ 99% + frecuencia respiratoria 5 no lo es. Evaluar SMOTE-NC (para variables mixtas) o variantes con restricciones de dominio.
