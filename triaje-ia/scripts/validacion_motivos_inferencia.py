"""Valida el impacto de los motivos del catálogo en la inferencia del modelo.

Para cada motivo: inferencia con signos vitales FIJOS moderados y el motivo
como CIE-10 + texto. Compara contra una línea base sin motivo y mide cuántos
tokens del motivo existen en el vocabulario TF-IDF del submodelo de texto.

Uso:  python scripts/validacion_motivos_inferencia.py
Salida: artifacts/metrics/validacion_motivos_inferencia.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.catalogos import CATALOGO_MOTIVOS  # noqa: E402
from app.services.inference_service import inference_service  # noqa: E402

SALIDA = (
    Path(__file__).resolve().parents[1]
    / "artifacts" / "metrics" / "validacion_motivos_inferencia.json"
)

DATOS_BASE = {
    "temperatura": 37.0,
    "frecuencia_cardiaca": 82,
    "frecuencia_respiratoria": 17,
    "saturacion_o2": 97,
    "presion_sistolica": 118,
    "presion_diastolica": 76,
    "peso": 68.0,
    "talla": 1.66,
    "episodios_previos_urgencias": 1,
    "anio_nacimiento": 1985,
    "sexo": "Femenino",
    "via_llegada": "Particular",
    "regimen": "Contributivo",
    "departamento": "Antioquia",
}


def _vocabulario() -> dict[str, int] | None:
    paquete = inference_service._cargar()  # noqa: SLF001 — introspección de validación
    if paquete is None:
        return None
    vectorizador = paquete.get("vectorizador_texto")
    if vectorizador is None:
        return None
    return getattr(vectorizador, "_vectorizador", None) and dict(
        vectorizador._vectorizador.vocabulary_  # noqa: SLF001
    )


def _predecir(motivo_codigo: str = "", motivo_texto: str = "") -> dict:
    datos = dict(DATOS_BASE)
    datos["motivo_codigo_cie10"] = motivo_codigo
    datos["motivo_texto"] = motivo_texto
    return inference_service.predecir(datos)


def main() -> None:
    vocab = _vocabulario()
    if vocab is None:
        print("ERROR: modelo o vectorizador no disponibles")
        return
    print(f"Vocabulario TF-IDF del submodelo de texto: {len(vocab)} términos")

    base = _predecir()
    print(f"Línea base (sin motivo): nivel={base.get('nivel_sugerido')} "
          f"confianza={base.get('confianza')}")

    resultados = []
    cambian = 0
    por_nivel: dict[str, int] = {}
    for codigo, descripcion, categoria in CATALOGO_MOTIVOS:
        res = _predecir(motivo_codigo=codigo, motivo_texto=descripcion)
        nivel = res.get("nivel_sugerido")
        por_nivel[nivel] = por_nivel.get(nivel, 0) + 1
        if nivel != base.get("nivel_sugerido"):
            cambian += 1
        tokens = set(str(codigo).upper().split()) | set(
            (codigo + " " + descripcion).lower().replace(",", "").split()
        )
        cobertura = len(tokens & set(vocab)) / len(tokens) if tokens else 0.0
        resultados.append(
            {
                "codigo": codigo,
                "descripcion": descripcion,
                "categoria": categoria,
                "nivel_sugerido": nivel,
                "confianza": res.get("confianza"),
                "tiempo_ms": res.get("tiempo_ms"),
                "cobertura_tokens_vocab": round(cobertura, 3),
            }
        )

    total = len(CATALOGO_MOTIVOS)
    resumen = {
        "vocab_tamano": len(vocab),
        "base": {"nivel": base.get("nivel_sugerido"), "confianza": base.get("confianza")},
        "total_motivos": total,
        "motivos_que_cambian_nivel": cambian,
        "pct_que_cambian": round(100 * cambian / total, 1),
        "distribucion_niveles": por_nivel,
        "detalle": resultados,
    }
    print(f"Motivos que CAMBIAN la sugerencia vs línea base: {cambian}/{total} "
          f"({resumen['pct_que_cambian']}%)")
    print(f"Distribución de niveles sugeridos: {por_nivel}")
    print("\nMotivos con cobertura de vocabulario = 0 (el texto NO influye):")
    for r in resultados:
        if r["cobertura_tokens_vocab"] == 0.0:
            print(f"  {r['codigo']} {r['descripcion']} ({r['categoria']})")
    print("\nNiveles sugeridos I/II (alta urgencia) por motivo:")
    for r in resultados:
        if r["nivel_sugerido"] in ("I", "II"):
            print(f"  {r['codigo']} {r['descripcion']} → {r['nivel_sugerido']}")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGuardado en {SALIDA}")


if __name__ == "__main__":
    main()
