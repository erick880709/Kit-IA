"""Servicio de pacientes (HU-E2-01).

CA1: captura ENT-001 completa con ViaLlegada y EpisodiosPreviosUrgencias.
CA2: búsqueda de duplicados por documento y por nombre/apellidos.
CA3: obligatorios no vacíos, teléfono ≥10 dígitos aceptando +57, correo válido.
CA4: modificaciones registradas en auditoría (ControlCambios).
"""

from __future__ import annotations

import re
from datetime import UTC, datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.domain.catalogos import SEXO, VIA_LLEGADA
from app.domain.entities import Paciente
from app.domain.exceptions import ValidationError
from app.services import audit_service

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalizar_telefono(telefono: str) -> str:
    """Acepta formatos +57 300..., (57) 300..., 300... — valida ≥10 dígitos."""
    digitos = re.sub(r"\D", "", telefono)
    if digitos.startswith("57") and len(digitos) == 12:
        digitos = digitos[2:]  # +57 nacional → local de 10
    if len(digitos) < 10:
        raise ValidationError("El teléfono debe tener al menos 10 dígitos", detalle=telefono)
    return digitos


def _validar_campos(datos: dict) -> None:
    obligatorios = [
        "tipo_documento",
        "numero_documento",
        "nombres",
        "apellidos",
        "fecha_nacimiento",
        "sexo",
        "via_llegada",
        "departamento",
        "ciudad",
    ]
    for campo in obligatorios:
        valor = datos.get(campo)
        if valor is None or str(valor).strip() == "":
            raise ValidationError("Campo obligatorio ausente", detalle=campo)
    if datos["via_llegada"] not in VIA_LLEGADA:
        raise ValidationError("Vía de llegada inválida", detalle=str(datos["via_llegada"]))
    if datos["sexo"] not in SEXO:
        raise ValidationError("Sexo inválido", detalle=str(datos["sexo"]))
    if datos.get("telefono"):
        datos["telefono"] = _normalizar_telefono(datos["telefono"])
    # Contacto de emergencia OPCIONAL: si trae teléfono, debe ser válido.
    if (datos.get("numero_contacto_emergencia") or "").strip():
        datos["numero_contacto_emergencia"] = _normalizar_telefono(
            datos["numero_contacto_emergencia"]
        )
    if datos.get("correo"):
        if not _EMAIL_RE.match(datos["correo"].strip()):
            raise ValidationError("Correo inválido", detalle=str(datos["correo"]))


def buscar_duplicados(
    session: Session, *, tipo_documento: str, numero_documento: str,
    nombres: str, apellidos: str,
) -> list[Paciente]:
    """CA2: duplicado exacto por documento o coincidencia por nombre+apellidos."""
    por_documento = session.scalars(
        select(Paciente).where(
            Paciente.tipo_documento == tipo_documento.strip().upper(),
            Paciente.numero_documento == numero_documento.strip(),
        )
    ).all()
    if por_documento:
        return list(por_documento)

    nombre = nombres.strip().casefold()
    apellido = apellidos.strip().casefold()
    return list(
        session.scalars(
            select(Paciente).where(
                or_(
                    Paciente.nombres.ilike(f"%{nombre}%"),
                    Paciente.apellidos.ilike(f"%{apellido}%"),
                )
            )
        ).all()
    )


def registrar_paciente(
    session: Session, *, usuario_id: str | None, datos: dict
) -> Paciente:
    """Registra paciente validando CA3 y registra el alta en auditoría (CA4)."""
    datos = dict(datos)
    _validar_campos(datos)

    tipo_doc = datos["tipo_documento"].strip().upper()
    num_doc = datos["numero_documento"].strip()
    existente = session.scalar(
        select(Paciente).where(
            Paciente.tipo_documento == tipo_doc, Paciente.numero_documento == num_doc
        )
    )
    if existente is not None:
        raise ValidationError(
            "Ya existe un paciente con ese documento", detalle=f"{tipo_doc} {num_doc}"
        )

    try:
        episodios = int(datos.get("episodios_previos_urgencias") or 0)
    except (TypeError, ValueError):
        raise ValidationError(
            "Episodios previos inválidos — debe ser un número entero",
            detalle="episodios_previos_urgencias",
        ) from None
    if episodios < 0:
        raise ValidationError(
            "Episodios previos no puede ser negativo",
            detalle="episodios_previos_urgencias",
        )

    paciente = Paciente(
        tipo_documento=tipo_doc,
        numero_documento=num_doc,
        nombres=datos["nombres"].strip(),
        apellidos=datos["apellidos"].strip(),
        fecha_nacimiento=datos["fecha_nacimiento"],
        sexo=datos["sexo"],
        via_llegada=datos["via_llegada"],
        episodios_previos_urgencias=episodios,
        telefono=datos.get("telefono"),
        correo=(datos.get("correo") or "").strip() or None,
        contacto_emergencia=(datos.get("contacto_emergencia") or "").strip() or "",
        numero_contacto_emergencia=(
            (datos.get("numero_contacto_emergencia") or "").strip() or ""
        ),
        departamento=datos["departamento"],
        ciudad=datos["ciudad"],
        direccion_residencia=(datos.get("direccion_residencia") or "").strip() or None,
        regimen=datos.get("regimen"),
        eps=(datos.get("eps") or "").strip() or None,
        tipo_sangre=datos.get("tipo_sangre"),
        alergias=(datos.get("alergias") or "").strip() or None,
    )
    session.add(paciente)
    session.commit()
    audit_service.registrar(
        session,
        usuario_id=usuario_id,
        accion="CREAR_PACIENTE",
        entidad="Paciente",
        detalle=f"{tipo_doc} {num_doc} · {paciente.nombres} {paciente.apellidos}",
    )
    return paciente


def actualizar_paciente(
    session: Session, *, paciente_id: str, usuario_id: str | None, datos: dict
) -> Paciente:
    """Actualiza datos de contacto/demográficos registrando el cambio (CA4)."""
    paciente = session.get(Paciente, paciente_id)
    if paciente is None:
        raise ValidationError("Paciente inexistente", detalle=paciente_id)
    datos = dict(datos)
    _validar_campos({**{
        "tipo_documento": paciente.tipo_documento,
        "numero_documento": paciente.numero_documento,
        "nombres": paciente.nombres,
        "apellidos": paciente.apellidos,
        "fecha_nacimiento": paciente.fecha_nacimiento,
        "sexo": paciente.sexo,
        "via_llegada": paciente.via_llegada,
        "departamento": paciente.departamento,
        "ciudad": paciente.ciudad,
    }, **datos})

    for campo in ("telefono", "correo", "contacto_emergencia", "numero_contacto_emergencia",
                  "direccion_residencia", "regimen", "eps", "tipo_sangre", "alergias"):
        if campo in datos and datos[campo] is not None:
            setattr(paciente, campo, (str(datos[campo]).strip() or None))
    paciente.actualizado_en = datetime.now(UTC)
    audit_service.registrar(
        session,
        usuario_id=usuario_id,
        accion="ACTUALIZAR_PACIENTE",
        entidad="Paciente",
        detalle=paciente_id,
        commit=False,
    )
    session.commit()
    return paciente


def actualizar_alergias(
    session: Session, *, paciente_id: str, alergias: str, usuario_id: str | None
) -> Paciente:
    """Actualiza alergias conocidas con auditoría (usado por HU-E2-05).

    Evita la mutación directa del modelo desde la vista (hallazgo de
    revision-calidad: sin servicio ni auditoría).
    """
    paciente = session.get(Paciente, paciente_id)
    if paciente is None:
        raise ValidationError("Paciente inexistente", detalle=paciente_id)
    nuevo = alergias.strip() or None
    paciente.alergias = nuevo
    paciente.actualizado_en = datetime.now(UTC)
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="ACTUALIZAR_ALERGIAS",
        entidad="Paciente", detalle=paciente_id, commit=False,
    )
    session.commit()
    return paciente
