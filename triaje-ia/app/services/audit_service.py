"""Servicio de auditoría (ENT-012, RF-012/013, Épica E5).

- Registro **append-only** (TT-E5-01): UPDATE/DELETE bloqueados vía eventos de
  SQLAlchemy — la integridad se protege también fuera de la app.
- Decorador `@auditar` reutilizable en servicios.
- Consulta paginada con filtros y exportación CSV/Excel/PDF (HU-E5-01).
"""

from __future__ import annotations

import csv
import functools
import io
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from sqlalchemy import event, select
from sqlalchemy.orm import Session

from app.domain.entities import Auditoria


class AuditoriaProtegidaError(Exception):
    """El registro de auditoría es append-only (TT-E5-01)."""


def _bloquear_modificacion(mapper, connection, target) -> None:  # noqa: ARG001
    raise AuditoriaProtegidaError(
        "El registro de auditoría es append-only: no se permite modificar ni borrar."
    )


# TT-E5-01: protección a nivel ORM (además de la disciplina en servicios).
event.listen(Auditoria, "before_update", _bloquear_modificacion)
event.listen(Auditoria, "before_delete", _bloquear_modificacion)


def registrar(
    session: Session,
    *,
    usuario_id: str | None,
    accion: str,
    entidad: str,
    detalle: str | None = None,
    evento_id: str | None = None,
    commit: bool = True,
) -> Auditoria:
    """Persiste un evento de auditoría (append-only).

    `commit=False` permite escribir la auditoría en la MISMA transacción que
    el cambio auditado (atomicidad — hallazgo de revision-calidad).
    """
    registro = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        entidad=entidad,
        detalle=detalle,
        evento_id=evento_id,
    )
    session.add(registro)
    if commit:
        session.commit()
    return registro


def auditar(accion: str, entidad: str, *, detalle: Callable | None = None):
    """Decorador reutilizable: audita tras la ejecución exitosa de un servicio.

    El servicio debe recibir `session` (posicional o keyword) y `usuario_id`
    (keyword). `detalle` es opcional: función que recibe el resultado y los
    argumentos y devuelve el texto del detalle.
    """

    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            resultado = func(*args, **kwargs)
            session = next(
                (a for a in args if isinstance(a, Session)), kwargs.get("session")
            )
            if session is None:
                raise TypeError("El servicio auditado debe recibir una Session")
            texto = detalle(resultado, *args, **kwargs) if detalle else None
            registrar(
                session,
                usuario_id=kwargs.get("usuario_id"),
                accion=accion,
                entidad=entidad,
                detalle=texto,
                evento_id=kwargs.get("evento_id"),
            )
            return resultado

        return envoltura

    return decorador


def consultar(
    session: Session,
    *,
    desde: datetime | None = None,
    hasta: datetime | None = None,
    usuario_id: str | None = None,
    entidad: str | None = None,
    accion: str | None = None,
    evento_id: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Auditoria], int]:
    """HU-E5-01 CA1/CA2: filtros por fecha/usuario/entidad/acción/evento.

    Índices + límite de página mantienen la consulta < 1 s (RNP-003).
    """
    cond = []
    if desde is not None:
        cond.append(Auditoria.creado_en >= desde)
    if hasta is not None:
        cond.append(Auditoria.creado_en <= hasta)
    if usuario_id:
        cond.append(Auditoria.usuario_id == usuario_id)
    if entidad:
        cond.append(Auditoria.entidad == entidad)
    if accion:
        cond.append(Auditoria.accion == accion)
    if evento_id:
        cond.append(Auditoria.evento_id == evento_id)
    consulta = select(Auditoria).where(*cond)
    total = len(session.scalars(consulta).all())
    filas = list(
        session.scalars(
            consulta.order_by(Auditoria.creado_en.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).all()
    )
    return filas, total


def _filas_a_tabla(filas: list[Auditoria]) -> list[dict]:
    return [
        {
            "Fecha (UTC)": f.creado_en.strftime("%Y-%m-%d %H:%M:%S") if f.creado_en else "",
            "Usuario": f.usuario_id or "—",
            "Acción": f.accion,
            "Entidad": f.entidad,
            "Evento": f.evento_id or "—",
            "Detalle": (f.detalle or "")[:120],
        }
        for f in filas
    ]


def exportar_csv(filas: list[Auditoria]) -> bytes:
    buffer = io.StringIO()
    tabla = _filas_a_tabla(filas)
    campos = list(tabla[0].keys()) if tabla else []
    escritor = csv.DictWriter(buffer, fieldnames=campos)
    if tabla:
        escritor.writeheader()
        escritor.writerows(tabla)
    return buffer.getvalue().encode("utf-8-sig")


def exportar_excel(filas: list[Auditoria]) -> bytes:
    """Excel vía pandas/openpyxl (HU-E5-01 CA3)."""
    buffer = io.BytesIO()
    pd.DataFrame(_filas_a_tabla(filas)).to_excel(buffer, index=False, sheet_name="auditoria")
    return buffer.getvalue()


def exportar_pdf(filas: list[Auditoria], *, filtros: str = "") -> bytes:
    """Exportación PDF con encabezado institucional (HU-E5-01 CA3)."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    pdf.setFillColor("#0891B2")
    pdf.rect(0, h - 2.5 * cm, w, 2.5 * cm, stroke=0, fill=1)
    pdf.setFillColor("#FFFFFF")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(2 * cm, h - 1.6 * cm, "TriajeIA — Registro de auditoría")
    pdf.setFillColor("#164E63")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        2 * cm, h - 3.2 * cm,
        f"Filtros: {filtros or 'sin filtros'} · Registros: {len(filas)}",
    )
    y = h - 4.2 * cm
    pdf.setFont("Helvetica", 8)
    for f in filas[:400]:  # límite de páginas razonable para exportación
        pdf.drawString(
            2 * cm, y,
            f"{f.creado_en:%Y-%m-%d %H:%M:%S} · {f.usuario_id or '—'} · {f.accion} · "
            f"{f.entidad}" + (f" · {(f.detalle or '')[:80]}" if f.detalle else ""),
        )
        y -= 0.5 * cm
        if y < 2 * cm:
            pdf.showPage()
            y = h - 2.5 * cm
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def exportar(
    filas: list[Auditoria], *, formato: str, filtros: str = ""
) -> tuple[bytes, str]:
    """Devuelve (bytes, nombre de archivo) según formato csv/excel/pdf."""
    if formato == "csv":
        return exportar_csv(filas), "auditoria.csv"
    if formato == "excel":
        return exportar_excel(filas), "auditoria.xlsx"
    if formato == "pdf":
        return exportar_pdf(filas, filtros=filtros), "auditoria.pdf"
    raise ValueError(f"Formato no soportado: {formato}")


def ahora_utc_naive() -> datetime:
    """Único helper de "ahora" en UTC naive para comparaciones de fechas.

    Evita mezclar escritura UTC con lectura en hora local (hallazgo de
    revision-calidad sobre filtros de fecha).
    """
    return datetime.now(UTC).replace(tzinfo=None)


def rango_por_defecto() -> tuple[datetime, datetime]:
    """Rango por defecto de consulta: últimos 7 días en UTC."""
    ahora = ahora_utc_naive()
    return ahora - timedelta(days=7), ahora
