"""Genera los diagramas de flujo del manual de uso (PNG por rol + general).

Sin dependencias nuevas: usa Pillow (dependencia de Streamlit).
Uso:  python scripts/generar_diagramas_manual.py
Salida: assets/manual/<rol>_flujo.png y flujo_general.png
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DESTINO = Path(__file__).resolve().parents[1] / "assets" / "manual"

FLUJOS: dict[str, tuple[list[str], str]] = {
    "medico": (
        [
            "Registro de paciente\n(verificar documento)",
            "Signos vitales\n(8 campos + IMC)",
            "Evaluación clínica\n(CIE-10 + dolor + Glasgow)",
            "Clasificación IA\n(nivel + probabilidades)",
            "Explicación SHAP\n(top-5 factores)",
            "Validación profesional\n(concordancia + motivo)",
            "Cierre del evento\n(PDF de evidencia)",
        ],
        "Flujo clínico del Médico",
    ),
    "enfermera": (
        [
            "Registro / búsqueda\nde paciente",
            "Signos vitales",
            "Evaluación clínica",
            "Clasificación IA\n+ explicación SHAP",
            "Validación con el médico",
            "Cierre del evento",
        ],
        "Flujo de la Enfermera",
    ),
    "administrador": (
        [
            "Flujo clínico completo",
            "Gestión de roles\ny permisos",
            "Gestión de modelos\n(activar / rollback)",
            "Auditoría\ny trazabilidad",
            "Dashboard operativo",
        ],
        "Flujo del Administrador",
    ),
    "investigador": (
        [
            "Comparación\nde modelos",
            "Explicación SHAP",
            "Historial de triajes",
            "Gestión de modelos\n(registro de versiones)",
            "Dashboard operativo",
        ],
        "Flujo del Investigador",
    ),
    "auditor": (
        [
            "Auditoría y trazabilidad\n(filtros + export)",
            "Dashboard operativo",
            "Reporte de hallazgos\nal administrador",
        ],
        "Flujo del Auditor",
    ),
}

FLUJO_GENERAL = [
    "Paciente\n(registro / nuevo triaje)",
    "Signos vitales",
    "Evaluación clínica\n(motivo CIE-10)",
    "Clasificación IA\n(fusión tardía)",
    "Explicación SHAP",
    "Validación profesional",
    "Cierre + PDF\n(1 evento por visita)",
]

COLORES = {
    "medico": "#0891B2",
    "enfermera": "#0D9488",
    "administrador": "#7C3AED",
    "investigador": "#2563EB",
    "auditor": "#B45309",
}

_FUENTE: Path | None = None


def _fuente(tamano: int):
    global _FUENTE  # noqa: PLW0603
    if _FUENTE is None:
        candidatos = [
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
        _FUENTE = next((p for p in candidatos if p.exists()), None)
    if _FUENTE is None:
        return ImageFont.load_default()
    return ImageFont.truetype(str(_FUENTE), tamano)


def dibujar(
    pasos: list[str], titulo: str, color: str, vertical: bool = True
) -> Image.Image:
    n = len(pasos)
    caja_h = 82
    ancho = 680
    alto = 90 + caja_h * n + 30 * (n + 1) if vertical else 380
    img = Image.new("RGB", (ancho, alto), "white")
    d = ImageDraw.Draw(img)
    fuente_titulo = _fuente(22)
    fuente_caja = _fuente(16)

    d.text((ancho // 2, 24), titulo, fill="#0F172A", anchor="mm", font=fuente_titulo)

    caja_w = 420
    espacio = 30
    for i, paso in enumerate(pasos):
        cx = ancho // 2 if vertical else int(ancho * (i + 0.5) / n)
        cy = (
            70 + (espacio + caja_h) * i + caja_h // 2
            if vertical
            else alto // 2
        )
        x0, y0 = cx - caja_w // 2, cy - caja_h // 2
        x1, y1 = cx + caja_w // 2, cy + caja_h // 2
        d.rounded_rectangle(
            (x0, y0, x1, y1), radius=12, outline=color, width=3, fill="#ECFEFF"
        )
        d.text((cx, cy), paso, fill="#164E63", anchor="mm", font=fuente_caja, align="center")
        if i < n - 1:
            if vertical:
                ax0, ay0 = cx, y1 + 4
                ax1, ay1 = cx, y1 + espacio - 4
            else:
                ax0, ay0 = x1 + 10, cy
                ax1, ay1 = cx + caja_w + 10 + (ancho - caja_w) / (n - 1) - caja_w, cy
            d.line((ax0, ay0, ax1, ay1), fill=color, width=3)
            d.polygon(
                [(ax1, ay1), (ax1 - 12, ay1 - 7), (ax1 - 12, ay1 + 7)],
                fill=color,
            )
    return img


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for rol, (pasos, titulo) in FLUJOS.items():
        img = dibujar(pasos, titulo, COLORES[rol], vertical=True)
        ruta = DESTINO / f"{rol}_flujo.png"
        img.save(ruta)
        print(f"generado: {ruta.relative_to(DESTINO.parent)}")
    img = dibujar(FLUJO_GENERAL, "Vista general del sistema TriajeIA", "#0891B2", vertical=False)
    ruta = DESTINO / "flujo_general.png"
    img.save(ruta)
    print(f"generado: {ruta.relative_to(DESTINO.parent)}")


if __name__ == "__main__":
    main()

