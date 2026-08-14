"""Pantalla de gestión de modelos (HU-E6-02, rol Administrador/Investigador).

Registro versionado (CA1), activación/rollback con un clic (CA2), historial
de activaciones auditado (CA3) y acceso restringido por RBAC (CA4).
"""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from app.domain.exceptions import ProhibidoError, ValidationError
from app.infra.db import SessionLocal
from app.services import authorization_service, inference_service, modelo_service


def _metricas_cortas(modelo) -> str:
    try:
        datos = json.loads(modelo.metricas_json or "{}")
        macro = datos.get("macro", {})
        return f"F1 {macro.get('f1', '—')} · AUC {datos.get('auc_roc_ovr', '—')}"
    except (json.JSONDecodeError, TypeError):
        return "—"


def render() -> None:
    rol = st.session_state.get("usuario_rol", "")
    try:
        authorization_service.verificar_acceso(rol, "gestion_modelos")
    except ProhibidoError as exc:
        st.error(exc.mensaje)
        return

    st.title("Gestión de modelos")
    st.caption(
        "Control de la versión en producción: activación, rollback y trazabilidad "
        "(RF-008, HU-E6-02)."
    )

    with SessionLocal() as session:
        modelos = modelo_service.listar(session)
        activo = modelo_service.modelo_activo(session)
        historial = modelo_service.historial_activaciones(session)

    if activo is not None:
        st.success(
            f"Modelo activo en producción: **{activo.version}** · {activo.algoritmo} "
            f"· {_metricas_cortas(activo)}"
        )
    else:
        st.warning("No hay modelo activo — la inferencia usará el artefacto más reciente.")

    if modelos:
        tabla = pd.DataFrame(
            [
                {
                    "Versión": m.version,
                    "Algoritmo": m.algoritmo,
                    "Entrenado": str(m.fecha_entrenamiento),
                    "Activo": "✅" if m.activo else "—",
                    "Métricas": _metricas_cortas(m),
                }
                for m in modelos
            ]
        )
        st.dataframe(tabla, hide_index=True, width="stretch")

    st.subheader("Acciones por versión")
    for modelo in modelos:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.write(
                f"**{modelo.version}** · {modelo.algoritmo} · "
                f"entrenado {modelo.fecha_entrenamiento}"
            )
        with c2:
            if not modelo.activo:
                if st.button(f"Activar {modelo.version}", key=f"act_{modelo.version}"):
                    with SessionLocal() as session:
                        try:
                            modelo_service.activar(
                                session, version=modelo.version,
                                usuario_id=st.session_state.get("usuario_id"),
                            )
                        except ValidationError as exc:
                            st.error(exc.mensaje)
                            return
                    inference_service.recargar()  # rollback efectivo de inmediato
                    st.rerun()
            else:
                if st.button(
                    f"Desactivar {modelo.version}", key=f"des_{modelo.version}"
                ):
                    with SessionLocal() as session:
                        try:
                            modelo_service.desactivar(
                                session, version=modelo.version,
                                usuario_id=st.session_state.get("usuario_id"),
                            )
                        except ValidationError as exc:
                            st.error(exc.mensaje)
                            return
                    inference_service.recargar()
                    st.rerun()

    st.divider()
    st.subheader("Historial de activaciones y registros (CA3)")
    if historial:
        filas = [
            {
                "Fecha (UTC)": h.creado_en.strftime("%Y-%m-%d %H:%M:%S"),
                "Usuario": h.usuario_id or "—",
                "Acción": h.accion,
                "Detalle": (h.detalle or "")[:100],
            }
            for h in historial
        ]
        st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    else:
        st.info("Sin registros todavía.")

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
