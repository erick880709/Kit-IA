---
fecha: 2026-08-13
tags: [kit-ia, sesiones]
proyecto: Kit IA
---

# Contexto actual

Kit IA es un pipeline SDD de **24 skills** que cubre negocio → arquitectura → scaffold → ingeniería → entrega (repo público `erick880709/Kit-IA`, MIT).

**Estado (2026-08-13):**
- Kit IA v1.0 entregado y validado (24/24 skills, 0 referencias rotas).
- Skills académicos nuevos: [[tfm-redactor]] y [[validacion-cientifica-ml]] (sin commitear).
- Proyecto activo: TFM triaje multimodal IA (UNIR) — ver [[MOC-TFM]].

**Lo que sigue:**
1. Resolver privacidad de `datasets/` ([[datasets-privacidad]]).
2. Actualizar README + [[orquestador]] con los 2 skills nuevos.
3. Iniciar pipeline TFM: [[janus]] → [[refinador]] → [[archi]] → [[builder]].

**Decisiones abiertas:**
- ¿Versionar `context/` y `datasets/` en repo público? (Art. 2.7 UNIR)

**Riesgos:**
- Fuga de datos sanitarios si `datasets/` se publica.
- README y orquestador desactualizados.

Fuente canónica: `resources/session/contexto.md`
