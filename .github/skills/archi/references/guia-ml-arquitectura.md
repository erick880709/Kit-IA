# Guía: Arquitectura de Sistemas de Machine Learning / IA

Se activa cuando el sistema a documentar o diseñar **no es una aplicación transaccional tradicional**, sino uno donde un modelo entrenado (clásico, deep learning, o multimodal) es un componente central: predice, clasifica, genera texto/imagen, o soporta una decisión. Ejemplos de disparadores: "sistema de clasificación con IA", "modelo predictivo", "pipeline de entrenamiento", "motor de recomendación", "TFM/tesis con componente de ML", "necesito documentar la arquitectura de mi modelo".

El C4 Model (`references/diagramas-c4-ejemplos.md`) sigue aplicando para la parte de **aplicación** (API, frontend, orquestación) — no lo reemplaces. Lo que esta guía agrega es lo que el C4 clásico no cubre bien: el ciclo de vida de los **datos** y del **modelo**, que en un sistema de ML es tan arquitectónico como los contenedores de software.

## Cuándo un proyecto necesita esta guía además del flujo normal (Caso A/B/C)

- El sistema entrena o va a entrenar un modelo propio (no solo consume una API de IA de terceros sin ajuste).
- Hay un pipeline de datos no trivial (ingesta, limpieza, feature engineering) que alimenta ese modelo.
- El documento de arquitectura necesita responder no solo "cómo se despliega el software" sino "cómo se entrena, valida, versiona y monitorea el modelo".

Si el sistema **solo consume** un modelo de terceros vía API (ej. llamar a un LLM comercial sin fine-tuning ni pipeline de datos propio), no actives esta guía completa — trátalo como una integración externa más en el C4 (`System_Ext`) y sigue el flujo normal.

## 1. Las dos arquitecturas de un sistema de ML

A diferencia del software tradicional, un sistema de ML tiene **dos ciclos de vida distintos** que hay que documentar por separado y luego mostrar cómo se conectan:

1. **Arquitectura de entrenamiento (offline):** cómo los datos crudos se convierten en un modelo evaluado y versionado. No sirve al usuario final en tiempo real — es el proceso que produce el artefacto "modelo".
2. **Arquitectura de inferencia/servicio (online u offline por lotes):** cómo ese modelo, una vez entrenado, se integra en el sistema para producir predicciones que un usuario o proceso de negocio consume.

Documenta ambas explícitamente — es un error común mezclar los dos en un solo diagrama y terminar sin claridad sobre qué corre en producción con el usuario esperando respuesta y qué corre en batch sin nadie esperando.

## 2. Pipeline de datos (Data Pipeline)

Para cada fuente de datos, documenta en una tabla:

| Fuente | Tipo | Volumen / frecuencia de actualización | Rol (entrenamiento / validación / producción) | Sensibilidad |
|---|---|---|---|---|
| [ej. Historial clínico Hospital X] | Estructurado, tabular | [ej. ~50k registros, actualización mensual] | Adaptación al contexto local | Datos de salud — requiere anonimización |
| [ej. Dataset público internacional] | Estructurado + texto libre | [ej. 422.500 registros, estático] | Preentrenamiento / baseline | Pública, ya anonimizada |

Etapas típicas a documentar (usa `references/diagramas-ml-ejemplos.md` para el diagrama):
1. **Ingesta:** de dónde vienen los datos y cómo llegan (batch/CSV, streaming, API, base de datos operacional).
2. **Limpieza y calidad de datos:** imputación de nulos, outliers, deduplicación, reglas de validación. Documenta qué política se sigue cuando un registro no pasa la validación (¿se descarta, se marca, se corrige?).
3. **Anonimización/pseudonimización** (obligatorio si hay datos personales o sensibles — ver sección 7).
4. **Feature engineering:** transformación de variables crudas en features de entrada al modelo (normalización, one-hot, embeddings de texto, agregaciones). Si hay un **feature store** (ej. Feast, Databricks Feature Store, o una tabla propia versionada), documéntalo como componente explícito — evita que features de entrenamiento y de producción diverjan silenciosamente (*training-serving skew*), que es uno de los fallos más comunes y difíciles de detectar en sistemas de ML.
5. **Split de datos:** train/validation/test (y su proporción), y si aplica, estrategia de validación cruzada (k-fold). Documenta el criterio de partición (aleatorio, temporal, estratificado por clase) — es una decisión arquitectónica, no un detalle de notebook: una partición mal elegida (ej. aleatoria en datos con fuga temporal) infla artificialmente las métricas.

## 3. Arquitectura de entrenamiento

Documenta como un pipeline (diagrama de flujo, ver `references/diagramas-ml-ejemplos.md`), no como prosa:

1. **Modelos baseline (unimodal/simple):** los primeros modelos que establecen una cota de comparación (ej. regresión logística, Random Forest) — nunca saltes directo al modelo complejo sin un baseline documentado; sin él no puedes justificar que la complejidad adicional (deep learning, fusión multimodal) realmente aporta.
2. **Modelo(s) candidato(s):** arquitectura elegida y por qué (ej. "fusión temprana vs. tardía" para datos multimodales — documenta ambas si el proyecto las compara, igual que un ADR de software).
3. **Entrenamiento e hiperparámetros:** framework (scikit-learn, XGBoost, TensorFlow/Keras, PyTorch), estrategia de búsqueda de hiperparámetros si aplica (grid/random search, Optuna), y **seguimiento de experimentos** (MLflow, Weights & Biases, o al menos una tabla versionada de corridas) — sin esto, nadie puede reproducir por qué se eligió una configuración sobre otra.
4. **Cómputo de entrenamiento:** dónde corre (CPU/GPU local, notebook cloud tipo Colab/SageMaker/Vertex AI Workbench, cluster) — esto es una decisión de infraestructura real, va en la Vista de Despliegue igual que cualquier otro componente.
5. **Versionado del modelo y de los datos:** cómo se identifica de forma única una combinación (versión de datos + código + hiperparámetros + modelo resultante). Si no hay una herramienta dedicada (DVC, MLflow Model Registry), como mínimo documenta la convención de nombres/tags que se usa y dónde vive cada artefacto.

### ADR para decisiones de modelo

Usa el mismo formato de ADR de la Sección 11 de `references/plantilla-documento-arquitectura.md` para decisiones como "por qué fusión tardía y no temprana", "por qué XGBoost y no una red neuronal", "por qué se descartó aumentar la clase minoritaria con SMOTE" — son decisiones arquitectónicas tanto como elegir microservicios vs. monolito, y deben tener el mismo rigor de contexto/alternativas/consecuencias.

## 4. Evaluación y métricas — cómo documentarlas

No basta con reportar una métrica global. Documenta siempre:

- **Métricas objetivo** definidas antes de entrenar (F1, precisión, recall, AUC-ROC, AUPRC — según el problema), con el valor meta y el valor obtenido.
- **Métricas por clase**, no solo el macro-promedio, cuando hay desbalance de clases — un buen promedio puede esconder que la clase más crítica de negocio (ej. el nivel más grave de una clasificación de riesgo) tiene mal desempeño.
- **Matriz de confusión** del modelo ganador.
- **Comparación contra baseline y contra benchmarks externos** (literatura, estándar de la industria, sistema que se reemplaza) — un modelo no se evalúa en el vacío.
- **Estrategia de manejo de desbalance** si aplica (class weights, SMOTE, focal loss) y por qué se eligió esa y no otra.

## 5. Explicabilidad (XAI)

Si el sistema debe justificar sus predicciones ante un humano (especialmente en dominios regulados: salud, crédito, selección de personal, justicia), documenta:

- **Técnica usada** (SHAP, LIME, feature importance nativa del modelo, attention weights) y por qué es apropiada para el tipo de modelo.
- **Qué se le muestra al usuario final**: no es lo mismo un valor SHAP crudo que una explicación en lenguaje natural para un profesional no técnico — documenta el contrato de esa traducción.
- **Alcance de la explicación**: ¿es global (qué variables importan en general) o local (por qué esta predicción específica)? La mayoría de los casos de negocio necesitan explicación local.

## 6. Arquitectura de inferencia / servicio del modelo

Documenta como un contenedor más del C4 Nivel 2, con estas decisiones específicas:

| Decisión | Opciones típicas |
|---|---|
| Modo de inferencia | Tiempo real (API síncrona) vs. batch (proceso periódico) vs. streaming |
| Dónde vive el modelo | Empaquetado dentro del servicio de aplicación vs. servicio de inferencia dedicado (ej. TensorFlow Serving, TorchServe, Triton, un endpoint gestionado de SageMaker/Vertex AI/Azure ML) |
| Latencia objetivo | [SLA en ms/s — si es tiempo real, es un requerimiento no funcional que condiciona la elección de modelo] |
| Reentrenamiento | Manual bajo demanda vs. programado (ej. mensual) vs. disparado por detección de deriva |

## 7. Gobernanza, ética y cumplimiento (específico de IA)

Esto va en la Sección 2 (Restricciones) y 13 (Riesgos) del documento, pero no lo omitas por estar acostumbrado a pensar en restricciones puramente técnicas:

- **Rol del sistema:** ¿es de apoyo a una decisión humana, o autónomo? Si es de apoyo, esto debe quedar explícito en cualquier interfaz o documento — es una restricción de diseño, no un detalle de UX.
- **Marco normativo de datos personales/sensibles aplicable** (ej. Ley 1581 de 2012 en Colombia, GDPR, HIPAA) y qué implica para el pipeline: anonimización obligatoria antes de procesar, base legal para el uso de los datos, autorización de comités de ética si los datos son de salud o de otra categoría sensible.
- **Sesgo y representatividad de los datos:** si el dataset de entrenamiento no representa bien la población real donde se va a usar el sistema (ej. un dataset internacional aplicado a un contexto local sin adaptación), documéntalo como limitación explícita, no lo dejes implícito.
- **Trazabilidad:** cada predicción en producción debería quedar registrada (input, versión del modelo, output, y si hubo intervención humana que la modificó) — necesario tanto para auditoría como para detectar deriva del modelo.
- **Detección de deriva (drift):** cómo se monitorea que la distribución de datos en producción no se aleje de la de entrenamiento (data drift) y que el desempeño del modelo no se degrade con el tiempo (concept drift). Aunque el proyecto no lo implemente todavía, documenta al menos la estrategia prevista.

## 8. Qué sección de la plantilla usar

Usa `references/plantilla-documento-arquitectura-ml.md` en vez de (o como complemento de) `references/plantilla-documento-arquitectura.md` cuando el sistema tiene componente de ML relevante — esa plantilla inserta las secciones de datos/entrenamiento/evaluación/explicabilidad en el lugar correcto del esqueleto arc42/C4 sin duplicar lo que ya cubre la plantilla base.

Para el stack técnico (Python, notebooks, pandas, scikit-learn/TensorFlow) y cómo documentar el código de ML de forma reproducible, ver `references/guia-notebooks-python.md`.
