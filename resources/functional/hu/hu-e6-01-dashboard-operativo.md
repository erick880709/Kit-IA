---
id: HU-E6-01
type: Historia de Usuario
epic: E6 - Gestión de Modelos, Dashboard y Analítica
priority: High
points: 8
---

# HU-E6-01: Dashboard operativo con indicadores y semáforo de metas

## Como
Médico / Administrador

## Quiero
ver los indicadores operativos del triaje en un dashboard

## Para
monitorear el desempeño del sistema y de la IA (RF-013, RF-REP-001 a 005).

## Criterios de Aceptación
- [ ] CA1: 7 indicadores: distribución de triaje por nivel, tiempo promedio de atención, desempeño IA (accuracy/precision/recall/F1/AUC), concordancia IA vs. profesional (global y por nivel), volumen de eventos.
- [ ] CA2: Semáforo de metas (RNF-001: F1 ≥ 0,82, etc.) con estado visual.
- [ ] CA3: Matriz de confusión IA vs. profesional y listado filtrable de discrepancias con motivo.
- [ ] CA4: Datos actualizados desde los registros reales de la demo (no estáticos).

## Dependencias
HU-E6-02 + E4 completo

## Subtareas
- [ ] Cálculo de indicadores
- [ ] Semáforo de metas
- [ ] Vista de discrepancias
