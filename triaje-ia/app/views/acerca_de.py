"""Pantalla «Acerca de» — información del proyecto (visible para todos los roles)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.domain.exceptions import ProhibidoError
from app.services import authorization_service
from app.version import version_app

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "manual"


def render() -> None:
    rol = st.session_state.get("usuario_rol", "")
    if not authorization_service.puede_acceder(rol, "acerca_de"):
        raise ProhibidoError("Acceso denegado a «Acerca de»", detalle=rol)

    st.title("ℹ️ Acerca de TriajeIA")
    st.divider()

    st.subheader("Proyecto")
    st.markdown(
        "**TriajeIA** es un sistema de **apoyo a la decisión de triaje en urgencias** "
        "con inteligencia artificial multimodal: sugiere el nivel de triaje "
        "(I–V, Resolución 5596/2015) a partir de signos vitales, motivo de consulta "
        "y texto libre, con explicación SHAP y validación profesional obligatoria.\n\n"
        "Es el **Trabajo de Fin de Máster (TFM)** del equipo, desarrollado como "
        "proyecto final de maestría."
    )
    st.caption(f"Versión desplegada: `{version_app()}`")

    st.subheader("Autores")
    st.markdown(
        "- **Medina Betancur, Diego Andrés**\n"
        "- **Rivera Villanueva, Leyniker**\n"
        "- **Soto Díaz, Erick Duván**"
    )

    st.subheader("Alcance y límites")
    st.markdown(
        "- **Sistema de apoyo a la decisión** — no autónomo: el profesional valida y decide.\n"
        "- **No es un dispositivo médico**: demo académica con datos sintéticos.\n"
        "- **Modelo de clasificación**: fusión tardía XGBoost (estructurado) + Regresión "
        "Logística (texto), umbrales calibrados por clase, SHAP top-5.\n"
        "- **Stack**: Python 3.11 · Streamlit · SQLAlchemy/SQLite · scikit-learn · XGBoost · SHAP."
    )

    st.subheader("Propiedad y uso")
    st.markdown(
        "Proyecto académico sin fines comerciales. El uso de los datos sigue el "
        "protocolo de anonimización del proyecto (Ley 1581/2012 de protección de "
        "datos personales)."
    )

    imagen = ASSETS_DIR / "flujo_general.png"
    if imagen.exists():
        st.image(str(imagen), caption="Vista general del sistema", width="stretch")

    st.divider()
    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
