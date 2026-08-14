---
fecha: 2026-08-13
tags: [tfm, triaje, unir, moc]
proyecto: TFM Triaje IA UNIR
---

# 🎓 MOC — TFM Triaje IA (UNIR)

**Título:** Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia
**Autores:** Medina Betancur, D. · Rivera Villanueva, L. · Soto Díaz, E.
**Directora:** Damaris Fuentes Lorenzo
**Estado:** Predepósito (Ordinaria) — 14/07/2026

## Documentos de contexto (`context/`)

- [[tfm-triaje/brief_finalizacion_tfm|Brief de finalización]] — briefing operativo con reglas UNIR
- [[tfm-triaje/00-validacion-hallazgos|00 · Validación de hallazgos]]
- [[tfm-triaje/01-contexto-maestro|01 · Contexto maestro consolidado]]
- [[tfm-triaje/02-especificacion-tecnica-modelos|02 · Especificación técnica de modelos IA]]
- [[tfm-triaje/03-catalogo-datos|03 · Catálogo de datos y variables]]
- [[tfm-triaje/04-especificacion-app-demo|04 · Especificación de la app demo]]
- [[tfm-triaje/07-mapeo-descarga-datasets|07 · Mapeo y descarga de datasets]]

## Datos

- [[datasets-privacidad]] — ⚠️ advertencia de privacidad (datos clínicos reales)

## Skills del kit aplicables

- [[janus]] → extraer requerimientos del brief
- [[archi]] → arquitectura del sistema multimodal
- [[builder]] → scaffold del pipeline ML
- [[validacion-cientifica-ml]] → rigor científico antes de declarar resultados
- [[tfm-redactor]] → redactar capítulos depositables

## Pipeline sugerido

```mermaid
flowchart LR
    A[janus sobre context/] --> B[refinador]
    B --> C[archi]
    C --> D[builder]
    D --> E[validacion-cientifica-ml]
    E --> F[tfm-redactor]
```

## Cierre del proyecto (2026-08-14)

- [[tfm-triaje/capitulos-tfm|Capítulos TFM generados]] — resumen, desarrollo, resultados, conclusiones + checklist UNIR
- [[tfm-triaje/evidencia-ingenieria|Evidencia de ingeniería]] — hardening, performance, release, auditoría científica
- [[sesiones/learning/LNN-003-gitignore-patron-anclado|LNN-003 · gitignore anclado]] · [[sesiones/learning/LNN-004-hash-antes-de-deserializar|LNN-004 · CWE-502]] · [[sesiones/learning/LNN-005-timeout-deterministico|LNN-005 · timeout flaky]]
