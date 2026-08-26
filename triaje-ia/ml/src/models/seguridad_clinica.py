"""Red de contención clínica (Res. 5596/2015) — sistema de apoyo, NO autónomo.

El modelo estadístico no alcanza los extremos I/V con datos sintéticos
(prevalencia I 0.23% / V 0.46%). Esta regla garantiza cobertura en riesgo
vital (Nivel I) y en el otro extremo (Nivel V), y SIEMPRE queda registrada
cuando actúa (la inferencia lo loguea y lo incluye en el resultado).
"""

from __future__ import annotations


def _num(valor) -> float | None:
    try:
        if valor is None or valor == "":
            return None
        return float(valor)
    except (TypeError, ValueError):
        return None


def regla_seguridad_clinica(
    datos: dict, probabilidades: dict[str, float]
) -> str | None:
    """Devuelve "I" (riesgo vital), "V" (todo normal) o None (no actúa).

    Criterios de riesgo vital: SpO₂ < 85, PAS < 70, FC > 150 o < 40,
    FR > 35 o Glasgow ≤ 8. Criterio de no urgencia: signos normales,
    dolor ≤ 3, Glasgow 15 y P(V) ≥ 0.2 según el modelo.
    """
    spo2 = _num(datos.get("saturacion_o2"))
    pas = _num(datos.get("presion_sistolica"))
    fc = _num(datos.get("frecuencia_cardiaca"))
    fr = _num(datos.get("frecuencia_respiratoria"))
    temp = _num(datos.get("temperatura"))
    glasgow = _num(datos.get("glasgow"))
    dolor = _num(datos.get("escala_dolor"))
    p_v = float(probabilidades.get("V", 0.0) or 0.0)

    riesgo_vital = (
        (spo2 is not None and spo2 < 85)
        or (pas is not None and pas < 70)
        or (fc is not None and (fc > 150 or fc < 40))
        or (fr is not None and fr > 35)
        or (glasgow is not None and glasgow <= 8)
    )
    if riesgo_vital:
        return "I"

    todo_normal = (
        (spo2 is None or spo2 >= 98)
        and (fc is None or 60 <= fc <= 80)
        and (fr is None or 12 <= fr <= 16)
        and (temp is None or 36.3 <= temp <= 37.2)
        and (pas is None or 110 <= pas <= 130)
        and (glasgow is None or glasgow >= 15)
        and (dolor is None or dolor <= 3)
        and p_v >= 0.2
    )
    if todo_normal:
        return "V"
    return None
