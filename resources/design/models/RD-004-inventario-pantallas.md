# RD-004: Inventario de Pantallas de la Demo

**Tipo:** Información de diseño
**Fuente:** `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3 · `context/06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §7

## Descripción
Inventario completo de pantallas de la demo, derivado de los módulos funcionales, listo como input para mockups (figma-prd-mockups).

| Pantalla | Rol(es) | Requerimientos que cubre |
|---|---|---|
| Login | Todos | RF-SEC-001, 003, 004 |
| Registro de paciente | Administrativo | RF-PAC-001 a 004 |
| Captura de signos vitales | Enfermera | RF-VIT-001 a 010 |
| Evaluación clínica | Enfermera / Médico | RF-EVA-001 a 007 |
| Ejecutar clasificación IA | Médico / Enfermera | RF-IA-001 a 003, 006, 009, 010 + captura `NivelAsignadoProfesional` |
| Explicación SHAP | Médico | RF-XAI-001 a 006 |
| Validación de triaje | Médico | RF-TRI-003 a 005 (captura MotivoDiscrepancia) |
| Comparación de modelos | Investigador | RF-IA-007, RF-MOD-* |
| Gestión de modelos | Administrador | RF-MOD-001 a 005 |
| Dashboard operativo | Médico / Administrador | RF-REP-001 a 005 |
| Auditoría | Auditor | RF-AUD-001 a 006 |
| Registro de triaje descargable | Médico / Auditor | RF-REP-006 + normativa |

## Estados de pantalla a diseñar
Vacío, error de validación, alerta por valor fuera de rango, cargando (async), error de inferencia, discrepancia (motivo obligatorio), vacío sin modelos registrados, vacío sin resultados de filtro.
