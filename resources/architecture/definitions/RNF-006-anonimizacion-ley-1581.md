# RNF-006: Anonimización y Protección de Datos (Ley 1581 de 2012)

**Tipo:** Requerimiento no funcional
**Categoría:** Seguridad / Cumplimiento normativo
**Fuente:** `context/CONTEXTO TRIAJE.txt` §9 · `context/03-CATALOGO-DATOS-Y-VARIABLES.md` §4 · `context/CONTEXT TRIA.txt` (RNS-009, RNS-010, RNGD-*)

## Descripción
Todos los datos personales y sanitarios deben ser anonimizados antes de cualquier procesamiento, almacenamiento o exportación.

## Criterio medible / restricción concreta
- Anonimización obligatoria **antes** de cualquier paso del pipeline (ingesta → entrenamiento → exportación).
- Cumplimiento de la Ley 1581 de 2012 (protección de datos personales, Colombia).
- El uso del registro clínico del Hospital San Juan de Dios requiere la autorización del Comité de Ética (Art. 2.7 Reglamento UNIR) — estado: APROBADA según v2.0 (16 jul 2026); pendiente reflejar en el PDF oficial.
- El registro de triaje generado muestra paciente anonimizado.

## Impacto en la arquitectura
Define un paso de anonimización en el pipeline (antes de limpieza) y restringe qué campos pueden persistirse/exportarse. Los datasets locales con datos reales (`datasets/`) no deben publicarse en repositorios abiertos.

## Notas del analista
**Riesgo abierto:** `datasets/` contiene CSVs de datos reales y el repo del kit es público — mantener excluidos de Git hasta validar anonimización.
