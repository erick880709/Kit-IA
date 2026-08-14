---
id: TT-E1-01
type: Tarea Técnica
epic: 001-fundacion-del-sistema
priority: Alta
points: 5
---

# TT-E1-01: Inicializar Proyecto con Stack Python + Streamlit

## Descripción
Crear la estructura base del proyecto: entorno virtual, dependencias, script de arranque, y decisión de stack de UI.

[SUPUESTO] Se asume **Streamlit** como framework para la demo (recomendado en `04-ESPECIFICACION-APLICACION-DEMO.md` y `05-PENDIENTES-PARA-DIRECTORA.md`). Si la directora decide Flask, esta tarea debe re-planificarse.

## Criterios de Done
- [ ] Entorno virtual Python 3.10+ creado y documentado
- [ ] `requirements.txt` con: streamlit, pandas, numpy, scikit-learn, xgboost, shap, transformers, torch, sqlite3, bcrypt, plotly
- [ ] `app.py` principal con `streamlit run app.py` funcional (pantalla "Hola Mundo" con título del proyecto)
- [ ] Estructura de carpetas creada: `app/`, `models/`, `data/`, `utils/`, `tests/`
- [ ] `README.md` con instrucciones de instalación y arranque en ≤ 3 pasos
- [ ] Archivo `.gitignore` configurado (venv, __pycache__, .env, *.db, modelos serializados)

## Dependencias
Ninguna (es la primera tarea del proyecto)

## Subtareas
- [ ] Crear entorno virtual e instalar dependencias
- [ ] Configurar `requirements.txt`
- [ ] Crear `app.py` con estructura base Streamlit (sidebar, páginas)
- [ ] Crear estructura de carpetas del proyecto
- [ ] Redactar `README.md`
