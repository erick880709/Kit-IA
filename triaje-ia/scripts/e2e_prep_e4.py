"""Precarga E2E de la Épica E4: paciente + evento hasta EvaluacionClinica.

Usa los mismos servicios que la UI para dejar el evento listo para
clasificacion_ia (inferencia real). Idempotente por documento.
Uso:  python scripts/e2e_prep_e4.py
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import select

from app.domain.entities import Paciente
from app.infra.db import SessionLocal, init_db
from app.services import triaje_service

DOCUMENTO = "53012487"
USUARIO = "usr-medico-e4"


def main() -> None:
    init_db()
    with SessionLocal() as session:
        paciente = session.scalar(
            select(Paciente).where(Paciente.numero_documento == DOCUMENTO)
        )
        if paciente is None:
            paciente = Paciente(
                tipo_documento="CC",
                numero_documento=DOCUMENTO,
                nombres="Andrea",
                apellidos="López Sandoval",
                fecha_nacimiento=date(1990, 5, 12),
                sexo="Femenino",
                via_llegada="Ambulancia",
                episodios_previos_urgencias=1,
                telefono="3001112233",
                contacto_emergencia="Juan López",
                numero_contacto_emergencia="3101112233",
                departamento="Cundinamarca",
                ciudad="Bogotá D.C.",
                direccion_residencia="Cra 10 # 5-20",
                regimen="Subsidiado",
            )
            session.add(paciente)
            session.commit()
            print("paciente creado")

        evento = triaje_service.crear_evento(
            session, paciente_id=paciente.id, usuario_id=USUARIO
        )
        triaje_service.registrar_signos(
            session, evento_id=evento.id, usuario_id=USUARIO,
            datos={
                "temperatura": 38.9,
                "frecuencia_cardiaca": 121,
                "frecuencia_respiratoria": 30,
                "saturacion_o2": 86,
                "presion_sistolica": 98,
                "presion_diastolica": 62,
                "peso": 64.0,
                "talla": 1.62,
            },
        )
        triaje_service.registrar_evaluacion(
            session, evento_id=evento.id, usuario_id=USUARIO,
            datos={
                "codigo_cie10": "R07.4",
                "descripcion_estructurada": "Dolor torácico no especificado",
                "texto_libre": "Dolor opresivo retroesternal de 2 horas con disnea",
                "escala_dolor": 8,
                "glasgow": 15,
                "nivel_conciencia": "Alerta",
                "observaciones": "Sudoración profusa",
            },
        )
        print(f"evento listo para clasificacion_ia: {evento.id}")
        print(f"paciente_id: {paciente.id}")


if __name__ == "__main__":
    main()
