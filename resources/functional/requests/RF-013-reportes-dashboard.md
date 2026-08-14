# RF-013: Reportes y Dashboard Operativo

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-REP-001 a 006) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3 · `context/06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §6
**Prioridad:** Media

## Descripción
El sistema debe ofrecer un dashboard con indicadores operativos: distribución de triaje por nivel, tiempo promedio de atención, desempeño de la IA (Accuracy/Precision/Recall/F1/AUC), y concordancia IA vs. profesional (global y por nivel, con listado filtrable de discrepancias y sus motivos). Debe generar además el registro de triaje descargable exigido por normativa: paciente anonimizado, fecha/hora, nivel IA vs. humano, signos vitales, motivo de consulta y variables SHAP de mayor peso.

## Actores involucrados
Médico / administrador (dashboard), auditor (registro descargable).

## Criterios de aceptación
- Indicadores de desempeño IA por nivel, no solo globales.
- Matriz de confusión IA vs. profesional + % concordancia global y por nivel.
- Registro de triaje descargable/visualizable con los campos normativos mínimos.

## Dependencias / relacionados
[[RF-010]], [[RF-011]], RD-004.

## Notas del analista
La comparativa de la demo (casos reales operados) es distinta de la evaluación offline del modelo (10-fold CV): dos validaciones complementarias (06 §6).
