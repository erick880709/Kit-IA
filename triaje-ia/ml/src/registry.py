"""Serialización del modelo ganador + transformadores (TT-E3-09).

Artefacto único versionado con: preprocesadores + modelo + umbrales por clase
+ vectorizador de texto + manifiesto con métricas y hash de integridad.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from datetime import date
from pathlib import Path

import joblib

from ml.src import ARTIFACTS_MODELS


def serializar_paquete(
    *,
    modelo,
    pipeline_estructurado,
    vectorizador_texto,
    umbrales: dict,
    metricas: dict,
    nombre_algoritmo: str,
    fecha: date,
    destino: Path | None = None,
) -> Path:
    """TT-E3-09: pipeline completo serializable en un único archivo joblib.

    El manifiesto de integridad se escribe SIEMPRE junto al artefacto (mismo
    directorio y nombre base), sin importar el destino: `cargar_paquete` lo
    busca ahí para verificar el hash ANTES de deserializar.
    """
    version = f"modelo-{nombre_algoritmo}-v{fecha.strftime('%Y%m%d')}"
    ruta = destino or (ARTIFACTS_MODELS / f"{version}.joblib")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    contenido = {
        "modelo": modelo,
        "pipeline_estructurado": pipeline_estructurado,
        "vectorizador_texto": vectorizador_texto,
        "umbrales": umbrales,
        "version": version,
        "algoritmo": nombre_algoritmo,
        "fecha": fecha.isoformat(),
    }
    joblib.dump(contenido, ruta)

    hash_sha = hashlib.sha256(ruta.read_bytes()).hexdigest()[:16]
    manifiesto = {
        "version": version,
        "algoritmo": nombre_algoritmo,
        "fecha": fecha.isoformat(),
        "metricas": metricas,
        "umbrales": umbrales,
        "sha256_16": hash_sha,
    }
    manifest_path = Path(str(ruta).replace(".joblib", ".manifest.json"))
    manifest_path.write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return ruta


def cargar_paquete(ruta: str | Path) -> dict:
    """Carga el artefacto tras verificar su integridad (hash ANTES de cargar).

    `joblib.load` deserializa pickle, que ejecuta código dentro del proceso:
    la verificación del hash del manifiesto debe ocurrir SIEMPRE antes de
    deserializar. Sin manifiesto no hay procedencia verificable, así que la
    carga se rechaza (fail-closed).
    """
    ruta = Path(ruta)
    manifest_path = Path(str(ruta).replace(".joblib", ".manifest.json"))
    if not ruta.is_file():
        raise ValueError(f"Artefacto de modelo inexistente: {ruta}")
    if not manifest_path.is_file():
        raise ValueError(
            "Sin manifiesto de integridad junto al artefacto — carga rechazada "
            "(fail-closed)"
        )
    try:
        manifiesto = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError("Manifiesto de integridad ilegible") from exc
    hash_esperado = manifiesto.get("sha256_16")
    if not hash_esperado:
        raise ValueError("Manifiesto sin hash de integridad — carga rechazada")
    hash_actual = hashlib.sha256(ruta.read_bytes()).hexdigest()[:16]
    if not secrets.compare_digest(str(hash_esperado), hash_actual):
        raise ValueError("Hash de integridad del modelo no coincide")
    return joblib.load(ruta)
