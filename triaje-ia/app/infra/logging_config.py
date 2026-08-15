"""Logging estructurado (Sección 10 del documento de arquitectura).

Emite una línea JSON por evento a stdout Y al archivo rotativo `logs/app.log`
(raíz del proyecto) para reconstruir lo sucedido aunque el terminal ya haya
hecho scroll o el servidor se haya reiniciado.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.infra.config import PROJECT_ROOT


class JsonFormatter(logging.Formatter):
    """Formatter que emite una línea JSON por evento."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "mensaje": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level: str = "INFO", log_dir: Path | None = None) -> None:
    formatter = JsonFormatter()
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    root.addHandler(stdout)

    destino = log_dir or (PROJECT_ROOT / "logs")
    destino.mkdir(parents=True, exist_ok=True)
    archivo = RotatingFileHandler(
        destino / "app.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    archivo.setFormatter(formatter)
    root.addHandler(archivo)
