---
fecha: 2026-08-14
fase: entrega
tags: [git, gitignore, versionado, datos]
severidad: media
---

# LNN-003: Un patrón con barra intermedia en .gitignore queda anclado a la carpeta del .gitignore

## Contexto

El `.gitignore` de `triaje-ia/` tenía `data/*` con la intención de excluir los CSV crudos. Los archivos reales vivían en `triaje-ia/ml/data/raw/`, y `git add triaje-ia` los dejó staged: la exclusión nunca funcionó.

## Hallazgo

Un patrón con `/` en el medio (`data/*`) es **relativo al directorio del propio `.gitignore`** (solo excluye `triaje-ia/data/*`), no a cualquier nivel. Para excluir una ruta anidada hay que escribir la ruta completa relativa al `.gitignore` (`ml/data/raw/*`) o usar un patrón sin barra intermedia.

## Regla

- Antes de commitear, verificar con `git check-ignore -v <ruta>` que las exclusiones realmente aplican — un patrón "obvio" puede estar anclado sin darte cuenta.
- Revisar `git status --short` tras `git add` para detectar archivos que debían quedar fuera.

## Evidencia

- `git check-ignore -v triaje-ia\ml\data\raw\prueba.csv` → sin coincidencia con `data/*`.
- `git check-ignore -v triaje-ia\datasets\x.csv` → sí coincidía con `datasets/` (patrón sin anclaje engañoso).
