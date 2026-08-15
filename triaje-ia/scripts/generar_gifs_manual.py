"""Genera GIFs animados del manual de uso (recorrido paso a paso por rol).

Cada cuadro del GIF resalta el paso actual, muestra los pasos siguientes como
fantasma y una instrucción detallada debajo. El último cuadro muestra el flujo
completo y se mantiene más tiempo.

Uso:  python scripts/generar_gifs_manual.py
Salida: assets/manual/<rol>_flujo.gif
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.generar_diagramas_manual import COLORES, FLUJOS, _fuente  # noqa: E402

DESTINO = Path(__file__).resolve().parents[1] / "assets" / "manual"

# Instrucción detallada por paso, una por cada caja del flujo del rol.
INSTRUCCIONES: dict[str, list[str]] = {
    "medico": [
        "Ingrese a «Registrar paciente» y pulse «Verificar documento» con el "
        "documento del paciente; si ya existe, precargue datos e inicie el NUEVO triaje.",
        "Complete los 8 signos vitales; revise el IMC automático (talla en metros) "
        "y confirme explícitamente cualquier valor fuera de rango.",
        "Seleccione el motivo CIE-10 (código + categoría), escala de dolor, Glasgow "
        "y nivel de conciencia; registre antecedentes y alergias.",
        "Pulse «Ejecutar inferencia IA» y lea el nivel sugerido con probabilidades "
        "(presupuesto < 3 s); si el modelo no responde, continúe con triaje manual auditado.",
        "Revise el top-5 de la explicación SHAP con lenguaje clínico y dirección del efecto.",
        "Confirme o ajuste el nivel profesional; si difiere de la IA, registre el "
        "motivo de discrepancia (obligatorio).",
        "Cierre el evento con concordancia registrada y descargue el PDF de evidencia.",
    ],
    "enfermera": [
        "Verifique el documento del paciente; si ya existe, inicie un nuevo triaje "
        "con los datos precargados (cada visita es un evento independiente).",
        "Tome y registre los 8 signos vitales con la unidad correcta (talla en metros).",
        "Registre motivo CIE-10, dolor, Glasgow, nivel de conciencia y antecedentes.",
        "Ejecute la clasificación IA y revise el nivel sugerido con su explicación SHAP.",
        "Acompañe al médico en la validación profesional del nivel de triaje.",
        "Cierre el evento y entregue el PDF de evidencia al paciente o al servicio.",
    ],
    "administrador": [
        "Opere el flujo clínico completo para reproducir incidencias reportadas por el equipo.",
        "Cree usuarios y asigne roles con mínimo privilegio (todo cambio queda auditado).",
        "Active la versión ganadora del modelo; ante fallos, haga rollback de un clic "
        "reactivando la versión anterior.",
        "Revise la bitácora append-only con filtros por usuario, acción y fechas; "
        "exporte evidencia.",
        "Supervise indicadores operativos (volumen por nivel, tiempos, concordancia) "
        "en el dashboard.",
    ],
    "investigador": [
        "Compare experimentos por AUC, macro-F1, Brier y ECE lado a lado.",
        "Interprete el top-5 SHAP de los eventos clasificados y correlaciónelo con literatura.",
        "Consulte el historial cronológico de triajes de un paciente (1 paciente → N eventos).",
        "Registre nuevas versiones de modelo con las métricas de su manifiesto.",
        "Monitoree volumen y concordancia IA/profesional en el dashboard operativo.",
    ],
    "auditor": [
        "Filtre la auditoría por usuario, acción, entidad y fechas; exporte CSV, Excel o PDF.",
        "Revise indicadores operativos en el dashboard y compare períodos para "
        "detectar desviaciones.",
        "Reporte hallazgos al administrador sin alterar la evidencia (bitácora append-only).",
    ],
}

_ANCHO = 720
_CAJA_H = 76
_ESPACIO = 16
_TITULO_Y = 26
_CAPTURA_ALTO = 128
_MARGEN_X = 90


def _envolver(texto: str, fuente, ancho_max: int) -> list[str]:
    lineas: list[str] = []
    for parrafo in texto.split("\n"):
        lineas.extend(textwrap.wrap(parrafo, width=ancho_max))
    return lineas


def _alto_total(n: int) -> int:
    return _TITULO_Y + 16 + (_CAJA_H + _ESPACIO) * n + _CAPTURA_ALTO


def _dibujar_caja(
    d: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    texto: str,
    color: str,
    fuente_caja,
    estado: str,
) -> None:
    x0, y0 = cx - 240, cy - _CAJA_H // 2
    x1, y1 = cx + 240, cy + _CAJA_H // 2
    if estado == "actual":
        d.rounded_rectangle((x0, y0, x1, y1), radius=14, outline=color, width=4, fill="#E0F7FA")
        d.text((x0 + 18, cy), texto, fill="#0F172A", anchor="lm", font=fuente_caja, align="left")
    elif estado == "hecho":
        d.rounded_rectangle((x0, y0, x1, y1), radius=14, outline=color, width=2, fill="#ECFEFF")
        d.text((x0 + 18, cy), texto, fill="#164E63", anchor="lm", font=fuente_caja, align="left")
    else:  # fantasma (próximos pasos)
        d.rounded_rectangle((x0, y0, x1, y1), radius=14, outline="#CBD5E1", width=1, fill="#F8FAFC")
        d.text((x0 + 18, cy), texto, fill="#94A3B8", anchor="lm", font=fuente_caja, align="left")


def _cuadro(
    pasos: list[str],
    titulo: str,
    color: str,
    n: int,
    paso_actual: int,
    instruccion: str,
    es_final: bool,
) -> Image.Image:
    alto = _alto_total(n)
    img = Image.new("RGB", (_ANCHO, alto), "white")
    d = ImageDraw.Draw(img)
    fuente_titulo = _fuente(22)
    fuente_caja = _fuente(15)
    fuente_captura = _fuente(14)

    d.text((_ANCHO // 2, _TITULO_Y), titulo, fill="#0F172A", anchor="mm", font=fuente_titulo)
    inicio_y = _TITULO_Y + 30
    for i, paso in enumerate(pasos):
        cy = inicio_y + (_CAJA_H + _ESPACIO) * i + _CAJA_H // 2
        if es_final:
            estado = "hecho"
        elif i < paso_actual:
            estado = "hecho"
        elif i == paso_actual:
            estado = "actual"
        else:
            estado = "fantasma"
        _dibujar_caja(d, _ANCHO // 2, cy, paso, color, fuente_caja, estado)

    # Barra separadora y captura de instrucción
    sep_y = alto - _CAPTURA_ALTO + 4
    d.line((_MARGEN_X, sep_y, _ANCHO - _MARGEN_X, sep_y), fill="#E2E8F0", width=2)
    if es_final:
        caption = "✓ Flujo completo — repita este recorrido en cada atención"
        d.text(
            (_ANCHO // 2, sep_y + 22), caption, fill="#0F766E", anchor="mm",
            font=_fuente(18),
        )
    else:
        d.text(
            (_ANCHO // 2, sep_y + 18),
            f"PASO {paso_actual + 1} DE {n}",
            fill=color, anchor="mm", font=_fuente(17),
        )
        lineas = _envolver(instruccion, fuente_captura, 72)
        for j, linea in enumerate(lineas[:4]):
            d.text(
                (_ANCHO // 2, sep_y + 46 + j * 20),
                linea, fill="#334155", anchor="mm", font=fuente_captura,
            )
    return img


def generar_gif(rol: str, pasos: list[str], titulo: str, color: str) -> Path:
    n = len(pasos)
    instrucciones = INSTRUCCIONES[rol]
    if len(instrucciones) != n:
        raise ValueError(f"{rol}: {len(instrucciones)} instrucciones para {n} pasos")
    cuadros = []
    duraciones: list[int] = []
    # Título al inicio
    alto = _alto_total(n)
    intro = Image.new("RGB", (_ANCHO, alto), "white")
    d = ImageDraw.Draw(intro)
    d.text(
        (_ANCHO // 2, alto // 2 - 24), titulo, fill=color, anchor="mm", font=_fuente(28),
    )
    d.text(
        (_ANCHO // 2, alto // 2 + 26),
        "Recorrido animado del manual — paso a paso",
        fill="#475569", anchor="mm", font=_fuente(17),
    )
    cuadros.append(intro)
    duraciones.append(1600)

    for i in range(n):
        cuadros.append(_cuadro(pasos, titulo, color, n, i, instrucciones[i], es_final=False))
        duraciones.append(1400)

    cuadros.append(_cuadro(pasos, titulo, color, n, n, "", es_final=True))
    duraciones.append(3000)

    ruta = DESTINO / f"{rol}_flujo.gif"
    cuadros[0].save(
        ruta,
        save_all=True,
        append_images=cuadros[1:],
        duration=duraciones,
        loop=0,
        optimize=True,
    )
    return ruta


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for rol, (pasos, titulo) in FLUJOS.items():
        ruta = generar_gif(rol, pasos, titulo, COLORES[rol])
        print(f"generado: {ruta.relative_to(DESTINO.parent)}")


if __name__ == "__main__":
    main()
