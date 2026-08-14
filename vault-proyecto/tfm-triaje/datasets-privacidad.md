---
fecha: 2026-08-13
tags: [tfm, privacidad, seguridad, unir]
proyecto: TFM Triaje IA UNIR
severidad: alta
---

# ⚠️ datasets-privacidad — Datos clínicos reales

## Situación

`datasets/` contiene 4 CSVs con **datos reales de urgencias médicas** (triage y morbilidad hospitalaria), incluyendo registros del Hospital San Juan de Dios.

## Riesgo

El repo `erick880709/Kit-IA` es **público**. Publicar datos sanitarios personales viola la normativa de protección de datos y el **Art. 2.7 del Reglamento UNIR** (requiere autorización previa del Comité de Ética de la Investigación).

## Estado

- ❌ `datasets/` y `context/` NO han sido commiteados.
- ✅ El grafo y este vault son locales.
- Pendiente: validar anonimización de los CSVs o agregar `datasets/` a `.gitignore`.

## Acciones recomendadas

1. Verificar que los CSVs no contengan identificadores (nombres, DNI, direcciones).
2. Si los contienen: anonimizar o excluir del repo.
3. Agregar a `.gitignore`:

```
datasets/
context/
```

Ver también [[sesiones/learning/LNN-001-privacidad-datos-clinicos|LNN-001]].
