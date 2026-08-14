"""Pantalla de signos vitales (HU-E2-04, mockup s-signos).

CA1: 8 signos con IMC automático. CA2: valores fuera de rango → alerta y
confirmación antes de continuar. CA3: SpO₂, FR, temperatura y PA sistólica
prioritarias. CA4: estado de alerta visible.
"""

from __future__ import annotations

import streamlit as st

from app.domain.catalogos import RANGOS_SIGNOS
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import triaje_service


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    if not evento_id:
        st.warning("No hay un evento de triaje en curso.")
        return
    st.title("Captura de signos vitales")
    st.caption("(*) Signos prioritarios para el modelo")

    _FLOAT_CAMPOS = {"temperatura", "peso", "talla"}

    def _input(campo: str, col) -> float | int:
        minimo, maximo, unidad, prioritaria = RANGOS_SIGNOS[campo]
        label = f"{campo.replace('_', ' ').title()} ({unidad}){' *' if prioritaria else ''}"
        # Límites amplios (no los fisiológicos): así un valor fuera de rango
        # puede capturarse y dispara el flujo de confirmación de CA2.
        if campo in _FLOAT_CAMPOS:
            return col.number_input(
                label, min_value=0.0, max_value=1000.0,
                step=0.1, key=f"sv2_{campo}",
            )
        return col.number_input(
            label, min_value=0, max_value=500,
            step=1, key=f"sv2_{campo}",
        )

    c1, c2, c3, c4 = st.columns(4)
    datos = {
        "temperatura": _input("temperatura", c1),
        "frecuencia_cardiaca": _input("frecuencia_cardiaca", c2),
        "frecuencia_respiratoria": _input("frecuencia_respiratoria", c3),
        "saturacion_o2": _input("saturacion_o2", c4),
        "presion_sistolica": _input("presion_sistolica", c1),
        "presion_diastolica": _input("presion_diastolica", c2),
        "peso": _input("peso", c3),
        "talla": _input("talla", c4),
    }

    if datos["talla"] > 0:
        imc = round(datos["peso"] / (datos["talla"] ** 2), 1)
        st.metric("IMC (calculado automáticamente)", f"{imc} kg/m²")

    fuera = [
        campo for campo, valor in datos.items()
        if not (RANGOS_SIGNOS[campo][0] <= valor <= RANGOS_SIGNOS[campo][1])
    ]
    if fuera:  # CA2/CA4: alerta visible + confirmación
        st.warning(
            "Valores fuera de rango fisiológico: " + ", ".join(f.replace("_", " ") for f in fuera)
        )
        confirmado = st.checkbox(
            "Confirmo que los valores son correctos y deseo continuar", key="sv_confirmar"
        )
    else:
        confirmado = True

    if st.button("Continuar → Evaluación clínica", disabled=not confirmado):
        with SessionLocal() as session:
            try:
                triaje_service.registrar_signos(
                    session,
                    evento_id=evento_id,
                    usuario_id=st.session_state.get("usuario_id"),
                    datos=datos,
                    confirmar_fuera_rango=bool(fuera),  # CA2: confirmación explícita
                )
            except ValidationError as exc:
                st.error(f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else ""))
                return
        st.session_state["pantalla"] = "evaluacion_clinica"
        st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
