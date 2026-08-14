"""Código reutilizable del pipeline ML (Épica E3)."""

from __future__ import annotations

from pathlib import Path

ML_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ML_ROOT / "data" / "raw"
DATA_PROCESSED = ML_ROOT / "data" / "processed"
ARTIFACTS = ML_ROOT.parent / "artifacts"
ARTIFACTS_METRICS = ARTIFACTS / "metrics"
ARTIFACTS_MODELS = ARTIFACTS / "models"
ARTIFACTS_SHAP = ARTIFACTS / "shap"

for _d in (DATA_RAW, DATA_PROCESSED, ARTIFACTS_METRICS, ARTIFACTS_MODELS, ARTIFACTS_SHAP):
    _d.mkdir(parents=True, exist_ok=True)

SEMILLA_GLOBAL = 42
