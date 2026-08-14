---
id: TT-E1-01
type: Tarea Técnica
epic: E1 - Fundación del Sistema
priority: Highest
points: 5
---

# TT-E1-01: Inicializar proyecto con stack Python + Streamlit

## Descripción
Crear la base del proyecto de la demo: entorno Python 3.12, virtualenv, `requirements.txt`, estructura de carpetas y arranque con Streamlit (decisión cerrada por refinador, 2026-08-13).

## Criterios de Done
- [ ] Proyecto inicializa con un solo comando (`streamlit run app.py`).
- [ ] `requirements.txt` fija: streamlit, pandas, scikit-learn, xgboost, tensorflow (opcional CPU), shap, streamlit-shap, sqlite3 (stdlib).
- [ ] Estructura de carpetas definida (app/, services/, data/, ui/, models/, tests/).
- [ ] README con instrucciones de arranque en 3 pasos (RT-007).

## Dependencias
Ninguna (primera tarea).
