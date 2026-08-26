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


def _llave(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


class VectorizadorTexto:
    """TF-IDF con cache por texto (fallback liviano a BERT clínico)."""

    def __init__(self, max_features: int = 500, ngram: tuple[int, int] = (1, 2)) -> None:
        self._vectorizador = TfidfVectorizer(max_features=max_features, ngram_range=ngram)
        # Cache POR INSTANCIA (2026-08-26): la clave por texto a nivel de módulo
        # colisionaba entre vectorizadores con vocabularios distintos (p. ej.
        # 60 vs 80 features) y producía matrices con filas de dimensiones mixtas.
        self._cache: dict[str, np.ndarray] = {}

    def fit(self, textos: pd.Series, textos_extra: pd.Series | None = None) -> VectorizadorTexto:
        """Ajusta el vocabulario sobre `textos` (+ `textos_extra` sin etiqueta).

        `textos_extra` permite incluir términos del catálogo de motivos en el
        vocabulario aunque no aparezcan en el corpus etiquetado (validación
        2026-08-14: 8/71 motivos tenían 0% de cobertura de vocabulario).
        Nota: los términos que solo están en `textos_extra` tendrán coeficiente
        0 en sub_b hasta que existan ejemplos etiquetados (p. ej. MIMIC-IV-ED).
        """
        corpus = textos.fillna("")
        if textos_extra is not None and len(textos_extra):
            corpus = pd.concat([corpus, textos_extra.fillna("")], ignore_index=True)
        self._vectorizador.fit(corpus)
        return self

    @property
    def vocabulario(self) -> set[str]:
        """Tokens del vocabulario ajustado (auditorías de cobertura del catálogo)."""
        return set(self._vectorizador.vocabulary_)

    def transformar(self, textos: pd.Series) -> np.ndarray:
        salida = []
        for texto in textos.fillna(""):
            clave = _llave(str(texto))
            if clave not in self._cache:  # cache por texto (demo < 3 s)
                self._cache[clave] = self._vectorizador.transform([str(texto)]).toarray()[0]
            salida.append(self._cache[clave])
        return np.vstack(salida)

    def transformar_disperso(self, textos: pd.Series):
        """TF-IDF disperso para ENTRENAMIENTO: evita densificar 46k × 11k."""
        return self._vectorizador.transform(textos.fillna(""))

    @staticmethod
    def hay_texto(texto) -> bool:
        """RF-NLP-004: texto vacío no bloquea el flujo."""
        return bool(str(texto).strip())


def vectorizar_texto(
    df: pd.DataFrame, *, columna: str = "motivo_texto",
    max_features: int = 500, entrenar: bool = True,
    textos_extra: pd.Series | None = None,
    disperso: bool = False,
) -> tuple[np.ndarray, VectorizadorTexto | None]:
    """Devuelve matriz de embeddings y el vectorizador (None si no hay textos).

    `disperso=True` devuelve scipy.sparse (entrenamiento con vocabulario
    completo sin densificar); la inferencia usa el modo denso de a 1 fila.
    """
    textos = df[columna].fillna("") if columna in df.columns else pd.Series([""] * len(df))
    if not any(textos.map(VectorizadorTexto.hay_texto)):
        return None, None
    vectorizador = VectorizadorTexto(max_features=max_features)
    if entrenar:
        vectorizador.fit(textos, textos_extra=textos_extra)
    if disperso:
        matriz = vectorizador.transformar_disperso(textos)
    else:
        matriz = vectorizador.transformar(textos)
    return matriz, vectorizador
