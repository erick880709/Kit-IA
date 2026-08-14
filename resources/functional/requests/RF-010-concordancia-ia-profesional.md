# RF-010: Registro Dual IA-Profesional y Concordancia

**Tipo:** Requerimiento funcional
**Fuente:** `context/06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §1-6
**Prioridad:** Alta

## Descripción
Cada evento de triaje debe quedar con **dos clasificaciones registradas por separado**: la sugerida por la IA (`NivelSugeridoIA` + `ProbabilidadesIA` + versión de modelo) y la asignada por el profesional (`NivelAsignadoProfesional`). El sistema calcula la concordancia; si difieren, exige motivo de discrepancia. El flujo muestra primero la sugerencia de la IA y luego el profesional registra su propia clasificación, sin autocompletar ni sobrescribir.

## Actores involucrados
Médico / enfermera (clasificación propia), sistema (sugerencia, cálculo de concordancia).

## Criterios de aceptación
- El campo del profesional es obligatorio, independiente y nunca se autocompleta con el valor de la IA.
- Concordancia = `NivelSugeridoIA == NivelAsignadoProfesional` (calculado por el sistema).
- Motivo de discrepancia obligatorio cuando Concordancia = No.
- Ambos valores se guardan de forma permanente junto con `VersionModeloUsado`.

## Dependencias / relacionados
[[RF-002]], [[RF-011]], [[RF-013]], RD-003.

## Notas del analista
**Limitación metodológica para el TFM (Cap. 6):** el orden "IA primero" introduce sesgo de anclaje; la concordancia mide utilidad clínica real, no acuerdo ciego entre evaluadores. Un modo "a ciegas" quedó registrado como opción no implementada.
