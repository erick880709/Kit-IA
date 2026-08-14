---
fecha: 2026-08-14
tags: [tfm, triaje, capitulos, deposito]
proyecto: TFM Triaje IA UNIR
---

# Capítulos TFM generados (hechos consumados)

Redactados por `tfm-redactor` con cifras verificadas contra `triaje-ia/artifacts/`.
Ningún número fue inventado; los trámites externos quedaron marcados como pendientes.

- [[tfm-triaje/capitulo-resumen-abstract|00 · Resumen/Abstract]] — ES/EN con métricas reales
- [[tfm-triaje/capitulo-desarrollo|04 · Desarrollo de la contribución]] — arquitectura y pipeline en pretérito
- [[tfm-triaje/capitulo-resultados|05 · Resultados y discusión]] — tablas 5.1–5.10 con columna Fuente
- [[tfm-triaje/capitulo-conclusiones|07 · Conclusiones y trabajo futuro]] — metas alcanzadas/no alcanzadas con honestidad
- [[tfm-triaje/checklist-cumplimiento-unir|Checklist de cumplimiento UNIR]] — 2 bloqueantes externos + 3 hallazgos de trazabilidad resueltos

## Métricas reales clave (fuente: `triaje-ia/artifacts/metrics/`)

- Ganador (fusión tardía afinada): exactitud 0.978 · AUC-ROC macro 0.968 · macro-F1 0.551 (test, n=600)
- CV 5 folds: fusión temprana F1 0.578 · tardía promedio 0.555 · stacking 0.560
- Holdout SJdD (sin fuga): F1 0.088 · McNemar vs regla mayoritaria p≈0 · Brier 0.036 · ECE 0.042
