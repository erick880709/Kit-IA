"""Pantalla de login (HU-E1-01, mockup s-login).

Formulario correo + contraseña con:
- Verificación bcrypt (CA2).
- Bloqueo temporal tras 5 intentos (CA3).
- Aviso de demo académica y nota de no-autonomía del sistema.
"""

from __future__ import annotations

import streamlit as st

from app.domain.exceptions import (
    AutenticacionError,
    TokenInvalidoError,
    UsuarioBloqueadoError,
    ValidationError,
)
from app.infra.config import settings
from app.infra.db import SessionLocal
from app.services import auth_service


def render() -> None:
    st.title(f"{settings.app_name} · Acceso clínico")
    st.caption("Sistema de apoyo a la decisión de triaje — no es un dispositivo médico")

    with st.form("login_form"):
        correo = st.text_input("Correo institucional", placeholder="usuario@hospital.gov.co")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar", width="stretch")

    if submitted:
        if not correo or not password:
            st.error("Ingrese correo y contraseña")
            return
        with SessionLocal() as session:
            try:
                usuario = auth_service.autenticar(session, correo=correo, password=password)
            except UsuarioBloqueadoError as exc:
                st.error(exc.mensaje)
                return
            except AutenticacionError as exc:
                detalle = f" · {exc.detalle}" if exc.detalle else ""
                st.error(f"{exc.mensaje}{detalle}")
                return
            st.session_state["usuario_id"] = usuario.id
            st.session_state["usuario_nombre"] = usuario.nombre
            st.session_state["usuario_rol"] = usuario.rol.nombre
        st.rerun()

    st.info(
        "Uso de demostración académica con datos sintéticos. "
        f"Tras {settings.max_intentos_login} intentos fallidos la cuenta se bloquea "
        f"{settings.bloqueo_login_min} minutos."
    )

    _render_recuperacion()


def _render_recuperacion() -> None:
    """Flujo de recuperación de contraseña (HU-E1-03).

    CA1: token temporal + email simulado en la demo (sin SMTP real).
    CA2: token de un solo uso con expiración de 15 minutos.
    CA3: política mínima de 8 caracteres.
    """
    with st.expander("¿Olvidó su contraseña?"):
        correo = st.text_input("Correo registrado", key="rec_correo")
        if st.button("Enviar enlace de recuperación"):
            with SessionLocal() as session:
                token = auth_service.solicitar_recuperacion(session, correo=correo)
            if token:
                st.session_state["demo_token"] = token
                st.session_state["demo_correo"] = correo.strip().lower()
            else:
                st.info("Si el correo está registrado, recibirá un enlace de recuperación.")

        if "demo_token" in st.session_state:
            st.success(
                "Email simulado (demo sin SMTP): "
                f"token `{st.session_state['demo_token'][:12]}…` disponible abajo."
            )
            token_ingresado = st.text_input("Token de recuperación", key="rec_token")
            nueva = st.text_input("Nueva contraseña", type="password", key="rec_nueva")
            confirmar = st.text_input(
                "Confirmar nueva contraseña", type="password", key="rec_confirmar"
            )
            if st.button("Cambiar contraseña"):
                if nueva != confirmar:
                    st.error("Las contraseñas no coinciden")
                    return
                with SessionLocal() as session:
                    try:
                        auth_service.recuperar_contrasena(
                            session,
                            correo=st.session_state["demo_correo"],
                            token=token_ingresado,
                            nueva_password=nueva,
                        )
                    except (TokenInvalidoError, ValidationError) as exc:
                        st.error(exc.mensaje)
                        return
                st.session_state.pop("demo_token", None)
                st.session_state.pop("demo_correo", None)
                st.success("Contraseña actualizada — ya puede iniciar sesión.")
