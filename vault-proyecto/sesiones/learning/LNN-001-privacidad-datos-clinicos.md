---
fecha: 2026-08-13
fase: entrega
tags: [learning, privacidad, datos-sanitarios]
severidad: alta
proyecto: Kit IA
---

# LNN-001: Datos clínicos reales no deben versionarse en un repo público

## Contexto
Al incorporar el TFM (triaje UNIR) al workspace, `datasets/` quedó con 4 CSVs de datos reales de urgencias.

## Decisión
No commitear `datasets/` hasta validar anonimización. Art. 2.7 UNIR: datos sanitarios exigen autorización del Comité de Ética.

## Consecuencia
El repo público queda solo con el kit; los datos permanecen locales. Ver [[datasets-privacidad]].

## Revalidación
Revisar cuando se decida la estrategia de versionado del TFM.
