# RF-008: Gestión y Comparación de Modelos

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-IA-007, RF-IA-008; RF-MOD-001 a 005) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Media

## Descripción
El sistema debe permitir comparar múltiples modelos (early vs late fusion) sobre el mismo caso o dataset durante las pruebas, y gestionar el ciclo de vida de los modelos: registro, versionado, activación, desactivación (rollback) e historial. Solo usuarios autorizados pueden cambiar el modelo activo.

Cubre: RF-IA-007 (Comparación), RF-IA-008 (Cambio de modelo), RF-MOD-001 a 005.

## Actores involucrados
Investigador (comparación), administrador (gestión de modelos).

## Criterios de aceptación
- La comparación muestra early y late fusion lado a lado.
- Activación/desactivación de versiones con historial completo (rollback posible).
- El cambio de modelo activo exige rol autorizado.

## Dependencias / relacionados
[[RF-006]], [[RF-014]], [[RT-010]].

## Notas del analista
La coexistencia de versiones está soportada por RNA-006 del documento funcional; es la base funcional de la comparativa exigida por el TFM.
