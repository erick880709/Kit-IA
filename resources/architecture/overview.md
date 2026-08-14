# Arquitectura del Proyecto — TriajeIA

> Generado por `genesis` a partir de `resources/architecture/Documento_Arquitectura_TriajeIA.md` — `builder` debe actualizar este archivo incrementalmente, no regenerarlo desde cero.

## Lenguaje principal y versión

Python 3.12 (compatible 3.11)

## Tipo de proyecto

Aplicación fullstack **monolito modular Streamlit** (UI + lógica + inferencia en proceso) + pipeline de entrenamiento offline (notebooks/scripts, fuera del runtime).

## Estructura de paquetes / módulos

```
triaje-ia/
├── app/                 # Paquete principal de la aplicación Streamlit
│   ├── main.py          # Punto de entrada: bootstrap + router de pantallas
│   ├── views/           # Pantallas (builder: una por HU del flujo clínico)
│   ├── domain/          # Entidades y reglas puras (sin Streamlit)
│   ├── services/        # Inferencia, NLP, SHAP
│   └── infra/           # config.py, db.py, logging_config.py, errors.py, auth.py
├── scripts/             # healthcheck.py
├── tests/               # pytest
├── artifacts/models/    # Modelos versionados (joblib) + MLflow local
└── data/                # Datos demo sintéticos
```

## Patrón arquitectónico

**Layered / Services** dentro de un monolito modular: `views → services → domain → infra`.
La capa `domain` no depende de Streamlit ni de infraestructura (frontera de evolución a FastAPI/React — ADR-001).

## Convenciones de código

- Nombrado de archivos: `snake_case.py` (idiomático Python).
- Nombrado de clases / tipos: `PascalCase`; entidades ORM como declarative models sobre `Base` (`app/infra/db.py`).
- Inyección de dependencias: constructores + instancias de módulo (sin contenedor DI — patrón nativo del stack; documentado como supuesto de `genesis`).
- Manejo de errores: excepciones de dominio en `app/domain/exceptions.py` (`AppError`, `ValidationError`, `InferenceError`, `NotFoundError`), formato `{error:{codigo,mensaje,detalle}}` vía `app/infra/errors.py`.
- Validación de entrada: en el límite (formularios de `views`), nunca en el dominio.
- Logging: `logging` estándar con formato JSON (`app/infra/logging_config.py`).
- IDs: UUID v4 como texto (PK en SQLite).

## Módulo de referencia usado para scaffold

No aplica (greenfield) — este scaffold es la línea base que `builder` tomará como referencia viva desde su primera corrida.
