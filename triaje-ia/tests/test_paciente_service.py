"""Pruebas del registro de pacientes (HU-E2-01)."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Auditoria
from app.domain.exceptions import ValidationError
from app.services.paciente_service import (
    buscar_duplicados,
    buscar_por_documento,
    datos_precarga,
    registrar_paciente,
)


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as s:
        yield s


def _datos(**overrides) -> dict:
    datos = {
        "tipo_documento": "CC",
        "numero_documento": "52148903",
        "nombres": "María",
        "apellidos": "Gómez Ruiz",
        "fecha_nacimiento": date(1986, 2, 12),
        "sexo": "Femenino",
        "via_llegada": "Ambulancia",
        "episodios_previos_urgencias": 2,
        "telefono": "+57 300 123 4567",
        "correo": "m.gomez@correo.com",
        "contacto_emergencia": "Carlos Gómez",
        "numero_contacto_emergencia": "3107654321",
        "departamento": "Cundinamarca",
        "ciudad": "Bogotá D.C.",
        "direccion_residencia": "Calle 10 # 5-20",
        "regimen": "Contributivo",
        "tipo_sangre": "O+",
        "alergias": "Penicilina",
    }
    datos.update(overrides)
    return datos


def test_ca1_registro_completo_con_via_y_episodios(session: Session) -> None:
    p = registrar_paciente(session, usuario_id=None, datos=_datos())
    assert p.via_llegada == "Ambulancia"
    assert p.episodios_previos_urgencias == 2
    assert p.tipo_documento == "CC"


def test_ca3_obligatorios_no_vacios(session: Session) -> None:
    for campo in ("nombres", "numero_documento", "departamento", "ciudad"):
        with pytest.raises(ValidationError) as exc:
            registrar_paciente(session, usuario_id=None, datos=_datos(**{campo: ""}))
        assert exc.value.detalle == campo


def test_contacto_emergencia_es_opcional(session: Session) -> None:
    """Regla de negocio: no todos los pacientes tienen contacto de emergencia."""
    p = registrar_paciente(
        session,
        usuario_id=None,
        datos=_datos(contacto_emergencia="", numero_contacto_emergencia=""),
    )
    assert p.contacto_emergencia == ""
    assert p.numero_contacto_emergencia == ""


def test_eps_se_guarda_para_regimen_subsidiado(session: Session) -> None:
    p = registrar_paciente(
        session,
        usuario_id=None,
        datos=_datos(regimen="Subsidiado", eps="Nueva EPS"),
    )
    assert p.eps == "Nueva EPS"


def test_catalogo_quindio_completo() -> None:
    from app.domain.catalogos import CIUDADES_POR_DEPARTAMENTO

    quindio = CIUDADES_POR_DEPARTAMENTO["Quindío"]
    assert set(quindio) == {
        "Armenia", "Buenavista", "Calarcá", "Circasia", "Córdoba", "Filandia",
        "Génova", "La Tebaida", "Montenegro", "Pijao", "Quimbaya", "Salento",
    }
    # Todo departamento debe listar al menos sus municipios principales.
    assert all(len(CIUDADES_POR_DEPARTAMENTO[d]) >= 1 for d in CIUDADES_POR_DEPARTAMENTO)


def test_catalogo_motivos_integridad_y_trauma_presente() -> None:
    """El catálogo de motivos debe tener códigos únicos, descripciones y
    categorías no vacías, y cubrir trauma y motivos frecuentes."""
    from app.domain.catalogos import CATALOGO_MOTIVOS

    codigos = [codigo for codigo, _, _ in CATALOGO_MOTIVOS]
    assert len(codigos) == len(set(codigos)), "códigos CIE-10 duplicados"
    assert all(desc.strip() for _, desc, _ in CATALOGO_MOTIVOS)
    assert all(cat.strip() for _, _, cat in CATALOGO_MOTIVOS)
    descripciones = " | ".join(desc for _, desc, _ in CATALOGO_MOTIVOS).casefold()
    for motivo in ("fractura", "arma de fuego", "cortopunzante", "quemadura",
                   "estreñimiento", "tos", "disnea", "taquicardia", "celulitis"):
        assert motivo in descripciones, f"falta motivo: {motivo}"
    # Categorías esperadas del catálogo clínico
    categorias = {cat for _, _, cat in CATALOGO_MOTIVOS}
    assert {"Digestivo", "Respiratorio", "Neurológico", "Cardiovascular",
            "Trauma", "Salud mental", "Signos/Síntomas generales"} <= categorias


def test_ca3_telefono_minimo_10_digitos_y_acepta_57(session: Session) -> None:
    p = registrar_paciente(session, usuario_id=None, datos=_datos(telefono="+57 300 123 4567"))
    assert p.telefono == "3001234567"  # normalizado a 10 dígitos locales

    with pytest.raises(ValidationError):
        registrar_paciente(session, usuario_id=None, datos=_datos(telefono="300123"))
    with pytest.raises(ValidationError):
        registrar_paciente(
            session, usuario_id=None, datos=_datos(numero_contacto_emergencia="123")
        )


def test_episodios_previos_no_numericos_rechazados(session: Session) -> None:
    """Frontera externa: valor no numérico → ValidationError, nunca ValueError."""
    with pytest.raises(ValidationError) as exc:
        registrar_paciente(
            session, usuario_id=None,
            datos=_datos(episodios_previos_urgencias="muchos"),
        )
    assert exc.value.detalle == "episodios_previos_urgencias"


def test_ca3_correo_invalido_rechaza_y_vacio_permitido(session: Session) -> None:
    with pytest.raises(ValidationError):
        registrar_paciente(session, usuario_id=None, datos=_datos(correo="no-es-correo"))
    p = registrar_paciente(session, usuario_id=None, datos=_datos(correo=""))
    assert p.correo is None


def test_ca2_duplicado_por_documento(session: Session) -> None:
    registrar_paciente(session, usuario_id=None, datos=_datos())
    dup = buscar_duplicados(
        session,
        tipo_documento="CC",
        numero_documento="52148903",
        nombres="Otra",
        apellidos="Persona",
    )
    assert len(dup) == 1


def test_ca2_duplicado_por_nombre_apellidos(session: Session) -> None:
    registrar_paciente(session, usuario_id=None, datos=_datos(numero_documento="999"))
    dup = buscar_duplicados(
        session,
        tipo_documento="CC",
        numero_documento="123456",
        nombres="María",
        apellidos="Gómez",
    )
    assert any(p.numero_documento == "999" for p in dup)


def test_documento_duplicado_bloquea_alta(session: Session) -> None:
    registrar_paciente(session, usuario_id=None, datos=_datos())
    with pytest.raises(ValidationError):
        registrar_paciente(
            session, usuario_id=None, datos=_datos(numero_documento="52148903")
        )


def test_ca4_alta_queda_auditada(session: Session) -> None:
    registrar_paciente(session, usuario_id="usr-1", datos=_datos())
    registros = session.query(Auditoria).all()
    assert any(r.accion == "CREAR_PACIENTE" and r.usuario_id == "usr-1" for r in registros)


# ---------- Ajuste: nuevo triaje para paciente existente ----------

def test_buscar_por_documento_exacto_devuelve_paciente(session: Session) -> None:
    """Verificación por documento: coincide aunque el tipo llegue en minúsculas."""
    p = registrar_paciente(session, usuario_id=None, datos=_datos())
    encontrado = buscar_por_documento(
        session, tipo_documento="cc", numero_documento=" 52148903 "
    )
    assert encontrado is not None
    assert encontrado.id == p.id


def test_buscar_por_documento_sin_coincidencias_devuelve_none(session: Session) -> None:
    registrar_paciente(session, usuario_id=None, datos=_datos())
    assert (
        buscar_por_documento(session, tipo_documento="CC", numero_documento="999")
        is None
    )
    assert (
        buscar_por_documento(session, tipo_documento="CC", numero_documento="")
        is None
    )


def test_buscar_duplicados_con_formulario_vacio_no_devuelve_todos(
    session: Session,
) -> None:
    """Guard: verificar con el formulario vacío no debe tratar a TODOS como duplicados."""
    registrar_paciente(session, usuario_id=None, datos=_datos())
    dup = buscar_duplicados(
        session,
        tipo_documento="CC",
        numero_documento="",
        nombres="",
        apellidos="",
    )
    assert dup == []


def test_datos_precarga_mapean_todos_los_campos_del_formulario(session: Session) -> None:
    p = registrar_paciente(session, usuario_id=None, datos=_datos())
    precarga = datos_precarga(p)
    assert precarga == {
        "tipo_documento": "CC",
        "numero_documento": "52148903",
        "nombres": "María",
        "apellidos": "Gómez Ruiz",
        "fecha_nacimiento": date(1986, 2, 12),
        "sexo": "Femenino",
        "via_llegada": "Ambulancia",
        "episodios_previos_urgencias": 2,
        "telefono": "3001234567",
        "correo": "m.gomez@correo.com",
        "contacto_emergencia": "Carlos Gómez",
        "numero_contacto_emergencia": "3107654321",
        "departamento": "Cundinamarca",
        "ciudad": "Bogotá D.C.",
        "direccion_residencia": "Calle 10 # 5-20",
        "regimen": "Contributivo",
        "eps": "",
        "tipo_sangre": "O+",
        "alergias": "Penicilina",
    }


def test_datos_precarga_opcionales_none_se_mapean_a_vacio(session: Session) -> None:
    p = registrar_paciente(
        session,
        usuario_id=None,
        datos=_datos(
            telefono="",
            correo="",
            direccion_residencia="",
            regimen="",
            eps="",
            tipo_sangre="",
            alergias="",
        ),
    )
    precarga = datos_precarga(p)
    assert precarga["telefono"] == ""
    assert precarga["correo"] == ""
    assert precarga["eps"] == ""
    assert precarga["regimen"] == ""
    assert precarga["tipo_sangre"] == ""
    assert precarga["alergias"] == ""
