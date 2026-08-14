# RF-TRI-002: Registrar Hora de Inicio

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 41, Módulo de Triaje
**Prioridad:** Alta

## Descripción
El sistema registrará automáticamente la fecha y hora de inicio del proceso de triaje para cada evento, permitiendo el cálculo de tiempos de atención y la generación de indicadores operativos.

## Actores involucrados
- Sistema (automático)

## Criterios de aceptación
- La marca de tiempo se registra automáticamente al crear el evento de triaje (RF-TRI-001).
- Se almacena en formato UTC, presentándose en la zona horaria institucional (RNG-006).
- La marca de tiempo es inmutable (no puede modificarse manualmente).
- Sirve como base para el cálculo de tiempos de espera y duración del proceso.

## Dependencias / relacionados
- RF-TRI-001: Crear Evento de Triaje.
- RNG-006: Fechas en UTC con presentación en zona horaria institucional.
- RF-REP-003: Tiempo Promedio de Clasificación.

## Notas del analista
- Este requerimiento es simple pero crítico para los indicadores operativos (RF-REP-*) y para la auditoría del proceso.
