"""Pruebas del manual de uso por rol y del acceso a pantallas de soporte."""

from __future__ import annotations

from app.services import authorization_service
from app.views.manual_uso import (
    contenido_manual,
    pantallas_rbac_del_rol,
)

ROLES = ("Medico", "Enfermera", "Administrador", "Investigador", "Auditor")


def test_todos_los_roles_pueden_ver_manual_y_acerca_de() -> None:
    for rol in ROLES:
        assert authorization_service.puede_acceder(rol, "manual_uso"), rol
        assert authorization_service.puede_acceder(rol, "acerca_de"), rol


def test_cada_rol_tiene_su_manual_completo() -> None:
    for rol in ROLES:
        manual = contenido_manual(rol)
        assert manual is not None, f"falta manual para {rol}"
        assert manual["titulo"]
        assert manual["descripcion"]
        assert manual["imagen"].endswith(".png")
        assert manual["animacion"].endswith(".gif")
        assert manual["pantallas"], f"manual de {rol} sin pantallas"
        assert manual["advertencias"]
        for pantalla in manual["pantallas"]:
            assert pantalla["nombre"] and pantalla["objetivo"]
            assert pantalla["pasos"], f"{rol}: pantalla sin pasos ({pantalla['nombre']})"


def test_manual_desconocido_devuelve_none() -> None:
    assert contenido_manual("RolInexistente") is None


def test_manual_solo_ensena_pantallas_permitidas_al_rol() -> None:
    """Invariante de RBAC: cada manual cubre únicamente pantallas que el rol
    puede abrir, y coincide en cantidad con el inventario de pantallas del rol."""
    for rol in ROLES:
        manual = contenido_manual(rol)
        permitidas = pantallas_rbac_del_rol(rol)
        assert permitidas, f"sin inventario de pantallas para {rol}"
        assert len(manual["pantallas"]) == len(permitidas), (
            f"{rol}: el manual cubre {len(manual['pantallas'])} pantallas pero "
            f"el inventario RBAC tiene {len(permitidas)}"
        )
        for pantalla_id in permitidas:
            assert authorization_service.puede_acceder(rol, pantalla_id), (
                f"{rol} no puede acceder a {pantalla_id}"
            )


def test_los_manuales_difieren_entre_roles() -> None:
    """Cada rol ve SU manual: los títulos son distintos entre sí."""
    titulos = {contenido_manual(rol)["titulo"] for rol in ROLES}
    assert len(titulos) == len(ROLES)
