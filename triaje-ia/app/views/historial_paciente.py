"""Pantalla de historial de triajes (HU-E2-03) y reclasificación (HU-E2-07).

CA1 (E2-03): listado cronológico con nivel, fecha y profesional.
CA2 (E2-03): acceso restringido por rol (validado en el router).
CA1-4 (E2-07): reclasificación solo tras cierre, motivo obligatorio, evento
separado con trazabilidad completa.
"""

from __future__ import annotations

import streamlit as st

from app.domain.catalogos import NIVELES_TRIaje
from app.domain.entities import Paciente
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import triaje_service


def render() -> None:
    paciente_id = st.session_state.get("paciente_id")
    if not paciente_id:
        st.warning("Seleccione un paciente para ver su historial.")
        return

    with SessionLocal() as session:
        paciente = session.get(Paciente, paciente_id)
        eventos = triaje_service.historial_eventos(session, paciente_id=paciente_id)

    st.title(f"Historial de triajes — {paciente.nombres} {paciente.apellidos}" if paciente
             else "Historial de triajes")
    if not eventos:
        st.info("Este paciente aún no tiene eventos de triaje.")
        return

    for evento in eventos:  # CA1: cronológico descendente
        with st.container(border=True):
            c1, c2 = st.columns([4, 2])
            estado = evento.estado
            c1.markdown(
                f"**{evento.inicio.strftime('%d/%m/%Y %H:%M')}** · estado `{estado}` · "
                f"IA {evento.nivel_sugerido_ia or '—'} · Profesional "
                f"{evento.nivel_asignado_profesional or '—'} · "
                f"Concordancia {'Sí' if evento.concordancia else 'No'}"
            )
            if evento.motivo_cierre:
                c1.caption(
                    "🔒 Cierre automático — menor de 16 años (sin recomendación IA; "
                    "nivel de atención a cargo del profesional)."
                )
            if evento.motivo_reclasificacion:
                c1.caption(f"Reclasificación: {evento.motivo_reclasificacion}")
            if (
                evento.estado == "Cerrado"
                and not evento.motivo_cierre
                and c2.button("Reclasificar", key=f"recl_{evento.id}")
            ):
                st.session_state["evento_reclasificar"] = evento.id
                st.rerun()

    # Formulario de reclasificación (HU-E2-07)
    if "evento_reclasificar" in st.session_state:
        original_id = st.session_state["evento_reclasificar"]
        with st.expander("Reclasificar paciente", expanded=True):
            nuevo_nivel = st.selectbox("Nuevo nivel de triaje", NIVELES_TRIaje, index=2)
            motivo = st.text_area(
                "Motivo de reclasificación (obligatorio)",
                placeholder="Cambió el estado clínico: …",
            )
            if st.button("Registrar reclasificación"):
                with SessionLocal() as session:
                    try:
                        triaje_service.reclasificar(
                            session,
                            evento_original_id=original_id,
                            nuevo_nivel=nuevo_nivel,
                            motivo=motivo,
                            usuario_id=st.session_state.get("usuario_id"),
                        )
                    except ValidationError as exc:
                        st.error(
                            f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else "")
                        )
                        return
                st.session_state.pop("evento_reclasificar", None)
                st.success("Reclasificación registrada como evento separado (auditada).")
                st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
