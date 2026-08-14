# RF-TRI-005: Cierre del Evento de Triaje

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 41, Módulo de Triaje
**Prioridad:** Alta

## Descripción
El sistema permitirá cerrar formalmente un evento de triaje únicamente cuando se hayan cumplido todas las condiciones mínimas: clasificación asignada, validación por profesional y registro de auditoría. El cierre impide modificaciones posteriores sin una reclasificación formal.

## Actores involucrados
- Enfermera de Triaje
- Médico de Urgencias

## Criterios de aceptación
- Condiciones obligatorias para el cierre: (1) clasificación de triaje asignada (Nivel I-V), (2) validación por profesional registrada (`NivelAsignadoProfesional`), (3) registro de auditoría mínimo generado.
- Si hay discrepancia entre IA y profesional (Concordancia = No), el campo `MotivoDiscrepancia` es obligatorio antes de permitir el cierre.
- Un evento cerrado no puede ser modificado directamente — solo mediante reclasificación formal (RF-TRI-004).
- El sistema registra la fecha y hora de cierre.
- El evento cerrado queda disponible para consulta, auditoría y reportes.

## Dependencias / relacionados
- RNG-005: Ningún evento de triaje puede eliminarse físicamente.
- RF-TRI-003: Estados del Triaje.
- RF-TRI-004: Reclasificación.
- `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md`: flujo de cierre con captura de concordancia.

## Notas del analista
- El campo `Concordancia` (calculado automáticamente como `NivelSugeridoIA == NivelAsignadoProfesional`) habilita la comparativa IA vs. profesional definida en `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md`.
