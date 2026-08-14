"""Base declarativa del ORM — vive en dominio para que las entidades no
dependan de infraestructura (ADR-001 del documento de arquitectura)."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base compartida por todos los modelos ORM del dominio."""
