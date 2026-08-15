---
fecha: 2026-08-14
tags: [tfm, triaje, validacion-cientifica, datos, ml]
proyecto: TFM Triaje IA UNIR
fase: validacion
origen: "[[tfm-triaje/07-mapeo-descarga-datasets]]"
---

# Validación de motivos del catálogo + RIPS Medellín

## Nuevo dato público descargado

- **RIPS urgencias con observación (Medellín):** 1.708.104 registros 2019-2022
  (`datasets/rips_urgencias_observacion_medellin.csv`, 207 MB) desde
  `medata.gov.co` (federado de datos.gov.co `xveb-6jax`).
- Incluye CIE-10 de salida, causa externa y **estado de salida (vivo/muerto)**.
- Descarga con `curl -sk` (cadena TLS del portal no confiable desde Windows).
- CIE-10 codificado sin punto y con sufijo `X` (normalizar al cruzar).

## Cobertura del catálogo (71 motivos)

- **61/71 motivos presentes** en datos reales; **26,94 % de 1,7 M filas**.
- Mortalidad real por CIE: J96.0 28,3 % · J18.9 7,6 % · R06.0 7,6 % ·
  K92.2 4,4 % · R10.4 3,1 %. ⚠ La unidad de observación subestima la
  severidad del trauma (W34.9 n=9, 0 % porque el trauma grave se deriva).

## Impacto en la IA (validado)

- Solo **1/71 motivos** cambia la sugerencia (K92.2 → I); 8 motivos con
  cobertura 0 de vocabulario TF-IDF.
- **Conclusión honesta:** los motivos mejoran captura/cobertura clínica, pero
  HOY no cambian el diagnóstico. Ajuste: vocabulario TF-IDF extendido con el
  catálogo (`textos_extra`) listo para reentrenar con MIMIC-IV-ED.
- Detalle: `resources/tfm/validacion-cientifica/validacion-motivos-catalogo-rips.md`.

## MIMIC-IV-ED

- Solo con credenciales (CITI + DUA) — guía en [[tfm-triaje/07-mapeo-descarga-datasets]].
- Código listo: `ingestar_mimic_ed()` + pipeline + tests. Reentrenar al tener los CSV.

## Relacionado

- [[tfm-triaje/capitulos-tfm|Capítulos TFM]]
- [[tfm-triaje/evidencia-ingenieria|Evidencia de ingeniería]]
- [[tfm-triaje/despliegue-docker-hostinger|Despliegue Docker + Hostinger]]
