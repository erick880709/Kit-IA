# Guía: Python, Notebooks y Librerías de ML — convenciones para documentar y estructurar

Complementa `references/guia-ml-arquitectura.md`. Mientras esa guía cubre el "qué" arquitectónico (pipeline, modelo, evaluación), esta cubre el "cómo" a nivel de código: cómo debe estar estructurado un proyecto de ML en Python para que el documento de arquitectura describa algo reproducible y no una colección de notebooks sueltos.

## 1. Estructura de proyecto recomendada

```
proyecto-ml/
├── data/
│   ├── raw/              # Datos crudos, nunca se modifican a mano
│   ├── interim/          # Datos en transformación intermedia
│   └── processed/        # Datos listos para entrenar (features finales)
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_preprocesamiento.ipynb
│   ├── 03_entrenamiento_baseline.ipynb
│   ├── 04_entrenamiento_multimodal.ipynb
│   └── 05_evaluacion_shap.ipynb
├── src/
│   ├── data/              # Scripts de ingesta y limpieza (lo reutilizable, no en el notebook)
│   ├── features/          # Feature engineering
│   ├── models/            # Definición, entrenamiento y predicción
│   └── evaluation/         # Métricas, matrices de confusión, SHAP
├── models/                 # Artefactos de modelos entrenados versionados (o referencia a dónde viven si son pesados)
├── reports/
│   └── figures/
├── requirements.txt (o pyproject.toml + poetry.lock)
├── README.md
└── resources/architecture/   # Documento de arquitectura, diagramas, y esta guía
```

Regla práctica al documentar un proyecto existente (Caso B/AS-IS): si el código real no sigue esta estructura, **no la impongas retroactivamente en el documento** — describe la estructura real y señala en Riesgos/Deuda Técnica si la mezcla de lógica reutilizable dentro de notebooks dificulta la reproducibilidad o el testing.

## 2. Notebooks: qué va en un notebook y qué no

- Los notebooks son para **exploración, iteración visual y comunicación de resultados** (EDA, gráficas, comparación de modelos) — no para lógica que se ejecuta en producción.
- Cualquier función que se vaya a reutilizar (limpieza, feature engineering, entrenamiento parametrizado) debe vivir en `src/` como módulo Python importable, no copiada entre celdas de distintos notebooks. Si al documentar un AS-IS encuentras la misma función de preprocesamiento pegada en 3 notebooks distintos, es deuda técnica — repórtalo en la sección 13 del documento.
- Nombra los notebooks con prefijo numérico que indique el orden del pipeline (`01_`, `02_`...) — facilita entender el flujo sin abrir cada uno.
- Antes de considerar un notebook como fuente de verdad para el documento de arquitectura, verifica que las celdas se ejecutan en orden de arriba hacia abajo sin depender de estado oculto (`Restart & Run All` sin errores) — un notebook que solo funciona por el orden en que el autor ejecutó las celdas manualmente no es reproducible y esa limitación debe quedar anotada.

## 3. Reproducibilidad — qué debe quedar fijado

Para que el documento de arquitectura pueda afirmar que el entrenamiento es reproducible, verifica/documenta:

- **Semillas aleatorias fijadas** (`random_state` en scikit-learn/train_test_split, `numpy.random.seed`, `torch.manual_seed`/`tf.random.set_seed`) en cada paso con componente estocástico (split de datos, inicialización de pesos, SMOTE, cualquier `shuffle`).
- **Versiones exactas de dependencias** en `requirements.txt` (con versión fijada, `pandas==2.2.1`, no `pandas`) o `pyproject.toml`/`poetry.lock` — sin esto, el mismo código puede producir resultados distintos meses después por un cambio de versión de librería.
- **Versión de los datos usados** (hash del archivo, fecha de extracción, o herramienta de versionado como DVC) — un modelo entrenado con "los datos de hoy" sin más contexto no es reproducible.
- **Entorno de ejecución**: Python version, y si el entrenamiento requirió GPU/hardware específico, documentarlo (afecta tanto la reproducibilidad como el costo si se lleva a producción).

## 4. Librerías: cuándo usar cada una (referencia rápida para justificar decisiones en el documento)

### Manipulación y análisis de datos
| Librería | Uso típico | Cuándo preferirla |
|---|---|---|
| `pandas` | Datos tabulares en memoria, limpieza, agregaciones | Volúmenes que caben en memoria (hasta unos pocos millones de filas en una máquina estándar) |
| `numpy` | Operaciones numéricas vectorizadas, base de pandas/scikit-learn | Casi siempre presente como dependencia base |
| `polars` | Alternativa a pandas con mejor rendimiento en datasets grandes | Cuando pandas empieza a ser el cuello de botella de rendimiento |
| `pyspark` | Procesamiento distribuido | Volúmenes que no caben en memoria de una sola máquina |

### Modelos clásicos / tabulares
| Librería | Uso típico |
|---|---|
| `scikit-learn` | Baselines (regresión logística, RF), preprocesamiento (`Pipeline`, `ColumnTransformer`), validación cruzada, métricas |
| `xgboost` / `lightgbm` / `catboost` | Gradient boosting — suele ser el punto de partida más fuerte para datos tabulares antes de saltar a deep learning |
| `imbalanced-learn` | Técnicas de balanceo de clases (SMOTE y variantes) |

### Deep learning y texto
| Librería | Uso típico |
|---|---|
| `tensorflow` / `keras` | Redes neuronales, especialmente si el equipo ya tiene experiencia previa o el despliegue apunta a TF Serving |
| `pytorch` | Alternativa a TensorFlow, dominante en investigación y en modelos de NLP/transformers recientes |
| `transformers` (Hugging Face) | Modelos tipo BERT y variantes preentrenadas para embeddings de texto libre — documentar explícitamente el checkpoint usado (ej. `dccuchile/bert-base-spanish-wwm-cased` para español, o un BERT clínico si existe para el idioma/dominio) |

### Explicabilidad y evaluación
| Librería | Uso típico |
|---|---|
| `shap` | Explicabilidad local/global sobre modelos de árboles, lineales y deep learning |
| `scikit-learn.metrics` | F1, precisión, recall, AUC-ROC, matriz de confusión |

### Experimentos y versionado
| Herramienta | Uso típico |
|---|---|
| `mlflow` | Tracking de experimentos (parámetros, métricas, artefactos) y registro de modelos |
| `dvc` | Versionado de datasets y pipelines de datos junto con Git |
| `weights & biases` | Alternativa a MLflow, más orientada a deep learning |

No conviertas esta tabla en una lista de compras — documenta solo las librerías que el proyecto realmente usa o va a usar, con la justificación de por qué esa y no otra cuando haya una alternativa obvia (ej. "se eligió XGBoost sobre una red neuronal para el submodelo de datos estructurados por el volumen de datos disponible y la necesidad de explicabilidad directa vía feature importance").

## 5. Qué preguntar si falta información (para usar junto al Paso 0.5 / línea base)

Si el proyecto tiene componente de ML y el `.md` de especificaciones no lo resuelve, estas preguntas se agregan al cuestionario de línea base (ver Bloque 12 en `references/cuestionario-linea-base.md`) antes de proponer la arquitectura de entrenamiento/inferencia.
