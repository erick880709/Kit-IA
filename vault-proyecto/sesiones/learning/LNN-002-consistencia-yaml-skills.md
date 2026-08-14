---
fecha: 2026-08-13
fase: entrega
tags: [learning, skills, consistencia, yaml]
severidad: media
proyecto: Kit IA
---

# LNN-002: Validar consistencia YAML (name = carpeta) antes de commitear skills nuevos

## Contexto
Aparecieron desajustes: `name` de `front` decía `frontend-design`, carpetas con nombres viejos tras renombrados, referencias rotas.

## Decisión
Antes de commitear skills nuevos validar: (1) `name` = carpeta, (2) referencias internas existen, (3) README y orquestador los listan.

## Consecuencia
24/24 skills pasan validación. Deuda detectada: los 2 skills nuevos faltan en README y orquestador.

## Revalidación
Antes del próximo push: verificar README + árbol del orquestador con 24 skills.
