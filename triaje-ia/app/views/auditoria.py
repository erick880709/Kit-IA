"""Pantalla de auditoría y trazabilidad (HU-E5-01, rol Auditor/Administrador).

CA1: filtros por fecha, usuario, entidad, acción y evento de triaje.
CA2: consulta paginada (< 1 s). CA3: exportación CSV/Excel/PDF.
CA4: acceso restringido por RBAC (validado en el router y aquí).
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from app.domain.exceptions import ProhibidoError
from app.infra.db import SessionLocal
from app.services import audit_service, authorization_service

_PAGE_SIZE = 50


def _filtros_texto(desde, hasta, usuario, entidad, accion, evento) -> str:
    partes = []
    if desde:
        partes.append(f"desde {desde:%Y-%m-%d}")
    if hasta:
        partes.append(f"hasta {hasta:%Y-%m-%d}")
    for etiqueta, valor in (
        ("usuario", usuario), ("entidad", entidad), ("accion", accion), ("evento", evento)
    ):
        if valor:
            partes.append(f"{etiqueta}={valor}")
    return ", ".join(partes)


def render() -> None:
    rol = st.session_state.get("usuario_rol", "")
    try:
        authorization_service.verificar_acceso(rol, "auditoria")
    except ProhibidoError as exc:
        st.error(exc.mensaje)
        return

    st.title("Auditoría y trazabilidad")
    st.caption("Registro append-only de acciones del sistema (RF-012) · rol Auditor.")

    hoy = datetime.now().replace(tzinfo=None)
    c1, c2, c3 = st.columns(3)
    with c1:
        desde = st.date_input("Desde", value=hoy - timedelta(days=7))
        usuario = st.text_input("Usuario (id)")
    with c2:
        hasta = st.date_input("Hasta", value=hoy)
        entidad = st.text_input("Entidad")
    with c3:
        accion = st.text_input("Acción")
        evento = st.text_input("Evento de triaje (id)")
    pagina = st.number_input("Página", min_value=1, value=1, step=1)

    desde_dt = datetime.combine(desde, datetime.min.time())
    hasta_dt = datetime.combine(hasta, datetime.max.time())

    with SessionLocal() as session:
        filas, total = audit_service.consultar(
            session,
            desde=desde_dt,
            hasta=hasta_dt,
            usuario_id=(usuario.strip() or None),
            entidad=(entidad.strip() or None),
            accion=(accion.strip() or None),
            evento_id=(evento.strip() or None),
            page=pagina,
            page_size=_PAGE_SIZE,
        )
        # Exportación sobre el conjunto filtrado COMPLETO (no solo la página).
        filas_export, total_export = audit_service.consultar(
            session,
            desde=desde_dt,
            hasta=hasta_dt,
            usuario_id=(usuario.strip() or None),
            entidad=(entidad.strip() or None),
            accion=(accion.strip() or None),
            evento_id=(evento.strip() or None),
            page=1,
            page_size=10_000,
        )

    st.info(f"{total} registro(s) · página {pagina} de {max(1, -(-total // _PAGE_SIZE))}")
    if filas:
        tabla = pd.DataFrame(
            [
                {
                    "Fecha (UTC)": f.creado_en.strftime("%Y-%m-%d %H:%M:%S"),
                    "Usuario": f.usuario_id or "—",
                    "Acción": f.accion,
                    "Entidad": f.entidad,
                    "Evento": f.evento_id or "—",
                    "Detalle": (f.detalle or "")[:120],
                }
                for f in filas
            ]
        )
        st.dataframe(tabla, hide_index=True, width="stretch")

    st.divider()
    st.subheader("Exportar resultados (CA3)")
    st.caption(f"Exporta el conjunto filtrado completo: {total_export} registro(s).")
    filtros = _filtros_texto(desde_dt, hasta_dt, usuario, entidad, accion, evento)
    col1, col2, col3 = st.columns(3)
    with col1:
        bytes_csv, nombre_csv = audit_service.exportar(filas_export, formato="csv")
        st.download_button(
            "⬇ CSV", data=bytes_csv, file_name=nombre_csv, mime="text/csv"
        )
    with col2:
        bytes_xlsx, nombre_xlsx = audit_service.exportar(filas_export, formato="excel")
        st.download_button(
            "⬇ Excel", data=bytes_xlsx, file_name=nombre_xlsx,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col3:
        bytes_pdf, nombre_pdf = audit_service.exportar(
            filas_export, formato="pdf", filtros=filtros
        )
        st.download_button(
            "⬇ PDF", data=bytes_pdf, file_name=nombre_pdf, mime="application/pdf"
        )

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
