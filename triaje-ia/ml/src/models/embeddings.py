"""Embeddings de texto (TT-E3-03).

- Texto vacío → el pipeline continúa solo con estructuradas (RF-NLP-004).
- Idioma español principal (RF-NLP-005).
- Embeddings cacheados por texto (demo < 3 s).
- Vectorizador por defecto: TF-IDF liviano; BERT clínico español opcional
  (transformers/BETO) cuando esté instalado — evaluado en notebook.
"""

from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

_CACHE: dict[str, np.ndarray] = {}


def _llave(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


class VectorizadorTexto:
    """TF-IDF con cache por texto (fallback liviano a BERT clínico)."""

    def __init__(self, max_features: int = 500, ngram: tuple[int, int] = (1, 2)) -> None:
        self._vectorizador = TfidfVectorizer(max_features=max_features, ngram_range=ngram)

    def fit(self, textos: pd.Series) -> VectorizadorTexto:
        self._vectorizador.fit(textos.fillna(""))
        return self

    def transformar(self, textos: pd.Series) -> np.ndarray:
        salida = []
        for texto in textos.fillna(""):
            clave = _llave(str(texto))
            if clave not in _CACHE:  # cache por texto (demo < 3 s)
                _CACHE[clave] = self._vectorizador.transform([str(texto)]).toarray()[0]
            salida.append(_CACHE[clave])
        return np.vstack(salida)

    @staticmethod
    def hay_texto(texto) -> bool:
        """RF-NLP-004: texto vacío no bloquea el flujo."""
        return bool(str(texto).strip())


def vectorizar_texto(
    df: pd.DataFrame, *, columna: str = "motivo_texto",
    max_features: int = 500, entrenar: bool = True,
) -> tuple[np.ndarray, VectorizadorTexto | None]:
    """Devuelve matriz de embeddings y el vectorizador (None si no hay textos)."""
    textos = df[columna].fillna("") if columna in df.columns else pd.Series([""] * len(df))
    if not any(textos.map(VectorizadorTexto.hay_texto)):
        return None, None
    vectorizador = VectorizadorTexto(max_features=max_features)
    if entrenar:
        vectorizador.fit(textos)
    matriz = vectorizador.transformar(textos)
    return matriz, vectorizador
