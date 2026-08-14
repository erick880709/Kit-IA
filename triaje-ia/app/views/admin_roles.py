"""Administración de roles (HU-E1-02).

Acceso exclusivo de Administrador (CA3, validado en el router y aquí).
CA4: cada cambio de rol queda registrado en auditoría.
"""

from __future__ import annotations

import streamlit as st
from sqlalchemy import select

from app.domain.entities import ROLES_DEMO, Usuario
from app.domain.exceptions import ProhibidoError
from app.infra.db import SessionLocal
from app.services.authorization_service import cambiar_rol_usuario, verificar_acceso


def render() -> None:
    st.title("Gestión de roles y permisos")
    rol = st.session_state.get("usuario_rol", "")
    try:
        verificar_acceso(rol, "admin_roles")
    except ProhibidoError as exc:
        st.error(exc.mensaje)
        return

    with SessionLocal() as session:
        usuarios = session.scalars(select(Usuario).order_by(Usuario.correo)).all()
        if not usuarios:
            st.info("No hay usuarios registrados.")
            return
        for usuario in usuarios:
            c1, c2 = st.columns([3, 2])
            c1.markdown(f"**{usuario.nombre}** · `{usuario.correo}`")
            nuevo_rol = c2.selectbox(
                "Rol",
                ROLES_DEMO,
                index=ROLES_DEMO.index(usuario.rol.nombre)
                if usuario.rol.nombre in ROLES_DEMO
                else 0,
                key=f"rol_{usuario.id}",
            )
            if nuevo_rol != usuario.rol.nombre:
                if st.button(f"Aplicar cambio → {nuevo_rol}", key=f"btn_{usuario.id}"):
                    cambiar_rol_usuario(
                        session,
                        usuario_id=usuario.id,
                        nuevo_rol=nuevo_rol,
                        admin_id=st.session_state.get("usuario_id"),
                    )
                    st.success(
                        f"Rol de {usuario.correo} actualizado a {nuevo_rol} (auditado)"
                    )
                    st.rerun()

    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
