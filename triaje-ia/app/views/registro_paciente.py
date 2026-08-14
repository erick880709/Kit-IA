"""Pantalla de registro de paciente (HU-E2-01, mockup s-registro).

Flujo: formulario en 4 secciones → verificación de duplicados (CA2) →
si el paciente ya existe, se PRECARGAN sus datos personales y de contacto de
emergencia y la acción principal es continuar con el registro existente
(evita registros repetidos); si no existe, alta con validaciones (CA3) y
auditoría (CA4).
"""

from __future__ import annotations

import streamlit as st

from app.domain.catalogos import (
    CIUDADES_POR_DEPARTAMENTO,
    DEPARTAMENTOS_COLOMBIA,
    GRUPOS_SANGUINEOS,
    SEXO,
    VIA_LLEGADA,
)
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import paciente_service


def _precarga() -> dict:
    return st.session_state.get("precarga_paciente", {})


def _valor(campo: str, default=None):
    return _precarga().get(campo, default)


def _datos_desde_form() -> dict | None:
    p = _precarga()
    datos: dict = {}
    st.subheader("1 · Datos del paciente")
    c1, c2, c3 = st.columns(3)
    datos["tipo_documento"] = c1.selectbox(
        "Tipo documento", ["CC", "TI", "CE", "PA"],
        index=["CC", "TI", "CE", "PA"].index(p["tipo_documento"])
        if p.get("tipo_documento") in ["CC", "TI", "CE", "PA"] else 0,
    )
    datos["numero_documento"] = c2.text_input(
        "Número de documento", value=p.get("numero_documento", "")
    )
    datos["sexo"] = c3.selectbox(
        "Sexo", SEXO, index=SEXO.index(p["sexo"]) if p.get("sexo") in SEXO else 0
    )
    c1, c2 = st.columns(2)
    datos["nombres"] = c1.text_input("Nombres", value=p.get("nombres", ""))
    datos["apellidos"] = c2.text_input("Apellidos", value=p.get("apellidos", ""))
    c1, c2 = st.columns(2)
    datos["fecha_nacimiento"] = c1.date_input(
        "Fecha de nacimiento", value=p.get("fecha_nacimiento")
    )
    datos["via_llegada"] = c2.selectbox("Vía de llegada", VIA_LLEGADA)
    datos["episodios_previos_urgencias"] = st.number_input(
        "Episodios previos de urgencias",
        min_value=0,
        value=int(p.get("episodios_previos_urgencias", 0)),
        step=1,
    )

    st.subheader("2 · Contacto")
    c1, c2 = st.columns(2)
    datos["telefono"] = c1.text_input(
        "Teléfono", value=p.get("telefono", ""), placeholder="+57 300 123 4567"
    )
    datos["correo"] = c2.text_input(
        "Correo (opcional)", value=p.get("correo", "")
    )

    st.subheader("3 · Contacto de emergencia")
    c1, c2 = st.columns(2)
    datos["contacto_emergencia"] = c1.text_input(
        "Nombre del contacto", value=p.get("contacto_emergencia", "")
    )
    datos["numero_contacto_emergencia"] = c2.text_input(
        "Teléfono del contacto",
        value=p.get("numero_contacto_emergencia", ""),
        placeholder="+57 310 765 4321",
    )

    st.subheader("4 · Residencia y clínicos (opcionales)")
    c1, c2 = st.columns(2)
    departamento = c1.selectbox(
        "Departamento",
        DEPARTAMENTOS_COLOMBIA,
        index=DEPARTAMENTOS_COLOMBIA.index(p["departamento"])
        if p.get("departamento") in DEPARTAMENTOS_COLOMBIA else 0,
    )
    datos["departamento"] = departamento
    ciudades = CIUDADES_POR_DEPARTAMENTO.get(departamento, [])
    datos["ciudad"] = c2.selectbox(
        "Ciudad",
        ciudades if ciudades else [departamento],
        index=ciudades.index(p["ciudad"]) if p.get("ciudad") in ciudades else 0,
    )
    datos["direccion_residencia"] = st.text_input(
        "Dirección de residencia", value=p.get("direccion_residencia", "")
    )
    c1, c2, c3 = st.columns(3)
    regimen_opciones = ["", "Contributivo", "Subsidiado", "Especial", "No afiliado"]
    datos["regimen"] = c1.selectbox(
        "Régimen",
        regimen_opciones,
        index=regimen_opciones.index(p["regimen"])
        if p.get("regimen") in regimen_opciones else 0,
    )
    sangre_opciones = [""] + GRUPOS_SANGUINEOS
    datos["tipo_sangre"] = c2.selectbox(
        "Tipo de sangre",
        sangre_opciones,
        index=sangre_opciones.index(p["tipo_sangre"])
        if p.get("tipo_sangre") in sangre_opciones else 0,
    )
    datos["alergias"] = c3.text_input(
        "Alergias conocidas", value=p.get("alergias", "")
    )
    return datos


def render() -> None:
    st.title("Registro de paciente")
    usuario_id = st.session_state.get("usuario_id")

    if st.session_state.get("precarga_paciente"):
        st.success(
            "Datos personales y de contacto precargados del paciente existente — "
            "verifíquelos y continúe (o use «Continuar con el registro existente»)."
        )

    datos = _datos_desde_form()
    c1, c2 = st.columns(2)
    verificar = c1.button("Verificar duplicados", width="stretch")
    registrar_igual = c2.button(
        "Registrar como paciente nuevo", width="stretch"
    )

    if verificar or registrar_igual:
        with SessionLocal() as session:
            if verificar:
                duplicados = paciente_service.buscar_duplicados(
                    session,
                    tipo_documento=datos["tipo_documento"],
                    numero_documento=datos["numero_documento"],
                    nombres=datos["nombres"],
                    apellidos=datos["apellidos"],
                )
                if duplicados:
                    # Observación del negocio: si ya está registrado, precargar sus
                    # datos personales y de contacto, y priorizar continuar con él.
                    existente = duplicados[0]
                    st.session_state["precarga_paciente"] = {
                        "tipo_documento": existente.tipo_documento,
                        "numero_documento": existente.numero_documento,
                        "nombres": existente.nombres,
                        "apellidos": existente.apellidos,
                        "fecha_nacimiento": existente.fecha_nacimiento,
                        "sexo": existente.sexo,
                        "via_llegada": existente.via_llegada,
                        "episodios_previos_urgencias": (
                            existente.episodios_previos_urgencias
                        ),
                        "telefono": existente.telefono or "",
                        "correo": existente.correo or "",
                        "contacto_emergencia": existente.contacto_emergencia,
                        "numero_contacto_emergencia": existente.numero_contacto_emergencia,
                        "departamento": existente.departamento,
                        "ciudad": existente.ciudad,
                        "direccion_residencia": existente.direccion_residencia or "",
                        "regimen": existente.regimen or "",
                        "tipo_sangre": existente.tipo_sangre or "",
                        "alergias": existente.alergias or "",
                    }
                    st.session_state["duplicados_actuales"] = [
                        p.id for p in duplicados
                    ]
                    st.rerun()
                else:
                    st.success("Sin duplicados — proceda a registrar.")
                    registrar_igual = True

            if registrar_igual:
                try:
                    paciente = paciente_service.registrar_paciente(
                        session, usuario_id=usuario_id, datos=datos
                    )
                except ValidationError as exc:
                    st.error(f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else ""))
                    return
                st.session_state["paciente_id"] = paciente.id
                st.session_state.pop("precarga_paciente", None)
                st.session_state.pop("duplicados_actuales", None)
                st.success(
                    f"Paciente registrado: {paciente.nombres} {paciente.apellidos} "
                    f"({paciente.tipo_documento} {paciente.numero_documento})"
                )
                if st.button("Volver al inicio"):
                    st.session_state["pantalla"] = "inicio"
                    st.rerun()

    duplicados_ids = st.session_state.get("duplicados_actuales")
    if duplicados_ids:
        st.warning(
            "Este paciente ya está registrado. Acción recomendada: continuar con el "
            "registro existente para no duplicarlo."
        )
        if st.button("Continuar con el registro existente", type="primary"):
            st.session_state["paciente_id"] = duplicados_ids[0]
            st.session_state.pop("precarga_paciente", None)
            st.session_state.pop("duplicados_actuales", None)
            st.session_state["pantalla"] = "inicio"
            st.rerun()

    if st.button("← Volver sin registrar"):
        st.session_state.pop("precarga_paciente", None)
        st.session_state.pop("duplicados_actuales", None)
        st.session_state["pantalla"] = "inicio"
        st.rerun()
