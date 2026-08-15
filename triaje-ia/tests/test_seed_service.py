"""Pruebas del seed automático de la demo (idempotencia)."""

from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.base import Base
from app.domain.entities import Rol, Usuario
from app.services.seed_service import ROLES_DEMO, seed_demo_si_vacio


def _session() -> Session:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_seed_demo_si_vacio_crea_roles_y_usuarios() -> None:
    with _session() as session:
        creados = seed_demo_si_vacio(session)
        assert creados == 5
        assert len(session.scalars(select(Rol)).all()) == len(ROLES_DEMO)
        assert len(session.scalars(select(Usuario)).all()) == 5


def test_seed_demo_es_idempotente() -> None:
    with _session() as session:
        seed_demo_si_vacio(session)
        segunda = seed_demo_si_vacio(session)
    assert segunda == 0
