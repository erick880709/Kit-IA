"""Autorización RBAC por pantalla (HU-E1-02, RF-014, RF-SEC-002).

CA2: cada pantalla del inventario RD-004 declara sus roles permitidos.
CA3: la validación vive en el servicio (backend), no solo en la UI — las
vistas llaman a `verificar_acceso` antes de renderizar y el router de
`main.py` enruta con `roles_permitidos_pantalla`.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Rol, Usuario
from app.domain.exceptions import ProhibidoError
from app.services import audit_service

# Mapeo pantalla → roles permitidos (RD-004 + HU por pantalla).
PERMISOS_PANTALLA: dict[str, set[str]] = {
    "inicio": {"Administrador", "Medico", "Enfermera", "Investigador", "Auditor"},
    "registro_paciente": {"Medico", "Enfermera", "Administrador"},
    "buscar_paciente": {"Medico", "Enfermera", "Administrador"},
    "historial_paciente": {"Medico", "Enfermera", "Investigador"},
    "signos_vitales": {"Medico", "Enfermera"},
    "evaluacion_clinica": {"Medico", "Enfermera"},
    "clasificacion_ia": {"Medico", "Enfermera"},
    "explicacion_shap": {"Medico", "Enfermera", "Investigador"},
    "validacion_triaje": {"Medico", "Enfermera"},
    "cierre_evento": {"Medico", "Enfermera"},
    "comparacion_modelos": {"Investigador", "Administrador"},
    "gestion_modelos": {"Administrador", "Investigador"},
    "dashboard": {"Administrador", "Auditor", "Investigador", "Medico"},  # HU-E6-01
    "auditoria": {"Auditor", "Administrador"},
    "admin_roles": {"Administrador"},
}


def roles_permitidos_pantalla(pantalla: str) -> set[str]:
    return PERMISOS_PANTALLA.get(pantalla, set())


def puede_acceder(rol_nombre: str, pantalla: str) -> bool:
    return rol_nombre in roles_permitidos_pantalla(pantalla)


def verificar_acceso(rol_nombre: str, pantalla: str) -> None:
    """Lanza ProhibidoError si el rol no puede acceder a la pantalla (CA3)."""
    if not puede_acceder(rol_nombre, pantalla):
        raise ProhibidoError(
            f"El rol {rol_nombre} no tiene permiso sobre {pantalla}",
            detalle=pantalla,
        )


def cambiar_rol_usuario(
    session: Session, *, usuario_id: str, nuevo_rol: str, admin_id: str | None
) -> Usuario:
    """Cambia el rol de un usuario y deja constancia en auditoría (CA4)."""
    usuario = session.get(Usuario, usuario_id)
    if usuario is None:
        raise ProhibidoError("Usuario inexistente", detalle=usuario_id)
    rol = session.scalar(select(Rol).where(Rol.nombre == nuevo_rol))
    if rol is None:
        raise ProhibidoError("Rol inexistente", detalle=nuevo_rol)

    anterior = usuario.rol.nombre
    usuario.rol_id = rol.id
    session.commit()
    audit_service.registrar(
        session,
        usuario_id=admin_id,
        accion="CAMBIO_ROL",
        entidad="Usuario",
        detalle=f"{usuario.correo}: {anterior} → {nuevo_rol}",
    )
    return usuario
