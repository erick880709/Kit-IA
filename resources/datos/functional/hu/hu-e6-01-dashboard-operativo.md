---
id: HU-E6-01
type: Historia de Usuario
epic: 006-dashboard-gestion-modelos-analitica
priority: Media
points: 8
---

# HU-E6-01: Dashboard Operativo con Indicadores

## Como
Coordinador del Servicio / Médico

## Quiero
Ver un panel de control con los indicadores operativos del servicio de urgencias: distribución de triajes por nivel, tiempos promedio, desempeño de la IA y concordancia IA vs. profesional

## Para
Monitorear la operación, detectar cuellos de botella y evaluar el impacto del sistema de IA en la calidad del triaje

## Criterios de Aceptación
- [ ] CA1: Selector de período (hoy, esta semana, este mes, personalizado) en la parte superior
- [ ] CA2: Sección "Resumen": total de triajes, % por nivel (I-V), tiempo promedio de clasificación, tasa de reclasificaciones, disponibilidad del modelo IA
- [ ] CA3: Gráfico de distribución de triaje por niveles (barras apiladas o torta) con comparación contra referencia nacional (datos.gov.co)
- [ ] CA4: Gráfico de tiempo promedio de clasificación desglosado por nivel (I-V) y por profesional
- [ ] CA5: Sección "Desempeño IA": Accuracy, Precision, Recall, F1, AUC-ROC (macro-promedio y por nivel), AUPRC (Niveles I, II)
- [ ] CA6: Sección "Concordancia IA vs. Profesional": % global, % por nivel, matriz de confusión 5×5, listado de discrepancias con enlace a cada caso
- [ ] CA7: Indicador visual de cumplimiento de metas cuantitativas (F1 ≥ 0.82, etc.) con semáforo (verde = cumple, amarillo = cerca, rojo = no cumple)

## Recurso de datos involucrado
- **Nombre:** EventoTriaje + PrediccionIA (agregación)
- **Capa(s):** backend + frontend

## Subtareas
- [ ] Diseñar layout del dashboard
- [ ] Implementar consultas agregadas para cada indicador
- [ ] Implementar gráficos de distribución y tiempos
- [ ] Implementar sección de desempeño IA con semáforo de metas
- [ ] Implementar sección de concordancia con matriz de confusión
- [ ] Implementar filtro por período
