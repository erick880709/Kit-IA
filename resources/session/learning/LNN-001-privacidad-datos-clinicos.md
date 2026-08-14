---
fecha: 2026-08-13
fase: entrega
tags: [privacidad, datos-sanitarios, github, datasets]
severidad: alta
---

# LNN-001: Datos clínicos reales no deben versionarse en un repo público

## Contexto
Al incorporar el proyecto TFM (triaje de urgencias UNIR) al workspace del Kit IA, `datasets/` quedó con 4 CSVs de datos reales de urgencias (triage y morbilidad hospitalaria).

## Decisión
No commitear `datasets/` ni el grafo/vault derivados hasta validar anonimización. El brief del TFM cita el Art. 2.7 del reglamento UNIR: datos sanitarios exigen autorización del Comité de Ética antes de la recogida.

## Consecuencia
El repo público queda solo con el kit. Los datos del TFM permanecen locales. Pendiente: confirmar anonimización o agregar `datasets/` a `.gitignore`.

## Revalidación
Revisar cuando el usuario decida la estrategia de versionado del TFM.
