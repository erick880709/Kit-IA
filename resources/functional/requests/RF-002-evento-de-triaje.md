# RF-002: Gestión del Evento de Triaje

**Tipo:** Requerimiento funcional
**Fuente:** `context/CONTEXT TRIA.txt` (RF-TRI-001 a 005) · `context/06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §3-4
**Prioridad:** Alta

## Descripción
El sistema debe gestionar el ciclo de vida completo del evento de triaje: creación del evento, registro de hora de inicio, seguimiento del estado, reclasificación cuando cambian las condiciones clínicas, y cierre formal del evento con todos los datos persistidos.

Cubre los requerimientos fuente: RF-TRI-001 (Crear evento), RF-TRI-002 (Hora de inicio), RF-TRI-003 (Estado), RF-TRI-004 (Reclasificación), RF-TRI-005 (Cierre).

## Actores involucrados
Enfermera (creación), médico (reclasificación/cierre), sistema (estado y persistencia).

## Criterios de aceptación
- El evento queda vinculado al paciente (ENT-001) y registra fecha/hora de ingreso.
- El ciclo de vida sigue una **máquina de 7 estados** (épica E2, `resources/datos/functional/reqs/epicas-tfm-jira.csv`): creación → registro de signos/evaluación → clasificación IA → validación profesional → cierre; con transición de reclasificación ante cambio de condiciones clínicas.
- La reclasificación posterior se registra como evento separado, sin sobrescribir el registro inicial de concordancia (ver RF-010).
- La reclasificación exige motivo obligatorio (RF-TRI-004).
- El cierre exige que existan nivel sugerido por IA y nivel asignado por profesional (ver RD-003).

## Dependencias / relacionados
[[RF-010]], [[RF-011]], RD-003 (extensión ENT-002).

## Notas del analista
El flujo dual IA-profesional (06 §3) define que el cierre del evento guarda ambos niveles + motivo de discrepancia si aplica.
