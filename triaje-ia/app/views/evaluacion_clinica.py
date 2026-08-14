"""Pantalla de evaluación clínica (HU-E2-05, mockup s-evaluacion).

CA1: motivo en doble captura (catálogo CIE-10 + texto libre).
CA2: dolor 0-10, Glasgow, conciencia con catálogos.
CA3: antecedentes por autorreporte (MockHCE) precargados si existen.
CA4: texto libre vacío no bloquea.
"""

from __future__ import annotations

import streamlit as st

from app.domain.catalogos import CATALOGO_MOTIVOS, NIVEL_CONCIENCIA
from app.domain.entities import Paciente
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import history_connector, paciente_service, triaje_service


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    paciente_id = st.session_state.get("paciente_id")
    if not evento_id or not paciente_id:
        st.warning("No hay evento de triaje en curso.")
        return
    st.title("Evaluación clínica")

    with SessionLocal() as session:
        paciente = session.get(Paciente, paciente_id)
        previos = (
            history_connector.history_connector.obtener_antecedentes(session, paciente)
            if paciente else None
        )

    opciones = [f"{codigo} — {desc}" for codigo, desc in CATALOGO_MOTIVOS]
    motivo = st.selectbox("Motivo estructurado (CIE-10)", opciones)
    codigo = motivo.split(" — ")[0]
    texto_libre = st.text_area(
        "Texto libre (opcional — alimenta el NLP)",
        placeholder='"Dolor opresivo retroesternal desde hace 2 horas…"',
    )

    c1, c2, c3 = st.columns(3)
    dolor = c1.slider("Escala de dolor (0-10)", 0, 10, 0)
    glasgow = c2.number_input("Glasgow (3-15)", 3, 15, 15)
    conciencia = c3.selectbox("Nivel de conciencia", NIVEL_CONCIENCIA)

    st.subheader("Antecedentes (autorreporte — sin integración HCE)")
    c1, c2, c3, c4 = st.columns(4)
    ant = {
        "diabetes": c1.checkbox("Diabetes", value=bool(previos and previos["diabetes"])),
        "hta": c2.checkbox("HTA", value=bool(previos and previos["hta"])),
        "erc": c3.checkbox("ERC", value=bool(previos and previos["erc"])),
        "embarazo": c4.checkbox("Embarazo", value=bool(previos and previos["embarazo"])),
        "cancer": c1.checkbox("Cáncer", value=bool(previos and previos["cancer"])),
        "cardiopatias": c2.checkbox(
            "Cardiopatías", value=bool(previos and previos["cardiopatias"])
        ),
        "epoc": c3.checkbox("EPOC", value=bool(previos and previos["epoc"])),
    }
    ant["cirugias"] = st.text_input(
        "Cirugías previas", value=(previos or {}).get("cirugias") or ""
    )
    ant["medicacion"] = st.text_input(
        "Medicación habitual", value=(previos or {}).get("medicacion") or ""
    )
    alergias = st.text_input(
        "Alergias conocidas", value=(paciente.alergias if paciente else "") or ""
    )
    observaciones = st.text_area("Observaciones (opcional)")

    if st.button("Continuar → Clasificación IA"):
        with SessionLocal() as session:
            try:
                triaje_service.registrar_evaluacion(
                    session,
                    evento_id=evento_id,
                    usuario_id=st.session_state.get("usuario_id"),
                    datos={
                        "codigo_cie10": codigo,
                        "descripcion_estructurada": motivo,
                        "texto_libre": texto_libre,
                        "escala_dolor": dolor,
                        "glasgow": glasgow,
                        "nivel_conciencia": conciencia,
                        "observaciones": observaciones,
                    },
                )
                triaje_service.guardar_antecedentes(
                    session,
                    paciente_id=paciente_id,
                    antecedentes=ant,
                    usuario_id=st.session_state.get("usuario_id"),
                )
                if alergias.strip() and paciente:
                    paciente_service.actualizar_alergias(
                        session,
                        paciente_id=paciente_id,
                        alergias=alergias,
                        usuario_id=st.session_state.get("usuario_id"),
                    )
            except ValidationError as exc:
                st.error(f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else ""))
                return
        st.session_state["pantalla"] = "clasificacion_ia"
        st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
