"""Pantalla de validación profesional (HU-E2-08, mockup s-validacion).

CA1: exige ambos niveles. CA2: concordancia calculada por el sistema.
CA3: si difieren → motivo obligatorio. La decisión del profesional prevalece.
"""

from __future__ import annotations

import streamlit as st

from app.domain.catalogos import NIVELES_TRIaje
from app.domain.entities import EventoTriaje
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import triaje_service


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    if not evento_id:
        st.warning("No hay evento de triaje en curso.")
        return
    st.title("Validación de triaje")

    with SessionLocal() as session:
        evento = session.get(EventoTriaje, evento_id)

    if evento is None:
        st.error("Evento inexistente")
        return

    st.info(f"**Sugerencia de la IA:** nivel {evento.nivel_sugerido_ia or '—'}")
    # HU-E4-03 CA1: el nivel del profesional NUNCA viene preseleccionado —
    # se exige una elección consciente del clínico.
    opciones = ["— Seleccionar nivel —"] + NIVELES_TRIaje
    nivel = st.selectbox("Nivel asignado por el profesional (obligatorio)", opciones, index=0)
    motivo = None
    if nivel != "— Seleccionar nivel —" and nivel != evento.nivel_sugerido_ia:
        st.warning("Los niveles difieren — el motivo de discrepancia es obligatorio.")
        motivo = st.text_area(
            "Motivo de discrepancia (obligatorio)",
            placeholder="Dolor torácico con irradiación — riesgo vital, prioridad superior",
        )

    if st.button("Confirmar y continuar → Cierre"):
        if nivel == "— Seleccionar nivel —":
            st.error("Debe seleccionar un nivel de triaje antes de confirmar.")
            return
        with SessionLocal() as session:
            try:
                triaje_service.validar_nivel_profesional(
                    session,
                    evento_id=evento_id,
                    nivel_profesional=nivel,
                    usuario_id=st.session_state.get("usuario_id"),
                    motivo_discrepancia=motivo,
                )
            except ValidationError as exc:
                st.error(f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else ""))
                return
        st.session_state["pantalla"] = "cierre_evento"
        st.rerun()
