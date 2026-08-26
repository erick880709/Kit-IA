"""Servicio del flujo de triaje (HU-E2-04 a HU-E2-08).

- Máquina de 7 estados con transiciones validadas en backend (E2-06).
- Signos vitales con rangos fisiológicos y alertas (E2-04).
- Evaluación clínica con doble captura de motivo (E2-05).
- Clasificación IA simulada (se reemplaza por el modelo real en Épica E4).
- Validación profesional con concordancia calculada (E2-08, RD-003).
- Reclasificación como evento separado con trazabilidad (E2-07).
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.catalogos import (
    NIVEL_CONCIENCIA,
    RANGOS_SIGNOS,
    TRANSICIONES_VALIDAS,
    ESTADOS_TRIaje,
    NIVELES_TRIaje,
)
from app.domain.entities import (
    Antecedentes,
    EvaluacionClinica,
    EventoTriaje,
    MotivoConsulta,
    Paciente,
    SignosVitales,
)
from app.domain.exceptions import ValidationError
from app.services import audit_service

logger = logging.getLogger(__name__)

# Regla de aplicabilidad del sistema de recomendación IA (ámbito adulto,
# Res. 5596/2015): aplica SOLO a personas entre 16 y 60 años (inclusive).
EDAD_MINIMA_TRIaje_IA = 16
EDAD_MAXIMA_TRIaje_IA = 60

_MOTIVO_SUFIJO_FUERA_RANGO = (
    "el sistema de recomendación IA no aplica; el diagnóstico del nivel de urgencia "
    "recae 100% en el profesional y el triaje de la herramienta no puede usarse "
    "como apoyo."
)

MOTIVO_CIERRE_MENOR = (
    f"Paciente menor de 16 años (fuera del rango {EDAD_MINIMA_TRIaje_IA}-"
    f"{EDAD_MAXIMA_TRIaje_IA} años) — {_MOTIVO_SUFIJO_FUERA_RANGO}"
)

MOTIVO_CIERRE_MAYOR = (
    f"Paciente mayor de 60 años (fuera del rango {EDAD_MINIMA_TRIaje_IA}-"
    f"{EDAD_MAXIMA_TRIaje_IA} años) — {_MOTIVO_SUFIJO_FUERA_RANGO}"
)

# ---------- Búsqueda e historial (HU-E2-02 / HU-E2-03) ----------

def buscar_pacientes(
    session: Session, *, termino: str, page: int = 1, page_size: int = 20
) -> tuple[list[Paciente], int]:
    """CA1: búsqueda por documento exacto, nombre o apellidos parciales.
    CA2: resultados paginados."""
    termino = termino.strip()
    if not termino:
        return [], 0
    if termino.isdigit():
        cond = Paciente.numero_documento == termino
    else:
        patron = f"%{termino.casefold()}%"
        cond = Paciente.nombres.ilike(patron) | Paciente.apellidos.ilike(patron)
    total = len(session.scalars(select(Paciente).where(cond)).all())
    items = list(
        session.scalars(
            select(Paciente).where(cond)
            .order_by(Paciente.apellidos)
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).all()
    )
    return items, total


def historial_eventos(session: Session, *, paciente_id: str) -> list[EventoTriaje]:
    """CA1: listado cronológico de eventos (más reciente primero)."""
    return list(
        session.scalars(
            select(EventoTriaje)
            .where(EventoTriaje.paciente_id == paciente_id)
            .order_by(EventoTriaje.inicio.desc())
        ).all()
    )


# ---------- Máquina de estados (HU-E2-06) ----------

def edad_en_anios(fecha_nacimiento: date, hoy: date | None = None) -> int:
    """Edad exacta en años cumplidos. `hoy` inyectable para tests deterministas."""
    hoy = hoy or date.today()
    anios = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        anios -= 1
    return anios


def crear_evento(
    session: Session,
    *,
    paciente_id: str,
    usuario_id: str | None,
    hoy: date | None = None,
) -> EventoTriaje:
    """Crea el evento y aplica la regla de aplicabilidad por edad:

    - Entre 16 y 60 años (inclusive): flujo normal con recomendación IA.
    - Fuera de ese rango (menor de 16 o mayor de 60): NO se aplica la
      recomendación IA; el evento queda cerrado automáticamente y el
      diagnóstico del nivel de urgencia recae 100% en el profesional,
      dejando trazabilidad completa en auditoría.
    """
    paciente = session.get(Paciente, paciente_id)
    if paciente is None:
        raise ValidationError("Paciente inexistente", detalle=paciente_id)
    evento = EventoTriaje(paciente_id=paciente_id, usuario_id=usuario_id, estado="Registrado")
    session.add(evento)
    session.flush()  # genera evento.id (default en INSERT) antes de usarlo
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="CREAR_EVENTO",
        entidad="EventoTriaje", detalle=evento.id, commit=False,
    )
    edad = edad_en_anios(paciente.fecha_nacimiento, hoy)
    if not (EDAD_MINIMA_TRIaje_IA <= edad <= EDAD_MAXIMA_TRIaje_IA):
        es_menor = edad < EDAD_MINIMA_TRIaje_IA
        motivo = MOTIVO_CIERRE_MENOR if es_menor else MOTIVO_CIERRE_MAYOR
        accion = "CIERRE_AUTOMATICO_MENOR" if es_menor else "CIERRE_AUTOMATICO_MAYOR"
        transicionar_estado(
            session, evento_id=evento.id, nuevo_estado="Cerrado", usuario_id=usuario_id
        )
        evento.cierre = datetime.now(UTC)
        evento.motivo_cierre = motivo
        audit_service.registrar(
            session, usuario_id=usuario_id, accion=accion,
            entidad="EventoTriaje", evento_id=evento.id,
            detalle=f"{evento.id} · {motivo}", commit=False,
        )
        logger.info(
            "Evento %s creado y cerrado automáticamente: paciente %s (%s años, "
            "fuera del rango %s-%s) — sin recomendación IA, diagnóstico 100%% "
            "a cargo del profesional",
            evento.id, paciente_id, edad, EDAD_MINIMA_TRIaje_IA, EDAD_MAXIMA_TRIaje_IA,
        )
    session.commit()  # cambio + auditoría en una sola transacción
    logger.info(
        "Evento de triaje creado: %s (paciente %s, usuario %s, estado %s)",
        evento.id, paciente_id, usuario_id, evento.estado,
    )
    return evento


def transicionar_estado(
    session: Session, *, evento_id: str, nuevo_estado: str, usuario_id: str | None
) -> EventoTriaje:
    """CA2: solo transiciones válidas; CA3: cambio auditado (misma transacción).

    No commitea: el llamante persiste el cambio junto con su auditoría en un
    único commit.
    """
    evento = session.get(EventoTriaje, evento_id)
    if evento is None:
        raise ValidationError("Evento inexistente", detalle=evento_id)
    if nuevo_estado not in ESTADOS_TRIaje:
        raise ValidationError("Estado inválido", detalle=nuevo_estado)
    if nuevo_estado not in TRANSICIONES_VALIDAS.get(evento.estado, set()):
        raise ValidationError(
            f"Transición inválida: {evento.estado} → {nuevo_estado}",
            detalle=evento_id,
        )
    estado_anterior = evento.estado
    evento.estado = nuevo_estado
    logger.info(
        "Transición de estado: %s → %s (evento %s, usuario %s)",
        estado_anterior, nuevo_estado, evento_id, usuario_id,
    )
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="CAMBIO_ESTADO",
        entidad="EventoTriaje", detalle=f"{evento_id}: {nuevo_estado}",
        commit=False,
    )
    return evento


# ---------- Signos vitales (HU-E2-04) ----------

def normalizar_talla_m(valor: float) -> tuple[float, bool]:
    """Talla en metros. Si llega en centímetros (> 3 m), convierte e informa.

    Evita el error clásico de IMC ≈ 0 cuando se digita 170 en vez de 1.70.
    """
    if valor > 3.0:
        return valor / 100.0, True
    return valor, False


def _validar_signos(datos: dict, *, permitir_fuera_rango: bool = False) -> dict:
    for campo in (
        "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
        "saturacion_o2", "presion_sistolica", "presion_diastolica", "peso", "talla",
    ):
        valor = datos.get(campo)
        if valor is None or valor == "":
            raise ValidationError("Campo obligatorio ausente", detalle=campo)
        minimo, maximo, unidad, _ = RANGOS_SIGNOS[campo]
        try:
            num = float(valor)
        except ValueError:
            raise ValidationError("Valor numérico inválido", detalle=campo) from None
        if campo == "talla":
            num, _ = normalizar_talla_m(num)
        if not permitir_fuera_rango and not (minimo <= num <= maximo):
            raise ValidationError(
                f"{campo} fuera de rango fisiológico ({minimo}-{maximo} {unidad})",
                detalle=campo,
            )
        datos[campo] = num
    return datos


def registrar_signos(
    session: Session,
    *,
    evento_id: str,
    usuario_id: str | None,
    datos: dict,
    confirmar_fuera_rango: bool = False,
) -> SignosVitales:
    """CA1: 8 signos + IMC; CA2: fuera de rango exige confirmación explícita.

    Validación ANTES de transicionar: un intento fallido no deja el evento
    atascado (hallazgo bloqueante de revision-calidad).
    """
    datos = _validar_signos(dict(datos), permitir_fuera_rango=confirmar_fuera_rango)
    existente = session.scalar(
        select(SignosVitales).where(SignosVitales.evento_id == evento_id)
    )
    if existente is not None:
        raise ValidationError("Los signos vitales ya fueron registrados", detalle=evento_id)
    evento = transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="SignosVitales", usuario_id=usuario_id
    )
    imc = round(datos["peso"] / (datos["talla"] ** 2), 1)
    signos = SignosVitales(
        evento_id=evento.id,
        temperatura=datos["temperatura"],
        frecuencia_cardiaca=int(datos["frecuencia_cardiaca"]),
        frecuencia_respiratoria=int(datos["frecuencia_respiratoria"]),
        saturacion_o2=int(datos["saturacion_o2"]),
        presion_sistolica=int(datos["presion_sistolica"]),
        presion_diastolica=int(datos["presion_diastolica"]),
        peso=datos["peso"],
        talla=datos["talla"],
        imc=imc,
    )
    session.add(signos)
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="REGISTRAR_SIGNOS",
        entidad="EventoTriaje", detalle=evento_id, commit=False,
    )
    session.commit()
    logger.info(
        "Signos vitales registrados: evento %s (IMC %.1f, usuario %s)",
        evento_id, imc, usuario_id,
    )
    return signos


# ---------- Evaluación clínica (HU-E2-05) ----------

def registrar_evaluacion(
    session: Session, *, evento_id: str, usuario_id: str | None, datos: dict
) -> tuple[MotivoConsulta, EvaluacionClinica]:
    codigo = datos.get("codigo_cie10")
    descripcion = datos.get("descripcion_estructurada")
    if codigo in (None, "") or descripcion in (None, ""):
        raise ValidationError("Motivo de consulta estructurado obligatorio", detalle="motivo")

    try:
        dolor = int(datos.get("escala_dolor", 0))
    except (TypeError, ValueError):
        raise ValidationError(
            "Escala de dolor inválida — debe ser un número entero 0-10",
            detalle="escala_dolor",
        ) from None
    if not 0 <= dolor <= 10:
        raise ValidationError("Dolor fuera de rango 0-10", detalle="escala_dolor")
    try:
        glasgow = int(datos.get("glasgow", 15))
    except (TypeError, ValueError):
        raise ValidationError(
            "Glasgow inválido — debe ser un número entero 3-15",
            detalle="glasgow",
        ) from None
    if not 3 <= glasgow <= 15:
        raise ValidationError("Glasgow fuera de rango 3-15", detalle="glasgow")
    conciencia = datos.get("nivel_conciencia")
    if conciencia not in NIVEL_CONCIENCIA:
        raise ValidationError("Nivel de conciencia inválido", detalle=str(conciencia))

    evento = transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="EvaluacionClinica", usuario_id=usuario_id
    )

    motivo = MotivoConsulta(
        evento_id=evento.id,
        codigo_cie10=codigo,
        descripcion_estructurada=descripcion,
        texto_libre=(datos.get("texto_libre") or "").strip() or None,  # CA4: vacío no bloquea
    )
    evaluacion = EvaluacionClinica(
        evento_id=evento.id,
        escala_dolor=dolor,
        glasgow=glasgow,
        nivel_conciencia=conciencia,
        observaciones=(datos.get("observaciones") or "").strip() or None,
    )
    session.add_all([motivo, evaluacion])
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="REGISTRAR_EVALUACION",
        entidad="EventoTriaje", detalle=f"{evento_id} · {codigo}", commit=False,
    )
    session.commit()
    logger.info(
        "Evaluación clínica registrada: evento %s (CIE-11 %s, usuario %s)",
        evento_id, codigo, usuario_id,
    )
    return motivo, evaluacion


def guardar_antecedentes(
    session: Session, *, paciente_id: str, antecedentes: dict, usuario_id: str | None
) -> Antecedentes:
    """CA3: autorreporte persistido (lo consume MockHCE en el siguiente evento)."""
    registro = session.scalar(
        select(Antecedentes).where(Antecedentes.paciente_id == paciente_id)
    )
    campos = ("diabetes", "hta", "erc", "embarazo", "cancer", "cardiopatias", "epoc")
    if registro is None:
        registro = Antecedentes(
            paciente_id=paciente_id,
            **{campo: bool(antecedentes.get(campo)) for campo in campos},
            cirugias=(antecedentes.get("cirugias") or "").strip() or None,
            medicacion=(antecedentes.get("medicacion") or "").strip() or None,
        )
        session.add(registro)
    else:
        for campo in campos:
            setattr(registro, campo, bool(antecedentes.get(campo)))
        registro.cirugias = (antecedentes.get("cirugias") or "").strip() or None
        registro.medicacion = (antecedentes.get("medicacion") or "").strip() or None
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="ACTUALIZAR_ANTECEDENTES",
        entidad="Paciente", detalle=paciente_id, commit=False,
    )
    session.commit()
    return registro


# ---------- Clasificación IA simulada + validación (E2-08, RD-003) ----------

def registrar_clasificacion_ia_simulada(
    session: Session, *, evento_id: str, nivel_sugerido: str, usuario_id: str | None
) -> EventoTriaje:
    """Etapa ClasificacionIA con inferencia simulada (Épica E4 la reemplaza)."""
    if nivel_sugerido not in NIVELES_TRIaje:
        raise ValidationError("Nivel inválido", detalle=nivel_sugerido)
    evento = transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="ClasificacionIA", usuario_id=usuario_id
    )
    evento.nivel_sugerido_ia = nivel_sugerido
    evento.probabilidades_ia = json.dumps({n: 0.2 for n in NIVELES_TRIaje})
    evento.version_modelo = "simulada-v0"
    session.commit()
    return evento


def registrar_clasificacion_ia(
    session: Session, *, evento_id: str, usuario_id: str | None, resultado: dict
) -> EventoTriaje:
    """HU-E4-01: persiste la inferencia real con probabilidades, metadatos,
    latencia (< 3 s), confianza y explicación SHAP. La transición se audita."""
    if resultado.get("estado") != "ok":
        raise ValidationError(
            "Inferencia no disponible — usar fallback manual",
            detalle=str(resultado.get("motivo")),
        )
    nivel = resultado.get("nivel_sugerido")
    if nivel not in NIVELES_TRIaje:
        raise ValidationError("Nivel sugerido inválido", detalle=str(nivel))
    evento = transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="ClasificacionIA", usuario_id=usuario_id
    )
    evento.nivel_sugerido_ia = nivel
    evento.probabilidades_ia = json.dumps(resultado.get("probabilidades", {}))
    evento.version_modelo = resultado.get("version")
    evento.algoritmo_modelo = resultado.get("algoritmo")
    evento.fecha_inferencia = datetime.now(UTC)
    evento.tiempo_inferencia_ms = resultado.get("tiempo_ms")
    evento.confianza_ia = resultado.get("confianza")
    evento.explicacion_shap = json.dumps(
        resultado.get("explicacion", []), ensure_ascii=False
    )
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="CLASIFICACION_IA",
        entidad="EventoTriaje", evento_id=evento_id,
        detalle=f"{evento_id} · nivel {nivel} · {resultado.get('version')} · "
                f"{resultado.get('tiempo_ms')} ms · confianza "
                f"{resultado.get('confianza')} · umbrales "
                f"{json.dumps(resultado.get('umbrales', {}))}",  # RNA-010
        commit=False,
    )
    logger.info(
        "Clasificación IA persistida: evento %s nivel %s version %s (%.1f ms)",
        evento_id, nivel, resultado.get("version"), resultado.get("tiempo_ms"),
    )
    session.commit()
    return evento


def validar_nivel_profesional(
    session: Session,
    *,
    evento_id: str,
    nivel_profesional: str,
    usuario_id: str | None,
    motivo_discrepancia: str | None = None,
) -> EventoTriaje:
    """CA1: ambos niveles presentes; CA2: concordancia calculada; CA3: motivo."""
    if nivel_profesional not in NIVELES_TRIaje:
        raise ValidationError("Nivel inválido", detalle=nivel_profesional)
    evento = session.get(EventoTriaje, evento_id)
    if evento is None or evento.nivel_sugerido_ia is None:
        raise ValidationError("Falta la clasificación de la IA", detalle=evento_id)

    # CA3: el motivo se valida ANTES de mutar el evento (sin estados a medias)
    if nivel_profesional != evento.nivel_sugerido_ia and not (motivo_discrepancia or "").strip():
        raise ValidationError(
            "Motivo de discrepancia obligatorio cuando los niveles difieren",
            detalle="motivo_discrepancia",
        )

    evento.nivel_asignado_profesional = nivel_profesional
    evento.concordancia = evento.nivel_sugerido_ia == nivel_profesional
    if not evento.concordancia:
        evento.motivo_discrepancia = motivo_discrepancia.strip()
    else:
        evento.motivo_discrepancia = None
    transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="ValidacionProfesional",
        usuario_id=usuario_id,
    )

    audit_service.registrar(
        session, usuario_id=usuario_id, accion="VALIDACION_PROFESIONAL",
        entidad="EventoTriaje", evento_id=evento_id,
        detalle=f"{evento_id} · IA {evento.nivel_sugerido_ia} vs "
                f"{nivel_profesional} · concordancia {evento.concordancia}",
        commit=False,
    )
    logger.info(
        "Validación profesional: evento %s IA %s vs %s (concordancia %s)",
        evento_id, evento.nivel_sugerido_ia, nivel_profesional, evento.concordancia,
    )
    session.commit()
    return evento


def cerrar_evento(session: Session, *, evento_id: str, usuario_id: str | None) -> EventoTriaje:
    """CA4 (E2-06): sin clasificación IA no se permite el cierre; persiste dual."""
    evento = session.get(EventoTriaje, evento_id)
    if evento is None:
        raise ValidationError("Evento inexistente", detalle=evento_id)
    if evento.nivel_sugerido_ia is None or evento.nivel_asignado_profesional is None:
        raise ValidationError("No se puede cerrar sin clasificación IA y validación profesional")
    if evento.estado != "ValidacionProfesional":
        raise ValidationError(f"Estado actual {evento.estado} no permite cierre", detalle=evento_id)
    transicionar_estado(
        session, evento_id=evento_id, nuevo_estado="Cerrado", usuario_id=usuario_id
    )
    evento.cierre = datetime.now(UTC)
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="CIERRE_EVENTO",
        entidad="EventoTriaje", evento_id=evento_id, detalle=evento_id,
        commit=False,
    )
    logger.info(
        "Evento cerrado: %s — IA %s vs profesional %s (usuario %s)",
        evento_id, evento.nivel_sugerido_ia, evento.nivel_asignado_profesional,
        usuario_id,
    )
    session.commit()
    return evento


def reclasificar(
    session: Session, *, evento_original_id: str, nuevo_nivel: str, motivo: str,
    usuario_id: str | None,
) -> EventoTriaje:
    """HU-E2-07: reclasificación como evento separado con trazabilidad completa."""
    if nuevo_nivel not in NIVELES_TRIaje:
        raise ValidationError("Nivel inválido", detalle=nuevo_nivel)
    if not (motivo or "").strip():
        raise ValidationError("Motivo de reclasificación obligatorio", detalle="motivo")
    original = session.get(EventoTriaje, evento_original_id)
    if original is None:
        raise ValidationError("Evento original inexistente", detalle=evento_original_id)
    if original.estado != "Cerrado":  # CA1: solo tras el cierre inicial
        raise ValidationError(
            "La reclasificación solo está disponible tras el cierre del evento",
            detalle=original.estado,
        )
    if original.motivo_cierre:
        raise ValidationError(
            "Evento cerrado automáticamente (fuera del rango 16-60 años) — sin "
            "recomendación IA, la reclasificación asistida no aplica",
            detalle=evento_original_id,
        )
    anterior = original.nivel_asignado_profesional
    nuevo = EventoTriaje(
        paciente_id=original.paciente_id,
        usuario_id=usuario_id,
        estado="Reclasificado",
        evento_anterior_id=original.id,
        nivel_sugerido_ia=original.nivel_sugerido_ia,
        version_modelo=original.version_modelo,
        nivel_asignado_profesional=nuevo_nivel,
        concordancia=original.nivel_sugerido_ia == nuevo_nivel,
        motivo_reclasificacion=motivo.strip(),
        inicio=datetime.now(UTC),
    )
    session.add(nuevo)
    audit_service.registrar(
        session, usuario_id=usuario_id, accion="RECLASIFICACION",
        entidad="EventoTriaje", evento_id=nuevo.id,
        detalle=(
            f"{evento_original_id} → {nuevo.id} · {anterior} → "
            f"{nuevo_nivel} · {motivo.strip()}"
        ),
        commit=False,
    )
    session.commit()
    return nuevo
