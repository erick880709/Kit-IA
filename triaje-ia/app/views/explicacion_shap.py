"""Pantalla de explicación SHAP (HU-E4-02).

- Top 5 variables con lenguaje clínico y dirección del efecto (+/−).
- Gráfico estilo waterfall con pesos relativos.
- Sugerencia clínica si signos prioritarios (SpO₂ / FR) empujan la severidad.
- Exportación del detalle en JSON.
"""

from __future__ import annotations

import json

import streamlit as st

from app.domain.entities import EventoTriaje
from app.infra.db import SessionLocal

_SIGNOS_PRIORITARIOS = {"saturacion_o2", "frecuencia_respiratoria"}


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    if not evento_id:
        st.warning("No hay evento de triaje en curso.")
        return
    st.title("Explicación de la clasificación IA")

    with SessionLocal() as session:
        evento = session.get(EventoTriaje, evento_id)

    if evento is None:
        st.error("Evento inexistente")
        return
    if not evento.explicacion_shap:
        st.info(
            "Este evento no tiene explicación SHAP (inferencia manual o modelo "
            "sin explicabilidad)."
        )
    else:
        top = json.loads(evento.explicacion_shap)
        st.subheader("Variables que más influyeron en la clasificación")
        st.caption(
            "Verde: la variable empuja hacia mayor severidad · "
            "Rojo: empuja hacia menor severidad."
        )
        max_peso = max((item["peso_absoluto"] for item in top), default=1.0) or 1.0
        for item in top:
            impacto = item["impacto"]
            signo = "+" if impacto >= 0 else "−"
            color = "#059669" if impacto >= 0 else "#DC2626"
            st.markdown(
                f"**{item['clinico']}** ({item['feature']}) — impacto "
                f"<span style='color:{color};font-weight:700'>{signo}{abs(impacto):.4f}</span>",
                unsafe_allow_html=True,
            )
            st.progress(
                min(float(item["peso_absoluto"]) / max_peso, 1.0),
                text=f"peso relativo {item['peso_absoluto']:.4f}",
            )

        prioritarios = [
            item for item in top if item["feature"] in _SIGNOS_PRIORITARIOS
            and item["impacto"] >= 0
        ]
        if prioritarios:
            st.warning(
                "⚠ Signos prioritarios del Manchester Triage System con efecto "
                "hacia mayor severidad — validar clínicamente antes de confirmar."
            )

        payload = json.dumps(
            {
                "evento_id": evento_id,
                "nivel_sugerido": evento.nivel_sugerido_ia,
                "version_modelo": evento.version_modelo,
                "explicacion": top,
            },
            ensure_ascii=False,
            indent=2,
        )
        st.download_button(
            "⬇ Exportar explicación (JSON)",
            data=payload,
            file_name=f"shap_{evento_id}.json",
            mime="application/json",
        )

    st.divider()
    if st.button("Continuar → Validación profesional", type="primary"):
        st.session_state["pantalla"] = "validacion_triaje"
        st.rerun()
    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
