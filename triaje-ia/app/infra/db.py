"""Conexión a SQLite vía SQLAlchemy 2.0 (ADR-002).

Sin modelos de negocio todavía — `builder` agrega las entidades de
`resources/design/data-model.md` como declarative models sobre `Base`.
"""

from __future__ import annotations

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.domain.base import Base
from app.infra.config import settings

# Columnas agregadas después del arranque inicial (HU-E1-03): SQLite + create_all
# no altera tablas existentes, por eso se aplica esta migración ligera.
_COLUMNAS_NUEVAS: dict[str, list[tuple[str, str]]] = {
    "usuarios": [
        ("token_recuperacion", "VARCHAR(120)"),
        ("token_expira", "DATETIME"),
    ],
    "eventos_triaje": [
        ("algoritmo_modelo", "VARCHAR(60)"),
        ("fecha_inferencia", "DATETIME"),
        ("tiempo_inferencia_ms", "FLOAT"),
        ("confianza_ia", "FLOAT"),
        ("explicacion_shap", "TEXT"),
    ],
    "auditoria": [
        ("evento_id", "VARCHAR(36)"),
    ],
    "pacientes": [
        ("eps", "VARCHAR(80)"),
    ],
}


def _aplicar_migracion_ligera() -> None:
    """Agrega columnas nuevas a tablas existentes si faltan (idempotente)."""
    inspector = inspect(engine)
    for tabla, columnas in _COLUMNAS_NUEVAS.items():
        if not inspector.has_table(tabla):
            continue
        existentes = {c["name"] for c in inspector.get_columns(tabla)}
        for nombre, tipo in columnas:
            if nombre not in existentes:
                with engine.begin() as conn:
                    conn.execute(text(f"ALTER TABLE {tabla} ADD COLUMN {nombre} {tipo}"))

engine = create_engine(
    f"sqlite:///{settings.db_path}",
    connect_args={"check_same_thread": False},  # Streamlit reutiliza hilos por sesión
    echo=False,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Crea las tablas pendientes y aplica la migración ligera de columnas."""
    Base.metadata.create_all(bind=engine)
    _aplicar_migracion_ligera()


def get_session() -> Session:
    """Devuelve una sesión nueva. Cerrar con `with get_session() as s:` o try/finally."""
    return SessionLocal()


def db_ok() -> bool:
    """Chequeo de salud de la conexión (usado por healthcheck)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
