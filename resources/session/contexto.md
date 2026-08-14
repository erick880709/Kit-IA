# Contexto del Proyecto — Kit IA

## Qué es

Kit IA es un pipeline SDD (Spec-Driven Development) de **24 skills de IA** que cubre el ciclo completo de construcción de software: negocio → arquitectura → scaffold → ingeniería → entrega. Repositorio público: `erick880709/Kit-IA` (rama `main`, licencia MIT).

## Estado actual (2026-08-13)

- **Kit IA v1.0 entregado y validado**: 24/24 skills con YAML válido, 0 referencias rotas, 0 rastros corporativos.
- **Pipeline TFM completo hasta scaffold**: `janus` (16 RF + 9 RNF + 10 RT + 6 RD) → `desglosador` (43 issues) → `refinador` (IA 14/100) → `figma-prd-mockups` (9 vistas Excalidraw + mockups HTML/JPG + design system) → `archi` Caso A modo ML (`Documento_Arquitectura_TriajeIA.md` + línea base + 4 ADRs) → `genesis` (scaffold `triaje-ia/` verificado: healthcheck OK, pytest 1/1, Streamlit arranca).
- **Arquitectura decidida:** monolito modular Streamlit + SQLite (ADR-002), modelo empaquetado en proceso, fusión temprana+tardía, SHAP, umbrales por clase (recall I–II).
- **Dos skills académicos nuevos** incorporados (aún sin commitear): `tfm-redactor`, `validacion-cientifica-ml`.
- `datasets/` — CSVs reales de urgencias. **Datos sanitarios: no publicar sin autorización del Comité de Ética (Art. 2.7 UNIR).**

## Lo que sigue

1. **`builder`** sobre `triaje-ia/`: HU-E1-01 (login) → HU-E2-* → HU-E4-* en el orden del flujo clínico (handoff: `.github/resources/diseno/handoff-mockups.md`).
2. **`validacion-cientifica-ml`** cuando existan métricas de entrenamiento reales → **`tfm-redactor`** para el depósito.
3. **Completar descargas**: Línea 123 Bogotá, MIMIC-IV-Demo; buscar RIPS republicado (xveb-6jax dio 403).
4. **Actualizar README y orquestador** con los 2 skills nuevos.
5. **Validar ENT-006/007/010-012** con negocio (Supuesto #1 de la arquitectura).

## Decisiones y preguntas abiertas

- ¿Los CSVs están realmente anonimizados? Validar antes de cualquier uso o publicación.
- ¿Commitear las skills nuevas + graphify-out + vault-proyecto + triaje-ia? (recomendado: sí, son parte del kit; excluir datasets/ y .venv/).

## Riesgos

- Fuga de datos personales si `datasets/` llega al repo público.
- El README y el orquestador están desactualizados respecto de los 2 skills nuevos.
