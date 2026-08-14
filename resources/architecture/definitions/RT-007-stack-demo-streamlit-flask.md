# RT-007: Stack de la Demo (Streamlit o Flask) — DECISIÓN PENDIENTE

**Tipo:** Requisito técnico
**Categoría:** Stack tecnológico
**Fuente:** `context/04-ESPECIFICACION-APLICACION-DEMO.md` §1 · `context/05-PENDIENTES-PARA-DIRECTORA.md` §1

## Descripción
La demo funcional interactiva se construye con Streamlit o Flask — ambas opciones aparecen en los documentos de origen sin decisión tomada.

## Criterio medible / restricción concreta
- Alcance: modelo offline + demo funcional (dashboard interactivo con formularios, probabilidades, SHAP, auditoría).
- **Decisión cerrada (refinador, 2026-08-13, IA 14/100): Streamlit.** Flask queda documentado como alternativa. Ver `resources/functional/reqs/001-decisiones-demo-triaje-ia.md`.
- **Entorno de despliegue (extracción previa `resources/datos/definitions/RT-007`):** máquina local sin GPU; Python 3.10+ con `requirements.txt`; arranque en un solo comando; persistencia en **SQLite** (archivo local); datos sintéticos precargados (~100-200 pacientes con distribución realista de niveles I-V); modelos cargados desde artefactos serializados (pickle/joblib/h5); demo autocontenida sin dependencia de servicios cloud ni internet en inferencia.
- Si se elige Streamlit: evaluar `streamlit-shap` para las visualizaciones SHAP nativas.
- Empaquetado opcional como imagen Docker para reproducibilidad; grabación de video de la demo como respaldo para la sustentación.

## Impacto en la arquitectura
Determina la capa web de la demo (estilo de componentes, manejo de sesión, despliegue); el modelo se sirve igual en ambos casos (artefacto serializado + API interna).

## Notas del analista
No bloquear el diseño: la decisión afecta solo la capa de presentación. Pendiente #1 de `05-PENDIENTES-PARA-DIRECTORA.md`.
