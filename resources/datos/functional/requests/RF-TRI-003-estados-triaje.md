# RF-TRI-003: Gestión de Estados del Triaje

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 41, Módulo de Triaje; 06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md
**Prioridad:** Crítica

## Descripción
El sistema gestionará el ciclo de vida completo de un evento de triaje mediante una máquina de estados que controla las transiciones permitidas y asegura la integridad del proceso clínico. Los estados reflejan el avance del paciente desde el registro hasta el cierre, incluyendo la ejecución de IA y la validación del profesional.

## Actores involucrados
- Sistema (gestiona transiciones automáticas)
- Enfermera de Triaje
- Médico de Urgencias

## Criterios de aceptación
- Estados definidos: Registrado → En evaluación → Pendiente IA → Clasificado → Validado → Cerrado. El estado "Cancelado" es un estado terminal alternativo.
- Transiciones controladas: no se permite saltar estados sin pasar por los intermedios obligatorios.
- El estado "Pendiente IA" se activa automáticamente al solicitar la ejecución del modelo (RF-IA-001).
- El estado "Clasificado" requiere que la IA haya generado una predicción con todos los campos obligatorios (nivel, probabilidad, confianza, versión del modelo).
- El estado "Validado" requiere que el profesional haya registrado su propia clasificación (`NivelAsignadoProfesional`), independiente de la sugerencia de IA.
- El estado "Cerrado" solo se alcanza con clasificación, validación y registro de auditoría completos (RF-TRI-005).
- Los estados se reflejan visualmente en la interfaz para que el profesional sepa en qué etapa está cada paciente.

## Dependencias / relacionados
- RF-TRI-001: Crear Evento de Triaje.
- RF-TRI-004: Reclasificación.
- RF-TRI-005: Cierre del Evento.
- RF-IA-001: Ejecutar Inferencia.
- `06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md`: flujo detallado de la pantalla de clasificación.

## Notas del analista
- El flujo de la pantalla de clasificación (documento `06-...`) especifica que el profesional ve primero la sugerencia de la IA y luego registra su propia clasificación en un campo separado. Esto introduce un sesgo de anclaje que debe documentarse como limitación metodológica en el TFM (Cap. 6).
