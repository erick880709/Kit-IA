# RT-002: Stack Tecnológico y Herramientas

**Tipo:** Requisito técnico
**Categoría:** Stack tecnológico
**Fuente:** 02-ESPECIFICACION-TECNICA-MODELOS-IA.md; 04-ESPECIFICACION-APLICACION-DEMO.md §1; contexto-tfm.md §6; 05-PENDIENTES-PARA-DIRECTORA.md

## Descripción
El sistema se desarrollará sobre un stack Python para ciencia de datos y machine learning, con una capa de aplicación web para la demo funcional. El stack se divide en dos componentes principales: (1) pipeline de entrenamiento/evaluación de modelos (offline) y (2) aplicación demo interactiva.

## Stack definido

### Pipeline de Entrenamiento y Modelado (offline)
| Componente | Tecnología | Justificación |
|---|---|---|
| Lenguaje | Python 3.10+ | Estándar en ML/Data Science |
| Manipulación de datos | pandas, numpy | Estándar |
| Modelos clásicos | scikit-learn (Random Forest, Logistic Regression) | Baselines unimodales |
| Gradient Boosting | XGBoost | Estado del arte en datos tabulares |
| Deep Learning | TensorFlow / Keras o PyTorch | Redes neuronales para fusión y NLP |
| NLP / Embeddings | Transformers (HuggingFace), BioBERT-es o BETO | Embeddings de texto clínico en español |
| Explicabilidad | SHAP (TreeExplainer para RF/XGBoost, KernelExplainer como fallback) | XAI |
| Validación | scikit-learn (10-fold CV, métricas) | Estándar |
| Manejo de desbalance | imbalanced-learn (SMOTE), class_weight en scikit-learn/XGBoost | Clases minoritarias (Nivel I) |
| Entorno | Jupyter Notebooks + scripts Python | Experimentación + producción |

### Aplicación Demo (interfaz interactiva)
| Componente | Alternativas | Estado |
|---|---|---|
| Framework web | **Streamlit** (recomendado) o Flask | **PENDIENTE DE DECISIÓN** (ver `05-PENDIENTES-PARA-DIRECTORA.md` #1) |
| Visualización | matplotlib, seaborn, plotly, streamlit-shap | Gráficos SHAP y dashboard |
| Base de datos | SQLite (demo) / PostgreSQL (producción) | Almacenamiento de eventos, auditoría |
| API REST | FastAPI (si se elige Flask) o integrado en Streamlit | Separación frontend/backend |

### Infraestructura y DevOps
| Componente | Tecnología |
|---|---|
| Control de versiones | Git + GitHub |
| Gestión de dependencias | pip + requirements.txt o poetry |
| Entorno virtual | venv o conda |
| Contenedores (opcional) | Docker |

## Impacto en la arquitectura
- La separación entre pipeline offline (notebooks/scripts de entrenamiento) y aplicación online (demo) es fundamental: el modelo se entrena una vez y se carga en la demo como un artefacto serializado (pickle/joblib para sklearn/XGBoost, SavedModel para TF/PyTorch).
- Streamlit simplifica el desarrollo al unificar frontend y backend en un solo archivo, pero limita la personalización de la UI. Flask/FastAPI + frontend separado da más control a costa de mayor esfuerzo.
- Para la demo TFM, Streamlit ofrece el mejor balance esfuerzo/resultado.

## Notas del analista
- **La decisión Streamlit vs. Flask está PENDIENTE.** `04-ESPECIFICACION-APLICACION-DEMO.md` recomienda Streamlit; `05-PENDIENTES-PARA-DIRECTORA.md` lo lista como decisión #1 que requiere confirmación de Damaris Fuentes Lorenzo.
- Independientemente de la elección, el motor de IA (inferencia) debe estar desacoplado como un módulo Python independiente, no embebido en el código de la UI.
- Usar el mismo entorno Python para entrenamiento y demo simplifica la compatibilidad de versiones de librerías.
