"""Health check end-to-end de la plomería (FASE 6 de genesis).

Uso:  python scripts/healthcheck.py
Salida: JSON con estado de cada chequeo; exit code 0 solo si TODO OK.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infra.config import settings  # noqa: E402
from app.infra.db import db_ok  # noqa: E402


def run() -> dict:
    checks: dict[str, bool] = {
        "configuracion": bool(settings.app_name),
        "base_de_datos": db_ok(),
        "directorio_modelos": Path(settings.models_dir).is_dir(),
    }
    return {
        "estado": "OK" if all(checks.values()) else "FALLO",
        "checks": checks,
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["estado"] == "OK" else 1)
