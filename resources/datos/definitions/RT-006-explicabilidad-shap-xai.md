# RT-006: Estrategia de Explicabilidad (XAI) con SHAP

**Tipo:** Requisito técnico
**Categoría:** IA Explicable / XAI
**Fuente:** 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §6; CONTEXT TRIA.txt — Sección 32 (RNX-001 a 006)

## Descripción
Cada predicción del modelo debe generar una explicación interpretable mediante SHAP (SHapley Additive exPlanations) que permita al profesional comprender qué variables influyeron en la clasificación, en qué dirección y con qué magnitud. La explicación debe presentarse en lenguaje clínico, no en términos técnicos del modelo.

## Especificación técnica

### Método SHAP
- **Para modelos basados en árboles (Random Forest, XGBoost):** TreeExplainer — exacto y rápido, aprovecha la estructura del modelo.
- **Para redes neuronales o early fusion con componentes no arbóreos:** KernelExplainer con submuestreo del background dataset, o DeepExplainer (TF/PyTorch).
- **Optimización:** si SHAP es demasiado lento para inferencia en tiempo real (< 3s, RNP-001), evaluar:
  - Precomputar valores SHAP esperados por rango de variables y mostrarlos como referencia (no personalizados por paciente, pero orientativos).
  - Usar TreeExplainer con un subconjunto pequeño del background (100-200 muestras).
  - Ejecutar SHAP en segundo plano y mostrar primero la predicción, luego la explicación cuando esté lista (RNP-004).

### Contrato de salida por predicción (4 elementos obligatorios)
1. **Nivel predicho (I-V) + probabilidad/confianza + versión del modelo** (RNA-002, RNA-005).
2. **Top-5 a Top-10 variables SHAP** con mayor influencia, expresadas en lenguaje clínico comprensible. Ejemplo: "Saturación de O₂ baja (88%) fue el factor de mayor peso para clasificar como Nivel II", no "SpO₂: SHAP = +0.34".
3. **Comparación implícita con criterios MTS/Manchester** cuando las variables coincidan con los criterios de esos sistemas (frecuencia respiratoria, SpO₂, temperatura, nivel de conciencia). Refuerza la confianza clínica al mostrar convergencia con sistemas de triaje validados internacionalmente.
4. **Tiempo de inferencia** (RNA-003) — objetivo < 3 segundos.

### Visualización (RF-XAI-005)
- Gráfico de barras horizontales con top variables y sus valores SHAP (dirección + magnitud).
- Waterfall plot: contribución acumulada de cada variable desde el valor base (expected value) hasta la predicción final.
- Force plot: alternativa compacta al waterfall, útil para pantallas pequeñas.
- Colores: rojo = aumenta la probabilidad del nivel predicho, azul = la disminuye.

## Impacto en la arquitectura
- SHAP se calcula como un paso adicional después de la predicción, no durante el entrenamiento.
- El explainer SHAP se carga en memoria junto con el modelo al iniciar el servicio de inferencia (evita recargarlo en cada predicción).
- Las explicaciones generadas se almacenan junto con la predicción (ENT-010, RNX-005) para auditoría y consulta futura.

## Notas del analista
- SHAP es computacionalmente costoso, especialmente KernelExplainer. Para la demo TFM, si el tiempo de respuesta excede 3 segundos, se debe priorizar la funcionalidad (que exista la explicación) sobre la velocidad (que sea inmediata), y documentar la limitación.
- La comparación con MTS/Manchester es cualitativa (no es una segunda predicción), pero añade valor clínico significativo.
