"""Servicio de inferencia del modelo de triaje (TT-E4-01, HU-E4-01).

- Carga del artefacto versionado al primer uso, con log de versión (TT-E4-01).
- Presupuesto de latencia < 3 s (RNF-007) con timeout y fallback a triaje
  manual (RNF-009) cuando el modelo no responde o está indisponible.
- Circuit breaker: 3 fallos consecutivos → indisponible 60 s (RNO-007); la
  vista registra la auditoría de indisponibilidad.
- Registro del modelo en BD (ENT-009) desde su manifiesto.
"""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturoTimeout
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Modelo
from app.services.audit_service import auditar

logger = logging.getLogger(__name__)

_TIMEOUT_S = 3.0
_MAX_FALLOS = 3
_VENTANA_REINTENTO_S = 60.0

_COLUMNAS_ESPERADAS = [
    "temperatura", "frecuencia_cardiaca", "frecuencia_respiratoria",
    "saturacion_o2", "presion_sistolica", "presion_diastolica",
    "peso", "talla", "episodios_previos_urgencias", "anio_nacimiento",
    "sexo", "via_llegada", "regimen", "departamento",
]


def _normalizar_regimen(valor: str | None) -> str:
    if not valor:
        return "Contributivo"
    mapeo = {
        "contributivo": "Contributivo", "subsidiado": "Subsidiado",
        "especial": "Especial", "no afiliado": "NoAfiliado", "noafiliado": "NoAfiliado",
    }
    return mapeo.get(valor.strip().lower(), valor)


class InferenceService:
    """Singleton de inferencia con cache de embeddings y circuit breaker."""

    def __init__(self, dir_modelos: Path | None = None, timeout_s: float = _TIMEOUT_S) -> None:
        from ml.src import ARTIFACTS_MODELS

        self.dir_modelos = dir_modelos or ARTIFACTS_MODELS
        self.timeout_s = timeout_s
        self._paquete: dict | None = None
        self._explainer = None
        self._fallos = 0
        self._proximo_reintento = 0.0

    # ---------- carga y disponibilidad ----------

    @property
    def disponible(self) -> bool:
        return self._cargar() is not None

    @property
    def version(self) -> str | None:
        paquete = self._cargar()
        return paquete.get("version") if paquete else None

    def recargar(self) -> None:
        """HU-E6-02: invalida la caché tras activar/desactivar un modelo.

        El rollback es efectivo de inmediato: la siguiente predicción carga
        la versión activa en BD.
        """
        self._paquete = None
        self._explainer = None
        self._fallos = 0
        logger.info("Caché de inferencia invalidada — próxima carga usará el modelo activo")

    def _rutas_candidatas(self) -> list[Path]:
        if not self.dir_modelos.exists():
            return []
        return sorted(self.dir_modelos.glob("*.joblib"), key=lambda p: p.stat().st_mtime)

    def _ruta_activa(self, candidatas: list[Path]) -> Path | None:
        """HU-E6-02: la inferencia usa la versión activa en BD (rollback).

        Si no hay fila activa en BD (p. ej. entornos de prueba), se usa el
        artefacto más reciente.
        """
        try:
            from sqlalchemy import select

            from app.infra.db import SessionLocal

            with SessionLocal() as session:
                activo = session.scalar(
                    select(Modelo).where(Modelo.activo.is_(True)).order_by(
                        Modelo.creado_en.desc()
                    )
                )
            if activo:
                ruta = Path(activo.ruta_artefacto)
                # Solo aplica si el artefacto vive en el directorio de este
                # servicio (los tests usan directorios temporales).
                if ruta.exists() and ruta.parent == self.dir_modelos.resolve():
                    return ruta
        except Exception:  # noqa: BLE001 — sin BD accesible se degrada a mtime
            logger.exception("BD no accesible para resolver modelo activo")
        return candidatas[-1] if candidatas else None

    def _cargar(self) -> dict | None:
        if self._paquete is not None:
            return self._paquete
        if self._fallos >= _MAX_FALLOS and time.monotonic() < self._proximo_reintento:
            logger.warning("Modelo en circuit breaker abierto — fallback manual")
            return None
        candidatas = self._rutas_candidatas()
        ruta = self._ruta_activa(candidatas)
        if ruta is None:
            logger.error("No hay artefacto de modelo en %s", self.dir_modelos)
            self._registrar_fallo()
            return None
        try:
            from ml.src.registry import cargar_paquete

            paquete = cargar_paquete(ruta)
            self._paquete = paquete
            self._fallos = 0
            logger.info(
                "Modelo cargado: %s (algoritmo %s, fecha %s)",
                paquete.get("version"), paquete.get("algoritmo"), paquete.get("fecha"),
            )
            return paquete
        except Exception:  # noqa: BLE001 — cualquier fallo deriva a manual
            logger.exception("Fallo al cargar el modelo — fallback manual")
            self._registrar_fallo()
            return None

    def _registrar_fallo(self) -> None:
        self._fallos += 1
        self._proximo_reintento = time.monotonic() + _VENTANA_REINTENTO_S

    # ---------- inferencia ----------

    @staticmethod
    def _predecir_proba(paquete: dict, X_est, X_txt) -> np.ndarray:
        modelo = paquete["modelo"]
        # El artefacto ganador es LateFusionClassifier (sub_a + sub_b) y acepta
        # (X_estructurada, X_texto). Un modelo plano (XGBoost/RF) interpreta el
        # segundo argumento posicional como ntree_limit/validate_features y
        # explota con ValueError de array ambiguo (bug real 2026-08-14).
        if getattr(modelo, "sub_b", None) is not None and X_txt is not None:
            return np.asarray(modelo.predict_proba(X_est, X_txt))
        if getattr(modelo, "sub_b", None) is None and X_txt is not None:
            logger.warning(
                "Artefacto %s sin submodelo de texto — predicción solo con "
                "features estructuradas",
                paquete.get("version"),
            )
        return np.asarray(modelo.predict_proba(X_est))

    @staticmethod
    def _vectorizar_texto(paquete: dict, datos: dict):
        vectorizador = paquete.get("vectorizador_texto")
        if vectorizador is None:
            return None
        texto = (
            f"{datos.get('motivo_codigo_cie10', '')} {datos.get('motivo_texto', '')}"
        ).strip()
        if not texto:
            return None
        return vectorizador.transformar(pd.Series([str(texto)]))

    def _construir_fila(self, datos: dict) -> pd.DataFrame:
        fila = {
            col: datos.get(col, 0 if col != "anio_nacimiento" else 1950)
            for col in _COLUMNAS_ESPERADAS
        }
        fila["sexo"] = fila.get("sexo") or "Femenino"
        fila["via_llegada"] = fila.get("via_llegada") or "Particular"
        fila["regimen"] = _normalizar_regimen(fila.get("regimen"))
        fila["departamento"] = fila.get("departamento") or "Cundinamarca"
        return pd.DataFrame([fila])

    def predecir(self, datos: dict) -> dict:
        """Predicción con probabilidades por nivel y sugerencia por umbrales.

        Devuelve `estado: "ok"` o `estado: "indisponible"` (fallback manual).
        """
        paquete = self._cargar()
        if paquete is None:
            return {"estado": "indisponible", "motivo": "modelo_no_disponible"}
        try:
            fila = self._construir_fila(datos)
            pipeline = paquete["pipeline_estructurado"]
            X_est = pipeline.transform(fila)
            X_txt = self._vectorizar_texto(paquete, datos)

            inicio = time.perf_counter()
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                futuro = pool.submit(self._predecir_proba, paquete, X_est, X_txt)
                proba = futuro.result(timeout=self.timeout_s)
            finally:
                # Sin bloqueo tras timeout (shutdown no-bloqueante).
                pool.shutdown(wait=False, cancel_futures=True)
            explicacion = self.explicar(fila)
            tiempo_ms = (time.perf_counter() - inicio) * 1000  # incluye SHAP (CA2 HU-E4-01)

            from ml.src.evaluation.metrics import CLASES
            from ml.src.models.thresholds import sugerir_nivel

            probabilidades = {CLASES[i]: float(proba[0, i]) for i in range(len(CLASES))}
            umbrales = paquete.get("umbrales", {c: 0.5 for c in CLASES})
            nivel = sugerir_nivel(probabilidades, umbrales)
            confianza = max(probabilidades.values())
            self._fallos = 0
            logger.info(
                "Inferencia OK: nivel=%s confianza=%.3f tiempo_ms=%.1f version=%s",
                nivel, confianza, tiempo_ms, paquete.get("version"),
            )
            return {
                "estado": "ok",
                "nivel_sugerido": nivel,
                "probabilidades": probabilidades,
                "confianza": round(confianza, 4),
                "tiempo_ms": round(tiempo_ms, 2),
                "version": paquete.get("version"),
                "algoritmo": paquete.get("algoritmo"),
                "fecha_entrenamiento": paquete.get("fecha"),
                "umbrales": umbrales,
                "explicacion": explicacion,
            }
        except (FuturoTimeout, TimeoutError):
            logger.error("Inferencia excedió %.1f s — fallback manual", self.timeout_s)
            self._registrar_fallo()
            return {"estado": "indisponible", "motivo": "timeout"}
        except Exception:  # noqa: BLE001
            logger.exception("Error en inferencia — fallback manual")
            self._registrar_fallo()
            return {"estado": "indisponible", "motivo": "error_inferencia"}

    def explicar(self, fila: pd.DataFrame) -> list[dict]:
        """Top-5 SHAP con mapeo a lenguaje clínico (TT-E3-08, HU-E4-02)."""
        paquete = self._cargar()
        if paquete is None:
            return []
        try:
            from ml.src.evaluation.shap_explain import NOMBRES_CLINICOS

            if self._explainer is None:
                import shap

                modelo_arbol = getattr(paquete["modelo"], "sub_a", paquete["modelo"])
                self._explainer = shap.TreeExplainer(modelo_arbol)
            pipeline = paquete["pipeline_estructurado"]
            X = pipeline.transform(fila)
            modelo_arbol = getattr(paquete["modelo"], "sub_a", paquete["modelo"])
            proba = modelo_arbol.predict_proba(X)[0]
            idx_clase = int(proba.argmax())
            valores = self._explainer.shap_values(X)
            if isinstance(valores, list):  # una matriz por clase
                valores = valores[idx_clase]
            valores = np.asarray(valores)
            if valores.ndim == 3:  # (n, features, clases)
                valores = valores[:, :, idx_clase]
            nombres = list(
                pipeline.named_steps["columnas"].get_feature_names_out()
            )
            medias = np.abs(valores).mean(axis=0)
            orden = np.argsort(-medias)[:5]
            top = []
            for i in orden:
                nombre_bruto = nombres[int(i)]
                corto = nombre_bruto.split("__", 1)[-1]
                partes = corto.split("_")
                clinico = corto
                for largo in range(len(partes), 0, -1):
                    candidato = "_".join(partes[:largo])
                    if candidato in NOMBRES_CLINICOS:
                        clinico = NOMBRES_CLINICOS[candidato]
                        break
                top.append(
                    {
                        "feature": corto,
                        "clinico": clinico,
                        "impacto": round(float(valores[0, int(i)]), 4),
                        "peso_absoluto": round(float(medias[int(i)]), 4),
                    }
                )
            return top
        except Exception:  # noqa: BLE001 — la explicación nunca bloquea el flujo
            logger.exception("SHAP no disponible para este modelo")
            return []

    # ---------- registro ENT-009 ----------

    @auditar("REGISTRAR_MODELO", "Modelo")
    def registrar_modelo(self, session: Session) -> str | None:
        """Registra la versión cargada en BD si aún no existe (idempotente)."""
        paquete = self._cargar()
        if paquete is None:
            return None
        version = str(paquete.get("version"))
        existente = session.scalar(select(Modelo).where(Modelo.version == version))
        if existente is not None:
            return version
        manifiesto = None
        candidatos = [p for p in self._rutas_candidatas() if p.stem == version]
        if candidatos:
            manifest_path = Path(str(candidatos[-1]).replace(".joblib", ".manifest.json"))
            if manifest_path.exists():
                manifiesto = json.loads(manifest_path.read_text(encoding="utf-8"))
        fecha = paquete.get("fecha") or date.today().isoformat()
        modelo = Modelo(
            version=version,
            algoritmo=str(paquete.get("algoritmo") or "desconocido"),
            fecha_entrenamiento=date.fromisoformat(str(fecha)[:10]),
            metricas_json=json.dumps(manifiesto.get("metricas", {}) if manifiesto else {},
                                     ensure_ascii=False, default=str),
            ruta_artefacto=str(candidatos[-1]) if candidatos else str(self.dir_modelos),
        )
        # HU-E6-02: el despliegue de una nueva versión la deja activa y
        # desactiva las anteriores (registro normalizado).
        for anterior in session.scalars(select(Modelo)).all():
            anterior.activo = False
        modelo.activo = True
        session.add(modelo)
        session.commit()
        logger.info("Modelo %s registrado en BD (ENT-009)", version)
        return version


inference_service = InferenceService()
