"""Pruebas del vectorizador de texto (vocabulario extendido con catálogo)."""

from __future__ import annotations

import pandas as pd

from app.domain.catalogos import CATALOGO_MOTIVOS
from ml.src.models.embeddings import VectorizadorTexto


def test_fit_sin_extra_no_incluye_terminos_del_catalogo() -> None:
    textos = pd.Series(["dolor abdominal", "fiebre alta"])
    vectorizador = VectorizadorTexto(max_features=2000).fit(textos)
    assert "fractura" not in vectorizador._vectorizador.vocabulary_  # noqa: SLF001


def test_fit_con_textos_extra_incluye_vocabulario_del_catalogo() -> None:
    """Ajuste 2026-08-14: los motivos del catálogo entran al vocabulario TF-IDF
    aunque no existan en el corpus etiquetado (8/71 tenían cobertura 0)."""
    textos = pd.Series(["dolor abdominal", "fiebre alta"])
    extra = pd.Series([f"{codigo} {descripcion}" for codigo, descripcion, _ in CATALOGO_MOTIVOS])
    vectorizador = VectorizadorTexto(max_features=2000).fit(textos, textos_extra=extra)
    vocab = vectorizador._vectorizador.vocabulary_  # noqa: SLF001
    for token in ("fractura", "herida", "quemadura", "tos"):
        assert token in vocab, f"falta token del catálogo: {token}"


def test_transformar_no_falla_con_textos_nuevos_del_catalogo() -> None:
    textos = pd.Series(["dolor abdominal"])
    extra = pd.Series([f"{codigo} {descripcion}" for codigo, descripcion, _ in CATALOGO_MOTIVOS])
    vectorizador = VectorizadorTexto(max_features=2000).fit(textos, textos_extra=extra)
    matriz = vectorizador.transformar(
        pd.Series(["W34.9 Herida por arma de fuego, no especificada"])
    )
    assert matriz.shape[0] == 1
    assert matriz.shape[1] > 0
