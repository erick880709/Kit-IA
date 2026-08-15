"""Dashboard operativo (HU-E6-01) con semáforo de metas y exportación (HU-E6-03).

CA1: 7 indicadores calculados desde los registros reales (CA4, nada estático).
CA2: semáforo de metas RNF-001. CA3: matriz de confusión y discrepancias.
HU-E6-03: exportación Excel/PDF/CSV anonimizada y auditada.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.domain.exceptions import ProhibidoError
from app.infra.db import SessionLocal
from app.services import audit_service, authorization_service, dashboard_service

_ICONOS = {"ok": "🟢", "alerta": "🔴", "sin_dato": "⚪"}


def _auditar_exportacion() -> None:
    with SessionLocal() as session:
        audit_service.registrar(
            session,
            usuario_id=st.session_state.get("usuario_id"),
            accion="EXPORTAR_REPORTE",
            entidad="Dashboard",
            detalle="reporte operativo descargado (anonimizado)",
        )


def render() -> None:
    rol = st.session_state.get("usuario_rol", "")
    try:
        authorization_service.verificar_acceso(rol, "dashboard")
    except ProhibidoError as exc:
        st.error(exc.mensaje)
        return

    st.title("Dashboard operativo")
    st.caption("Indicadores en vivo desde los registros de la demo (RF-013).")

    with SessionLocal() as session:
        indicadores = dashboard_service.calcular_indicadores(session)
        tendencia = dashboard_service.conteo_por_dia(session, dias=14)

    # CA1 · tarjetas de indicadores
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Eventos registrados", indicadores["n_eventos"])
    c2.metric("Eventos cerrados", indicadores["n_cerrados"])
    c3.metric(
        "Tiempo promedio de atención",
        f"{indicadores['tiempo_promedio_atencion_min']} min"
        if indicadores["tiempo_promedio_atencion_min"] is not None else "—",
    )
    c4.metric(
        "Concordancia IA vs profesional",
        f"{indicadores['concordancia_global']:.0%}"
        if indicadores["concordancia_global"] is not None else "—",
    )

    st.subheader("Distribución de triaje por nivel (CA1)")
    st.bar_chart(pd.Series(indicadores["distribucion"]))

    st.subheader("Tendencia diaria de eventos (14 días)")
    if tendencia:
        serie = pd.DataFrame(tendencia).set_index("fecha")
        st.line_chart(serie)
    else:
        st.info("Sin eventos en los últimos 14 días.")

    st.subheader("Concordancia IA vs profesional por nivel")
    conc_nivel = pd.Series(indicadores["concordancia_por_nivel"]).dropna()
    if not conc_nivel.empty:
        st.bar_chart(conc_nivel)
    else:
        st.info("Sin eventos cerrados para calcular concordancia por nivel.")

    # CA2 · semáforo de metas RNF-001
    st.subheader("Semáforo de metas del modelo (RNF-001)")
    semaforo = indicadores["semaforo"]
    filas_semaforo = []
    for clave, meta in semaforo.items():
        filas_semaforo.append(
            {
                "Meta": clave.upper(),
                "Umbral": meta["meta"],
                "Valor": meta["valor"],
                "Estado": f"{_ICONOS[meta['estado']]} {meta['estado']}",
            }
        )
    st.dataframe(pd.DataFrame(filas_semaforo), hide_index=True, width="stretch")

    desempeno = indicadores["desempeno_ia"]
    st.caption(
        f"Métricas del modelo `{desempeno['version']}` · precisión "
        f"{desempeno['precision']} · recall {desempeno['recall']} · F1 "
        f"{desempeno['f1']} · AUC {desempeno['auc']}"
    )

    # CA3 · matriz de confusión y discrepancias
    st.subheader("Matriz de confusión IA vs profesional (CA3)")
    st.dataframe(
        indicadores["matriz_confusion"].reset_index().rename(columns={"index": "IA ↓"}),
        hide_index=True,
        width="stretch",
    )
    st.subheader("Discrepancias con motivo (filtrables)")
    if indicadores["discrepancias"]:
        st.dataframe(
            pd.DataFrame(indicadores["discrepancias"]),
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("Sin discrepancias registradas.")

    # HU-E6-03 · exportación de reportes
    st.divider()
    st.subheader("Exportar reporte (HU-E6-03)")
    col1, col2, col3 = st.columns(3)
    with col1:
        csv_bytes, nombre = dashboard_service.exportar_reporte(
            indicadores, formato="csv"
        )
        st.download_button(
            "⬇ CSV", data=csv_bytes, file_name=nombre, mime="text/csv",
            on_click=_auditar_exportacion,
        )
    with col2:
        xlsx_bytes, nombre = dashboard_service.exportar_reporte(
            indicadores, formato="excel", tendencia=tendencia,
        )
        st.download_button(
            "⬇ Excel", data=xlsx_bytes, file_name=nombre,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            on_click=_auditar_exportacion,
        )
    with col3:
        pdf_bytes, nombre = dashboard_service.exportar_reporte(
            indicadores, formato="pdf", tendencia=tendencia,
        )
        st.download_button(
            "⬇ PDF", data=pdf_bytes, file_name=nombre, mime="application/pdf",
            on_click=_auditar_exportacion,
        )

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
