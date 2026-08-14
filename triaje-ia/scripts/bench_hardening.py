"""Mediciones de performance para la auditoría Muralla (seguridad-rendimiento).

Mide ANTES de optimizar, con números reales sobre los artefactos y la BD demo:

- Latencia de inferencia `InferenceService.predecir()`: p50/p95/p99 sobre 30+
  llamadas al artefacto real de `artifacts/models/` (presupuesto RNF-007: < 3 s).
- `dashboard_service.calcular_indicadores()` sobre `triaje.db` (demo).
- `audit_service.consultar()` paginado sobre `triaje.db` (RNP-003: < 1 s).
- Tiempo de importación de `app.main` (referencia del frontend Streamlit,
  sustituto de Core Web Vitals mientras no se levante un servidor de pruebas).

Uso (PowerShell, desde `triaje-ia/`):

    $env:PYTHONPATH = (ruta absoluta de triaje-ia)
    .venv\\Scripts\\python.exe scripts\\bench_hardening.py

Salida: resumen en consola + JSON en `artifacts/metrics/bench_hardening.json`.
"""

from __future__ import annotations

import importlib
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ml.src import ARTIFACTS_METRICS  # noqa: E402

N_LLAMADAS = 30
PRESUPUESTO_INFERENCIA_MS = 3000.0  # RNF-007
PRESUPUESTO_CONSULTAS_MS = 1000.0  # RNP-003


def _percentil(muestras: list[float], p: float) -> float:
    """Percentil por interpolación lineal sobre la muestra ordenada."""
    orden = sorted(muestras)
    if not orden:
        return 0.0
    k = (len(orden) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(orden) - 1)
    return orden[lo] + (orden[hi] - orden[lo]) * (k - lo)


def _datos_paciente() -> dict:
    """Caso clínico realista (sintético) para la medición de inferencia."""
    return {
        "temperatura": 38.9,
        "frecuencia_cardiaca": 121,
        "frecuencia_respiratoria": 30,
        "saturacion_o2": 86,
        "presion_sistolica": 98,
        "presion_diastolica": 62,
        "peso": 70.0,
        "talla": 1.7,
        "episodios_previos_urgencias": 2,
        "anio_nacimiento": 1980,
        "sexo": "Masculino",
        "via_llegada": "Ambulancia",
        "regimen": "subsidiado",
        "departamento": "Cundinamarca",
        "motivo_codigo_cie10": "R07.4",
        "motivo_texto": "Dolor opresivo retroesternal de 2 horas de evolución",
    }


def _medir_inferencia() -> dict:
    from app.services.inference_service import InferenceService

    servicio = InferenceService()
    # Carga del artefacto en frío (no cuenta en las muestras).
    if not servicio.disponible:
        return {"estado": "indisponible", "error": "artefacto no cargable"}
    calentamiento = servicio.predecir(_datos_paciente())
    if calentamiento.get("estado") != "ok":
        return {
            "estado": "indisponible",
            "error": calentamiento.get("motivo", "desconocido"),
        }
    muestras: list[float] = []
    errores = 0
    for _ in range(N_LLAMADAS):
        resultado = servicio.predecir(_datos_paciente())
        if resultado.get("estado") == "ok":
            muestras.append(float(resultado["tiempo_ms"]))
        else:
            errores += 1
    return {
        "estado": "ok",
        "n_llamadas": N_LLAMADAS,
        "errores": errores,
        "p50_ms": round(_percentil(muestras, 0.50), 2),
        "p95_ms": round(_percentil(muestras, 0.95), 2),
        "p99_ms": round(_percentil(muestras, 0.99), 2),
        "min_ms": round(min(muestras), 2) if muestras else None,
        "max_ms": round(max(muestras), 2) if muestras else None,
        "presupuesto_ms": PRESUPUESTO_INFERENCIA_MS,
        "cumple_rnf007": bool(muestras) and _percentil(muestras, 0.95) < PRESUPUESTO_INFERENCIA_MS,
        "version_modelo": calentamiento.get("version"),
        "algoritmo": calentamiento.get("algoritmo"),
    }


def _medir_consultas() -> dict:
    from app.infra.db import SessionLocal
    from app.services import audit_service, dashboard_service

    inicio = time.perf_counter()
    with SessionLocal() as session:
        dashboard_service.calcular_indicadores(session)
    ms_dashboard = (time.perf_counter() - inicio) * 1000

    inicio = time.perf_counter()
    with SessionLocal() as session:
        audit_service.consultar(session, page=1, page_size=50)
    ms_auditoria = (time.perf_counter() - inicio) * 1000

    return {
        "dashboard_calcular_indicadores_ms": round(ms_dashboard, 2),
        "auditoria_consultar_pagina50_ms": round(ms_auditoria, 2),
        "presupuesto_ms": PRESUPUESTO_CONSULTAS_MS,
        "cumple_rnp003": ms_dashboard < PRESUPUESTO_CONSULTAS_MS
        and ms_auditoria < PRESUPUESTO_CONSULTAS_MS,
    }


def _medir_import_main() -> float:
    inicio = time.perf_counter()
    importlib.import_module("app.main")
    return round((time.perf_counter() - inicio) * 1000, 2)


def ejecutar() -> dict:
    resultado = {
        "fecha_utc": datetime.now(UTC).isoformat(),
        "presupuestos": {
            "inferencia_ms": PRESUPUESTO_INFERENCIA_MS,
            "consultas_ms": PRESUPUESTO_CONSULTAS_MS,
        },
        "inferencia": _medir_inferencia(),
        "consultas": _medir_consultas(),
        "import_app_main_ms": _medir_import_main(),
    }
    salida = ARTIFACTS_METRICS / "bench_hardening.json"
    salida.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return resultado


if __name__ == "__main__":
    res = ejecutar()
    print(json.dumps(res, ensure_ascii=False, indent=2))
