"""Pantalla de búsqueda de pacientes (HU-E2-02).

CA1: por documento exacto, nombre o apellidos parciales. CA2: paginado.
CA4: sin resultados → ofrecer crear paciente (HU-E2-01).
"""

from __future__ import annotations

import math

import streamlit as st

from app.infra.db import SessionLocal
from app.services import triaje_service

PAGE_SIZE = 10


def render() -> None:
    st.title("Buscar paciente")
    termino = st.text_input("Documento, nombre o apellidos", placeholder="52148903 o Gómez")
    page = st.number_input("Página", 1, 100, 1, key="busq_page")

    if termino:
        with SessionLocal() as session:
            items, total = triaje_service.buscar_pacientes(
                session, termino=termino, page=page, page_size=PAGE_SIZE
            )
        if not items:
            st.info("Sin resultados.")  # CA4
            if st.button("➕ Crear paciente nuevo (flujo HU-E2-01)"):
                st.session_state["pantalla"] = "registro_paciente"
                st.rerun()
            return
        st.caption(
            f"{total} resultado(s) — página {page} de "
            f"{max(1, math.ceil(total / PAGE_SIZE))}"
        )
        for paciente in items:  # CA2: nombre completo visible en cabecera
            with st.container(border=True):
                c1, c2 = st.columns([4, 2])
                c1.markdown(
                    f"**{paciente.nombres} {paciente.apellidos}**\n\n"
                    f"{paciente.tipo_documento} {paciente.numero_documento} · "
                    f"{paciente.ciudad}, {paciente.departamento}"
                )
                if c2.button("Seleccionar", key=f"sel_{paciente.id}"):
                    st.session_state["paciente_id"] = paciente.id
                    st.session_state["pantalla"] = "inicio"
                    st.rerun()
    else:
        st.info("Ingrese un documento, nombre o apellido para buscar.")

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
