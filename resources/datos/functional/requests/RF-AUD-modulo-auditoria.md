# RF-AUD: Módulo de Auditoría

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 47, Módulo Auditoría; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md §7
**Prioridad:** Alta

## Descripción
El sistema registrará de forma inmutable todas las acciones realizadas sobre cada evento de triaje, incluyendo creación, modificaciones, ejecuciones de IA, validaciones del profesional y cierres. La auditoría es el mecanismo que garantiza la trazabilidad completa exigida por la normativa colombiana y por los principios de gobernanza del dato del proyecto.

## Actores involucrados
- Sistema (registro automático)
- Auditor (consulta y exportación)
- Administrador

## Criterios de aceptación

### RF-AUD-001 — Registrar Todas las Acciones
- Todo evento del sistema genera un registro de auditoría: creación de paciente, registro de signos vitales, ejecución de IA, validación, reclasificación, cierre, cambio de modelo activo, inicio/cierre de sesión.

### RF-AUD-002 — Registrar Usuario Responsable
- Cada registro de auditoría incluye el identificador del usuario que realizó la acción.

### RF-AUD-003 — Registrar Fecha y Hora
- Marca de tiempo en UTC para cada acción, con precisión de milisegundos.

### RF-AUD-004 — Registrar Cambios (Valor Anterior / Valor Nuevo)
- Toda modificación de datos clínicos registra el valor anterior y el nuevo valor (RNG-008, RNG-009).
- Aplica a: signos vitales, nivel de triaje, estado del evento, modelo activo.

### RF-AUD-005 — Consultar Auditoría
- Búsqueda con filtros por: usuario, paciente, fecha (rango), modelo/versión, tipo de acción, nivel de triaje.
- Resultados paginados y ordenables.
- Accesible solo para el rol Auditor y Administrador.

### RF-AUD-006 — Exportar Auditoría
- Formatos de exportación: CSV, Excel, PDF.
- La exportación respeta los filtros aplicados en la consulta.
- Los datos exportados de pacientes deben estar anonimizados si el destino es externo a la institución (RNS-009, Ley 1581 de 2012).

### Registro de Triaje para Normativa (requisito adicional, fuente `02-...` §7)
- Cada evento cerrado debe poder generar un resumen descargable que cumpla con los requisitos de registro de triaje de la normativa colombiana: paciente anonimizado, fecha/hora, nivel IA sugerido vs. nivel asignado por el profesional, signos vitales, motivo de consulta, top variables SHAP.
- Este resumen es adicional a los registros individuales de auditoría.

## Dependencias / relacionados
- RNAU-001 a 006: Reglas de Auditoría.
- RNG-007: Historial completo de modificaciones.
- RNG-008: Ningún dato se sobrescribe sin conservar valor anterior.
- RNG-009: Todo cambio registra: usuario, fecha, hora, motivo, valor anterior, valor nuevo.
- RNS-009: Cumplimiento Ley 1581 de 2012.
- `04-ESPECIFICACION-APLICACION-DEMO.md`: pantalla de Auditoría.

## Notas del analista
- La auditoría es el mecanismo que habilita la detección de deriva (RNA-010) y la comparativa IA vs. profesional (RF-REP-005).
- Los registros de auditoría son append-only (RNAU-003: no se permite eliminar registros).
