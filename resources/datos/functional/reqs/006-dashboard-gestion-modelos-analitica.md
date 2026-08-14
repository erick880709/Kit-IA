---
id: 006
slug: dashboard-gestion-modelos-analitica
tipo: epica
prioridad: Should-Have
orden: 5
dependencias: E1, E4
fecha: 2026-07-19
---

# ÉPICA 6 — Gestión de Modelos, Dashboard y Analítica

## Necesidad de Negocio

Proporcionar a los coordinadores médicos, investigadores y administradores IA las herramientas para monitorear el desempeño operativo del servicio de urgencias, evaluar la calidad del modelo a lo largo del tiempo, gestionar el ciclo de vida de los modelos (registro, versionado, activación, rollback) y tomar decisiones basadas en datos. Esta épica cierra el ciclo de mejora continua: medir → analizar → actuar.

## Justificación

Un sistema de apoyo a la decisión clínica no está completo sin retroalimentación. El dashboard permite a la dirección médica ver si el sistema está reduciendo tiempos de espera y variabilidad. La gestión de modelos permite al equipo de IA iterar sin riesgo (si un nuevo modelo degrada el desempeño, se hace rollback inmediato). Sin estas capacidades, el sistema opera a ciegas.

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Coordinador del Servicio / Dirección Médica | Beneficiario | Monitorear indicadores operativos y tomar decisiones |
| Administrador IA | Ejecutor | Gestionar versiones de modelos, activar/desactivar |
| Investigador / Científico de Datos | Beneficiario | Analizar desempeño, comparar modelos, detectar deriva |
| Médico | Beneficiario | Ver dashboard operativo de su servicio |

## Alcance

- ✅ IN SCOPE:
  - Dashboard general con indicadores agregados (triajes del período, distribución I-V, tiempos promedio, tasa de reclasificaciones)
  - Gráfico de distribución de triaje por niveles con comparación contra referencia nacional
  - Tiempo promedio de clasificación desglosado por nivel y profesional
  - Desempeño del modelo IA: Accuracy, Precision, Recall, F1, AUC-ROC (macro y por nivel), AUPRC para clases minoritarias
  - Concordancia IA vs. profesional: matriz de confusión, % global y por nivel, listado de discrepancias con motivo
  - Registro de nuevos modelos: nombre, algoritmo, arquitectura, hiperparámetros, dataset, métricas
  - Versionado: cada reentrenamiento genera nueva versión con historial completo
  - Activación (promoción a producción) y desactivación (rollback) de modelos
  - Historial de todas las versiones con métricas comparativas
  - Exportación de reportes en Excel, PDF, CSV

- ❌ OUT OF SCOPE:
  - Dashboards en tiempo real con WebSockets
  - Alertas automáticas por degradación de métricas
  - Recomendación automática de reentrenamiento
  - Comparación de modelos sobre datasets externos
  - Integración con herramientas de BI (Power BI, Tableau)

## Criterios de Aceptación

```
DADO que el coordinador accede al dashboard
CUANDO selecciona el período "último mes"
ENTONCES ve el total de triajes, distribución por niveles I-V, tiempo promedio de clasificación y % de concordancia IA vs. profesional

DADO que el Administrador IA registra un nuevo modelo con sus métricas
CUANDO las métricas superan los umbrales mínimos (F1 ≥ 0.82)
ENTONCES puede promoverlo a "activo" y el modelo anterior pasa a "inactivo" (no se elimina)

DADO que el modelo activo muestra degradación en producción
CUANDO el Administrador IA selecciona "Desactivar" sobre el modelo activo
ENTONCES el sistema revierte al modelo anterior y registra el motivo del rollback en auditoría

DADO que el investigador quiere comparar early vs. late fusion
CUANDO selecciona ambas versiones en la pantalla de comparación
ENTONCES ve Accuracy, Precision, Recall, F1, AUC-ROC y matriz de confusión lado a lado

DADO que hay discrepancias entre IA y profesional registradas
CUANDO el médico filtra el listado de discrepancias por Nivel I
ENTONCES ve cada caso con el motivo registrado, permitiendo identificar patrones de error del modelo
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| Indicadores del dashboard | 0 | 7 indicadores funcionales (distribución, tiempos, desempeño IA, concordancia, etc.) | Cierre de E6 |
| Flujo de gestión de modelos | 0 | CRUD completo: registrar → versionar → activar → desactivar (rollback) | Cierre de E6 |
| Exportaciones | 0 | 3 formatos (Excel, PDF, CSV) para reportes y dashboard | Cierre de E6 |
| Trazabilidad de versiones | No existe | Historial completo de cada modelo con métricas por versión | Cierre de E6 |

## Prioridad (MoSCoW)

- **Must Have:** Dashboard con indicadores básicos (distribución I-V, tiempos), registro y versionado de modelos, activación/desactivación
- **Should Have:** Concordancia IA vs. profesional con listado de discrepancias, comparación de modelos lado a lado, exportación Excel/PDF
- **Could Have:** AUPRC en dashboard, alertas de rendimiento, comparación contra benchmarks
- **Won't Have (en este alcance):** Dashboards en tiempo real, BI integration, recommendation engine para reentrenamiento

## Dependencias

- **E1 (Fundación):** Login, roles, modelo de dominio
- **E4 (Motor IA):** Sin predicciones registradas, el dashboard no tiene datos que mostrar. La gestión de modelos requiere que exista al menos un modelo registrado (producto de E3)

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RF-MOD-gestion-modelos.md` | Funcional |
| `RF-REP-modulo-reportes-dashboard.md` | Funcional |
