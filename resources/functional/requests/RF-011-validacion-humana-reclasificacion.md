# RF-011: Validación Humana y Reclasificación

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-TRI-003 a 005) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3-4
**Prioridad:** Alta

## Descripción
La decisión humana prevalece siempre sobre la sugerencia de la IA. El médico valida el nivel de triaje, registra motivo de discrepancia cuando su nivel difiere del sugerido por la IA, y puede reclasificar al paciente si las condiciones clínicas cambian. La reclasificación posterior se registra como evento separado, sin alterar el registro inicial de concordancia.

## Actores involucrados
Médico (validación y reclasificación).

## Criterios de aceptación
- El nivel del profesional nunca es sobrescrito por el sistema.
- Discrepancia → motivo obligatorio (catálogo o texto corto).
- Reclasificación = nuevo evento con trazabilidad completa (RNA-010, RF-AUD-*).

## Dependencias / relacionados
[[RF-002]], [[RF-010]], [[RF-012]], [[RNF-008]].

## Notas del analista
Pantalla "Validación de triaje" del inventario 04 §3; en el flujo actualizado (06 §7) es donde se captura el MotivoDiscrepancia.
