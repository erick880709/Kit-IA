# RT-001: Stack Tecnológico del Modelo

**Tipo:** Requisito técnico
**Categoría:** Stack tecnológico
**Fuente:** `context/contexto-tfm.md` §6 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §1-5

## Descripción
El entrenamiento y evaluación del modelo se desarrolla en Python con el ecosistema estándar de ciencia de datos y deep learning.

## Criterio medible / restricción concreta
- Lenguaje: Python.
- Librerías: pandas, scikit-learn, XGBoost, TensorFlow/Keras (redes y BERT), SHAP.
- Entorno de ejecución offline: Jupyter / VS Code.
- Enfoque cloud-native para artefactos reproducibles.

## Impacto en la arquitectura
Fija el estándar de artefactos (notebooks, modelos serializados, métricas) que consumen `builder`, `validacion-cientifica-ml` y `tfm-redactor`.

## Notas del analista
Sin restricciones de licenciamiento señaladas; el stack es sugerido por el proyecto y consistente entre documentos.
