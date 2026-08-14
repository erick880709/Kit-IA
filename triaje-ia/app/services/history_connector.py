"""Conector de Historia Clínica Electrónica (TT-E1-04, RF-015).

Interfaz desacoplada lista para reemplazar `MockHCE` por una integración real
sin tocar el resto del sistema.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Antecedentes, Paciente


class HistoryConnector(ABC):
    """Puerto para obtener antecedentes clínicos de un paciente (RF-INT-001)."""

    @abstractmethod
    def obtener_antecedentes(self, session: Session, paciente: Paciente) -> dict | None:
        """Devuelve dict de antecedentes o None si no hay fuente disponible."""


class MockHCE(HistoryConnector):
    """Implementación demo: autorreporte guardado en la tabla local `antecedentes`.

    Devuelve None si el paciente aún no registró antecedentes (se piden en el
    formulario de evaluación clínica, HU-E2-05 CA3).
    """

    def obtener_antecedentes(self, session: Session, paciente: Paciente) -> dict | None:
        registro = session.scalar(
            select(Antecedentes).where(Antecedentes.paciente_id == paciente.id)
        )
        if registro is None:
            return None
        return {
            "diabetes": registro.diabetes,
            "hta": registro.hta,
            "erc": registro.erc,
            "embarazo": registro.embarazo,
            "cancer": registro.cancer,
            "cardiopatias": registro.cardiopatias,
            "epoc": registro.epoc,
            "cirugias": registro.cirugias,
            "medicacion": registro.medicacion,
        }


# Inyección simple (documentada en README): se reemplaza por el conector real.
history_connector: HistoryConnector = MockHCE()
