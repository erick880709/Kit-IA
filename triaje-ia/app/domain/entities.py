"""Entidades de dominio (TT-E1-02, HU-E1-01/03, HU-E2-01).

El resto del catálogo ENT-001..012 lo agrega `builder` historia a historia
según `resources/design/data-model.md`.
"""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.base import Base

ROLES_DEMO = ["Medico", "Enfermera", "Administrador", "Investigador", "Auditor"]


def _uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Rol(Base):
    """Rol de acceso (RF-014)."""

    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    usuarios: Mapped[list[Usuario]] = relationship(back_populates="rol")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Rol {self.nombre}>"


class Usuario(Base):
    """Usuario autenticable del sistema (HU-E1-01)."""

    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    correo: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(120), nullable=False)
    rol_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("roles.id"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    intentos_fallidos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bloqueado_hasta: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    token_recuperacion: Mapped[str | None] = mapped_column(String(120), nullable=True)
    token_expira: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    rol: Mapped[Rol] = relationship(back_populates="usuarios")


class Auditoria(Base):
    """Registro de auditoría (ENT-012, RF-013)."""

    __tablename__ = "auditoria"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    usuario_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("usuarios.id"), nullable=True
    )
    accion: Mapped[str] = mapped_column(String(80), nullable=False)
    entidad: Mapped[str] = mapped_column(String(60), nullable=False)
    detalle: Mapped[str | None] = mapped_column(Text, nullable=True)
    evento_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("eventos_triaje.id"), nullable=True, index=True
    )  # HU-E5-01 CA1: filtro por evento de triaje
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)


class Paciente(Base):
    """Paciente (ENT-001, HU-E2-01)."""

    __tablename__ = "pacientes"
    __table_args__ = (
        UniqueConstraint("tipo_documento", "numero_documento", name="uq_paciente_documento"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tipo_documento: Mapped[str] = mapped_column(String(4), nullable=False)
    numero_documento: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    sexo: Mapped[str] = mapped_column(String(30), nullable=False)
    via_llegada: Mapped[str] = mapped_column(String(20), nullable=False)
    episodios_previos_urgencias: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    correo: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contacto_emergencia: Mapped[str] = mapped_column(String(120), nullable=False)
    numero_contacto_emergencia: Mapped[str] = mapped_column(String(20), nullable=False)
    departamento: Mapped[str] = mapped_column(String(60), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(80), nullable=False)
    direccion_residencia: Mapped[str | None] = mapped_column(String(160), nullable=True)
    regimen: Mapped[str | None] = mapped_column(String(40), nullable=True)
    eps: Mapped[str | None] = mapped_column(String(80), nullable=True)
    tipo_sangre: Mapped[str | None] = mapped_column(String(5), nullable=True)
    alergias: Mapped[str | None] = mapped_column(String(200), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    actualizado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EventoTriaje(Base):
    """Evento de triaje con registro dual IA/profesional (ENT-002, RD-003) y
    máquina de 7 estados (HU-E2-06)."""

    __tablename__ = "eventos_triaje"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    paciente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("pacientes.id"), nullable=False, index=True
    )
    usuario_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("usuarios.id"), nullable=True
    )
    estado: Mapped[str] = mapped_column(String(40), default="Registrado", nullable=False)
    nivel_sugerido_ia: Mapped[str | None] = mapped_column(String(2), nullable=True)
    probabilidades_ia: Mapped[str | None] = mapped_column(Text, nullable=True)
    nivel_asignado_profesional: Mapped[str | None] = mapped_column(String(2), nullable=True)
    concordancia: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    motivo_discrepancia: Mapped[str | None] = mapped_column(Text, nullable=True)
    motivo_reclasificacion: Mapped[str | None] = mapped_column(Text, nullable=True)
    motivo_cierre: Mapped[str | None] = mapped_column(Text, nullable=True)
    version_modelo: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Épica E4 · inferencia real (HU-E4-01)
    algoritmo_modelo: Mapped[str | None] = mapped_column(String(60), nullable=True)
    fecha_inferencia: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    tiempo_inferencia_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    confianza_ia: Mapped[float | None] = mapped_column(Float, nullable=True)
    explicacion_shap: Mapped[str | None] = mapped_column(Text, nullable=True)
    evento_anterior_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("eventos_triaje.id"), nullable=True
    )
    inicio: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    cierre: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class SignosVitales(Base):
    """Signos vitales del evento (ENT-003, HU-E2-04)."""

    __tablename__ = "signos_vitales"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    evento_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("eventos_triaje.id"), nullable=False, unique=True
    )
    temperatura: Mapped[float] = mapped_column(Float, nullable=False)
    frecuencia_cardiaca: Mapped[int] = mapped_column(Integer, nullable=False)
    frecuencia_respiratoria: Mapped[int] = mapped_column(Integer, nullable=False)
    saturacion_o2: Mapped[int] = mapped_column(Integer, nullable=False)
    presion_sistolica: Mapped[int] = mapped_column(Integer, nullable=False)
    presion_diastolica: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    talla: Mapped[float] = mapped_column(Float, nullable=False)
    imc: Mapped[float] = mapped_column(Float, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)


class MotivoConsulta(Base):
    """Motivo de consulta con doble captura (ENT-004, HU-E2-05 CA1)."""

    __tablename__ = "motivos_consulta"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    evento_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("eventos_triaje.id"), nullable=False, unique=True
    )
    codigo_cie10: Mapped[str] = mapped_column(String(10), nullable=False)
    descripcion_estructurada: Mapped[str] = mapped_column(String(200), nullable=False)
    texto_libre: Mapped[str | None] = mapped_column(Text, nullable=True)


class EvaluacionClinica(Base):
    """Evaluación clínica (ENT-006 supuesto, HU-E2-05)."""

    __tablename__ = "evaluaciones_clinicas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    evento_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("eventos_triaje.id"), nullable=False, unique=True
    )
    escala_dolor: Mapped[int] = mapped_column(Integer, nullable=False)
    glasgow: Mapped[int] = mapped_column(Integer, nullable=False)
    nivel_conciencia: Mapped[str] = mapped_column(String(40), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)


class Antecedentes(Base):
    """Antecedentes por autorreporte (ENT-005, HU-E2-05 CA3)."""

    __tablename__ = "antecedentes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    paciente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("pacientes.id"), nullable=False, unique=True
    )
    diabetes: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hta: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    erc: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    embarazo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cancer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cardiopatias: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    epoc: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cirugias: Mapped[str | None] = mapped_column(Text, nullable=True)
    medicacion: Mapped[str | None] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Antecedentes {self.paciente_id}>"


class Modelo(Base):
    """Registro de modelos de IA desplegados (ENT-009, TT-E4-01).

    Una fila por versión serializada en artifacts/models con métricas y hash.
    """

    __tablename__ = "modelos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    version: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    algoritmo: Mapped[str] = mapped_column(String(60), nullable=False)
    fecha_entrenamiento: Mapped[date] = mapped_column(Date, nullable=False)
    metricas_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    ruta_artefacto: Mapped[str] = mapped_column(String(500), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Modelo {self.version}>"
