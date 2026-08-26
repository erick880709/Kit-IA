"""Pantalla de clasificación IA con inferencia real (HU-E4-01).

- Ejecuta el modelo serializado (TT-E4-01) con latencia < 3 s registrada.
- Muestra probabilidades por nivel, nivel sugerido por umbrales (no argmax),
  confianza y metadatos (versión/algoritmo/fecha).
- RNF-009: si el modelo no está disponible o excede el timeout → triaje manual
  con auditoría de indisponibilidad (RNO-007).
"""

from __future__ import annotations

import streamlit as st
from sqlalchemy import select

from app.domain.catalogos import NIVELES_TRIaje
from app.domain.entities import (
    EvaluacionClinica,
    EventoTriaje,
    MotivoConsulta,
    Paciente,
    SignosVitales,
)
from app.domain.exceptions import ValidationError
from app.infra.db import SessionLocal
from app.services import audit_service, triaje_service
from app.services.inference_service import inference_service

_DESCRIPCION_NIVELES = {
    "I": "Resucitación inmediata",
    "II": "Emergencia — atención ≤ 30 min",
    "III": "Urgencia — atención 2-4 h",
    "IV": "Urgencia menor — 4-12 h",
    "V": "No urgente — 12-24 h",
}


def _datos_para_inferencia(session, evento_id: str) -> dict:
    evento = session.get(EventoTriaje, evento_id)
    paciente = session.get(Paciente, evento.paciente_id)
    signos = session.scalar(
        select(SignosVitales).where(SignosVitales.evento_id == evento_id)
    )
    motivo = session.scalar(
        select(MotivoConsulta).where(MotivoConsulta.evento_id == evento_id)
    )
    evaluacion = session.scalar(
        select(EvaluacionClinica).where(EvaluacionClinica.evento_id == evento_id)
    )
    anio = paciente.fecha_nacimiento.year if paciente.fecha_nacimiento else 1990
    return {
        "temperatura": signos.temperatura,
        "frecuencia_cardiaca": signos.frecuencia_cardiaca,
        "frecuencia_respiratoria": signos.frecuencia_respiratoria,
        "saturacion_o2": signos.saturacion_o2,
        "presion_sistolica": signos.presion_sistolica,
        "presion_diastolica": signos.presion_diastolica,
        "peso": signos.peso,
        "talla": signos.talla,
        "episodios_previos_urgencias": paciente.episodios_previos_urgencias,
        "anio_nacimiento": anio,
        "sexo": paciente.sexo,
        "via_llegada": paciente.via_llegada,
        "regimen": paciente.regimen,
        "departamento": paciente.departamento,
        "glasgow": evaluacion.glasgow if evaluacion else 15,
        "escala_dolor": evaluacion.escala_dolor if evaluacion else 0,
        "motivo_codigo_cie10": motivo.codigo_cie10 if motivo else "",
        "motivo_texto": (motivo.texto_libre or motivo.descripcion_estructurada) if motivo else "",
    }


def _auditar_indisponibilidad(motivo: str) -> None:
    with SessionLocal() as session:
        audit_service.registrar(
            session,
            usuario_id=st.session_state.get("usuario_id"),
            accion="MODELO_INDISPONIBLE",  # RNO-007
            entidad="InferenceService",
            detalle=f"fallback triaje manual · {motivo}",
        )


def render() -> None:
    evento_id = st.session_state.get("evento_id")
    if not evento_id:
        st.warning("No hay evento de triaje en curso.")
        return
    st.title("Ejecutar clasificación IA")
    st.caption("El modelo sugiere un nivel a partir de signos vitales y motivo de consulta.")

    if "resultado_ia" not in st.session_state:
        st.session_state["resultado_ia"] = None

    if st.button("⚡ Ejecutar inferencia IA", type="primary", width="stretch"):
        with SessionLocal() as session:
            datos = _datos_para_inferencia(session, evento_id)
        with st.spinner("Ejecutando inferencia del modelo (presupuesto < 3 s)…"):
            resultado = inference_service.predecir(datos)
        st.session_state["resultado_ia"] = resultado
        if resultado["estado"] != "ok":
            _auditar_indisponibilidad(str(resultado.get("motivo")))
        st.rerun()

    resultado = st.session_state["resultado_ia"]

    if resultado is not None and resultado["estado"] == "ok":
        nivel = resultado["nivel_sugerido"]
        st.success(
            f"**Nivel sugerido por la IA: {nivel}** — {_DESCRIPCION_NIVELES[nivel]} "
            f"(confianza {resultado['confianza']:.0%})"
        )
        if resultado.get("regla_seguridad"):
            st.caption(
                "🛡️ Nivel ajustado por la red de contención clínica "
                "(Res. 5596/2015) — criterio de riesgo vital o de no urgencia."
            )
        filas = [
            {"Nivel": n, "Descripción": _DESCRIPCION_NIVELES[n],
             "Probabilidad": f"{p:.2%}"}
            for n, p in resultado["probabilidades"].items()
        ]
        st.dataframe(filas, hide_index=True, width="stretch")
        st.caption(
            f"Modelo `{resultado['version']}` · algoritmo `{resultado['algoritmo']}` · "
            f"entrenado {resultado['fecha_entrenamiento']} · "
            f"inferencia en **{resultado['tiempo_ms']} ms** (< 3 s) · "
            "sugerencia por umbrales calibrados (no argmax)."
        )
        if st.button("Registrar y continuar → Explicación SHAP"):
            with SessionLocal() as session:
                try:
                    inference_service.registrar_modelo(session)  # ENT-009
                    triaje_service.registrar_clasificacion_ia(
                        session,
                        evento_id=evento_id,
                        usuario_id=st.session_state.get("usuario_id"),
                        resultado=resultado,
                    )
                except ValidationError as exc:
                    st.error(
                        f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else "")
                    )
                    return
            st.session_state["pantalla"] = "explicacion_shap"
            st.rerun()

    elif resultado is not None:  # indisponible → fallback manual (RNF-009)
        motivo = resultado.get("motivo")
        descripcion_motivo = {
            "modelo_no_disponible": "sin artefacto o en reintento de carga",
            "timeout": "la inferencia excedió el presupuesto de 3 s",
            "error_inferencia": "error interno durante la inferencia",
        }.get(motivo, str(motivo or "desconocido"))
        detalle = resultado.get("detalle")
        st.error(
            "⚠ Modelo no disponible (sin artefacto, error o timeout > 3 s). "
            "El sistema pasa a triaje manual — la indisponibilidad quedó auditada."
        )
        st.caption(
            f"Detalle técnico: {descripcion_motivo}"
            + (f" · {detalle}" if detalle else "")
            + ". Puede reintentar «Ejecutar inferencia IA» antes de asignar "
            + "el nivel manual."
        )
        nivel = st.selectbox(
            "Nivel asignado manualmente por el profesional",
            NIVELES_TRIaje,
            index=2,
        )
        if st.button("Registrar triaje manual y continuar"):
            with SessionLocal() as session:
                try:
                    triaje_service.registrar_clasificacion_ia_simulada(
                        session,
                        evento_id=evento_id,
                        nivel_sugerido=nivel,
                        usuario_id=st.session_state.get("usuario_id"),
                    )
                except ValidationError as exc:
                    st.error(
                        f"{exc.mensaje}" + (f" · {exc.detalle}" if exc.detalle else "")
                    )
                    return
            st.session_state["pantalla"] = "explicacion_shap"
            st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
