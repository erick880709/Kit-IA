"""Indicadores del dashboard operativo y exportación de reportes (HU-E6-01/03).

Todos los indicadores se calculan desde los registros reales de la BD
(CA4, nada estático). Reportes anonimizados: sin identificadores directos.
"""

from __future__ import annotations

import csv
import io
import json

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.catalogos import NIVELES_TRIaje
from app.domain.entities import EventoTriaje
from app.services import modelo_service

METAS_RNF001 = {"f1": 0.82, "precision": 0.85, "recall": 0.80, "auc_roc": 0.87}


def _metricas_modelo(session: Session) -> dict:
    activo = modelo_service.modelo_activo(session)
    if activo is None or not activo.metricas_json:
        return {}
    try:
        return json.loads(activo.metricas_json)
    except (json.JSONDecodeError, TypeError):
        return {}


def _tiempo_promedio_atencion(eventos: list[EventoTriaje]) -> float | None:
    duraciones = [
        (e.cierre - e.inicio).total_seconds() / 60
        for e in eventos
        if e.cierre is not None and e.inicio is not None
    ]
    return round(sum(duraciones) / len(duraciones), 1) if duraciones else None


def calcular_indicadores(session: Session) -> dict:
    """CA1: 7 indicadores + semáforo de metas + matriz de confusión."""
    eventos = list(session.scalars(select(EventoTriaje)).all())
    cerrados = [e for e in eventos if e.estado == "Cerrado"]

    nivel_profesional = [e.nivel_asignado_profesional for e in cerrados]
    distribucion = {
        n: nivel_profesional.count(n) for n in NIVELES_TRIaje
    }
    total_dist = sum(distribucion.values()) or 1

    concordancias = [e.concordancia for e in cerrados if e.concordancia is not None]
    concordancia_global = (
        round(sum(concordancias) / len(concordancias), 3) if concordancias else None
    )

    concordancia_por_nivel = {}
    for n in NIVELES_TRIaje:
        fila = [
            e for e in cerrados
            if e.nivel_asignado_profesional == n and e.concordancia is not None
        ]
        concordancia_por_nivel[n] = (
            round(sum(e.concordancia for e in fila) / len(fila), 3) if fila else None
        )

    confusion = pd.crosstab(
        pd.Series([e.nivel_sugerido_ia or "—" for e in cerrados], name="IA"),
        pd.Series([e.nivel_asignado_profesional or "—" for e in cerrados],
                 name="Profesional"),
    ).reindex(index=NIVELES_TRIaje, columns=NIVELES_TRIaje, fill_value=0)

    discrepancias = [
        {
            "fecha": e.cierre.strftime("%Y-%m-%d %H:%M") if e.cierre else "—",
            "nivel_ia": e.nivel_sugerido_ia or "—",
            "nivel_profesional": e.nivel_asignado_profesional or "—",
            "motivo": e.motivo_discrepancia or "—",
        }
        for e in cerrados
        if e.concordancia is False
    ]

    metricas = _metricas_modelo(session)
    macro = metricas.get("macro", {})
    desempeno = {
        "version": modelo_service.modelo_activo(session).version
        if modelo_service.modelo_activo(session) else "—",
        "precision": macro.get("precision"),
        "recall": macro.get("recall"),
        "f1": macro.get("f1"),
        "auc": metricas.get("auc_roc_ovr"),
    }

    # CA2: semáforo de metas RNF-001
    semaforo = {}
    for clave, meta in METAS_RNF001.items():
        clave_desempeno = "auc" if clave == "auc_roc" else clave
        valor = desempeno.get(clave_desempeno)
        if valor is None:
            semaforo[clave] = {"meta": meta, "valor": None, "estado": "sin_dato"}
        else:
            semaforo[clave] = {
                "meta": meta, "valor": round(float(valor), 4),
                "estado": "ok" if float(valor) >= meta else "alerta",
            }

    return {
        "n_eventos": len(eventos),
        "n_cerrados": len(cerrados),
        "distribucion": {n: v / total_dist for n, v in distribucion.items()},
        "tiempo_promedio_atencion_min": _tiempo_promedio_atencion(eventos),
        "desempeno_ia": desempeno,
        "concordancia_global": concordancia_global,
        "concordancia_por_nivel": concordancia_por_nivel,
        "matriz_confusion": confusion,
        "discrepancias": discrepancias,
        "semaforo": semaforo,
    }


def _hoja_exportacion(indicadores: dict) -> list[dict]:
    sem = indicadores["semaforo"]
    base = [
        {"indicador": "Volumen de eventos", "valor": indicadores["n_eventos"]},
        {"indicador": "Eventos cerrados", "valor": indicadores["n_cerrados"]},
        {"indicador": "Tiempo promedio de atención (min)",
         "valor": indicadores["tiempo_promedio_atencion_min"]},
        {"indicador": "Concordancia global IA vs profesional",
         "valor": indicadores["concordancia_global"]},
        {"indicador": "F1 (macro)", "valor": sem["f1"]["valor"],
         "meta": sem["f1"]["meta"], "estado": sem["f1"]["estado"]},
        {"indicador": "Precisión (macro)", "valor": sem["precision"]["valor"],
         "meta": sem["precision"]["meta"], "estado": sem["precision"]["estado"]},
        {"indicador": "Recall (macro)", "valor": sem["recall"]["valor"],
         "meta": sem["recall"]["meta"], "estado": sem["recall"]["estado"]},
        {"indicador": "AUC-ROC (OVR)", "valor": sem["auc_roc"]["valor"],
         "meta": sem["auc_roc"]["meta"], "estado": sem["auc_roc"]["estado"]},
        {"indicador": "Distribución I", "valor": indicadores["distribucion"].get("I")},
        {"indicador": "Distribución II", "valor": indicadores["distribucion"].get("II")},
        {"indicador": "Distribución III", "valor": indicadores["distribucion"].get("III")},
        {"indicador": "Distribución IV", "valor": indicadores["distribucion"].get("IV")},
        {"indicador": "Distribución V", "valor": indicadores["distribucion"].get("V")},
    ]
    for fila in base:
        fila.setdefault("meta", None)
        fila.setdefault("estado", None)
    return base


def exportar_reporte(indicadores: dict, *, formato: str) -> tuple[bytes, str]:
    """HU-E6-03 CA1/CA2: exportación CSV/Excel/PDF sin identificadores."""
    base = _hoja_exportacion(indicadores)
    if formato == "csv":
        buffer = io.StringIO()
        campos = list(base[0].keys())
        escritor = csv.DictWriter(buffer, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(base)
        return buffer.getvalue().encode("utf-8-sig"), "reporte_dashboard.csv"
    if formato == "excel":
        buffer = io.BytesIO()
        pd.DataFrame(base).to_excel(buffer, index=False, sheet_name="dashboard")
        return buffer.getvalue(), "reporte_dashboard.xlsx"
    if formato == "pdf":
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
        w, h = A4
        pdf.setFillColor("#0891B2")
        pdf.rect(0, h - 2.5 * cm, w, 2.5 * cm, stroke=0, fill=1)
        pdf.setFillColor("#FFFFFF")
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(2 * cm, h - 1.6 * cm, "TriajeIA — Reporte operativo")
        pdf.setFillColor("#164E63")
        y = h - 3.6 * cm
        pdf.setFont("Helvetica", 10)
        for fila in base:
            pdf.drawString(
                2 * cm, y,
                f"{fila['indicador']}: {fila['valor']}"
                + (f" · meta {fila['meta']} · {fila['estado']}"
                   if fila.get("meta") is not None else ""),
            )
            y -= 0.6 * cm
            if y < 2 * cm:
                pdf.showPage()
                y = h - 2.5 * cm
        pdf.drawString(
            2 * cm, y,
            "Reporte anonimizado — sin identificadores directos de pacientes.",
        )
        pdf.showPage()
        pdf.save()
        return buffer.getvalue(), "reporte_dashboard.pdf"
    raise ValueError(f"Formato no soportado: {formato}")


def conteo_por_dia(session: Session, dias: int = 14) -> list[dict]:
    """Serie diaria de eventos (para tendencia en el dashboard).

    Usa el helper único de "ahora" en UTC naive (sin mezcla de zonas).
    """
    from datetime import timedelta

    from app.services.audit_service import ahora_utc_naive

    desde = ahora_utc_naive() - timedelta(days=dias)
    filas = session.execute(
        select(func.date(EventoTriaje.inicio), func.count(EventoTriaje.id))
        .where(EventoTriaje.inicio >= desde)
        .group_by(func.date(EventoTriaje.inicio))
        .order_by(func.date(EventoTriaje.inicio))
    ).all()
    return [{"fecha": str(f), "n": int(n)} for f, n in filas]
