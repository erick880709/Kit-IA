"""Versión desplegable de la aplicación (hash corto del commit actual).

Permite verificar en producción (footer del login y «Acerca de») que la
instancia servida corresponde al último commit integrado en el repositorio
(2026-08-27).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]  # raíz del repo (kit-ia)


def version_app() -> str:
    """Hash corto del commit actual; fallback estable si no hay git disponible."""
    try:
        resultado = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=RAIZ_REPOSITORIO,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if resultado.returncode == 0 and resultado.stdout.strip():
            return f"build {resultado.stdout.strip()}"
    except Exception:  # pragma: no cover - defensivo ante entornos sin git
        pass
    return "build local"
