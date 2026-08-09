# Estructura de Carpetas Base para Proyecto de Triaje ML

> **Uso para `builder`:** Este archivo define las rutas absolutas (relativas a la raíz del proyecto) donde `builder` debe generar cada tipo de artefacto. No se permite desviación de esta estructura.

## 1. Raíz del proyecto

proyecto-triaje-ml/
├── data/ # Datos estáticos (no subir a Git si son pesados)
│ ├── raw/ # Archivos fuente (MIMIC-IV CSV, Hospital San Juan)
│ ├── interim/ # Datos en proceso de limpieza
│ └── processed/ # Features finales (X_train.npy, y_train.npy)
├── notebooks/ # Jupyter Notebooks (numerados por orden)
│ ├── 01_eda_exploracion.ipynb
│ ├── 02_preprocesamiento_features.ipynb
│ ├── 03_entrenamiento_baseline.ipynb
│ ├── 04_entrenamiento_multimodal.ipynb # Early vs Late Fusion
│ └── 05_evaluacion_shap.ipynb
├── src/ # Código fuente reutilizable (nunca código copiado en notebooks)
│   ├── __init__.py
│   ├── data/ # Scripts de ingesta y limpieza
│   │   ├── __init__.py
│   │   ├── ingesta.py
│   │   ├── limpieza.py
│   │   └── anonimizacion.py
│   ├── features/ # Feature engineering
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   ├── models/ # Entrenamiento y predicción
│   │   ├── __init__.py
│   │   ├── train_baseline.py
│   │   ├── train_early_fusion.py
│   │   ├── train_late_fusion.py
│   │   └── predict.py
│   ├── evaluation/ # Métricas y explicabilidad
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── shap_explain.py
│   └── serving/ # Interfaz de usuario (Streamlit)
│       ├── __init__.py
│       └── streamlit_app.py
├── models/ # Artefactos guardados (.pkl / .joblib)
├── requirements.txt # Dependencias con versiones fijas (ej. pandas==2.2.1)
└── README.md


## 2. Reglas de nombramiento para `builder`

- Los scripts en `src/` **siempre** deben tener un `__init__.py` para ser tratados como módulos.
- Los notebooks deben tener prefijo numérico (`01_`, `02_`) para indicar el orden de ejecución del pipeline.
- Los modelos guardados en `models/` deben incluir la versión y fecha: `model_early_v1_20260716.pkl`.