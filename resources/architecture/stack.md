# Stack Tecnológico — TriajeIA

> Generado por `genesis` a partir de `Documento_Arquitectura_TriajeIA.md` (RT-001, RT-007) — actualizar incrementalmente.

## Lenguaje

Python 3.12

## Backend / Aplicación

| Rol | Tecnología | Versión |
|---|---|---|
| Framework UI + app | Streamlit | ≥ 1.57 |
| ORM / acceso a datos | SQLAlchemy | ≥ 2.0 |
| Validación | Formularios Streamlit + rangos clínicos (reglas en `domain`) | — |
| Autenticación | Local: bcrypt + token simulado (demo) | bcrypt ≥ 4.0 |
| Migraciones | Sin migraciones en scaffold (SQLite + `create_all`); Alembic si se migra a PostgreSQL | — |
| Testing | pytest | ≥ 8.0 |
| Lint / formato | ruff | ≥ 0.5 |
| Configuración | python-dotenv (.env) | ≥ 1.0 |

## Frontend (si aplica)

Integrado en Streamlit (mismo contenedor). Design system TriajeIA:
`.github/resources/diseno/design-system.md` (paleta cyan-salud, Fira Sans/Code).

## Machine Learning (pipeline offline — fuera del runtime de la demo)

| Rol | Tecnología |
|---|---|
| Datos / features | pandas, numpy, scikit-learn |
| Modelos estructurados | scikit-learn, XGBoost |
| Modelo de texto | transformers (BERT clínico español) |
| Explicabilidad | SHAP |
| Tracking / versionado | MLflow (local) + convención `data-v<fecha>` |
| Hiperparámetros | Optuna |

## Base de datos

SQLite 3 (local, mono-usuario) vía SQLAlchemy ORM — ADR-002. Evolución prevista: PostgreSQL.

## Infraestructura y despliegue (si es visible en el código)

Ejecución local: `streamlit run app/main.py`. Sin Docker en el alcance demo.
Opcional: Streamlit Community Cloud ($0, solo datos sintéticos).
