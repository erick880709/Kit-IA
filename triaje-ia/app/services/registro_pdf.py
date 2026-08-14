"""Generador del registro de triaje descargable en PDF (HU-E5-02, normativa).

Contenido mínimo (CA1): paciente anonimizado, fecha/hora, nivel IA vs humano,
signos vitales, motivo de consulta y variables SHAP de mayor peso.
CA3: sin identificadores directos del paciente (Ley 1581/2012).
"""

from __future__ import annotations

import io
import json
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def _anonimizar_nombre(nombre: str) -> str:
    """Iniciales: 'Andrea López' → 'Andrea L.' (seudonimización, CA3)."""
    partes = nombre.split()
    if len(partes) <= 1:
        return nombre
    return f"{partes[0]} {partes[-1][0].upper()}."


def _anonimizar_documento(tipo: str, numero: str) -> str:
    """Máscara parcial: CC 53012487 → CC ****2487 (seudonimización, CA3)."""
    return f"{tipo} ****{numero[-4:]}" if len(numero) >= 4 else f"{tipo} ****"


def _top_shap(evento) -> list[dict]:
    """Top-3 de la explicación SHAP persistida (lenguaje clínico)."""
    if not evento.explicacion_shap:
        return []
    try:
        return json.loads(evento.explicacion_shap)[:3]
    except (json.JSONDecodeError, TypeError):
        return []


def generar_pdf_registro(evento, paciente, signos=None, motivo=None) -> bytes:
    """Construye el PDF normativo del registro de triaje (HU-E5-02)."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    w, h = A4

    def linea(y: float, texto: str, size: int = 11, bold: bool = False) -> None:
        pdf.setFillColor("#164E63")
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        pdf.drawString(2 * cm, y, texto)

    pdf.setFillColor("#0891B2")
    pdf.rect(0, h - 3 * cm, w, 3 * cm, stroke=0, fill=1)
    pdf.setFillColor("#FFFFFF")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(2 * cm, h - 1.8 * cm, "TriajeIA — Registro de evento de triaje")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        2 * cm, h - 2.5 * cm,
        "Resolución 5596 de 2015 · sistema de apoyo a la decisión (no autónomo)",
    )

    y = h - 4.5 * cm
    linea(y, "Datos del paciente (anonimizado — Ley 1581/2012)", size=10, bold=True)
    y -= 0.7 * cm
    linea(y, f"Paciente: {_anonimizar_nombre(f'{paciente.nombres} {paciente.apellidos}')} · "
             f"{_anonimizar_documento(paciente.tipo_documento, paciente.numero_documento)} · "
             f"Sexo: {paciente.sexo} · Nacimiento: {paciente.fecha_nacimiento.year}")
    y -= 0.9 * cm
    linea(y, f"Evento: {evento.id} · Inicio: {evento.inicio.strftime('%d/%m/%Y %H:%M')} · "
             f"Cierre: {evento.cierre.strftime('%d/%m/%Y %H:%M') if evento.cierre else '—'}")
    y -= 0.9 * cm
    linea(y, f"Nivel sugerido IA: {evento.nivel_sugerido_ia or '—'} · "
             f"Nivel profesional: {evento.nivel_asignado_profesional or '—'} · "
             f"Concordancia: {'Sí' if evento.concordancia else 'No'}", bold=True)
    y -= 0.7 * cm
    if evento.motivo_discrepancia:
        linea(y, f"Motivo de discrepancia: {evento.motivo_discrepancia}")
        y -= 0.7 * cm
    if evento.motivo_reclasificacion:
        linea(y, f"Motivo de reclasificación: {evento.motivo_reclasificacion}")
        y -= 0.7 * cm
    if signos is not None:
        linea(y, f"Signos: T {signos.temperatura}°C · FC {signos.frecuencia_cardiaca} · "
                 f"FR {signos.frecuencia_respiratoria} · SpO₂ {signos.saturacion_o2}% · "
                 f"PA {signos.presion_sistolica}/{signos.presion_diastolica} · IMC {signos.imc}")
        y -= 0.7 * cm
    if motivo is not None:
        linea(y, f"Motivo: {motivo.codigo_cie10} — {motivo.descripcion_estructurada}")
        y -= 0.7 * cm
    linea(y, f"Modelo: {evento.version_modelo or '—'} · algoritmo "
             f"{evento.algoritmo_modelo or '—'} · confianza "
             f"{evento.confianza_ia if evento.confianza_ia is not None else '—'} · "
             f"inferencia {evento.tiempo_inferencia_ms or '—'} ms")
    y -= 0.9 * cm

    shap = _top_shap(evento)
    if shap:
        linea(y, "Variables de mayor peso en la clasificación (SHAP):", bold=True)
        y -= 0.6 * cm
        for item in shap:
            signo = "+" if item.get("impacto", 0) >= 0 else "−"
            linea(y, f"  · {item.get('clinico', item.get('feature', '—'))} "
                     f"({item.get('feature', '')}): {signo}{abs(item.get('impacto', 0)):.4f}")
            y -= 0.5 * cm

    y -= 0.6 * cm
    linea(y, "Ambos niveles quedaron persistidos de forma permanente (RD-003).", size=9)
    y -= 0.5 * cm
    linea(y, "Documento sin identificadores directos del paciente (seudonimizado).", size=9)
    y -= 0.8 * cm
    linea(y, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", size=9)

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
