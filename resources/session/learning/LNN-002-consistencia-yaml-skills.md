---
fecha: 2026-08-13
fase: entrega
tags: [skills, consistencia, validacion, yaml]
severidad: media
---

# LNN-002: Validar consistencia YAML (name = carpeta) antes de commitear skills nuevos

## Contexto
Durante la construcción del kit aparecieron desajustes: el YAML `name` de `front` decía `frontend-design`, carpetas con nombres viejos tras renombrados, y referencias rotas entre skills.

## Decisión
Cada vez que se agrega o renombra un skill, correr una validación: (1) `name` del frontmatter coincide con el nombre de carpeta, (2) ninguna referencia interna apunta a rutas inexistentes, (3) el orquestador y el README lo listan.

## Consecuencia
Los 24 skills pasan la validación. Los 2 skills nuevos (tfm-redactor, validacion-cientifica-ml) quedaron pendientes de integrar en README y orquestador — la validación detecta esa deuda.

## Revalidación
Antes del próximo push: verificar README + árbol del orquestador con los 24 skills.
