"""Gestión de modelos (HU-E6-02, RF-008 / RF-MOD-001..005).

Registro versionado, activación y rollback con un clic, historial de
activaciones auditado y acceso restringido por rol (CA4, validado en vista
y router).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Modelo
from app.domain.exceptions import ValidationError
from app.services import audit_service

_ACCIONES_HISTORIAL = {"REGISTRAR_MODELO", "ACTIVAR_MODELO", "DESACTIVAR_MODELO"}


def modelo_activo(session: Session) -> Modelo | None:
    """Devuelve la versión activa (la que usa la inferencia en producción)."""
    return session.scalar(
        select(Modelo).where(Modelo.activo.is_(True)).order_by(Modelo.creado_en.desc())
    )


def listar(session: Session) -> list[Modelo]:
    return list(
        session.scalars(select(Modelo).order_by(Modelo.creado_en.desc())).all()
    )


def registrar(
    session: Session,
    *,
    version: str,
    algoritmo: str,
    fecha_entrenamiento,
    metricas_json: str | None = None,
    ruta_artefacto: str,
    usuario_id: str | None,
) -> Modelo:
    """CA1: registro de modelo idempotente por versión con métricas resumidas.

    La primera versión registrada queda activa; las nuevas versiones se
    registran inactivas hasta que el administrador las active (CA2).
    """
    existente = session.scalar(select(Modelo).where(Modelo.version == version))
    if existente is not None:
        return existente
    es_primera = session.scalar(select(Modelo).limit(1)) is None
    modelo = Modelo(
        version=version,
        algoritmo=algoritmo,
        fecha_entrenamiento=fecha_entrenamiento,
        metricas_json=metricas_json,
        ruta_artefacto=ruta_artefacto,
        activo=es_primera,
    )
    session.add(modelo)
    session.commit()
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="REGISTRAR_MODELO",
        entidad="Modelo", detalle=f"{version} · {algoritmo}",
    )
    return modelo


def activar(session: Session, *, version: str, usuario_id: str | None) -> Modelo:
    """CA2: activa una versión y desactiva las demás (rollback con un clic)."""
    objetivo = session.scalar(select(Modelo).where(Modelo.version == version))
    if objetivo is None:
        raise ValidationError("Modelo inexistente", detalle=version)
    anterior = modelo_activo(session)
    if anterior is not None and anterior.version == version:
        # normaliza flags inconsistentes (p. ej. registros previos a E6)
        for modelo in session.scalars(select(Modelo)).all():
            modelo.activo = modelo.version == version
        session.commit()
        return objetivo  # ya activo — sin cambios
    for modelo in session.scalars(select(Modelo)).all():
        modelo.activo = modelo.version == version
    session.commit()
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="ACTIVAR_MODELO",
        entidad="Modelo",
        detalle=f"{version} · anterior {anterior.version if anterior else 'ninguno'} "
                f"· rollback" if anterior else f"{version} · primer despliegue",
    )
    return objetivo


def desactivar(session: Session, *, version: str, usuario_id: str | None) -> Modelo:
    """CA2: desactiva una versión (no se permite dejar el sistema sin activa)."""
    objetivo = session.scalar(select(Modelo).where(Modelo.version == version))
    if objetivo is None:
        raise ValidationError("Modelo inexistente", detalle=version)
    if objetivo.activo:
        activas = list(session.scalars(select(Modelo).where(Modelo.activo.is_(True))).all())
        if len(activas) <= 1:
            raise ValidationError(
                "No se puede desactivar el único modelo activo — active otra versión primero",
                detalle=version,
            )
    objetivo.activo = False
    session.commit()
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="DESACTIVAR_MODELO",
        entidad="Modelo", detalle=version,
    )
    return objetivo


def historial_activaciones(session: Session) -> list:
    """CA3: historial completo de registros y activaciones/desactivaciones."""
    from app.domain.entities import Auditoria

    return list(
        session.scalars(
            select(Auditoria)
            .where(Auditoria.accion.in_(_ACCIONES_HISTORIAL))
            .order_by(Auditoria.creado_en.desc())
            .limit(100)
        ).all()
    )
