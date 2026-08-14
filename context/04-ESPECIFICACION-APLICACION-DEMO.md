# Especificación de la Aplicación Demo

Deriva la demo funcional (decisión cerrada: modelo offline + interfaz interactiva) directamente de los módulos RF-* ya definidos en `CONTEXT_TRIA.txt`, para que sirva de insumo a diseño (mockups) y desarrollo sin tener que reinterpretar el documento de 3500 líneas cada vez.

## 1. Decisión de stack (pendiente de tu confirmación — ver `05-PENDIENTES-PARA-DIRECTORA.md`)

Streamlit o Flask, ambas mencionadas sin decidir en los documentos de origen. Recomendación no vinculante: **Streamlit** — menor esfuerzo para un prototipo con formularios + visualización SHAP + dashboard, dado el alcance de TFM (Tipo 2+3, no producto productivo).

## 2. Roles (RF-SEC-002, sin cambios)

Administrador, Médico, Enfermera, Investigador, Auditor. Cada pantalla abajo indica qué rol(es) la usan.

## 3. Inventario de pantallas

Derivado de los módulos funcionales (`RF-PAC-*`, `RF-TRI-*`, `RF-VIT-*`, `RF-EVA-*`, `RF-IA-*`, `RF-XAI-*`, `RF-AUD-*`, `RF-REP-*`, `RF-MOD-*`, `RF-SEC-*`) — cada pantalla referencia los requerimientos que implementa.

| Pantalla | Rol(es) | Propósito | Requerimientos que cubre | Estados a diseñar |
|---|---|---|---|---|
| Login | Todos | Autenticación | RF-SEC-001, RF-SEC-003, RF-SEC-004 | — |
| Registro de paciente | Administrativo | Alta de episodio, búsqueda de duplicados | RF-PAC-001 a 004 | Vacío, error de validación |
| Captura de signos vitales | Enfermera | Ingreso de FR, SpO₂, PA, FC, temperatura, peso/talla (IMC auto) | RF-VIT-001 a 010 | Alerta por valor fuera de rango |
| Evaluación clínica | Enfermera / Médico | Motivo de consulta, dolor, Glasgow, nivel de conciencia, antecedentes, alergias, texto libre | RF-EVA-001 a 007 | — |
| Ejecutar clasificación IA | Médico / Enfermera | Dispara la inferencia, muestra probabilidades por nivel (I-V), **y captura la clasificación independiente del profesional en el mismo flujo** — ver `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` | RF-IA-001 a 003, 006, 009, 010 | Cargando (async), error de inferencia |
| Explicación SHAP | Médico | Top variables, impacto +/-, gráficos interpretables, comparación con MTS | RF-XAI-001 a 006 | — |
| Validación de triaje | Médico | Registrar motivo de discrepancia cuando el nivel del profesional difiere del sugerido por IA (decisión humana siempre prevalece) | RF-TRI-003, 004, 005 | Discrepancia (motivo obligatorio) |
| Comparación de modelos | Investigador | Ver early vs. late fusion lado a lado sobre el mismo caso/dataset | RF-IA-007, RF-MOD-* | — |
| Gestión de modelos | Administrador | Registrar, versionar, activar/desactivar (rollback) modelos | RF-MOD-001 a 005 | Vacío (sin modelos registrados) |
| Dashboard operativo | Médico / Administrador | Indicadores, distribución de triaje por nivel, tiempo promedio, desempeño IA (Accuracy/Precision/Recall/F1/AUC), concordancia IA vs. profesional | RF-REP-001 a 005 | Vacío (sin datos aún) |
| Auditoría | Auditor | Consulta y exportación (CSV/Excel/PDF) de todas las acciones | RF-AUD-001 a 006 | Vacío (sin resultados de filtro) |
| Registro de triaje descargable | Médico / Auditor | Resumen exigido por normativa: paciente anonimizado, fecha/hora, nivel IA vs. humano, signos vitales, motivo, SHAP top | RF-REP-006, requisito normativo (`02-...md` §7) | — |

## 4. Flujo principal (para prototipos click-through)

```
Login → Registro de paciente → Captura de signos vitales → Evaluación clínica
   → Ejecutar clasificación IA → Explicación SHAP → Validación de triaje
   → (rama) Reclasificación si aplica → Cierre del evento
```

Pantallas de Comparación de modelos, Gestión de modelos, Dashboard y Auditoría son de soporte/administración, no parte del flujo clínico principal — diseñarlas después del flujo principal.

## 5. Siguiente paso sugerido

Este inventario de pantallas es exactamente el input que espera la skill `figma-prd-mockups` — puedes pasarle este archivo directamente para que genere los mockups en Figma antes de que el skill de desarrollo/builder empiece a construir la demo.
