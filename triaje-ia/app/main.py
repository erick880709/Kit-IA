"""Punto de entrada de la aplicación Streamlit.

Bootstrap + routing por estado de sesión:
- Sin sesión → login (HU-E1-01) con recuperación de contraseña (HU-E1-03).
- Con sesión → router por pantalla con RBAC (HU-E1-02) y cierre automático
  por inactividad (HU-E1-04, 5 minutos, auditado).
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

import streamlit as st

from app.domain.exceptions import ProhibidoError
from app.infra.config import settings
from app.infra.db import SessionLocal, db_ok, init_db
from app.infra.logging_config import setup_logging
from app.services import (
    audit_service,
    authorization_service,
    seed_service,
    session_service,
    triaje_service,
)
from app.views import (
    acerca_de,
    admin_roles,
    auditoria,
    buscar_paciente,
    cierre_evento,
    clasificacion_ia,
    comparacion_modelos,
    dashboard,
    evaluacion_clinica,
    explicacion_shap,
    gestion_modelos,
    historial_paciente,
    login,
    manual_uso,
    registro_paciente,
    signos_vitales,
    validacion_triaje,
)

CLAVES_SESION = (
    "usuario_id", "usuario_nombre", "usuario_rol", "ultima_actividad",
    "pantalla", "paciente_id", "evento_id", "evento_reclasificar",
    "precarga_paciente", "duplicados_actuales", "paciente_existente_id",
    "aviso_cierre_motivo", "paciente_nuevo_para_triaje", "registro_ok",
)

PANTALLA_POR_ESTADO = {
    "Registrado": "signos_vitales",
    "SignosVitales": "evaluacion_clinica",
    "EvaluacionClinica": "clasificacion_ia",
    "ClasificacionIA": "explicacion_shap",
    "ValidacionProfesional": "cierre_evento",
    "Cerrado": "cierre_evento",
}


def bootstrap() -> None:
    """Inicializa plomería transversal (idempotente)."""
    setup_logging(settings.log_level)
    init_db()
    # Demo auto-arrancable en entornos efímeros (Community Cloud, contenedores):
    # siembra usuarios/roles demo solo cuando la BD está vacía (idempotente).
    with SessionLocal() as session:
        seed_service.seed_demo_si_vacio(session)
    # Precalentamiento del modelo (2026-08-26): mueve la carga del joblib y la
    # construcción del explainer SHAP al arranque para que la primera
    # inferencia en contenedores fríos cumpla el presupuesto < 3 s (RNF-007).
    # Además sincroniza la fila activa de BD con el artefacto más reciente
    # (la BD de /tmp puede persistir entre despliegues con una versión vieja).
    try:
        from app.services.inference_service import inference_service

        with SessionLocal() as session:
            inference_service.sincronizar_modelo_activo(session)
        inference_service.precalentar()
    except Exception:  # noqa: BLE001 — nunca debe bloquear el bootstrap
        logging.getLogger(__name__).exception(
            "Precalentamiento del modelo falló en bootstrap"
        )
    if settings.app_secret == "cambiar-en-produccion":
        logging.getLogger(__name__).warning(
            "APP_SECRET_KEY usa el valor por defecto ('cambiar-en-produccion') — "
            "genere una clave aleatoria y secreta antes de cualquier despliegue real"
        )


def cerrar_sesion(motivo: str | None = None) -> None:
    """Limpia la sesión y, si corresponde, audita el cierre (HU-E1-04 CA2)."""
    usuario_id = st.session_state.get("usuario_id")
    if motivo and usuario_id:
        with SessionLocal() as session:
            audit_service.registrar(
                session,
                usuario_id=usuario_id,
                accion=motivo,
                entidad="Sesion",
                detalle=f"cierre a las {datetime.now(UTC).isoformat()}",
            )
    for clave in CLAVES_SESION:
        st.session_state.pop(clave, None)
    logging.getLogger(__name__).info(
        "Sesión cerrada: %s (usuario %s)", motivo or "manual", usuario_id
    )


def render_home() -> None:
    """Pantalla inicial del rol con menú filtrado por permisos (HU-E1-02 CA2)
    y estado del triaje en curso (HU-E2-06 CA1)."""
    nombre = st.session_state.get("usuario_nombre", "")
    rol = st.session_state.get("usuario_rol", "")
    paciente_id = st.session_state.get("paciente_id")
    st.title(f"{settings.app_name} · Pantalla inicial")
    st.success(f"Sesión iniciada: {nombre} ({rol})")

    aviso = st.session_state.pop("aviso_cierre_motivo", None)
    if aviso:
        st.warning(
            f"ℹ️ {aviso} El triaje quedó registrado, cerrado y trazado en auditoría."
        )

    if paciente_id:
        with SessionLocal() as session:
            from sqlalchemy import select

            from app.domain.entities import EventoTriaje, Paciente

            paciente = session.get(Paciente, paciente_id)
            st.info(
                f"Paciente en contexto: **{paciente.nombres} {paciente.apellidos}** · "
                f"{paciente.tipo_documento} {paciente.numero_documento}"
            )
            evento = session.scalar(
                select(EventoTriaje)
                .where(
                    EventoTriaje.paciente_id == paciente_id,
                    EventoTriaje.estado != "Cerrado",
                    EventoTriaje.estado != "Reclasificado",  # terminal (HU-E2-07)
                )
                .order_by(EventoTriaje.inicio.desc())
            )

        st.subheader("Acciones disponibles para tu rol")
        if authorization_service.puede_acceder(rol, "registro_paciente"):
            if st.button("🏥 Registrar paciente", width="stretch"):
                st.session_state["pantalla"] = "registro_paciente"
                st.rerun()
        if authorization_service.puede_acceder(rol, "buscar_paciente"):
            if st.button("🔎 Buscar paciente", width="stretch"):
                st.session_state["pantalla"] = "buscar_paciente"
                st.rerun()
        if authorization_service.puede_acceder(rol, "historial_paciente"):
            if st.button("📋 Historial de triajes", width="stretch"):
                st.session_state["pantalla"] = "historial_paciente"
                st.rerun()
        if evento is None and authorization_service.puede_acceder(rol, "signos_vitales"):
            if st.button("➕ Iniciar evento de triaje", type="primary", width="stretch"):
                with SessionLocal() as session:
                    nuevo = triaje_service.crear_evento(
                        session,
                        paciente_id=paciente_id,
                        usuario_id=st.session_state.get("usuario_id"),
                    )
                if nuevo.estado == "Cerrado":  # fuera del rango 16-60: sin IA
                    st.session_state["aviso_cierre_motivo"] = nuevo.motivo_cierre
                    st.session_state.pop("evento_id", None)
                    st.session_state["pantalla"] = "inicio"
                else:
                    st.session_state["evento_id"] = nuevo.id
                    st.session_state["pantalla"] = "signos_vitales"
                st.rerun()
        elif evento is not None:
            st.info(f"⏳ Evento de triaje en curso — estado: `{evento.estado}`")
            siguiente = PANTALLA_POR_ESTADO.get(evento.estado)
            if siguiente and authorization_service.puede_acceder(rol, siguiente):
                if st.button("▶ Continuar triaje", width="stretch"):
                    st.session_state["evento_id"] = evento.id
                    st.session_state["pantalla"] = siguiente
                    st.rerun()
    else:
        st.subheader("Acciones disponibles para tu rol")
        if authorization_service.puede_acceder(rol, "registro_paciente"):
            if st.button("🏥 Registrar paciente (iniciar triaje)", width="stretch"):
                st.session_state["pantalla"] = "registro_paciente"
                st.rerun()
        if authorization_service.puede_acceder(rol, "buscar_paciente"):
            if st.button("🔎 Buscar paciente", width="stretch"):
                st.session_state["pantalla"] = "buscar_paciente"
                st.rerun()

    if authorization_service.puede_acceder(rol, "admin_roles"):
        if st.button("👥 Gestión de roles y permisos", width="stretch"):
            st.session_state["pantalla"] = "admin_roles"
            st.rerun()
    if authorization_service.puede_acceder(rol, "comparacion_modelos"):
        if st.button("📊 Comparación de modelos de IA", width="stretch"):
            st.session_state["pantalla"] = "comparacion_modelos"
            st.rerun()
    if authorization_service.puede_acceder(rol, "auditoria"):
        if st.button("🕵️ Auditoría y trazabilidad", width="stretch"):
            st.session_state["pantalla"] = "auditoria"
            st.rerun()
    if authorization_service.puede_acceder(rol, "dashboard"):
        if st.button("📈 Dashboard operativo", width="stretch"):
            st.session_state["pantalla"] = "dashboard"
            st.rerun()
    if authorization_service.puede_acceder(rol, "gestion_modelos"):
        if st.button("🧠 Gestión de modelos", width="stretch"):
            st.session_state["pantalla"] = "gestion_modelos"
            st.rerun()

    st.divider()
    st.subheader("Soporte")
    if st.button("📖 Manual de uso", width="stretch"):
        st.session_state["pantalla"] = "manual_uso"
        st.rerun()
    if st.button("ℹ️ Acerca de", width="stretch"):
        st.session_state["pantalla"] = "acerca_de"
        st.rerun()
    if st.button("Cerrar sesión"):
        cerrar_sesion()
        st.rerun()


def _aplicar_timeout_sesion() -> bool:
    """HU-E1-04 CA1: 5 min de inactividad → cierre con aviso y auditoría.

    Devuelve True si la sesión fue cerrada por inactividad.
    """
    ultima = st.session_state.get("ultima_actividad")
    ahora = datetime.now(UTC)
    if ultima is not None and session_service.debe_expirar(ultima, ahora):
        cerrar_sesion(motivo="CIERRE_SESION_INACTIVIDAD")
        st.warning(
            f"Sesión cerrada por inactividad "
            f"(más de {settings.session_timeout_min} minutos)."
        )
        return True
    st.session_state["ultima_actividad"] = ahora
    return False


def main() -> None:
    bootstrap()
    st.set_page_config(page_title=settings.app_name, page_icon="🏥", layout="wide")

    if "usuario_id" not in st.session_state:
        login.render()
    elif _aplicar_timeout_sesion():
        login.render()
    else:
        rol = st.session_state.get("usuario_rol", "")
        pantalla = st.session_state.get("pantalla", "inicio")
        try:
            authorization_service.verificar_acceso(rol, pantalla)
        except ProhibidoError as exc:
            st.error(exc.mensaje)
            pantalla = "inicio"
            st.session_state["pantalla"] = "inicio"
        {
            "inicio": render_home,
            "registro_paciente": registro_paciente.render,
            "buscar_paciente": buscar_paciente.render,
            "historial_paciente": historial_paciente.render,
            "signos_vitales": signos_vitales.render,
            "evaluacion_clinica": evaluacion_clinica.render,
            "clasificacion_ia": clasificacion_ia.render,
            "explicacion_shap": explicacion_shap.render,
            "comparacion_modelos": comparacion_modelos.render,
            "auditoria": auditoria.render,
            "dashboard": dashboard.render,
            "gestion_modelos": gestion_modelos.render,
            "validacion_triaje": validacion_triaje.render,
            "cierre_evento": cierre_evento.render,
            "admin_roles": admin_roles.render,
            "manual_uso": manual_uso.render,
            "acerca_de": acerca_de.render,
        }.get(pantalla, render_home)()

    if not db_ok():
        st.error("No se pudo conectar a la base de datos — revisar DB_PATH en .env")


if __name__ == "__main__":
    main()
