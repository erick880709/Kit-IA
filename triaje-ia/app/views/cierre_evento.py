"""Pantalla de cierre del evento (HU-E2-08, mockup s-cierre).

Exige clasificación IA + validación profesional (CA1), concordancia calculada
(CA2), motivo obligatorio si difieren (CA3) y persistencia dual permanente (CA4).
Ofrece el registro descargable en PDF.
"""

from __future__ import annotations

import streamlit as st
from sqlalchemy import select

from app.domain.entities import EventoTriaje, MotivoConsulta, Paciente, SignosVitales
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import audit_service, registro_pdf, triaje_service


def _auditar_generacion_pdf() -> None:
    """HU-E5-02 CA4: la generación del registro queda auditada."""
    with SessionLocal() as session:
        audit_service.registrar(
            session,
            usuario_id=st.session_state.get("usuario_id"),
            accion="GENERAR_REGISTRO_PDF",
            entidad="EventoTriaje",
            detalle=f"registro normativo descargable · {st.session_state.get('evento_id')}",
            evento_id=st.session_state.get("evento_id"),
        )


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    if not evento_id:
        st.warning("No hay evento de triaje en curso.")
        return
    st.title("Cierre del evento de triaje")

    with SessionLocal() as session:
        evento = session.get(EventoTriaje, evento_id)
        paciente = session.get(Paciente, evento.paciente_id) if evento else None
        signos = session.scalar(
            select(SignosVitales).where(SignosVitales.evento_id == evento_id)
        )
        motivo = session.scalar(
            select(MotivoConsulta).where(MotivoConsulta.evento_id == evento_id)
        )
        pdf_bytes = None
        if evento and evento.cierre:
            pdf_bytes = registro_pdf.generar_pdf_registro(
                evento, paciente, signos, motivo
            )

    if evento is None:
        st.error("Evento inexistente")
        return

    if evento.estado == "Cerrado":
        st.success("Evento cerrado — ambos niveles persistidos permanentemente.")
        st.write(
            f"**IA:** {evento.nivel_sugerido_ia} · **Profesional:** "
            f"{evento.nivel_asignado_profesional} · **Concordancia:** "
            f"{'Sí' if evento.concordancia else 'No'}"
        )
        if evento.motivo_discrepancia:
            st.write(f"**Motivo discrepancia:** {evento.motivo_discrepancia}")
        if pdf_bytes:
            st.download_button(
                "Registro de triaje descargable (PDF)",
                data=pdf_bytes,
                file_name=f"triaje_{evento_id[:8]}.pdf",  # sin documento (RNF-006)
                mime="application/pdf",
                on_click=_auditar_generacion_pdf,  # HU-E5-02 CA4
            )
        if st.button("Finalizar y volver al inicio"):
            for clave in ("evento_id",):
                st.session_state.pop(clave, None)
            st.session_state["pantalla"] = "inicio"
            st.rerun()
        return

    st.info(
        f"Resumen previo al cierre — IA: {evento.nivel_sugerido_ia} · "
        f"Profesional: {evento.nivel_asignado_profesional} · "
        f"Concordancia: {'Sí' if evento.concordancia else 'No'}"
    )
    if st.button("Confirmar cierre del evento"):
        with SessionLocal() as session:
            try:
                triaje_service.cerrar_evento(
                    session,
                    evento_id=evento_id,
                    usuario_id=st.session_state.get("usuario_id"),
                )
            except ValidationError as exc:
                st.error(f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else ""))
                return
        st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
