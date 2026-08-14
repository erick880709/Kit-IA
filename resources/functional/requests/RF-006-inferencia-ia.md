# RF-006: Ejecutar Inferencia y Clasificación IA

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-IA-001, 002, 004, 005, 006, 009, 010) · `context/04-ESPECIFICACION-APLICACION-DEMO.md` §3
**Prioridad:** Alta

## Descripción
El sistema debe ejecutar el modelo predictivo sobre los datos del paciente, calcular la probabilidad para cada nivel I–V, registrar versión/algoritmo/fecha/identificador del modelo usado, registrar el tiempo de inferencia y el score de confianza, permitir reprocesamiento ante cambios en los datos clínicos y ejecutar inferencia asíncrona sin bloquear la UI cuando el tiempo lo requiera.

## Actores involucrados
Médico / enfermera (disparan la inferencia), sistema (ejecución y registro).

## Criterios de aceptación
- Toda inferencia registra: versión del modelo, algoritmo, fecha, identificador (RF-IA-004).
- Se registra el tiempo empleado (RF-IA-005) — objetivo < 3 s ([[RNF-002]]).
- Se registra el score de confianza (RF-IA-006).
- Reprocesamiento permitido si cambian datos clínicos (RF-IA-009).
- Ejecución asíncrona con estado "Cargando" y manejo de error de inferencia (04 §3).

## Dependencias / relacionados
[[RF-007]], [[RF-009]], [[RNF-007]], [[RT-002]].

## Notas del analista
La pantalla "Ejecutar clasificación IA" muestra probabilidades por nivel y captura en el mismo flujo la clasificación del profesional (ver RF-010).
