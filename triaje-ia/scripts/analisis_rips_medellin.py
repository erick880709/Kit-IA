"""Análisis del dataset público RIPS urgencias con observación (Medellín).

Valida la cobertura del catálogo de motivos de la app y calcula severidad
real (mortalidad) por CIE-10 — insumo para validar si los motivos nuevos
del catálogo ayudan al diagnóstico de la IA.

Uso:  python scripts/analisis_rips_medellin.py
Salida: resumen en consola + JSON en artifacts/metrics/rips_medellin_resumen.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.catalogos import CATALOGO_MOTIVOS  # noqa: E402

RUTA_CSV = (
    Path(__file__).resolve().parents[2]
    / "datasets" / "rips_urgencias_observacion_medellin.csv"
)
SALIDA = (
    Path(__file__).resolve().parents[1]
    / "artifacts" / "metrics" / "rips_medellin_resumen.json"
)


def main() -> None:
    df = pd.read_csv(RUTA_CSV, low_memory=False, encoding="latin-1")
    df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce")
    df["EstadoSalida"] = df["EstadoSalida"].astype(str).str.strip()
    df["Muerto"] = df["EstadoSalida"].str.lower().str.startswith("2")

    def normalizar(codigo) -> str:
        """CIE-10 comparables: quita puntos, mayúsculas y sufijos X de relleno."""
        codigo = str(codigo).strip().upper().replace(".", "")
        if len(codigo) > 3 and codigo.endswith("X"):
            codigo = codigo[:-1]
        return codigo

    df["CodigoNorm"] = df["CodigoDiagnosticoPrincipalSalida"].map(normalizar)
    catalog_norm = {normalizar(codigo): codigo for codigo, _, _ in CATALOGO_MOTIVOS}
    df["EnCatalogo"] = df["CodigoNorm"].isin(catalog_norm)

    mortalidad_causa = (df.groupby("CausaExterna")["Muerto"].mean() * 100).round(2)

    resumen = {
        "filas": int(len(df)),
        "anios": sorted(df["Ano"].dropna().unique().astype(int).tolist()),
        "total_diagnosticos_unicos": int(df["CodigoDiagnosticoPrincipalSalida"].nunique()),
        "top15_diagnosticos": (
            df["CodigoDiagnosticoPrincipalSalida"].value_counts().head(15).to_dict()
        ),
        "cobertura_catalogo": {
            "filas_con_motivo_del_catalogo": int(df["EnCatalogo"].sum()),
            "pct_filas": round(100 * float(df["EnCatalogo"].mean()), 2),
            "motivos_del_catalogo_presentes": int(df.loc[df["EnCatalogo"], "CodigoNorm"].nunique()),
            "total_motivos_catalogo": len(catalog_norm),
        },
        "mortalidad_por_causa_externa": {
            str(k): float(v) for k, v in mortalidad_causa.items()
        },
        "severidad_motivos_catalogo": {},
    }

    # Mortalidad real por cada motivo del catálogo presente en el dataset
    por_codigo = df[df["EnCatalogo"]].groupby("CodigoNorm")
    for codigo, _, _ in CATALOGO_MOTIVOS:
        clave = normalizar(codigo)
        grupo = por_codigo.get_group(clave) if clave in por_codigo.groups else None
        if grupo is not None:
            resumen["severidad_motivos_catalogo"][codigo] = {
                "n": int(len(grupo)),
                "mortalidad_pct": round(100 * float(grupo["Muerto"].mean()), 2),
            }

    print("=== RIPS urgencias observación (Medellín) ===")
    print(f"Filas: {resumen['filas']} | Años: {resumen['anios']}")
    print(f"Cobertura del catálogo: {resumen['cobertura_catalogo']['pct_filas']}% de las filas "
          f"({resumen['cobertura_catalogo']['motivos_del_catalogo_presentes']}/"
          f"{resumen['cobertura_catalogo']['total_motivos_catalogo']} motivos presentes)")
    print("Top-15 diagnósticos (todo el dataset):")
    for codigo, n in list(resumen["top15_diagnosticos"].items())[:15]:
        print(f"  {codigo}: {n}")
    print("Mortalidad por causa externa (código -> %):")
    for causa, pct in resumen["mortalidad_por_causa_externa"].items():
        print(f"  {causa}: {pct}%")
    print("Severidad real de motivos del catálogo (mortalidad %):")
    for codigo, info in resumen["severidad_motivos_catalogo"].items():
        print(f"  {codigo}: n={info['n']} mortalidad={info['mortalidad_pct']}%")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"\nResumen guardado en {SALIDA}")


if __name__ == "__main__":
    main()
