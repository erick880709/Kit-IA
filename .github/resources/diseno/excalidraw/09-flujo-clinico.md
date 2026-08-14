# 09 — Diagrama de flujo clínico

- **Vista Excalidraw:** "Flujo clínico principal" — checkpoint `1c4392b150924a6bb8`
- **Implementa:** navegación de HU-E1→E2→E4→E2 (cierre)
- **Ruta:** Login → Registro → Signos vitales → Evaluación clínica → Clasificación IA → SHAP → Validación → Cierre
- **Decisión:** rombo "¿Concordancia?" — Sí → Cierre · No → Motivo de discrepancia (obligatorio) → Cierre
- **Nota:** reclasificación genera evento separado con trazabilidad completa
