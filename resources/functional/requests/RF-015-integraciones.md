# RF-015: Integraciones

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-INT-001 a 004) · `context/03-CATALOGO-DATOS-Y-VARIABLES.md` §1
**Prioridad:** Media

## Descripción
El sistema debe integrarse, cuando la disponibilidad institucional lo permita, con la Historia Clínica Electrónica para alimentar antecedentes (RF-INT-001), con sistemas hospitalarios para admisión y datos demográficos (RF-INT-002), y debe poder exportar datos (RF-INT-003) y generar el dataset de entrenamiento como exportación anonimizada (RF-INT-004).

## Actores involucrados
Sistema (integraciones), administrador (configuración).

## Criterios de aceptación
- Sin integración con HCE disponible, los antecedentes se capturan por autorreporte (RF-EVA-005).
- Toda exportación pasa por anonimización previa ([[RNF-006]]).
- El dataset de entrenamiento exportado no incluye identificadores directos ni indirectos.

## Dependencias / relacionados
[[RF-001]], [[RF-004]], [[RNF-006]], [[RT-006]].

## Notas del analista
RF-INT-004 original no nombraba fuentes de datos; el catálogo (03 §2) las mapea explícitamente (hallazgo #2 de la validación).
