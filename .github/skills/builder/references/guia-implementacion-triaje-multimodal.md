# Guía de Referencia para Implementación — Triaje Multimodal con IA

> **Propósito para `builder`:** Este documento define el estándar de código, las firmas de funciones y la estructura de artefactos que `builder` debe replicar al generar el proyecto. Actúa como el "módulo de referencia" para el pipeline de Machine Learning/IA.
>
> ⚠️ **IMPORTANTE:** Los archivos de paquete Python deben llamarse `__init__.py` (doble guion bajo). La representación ASCII del árbol de carpetas puede mostrar `init.py` por simplicidad visual, pero `builder` SIEMPRE debe generar `__init__.py`.

---

## 1. Estructura de Carpetas Objetivo (Scaffold esperado)

`builder` debe generar la siguiente estructura en la raíz del proyecto, imitando las convenciones de `references/guia-notebooks-python.md`:

proyecto-triaje-ml/
â”œâ”€â”€ data/
â”‚ â”œâ”€â”€ raw/ # Datos MIMIC-IV-ED y Hospital San Juan (nunca modificar)
â”‚ â”œâ”€â”€ interim/ # Datos despuÃ©s de limpieza/anonymizaciÃ³n
â”‚ â””â”€â”€ processed/ # Features listas para entrenar (X_train, y_train)
â”œâ”€â”€ notebooks/
â”‚ â”œâ”€â”€ 01_eda_exploracion.ipynb
â”‚ â”œâ”€â”€ 02_preprocesamiento_features.ipynb
â”‚ â”œâ”€â”€ 03_entrenamiento_baseline.ipynb
â”‚ â”œâ”€â”€ 04_entrenamiento_multimodal.ipynb # AquÃ­ se compara Early vs Late
â”‚ â””â”€â”€ 05_evaluacion_shap.ipynb
â”œâ”€â”€ src/
â”‚ â”œâ”€â”€ data/
â”‚ â”‚ â”œâ”€â”€ init.py
â”‚ â”‚ â”œâ”€â”€ ingesta.py # Carga desde CSV/PhysioNet
â”‚ â”‚ â”œâ”€â”€ limpieza.py # ImputaciÃ³n de nulos (KNN/Media) y outliers (IQR)
â”‚ â”‚ â””â”€â”€ anonimizacion.py # Enmascaramiento de datos sensibles (Ley 1581)
â”‚ â”œâ”€â”€ features/
â”‚ â”‚ â”œâ”€â”€ init.py
â”‚ â”‚ â””â”€â”€ feature_engineering.py # ColumnTransformer, escalado (StandardScaler), One-Hot
â”‚ â”œâ”€â”€ models/
â”‚ â”‚ â”œâ”€â”€ init.py
â”‚ â”‚ â”œâ”€â”€ train_baseline.py # RegresiÃ³n LogÃ­stica, Random Forest
â”‚ â”‚ â”œâ”€â”€ train_early_fusion.py # XGBoost sobre vector concatenado
â”‚ â”‚ â”œâ”€â”€ train_late_fusion.py # Stacking / Meta-clasificador
â”‚ â”‚ â””â”€â”€ predict.py # Carga de modelo y pipeline para inferencia
â”‚ â”œâ”€â”€ evaluation/
â”‚ â”‚ â”œâ”€â”€ init.py
â”‚ â”‚ â”œâ”€â”€ metrics.py # F1, Recall, AUC-ROC (Global y por clase)
â”‚ â”‚ â””â”€â”€ shap_explain.py # SHAP TreeExplainer + Top-5 features
â”‚ â””â”€â”€ serving/
â”‚ â”œâ”€â”€ init.py
â”‚ â””â”€â”€ streamlit_app.py # Demo interactiva con Streamlit
â”œâ”€â”€ models/ # Artefactos guardados (.pkl / .joblib)
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md


---

## 2. Convenciones de CÃ³digo (Naming & Estilo)

`builder` debe aplicar estas reglas estrictas al generar cada archivo:

| Elemento | ConvenciÃ³n | Ejemplo |
| :--- | :--- | :--- |
| **Archivos de scripts** | `snake_case` | `feature_engineering.py` |
| **Notebooks** | `NN_descripcion.ipynb` | `04_entrenamiento_multimodal.ipynb` |
| **Clases (para pipelines personalizados)** | `PascalCase` | `CustomBertVectorizer` |
| **Funciones pÃºblicas** | `snake_case` con verbo | `load_and_split_data()`, `evaluate_by_class()` |
| **Funciones privadas** | `_snake_case` con guion bajo | `_handle_missing_values()` |
| **Variables (DataFrames)** | `snake_case` | `train_df`, `X_test_structured` |
| **HiperparÃ¡metros** | `dict` con `lower_case` | `params = {'max_depth': 6, 'learning_rate': 0.01}` |
| **Semillas Aleatorias** | Fijadas en mÃ³dulo `config.py` o constante `RANDOM_STATE = 42` | |

---

## 3. PatrÃ³n de ImplementaciÃ³n para Features (Preprocesamiento)

`builder` debe replicar este patrÃ³n en `src/features/feature_engineering.py`:

```python
# src/features/feature_engineering.py
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def create_structured_pipeline(numeric_features, categorical_features):
    """
    Define el pipeline de preprocesamiento para variables estructuradas.
    Itera sobre los nombres de features para aplicarlos.
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor

def get_text_embedding(text_series, model_name="dccuchile/bert-base-spanish-wwm-uncased"):
    """
    Retorna embeddings de BERT para texto libre (Notas de enfermerÃ­a).
    PatrÃ³n esperado: Usar transformers con pooling (mean) para obtener vector de 768 dims.
    """
    # ImplementaciÃ³n estÃ¡ndar (builder debe copiar esta firma)
    from transformers import AutoTokenizer, AutoModel
    import torch
    # ... lÃ³gica de batch encoding ...
    return np.array(embeddings)
```

---

## 4. PatrÃ³n de ImplementaciÃ³n para Entrenamiento â€” Early Fusion

`builder` debe replicar este patrÃ³n en `src/models/train_early_fusion.py`:

```python
# src/models/train_early_fusion.py
import xgboost as xgb
from sklearn.metrics import f1_score, recall_score
import joblib
import numpy as np

def train_early_fusion(X_train_combined, y_train, params=None):
    """
    X_train_combined: numpy array concatenado de [estructuradas + embeddings BERT]
    y_train: array de etiquetas (0 a 4 correspondientes a niveles I-V)
    """
    if params is None:
        params = {
            'n_estimators': 200,
            'max_depth': 6,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'scale_pos_weight': compute_class_weights(y_train)  # Para manejo de desbalance
        }
    
    model = xgb.XGBClassifier(**params, eval_metric='mlogloss')
    model.fit(X_train_combined, y_train)
    return model

def compute_class_weights(y):
    """Calcula pesos inversamente proporcionales a la frecuencia para balancear clases."""
    from sklearn.utils.class_weight import compute_class_weight
    classes = np.unique(y)
    weights = compute_class_weight('balanced', classes=classes, y=y)
    return dict(zip(classes, weights))
```

---

## 5. PatrÃ³n de ImplementaciÃ³n para Entrenamiento â€” Late Fusion

`builder` debe replicar este patrÃ³n en `src/models/train_late_fusion.py`:

```python
# src/models/train_late_fusion.py
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb

def create_late_fusion_model(X_train_struct, X_train_text, y_train):
    """
    Crea un StackingClassifier que combina:
    - Submodelo A: XGBoost sobre datos estructurados.
    - Submodelo B: XGBoost sobre embeddings de texto.
    - Meta-clasificador: RegresiÃ³n LogÃ­stica para combinar probabilidades.
    """
    base_model_struct = xgb.XGBClassifier(random_state=42, n_estimators=100)
    base_model_text = xgb.XGBClassifier(random_state=42, n_estimators=100)
    
    meta_model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
    
    estimators = [
        ('xgb_struct', base_model_struct),
        ('xgb_text', base_model_text)
    ]
    
    stacking_model = StackingClassifier(
        estimators=estimators,
        final_estimator=meta_model,
        stack_method='predict_proba',
        cv=5
    )
    
    # NOTA: AquÃ­ se espera que X_train_struct y X_train_text estÃ©n preprocesados.
    # El stacking entrena los base models internamente.
    return stacking_model
```

---

## 6. PatrÃ³n de ImplementaciÃ³n para EvaluaciÃ³n â€” MÃ©tricas

`builder` debe replicar este patrÃ³n en `src/evaluation/metrics.py`:

```python
# src/evaluation/metrics.py
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def evaluate_model(y_true, y_pred, y_proba=None, target_names=['Nivel I', 'Nivel II', 'Nivel III', 'Nivel IV', 'Nivel V']):
    """
    Retorna un diccionario con mÃ©tricas globales y por clase.
    Prioriza el RECALL para las clases 0 (Nivel I) y 1 (Nivel II).
    """
    report = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)
    
    # ExtracciÃ³n especÃ­fica para prioridad clÃ­nica
    recall_nivel1 = report['Nivel I']['recall']
    recall_nivel2 = report['Nivel II']['recall']
    
    # MÃ©tricas globales
    f1_macro = report['macro avg']['f1-score']
    precision_macro = report['macro avg']['precision']
    recall_macro = report['macro avg']['recall']
    
    # AUC-ROC (One-vs-Rest) si y_proba estÃ¡ disponible
    auc_roc = None
    if y_proba is not None:
        auc_roc = roc_auc_score(y_true, y_proba, multi_class='ovr')
    
    # Matriz de confusiÃ³n (Ãºtil para reporte en Cap 5)
    conf_matrix = confusion_matrix(y_true, y_pred)
    
    results = {
        'f1_macro': f1_macro,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'recall_nivel_I': recall_nivel1,
        'recall_nivel_II': recall_nivel2,
        'auc_roc_ovr': auc_roc,
        'confusion_matrix': conf_matrix.tolist(),
        'classification_report': report
    }
    return results

def optimize_threshold_for_recall(model, X_val, y_val, class_id=0):
    """
    Ajusta el umbral de decisiÃ³n para maximizar el Recall en una clase especÃ­fica
    (ej. Nivel I), aunque baje la precisiÃ³n. Esta es la estrategia definida en el TFM.
    """
    from sklearn.metrics import recall_score, precision_score
    y_proba = model.predict_proba(X_val)[:, class_id]
    
    best_recall = 0
    best_threshold = 0.5
    # Grid search sobre thresholds posibles
    for threshold in np.arange(0.1, 0.9, 0.01):
        y_pred_adj = (y_proba >= threshold).astype(int)
        # Se asume que y_val es binario para esa clase o se usa one-vs-rest.
        # En prÃ¡ctica, se aplica sobre la predicciÃ³n de la clase especÃ­fica.
        # Para simplificar, se usa la probabilidad de pertenencia.
        recall = recall_score(y_val == class_id, y_pred_adj)
        if recall > best_recall:
            best_recall = recall
            best_threshold = threshold
            
    print(f"Optimal threshold for Class {class_id}: {best_threshold:.2f} (Recall: {best_recall:.4f})")
    return best_threshold
```

---

## 7. PatrÃ³n de ImplementaciÃ³n para Explicabilidad â€” SHAP

`builder` debe replicar este patrÃ³n en `src/evaluation/shap_explain.py`:

```python
# src/evaluation/shap_explain.py
import shap
import numpy as np
import pandas as pd

def get_shap_explanation(model, X_sample, feature_names):
    """
    Genera los valores SHAP para una instancia especÃ­fica.
    Retorna un DataFrame con el Top-5 de caracterÃ­sticas influyentes.
    """
    # Asumiendo modelo basado en Ã¡rboles (XGBoost) para usar TreeExplainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    # Para clasificaciÃ³n multiclase, shap_values es una lista. Tomamos la clase predicha.
    # simplificaciÃ³n: usamos la suma absoluta por feature para clasificaciÃ³n.
    if isinstance(shap_values, list):
        # Promedio del valor absoluto de SHAP a travÃ©s de las clases
        shap_values_agg = np.mean(np.abs(np.array(shap_values)), axis=0)
    else:
        shap_values_agg = np.abs(shap_values)
    
    # Crear DataFrame y ordenar por importancia
    shap_df = pd.DataFrame({
        'feature': feature_names,
        'shap_value': shap_values_agg[0]  # Asumiendo una sola muestra
    }).sort_values('shap_value', ascending=False)
    
    return shap_df.head(5)  # Top-5
```

---

## 8. PatrÃ³n de ImplementaciÃ³n para la Demo â€” Streamlit

`builder` debe replicar este patrÃ³n en `src/serving/streamlit_app.py`:

```python
# src/serving/streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from src.features.feature_engineering import create_structured_pipeline, get_text_embedding
from src.evaluation.shap_explain import get_shap_explanation

# ConfiguraciÃ³n de cachÃ© para cargar el modelo una sola vez
@st.cache_resource
def load_model_and_pipeline():
    model = joblib.load('models/best_model_multimodal.pkl')
    preprocessor = joblib.load('models/preprocessor.pkl')  # El ColumnTransformer entrenado
    return model, preprocessor

st.set_page_config(page_title="Sistema de Triaje IA", layout="wide")
st.title("ðŸ§  Apoyo al Triaje - ResoluciÃ³n 5596 de 2015")

# 1. Inputs del usuario (estructurados)
with st.form("triaje_form"):
    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Edad", min_value=0, max_value=120, value=45)
        spo2 = st.number_input("SaturaciÃ³n Oâ‚‚ (%)", min_value=50, max_value=100, value=96)
        fr = st.number_input("Frecuencia Respiratoria (rpm)", value=18)
    with col2:
        pa_sist = st.number_input("PresiÃ³n SistÃ³lica (mmHg)", value=120)
        fc = st.number_input("Frecuencia CardÃ­aca (lpm)", value=80)
        temp = st.number_input("Temperatura (Â°C)", value=36.5)
    
    motivo = st.text_area("Motivo de consulta (texto libre)", "Dolor en el pecho y dificultad para respirar")
    
    submitted = st.form_submit_button("Evaluar Nivel de Triaje")

# 2. LÃ³gica de PredicciÃ³n
if submitted:
    # Preprocesamiento estructurado
    structured_data = pd.DataFrame([[edad, spo2, fr, pa_sist, fc, temp]], 
                                   columns=['edad', 'spo2', 'fr', 'pa_sist', 'fc', 'temp'])
    
    model, preprocessor = load_model_and_pipeline()
    
    # Aplicar preprocesamiento (aquÃ­ el pipeline debe incluir el embedding de texto)
    # Nota: La integraciÃ³n real requiere unir structured + embedding.
    # SimulaciÃ³n para la demo:
    # X_final = np.concatenate([structured_processed, text_embedding], axis=1)
    
    # PredicciÃ³n
    prediction = model.predict(X_final)[0]
    proba = model.predict_proba(X_final)[0]
    
    levels = {0: "I - ResucitaciÃ³n", 1: "II - Emergencia", 2: "III - Urgencia", 
              3: "IV - Menor Urgencia", 4: "V - No Urgencia"}
    
    st.subheader(f"ðŸ”´ Nivel Predicho: **{levels[prediction]}**")
    st.write(f"Confianza: {max(proba)*100:.1f}%")
    
    # 3. Explicabilidad SHAP (Top-5)
    feature_names = ['Edad', 'SpO2', 'FR', 'PA Sist', 'FC', 'Temp', 'Embedding_BERT']
    shap_df = get_shap_explanation(model, X_final, feature_names)
    
    st.subheader("ðŸ“Š Factores que mÃ¡s influyeron en la decisiÃ³n")
    st.dataframe(shap_df, use_container_width=True)
```

---

## 9. MÃ³dulos complementarios

### 9.1 AnonimizaciÃ³n (`src/data/anonimizacion.py`)

Este mÃ³dulo ya estÃ¡ cubierto en la secciÃ³n 2 (Convenciones de CÃ³digo). PatrÃ³n resumido:

```python
# src/data/anonimizacion.py
import pandas as pd
import hashlib

def anonymize_patient_data(df, columns_to_hash=['nombre', 'documento', 'telefono']):
    """
    Aplica hash SHA256 a columnas sensibles para cumplir con la Ley 1581 de 2012.
    """
    def hash_column(series):
        return series.apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
    
    for col in columns_to_hash:
        if col in df.columns:
            df[col] = hash_column(df[col])
    return df
```

### 9.2 MÃ©tricas de evaluaciÃ³n mejoradas

La versiÃ³n completa de `evaluate_model` con type hints y manejo de errores estÃ¡ en la secciÃ³n 6. Usar esa versiÃ³n como referencia canÃ³nica.

---

> **Nota para `builder`:** Este documento define los patrones de cÃ³digo que deben replicarse
> al generar cada mÃ³dulo. Las firmas de funciones, convenciones de nombres y estructura de
> archivos son vinculantes. Los cuerpos de las funciones pueden adaptarse al contexto
> especÃ­fico de cada HU/TT, respetando las firmas y el comportamiento documentado.
