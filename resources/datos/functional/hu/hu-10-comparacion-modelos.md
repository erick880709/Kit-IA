---
id: HU-10
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Baja
points: 2
---

# HU-10: Comparación de modelos IA

## Como
Investigador o administrador

## Quiero
Comparar las métricas de diferentes modelos de IA (F1, AUC-ROC, Recall por clase, tiempo de inferencia) en una tabla comparativa

## Para
Evaluar objetivamente qué modelo tiene mejor desempeño y decidir cuál activar basado en evidencia cuantitativa

## Criterios de Aceptación

- [ ] CA1: La página lista todos los modelos serializados encontrados en disco con sus métricas en una tabla comparativa.
- [ ] CA2: Columnas de la tabla: Nombre, Versión, F1 Macro, AUC-ROC, Recall I, Recall II, Recall III, Recall IV, Recall V, Precisión, Tiempo Inferencia (ms), Features.
- [ ] CA3: La fila del modelo activo se resalta en verde.
- [ ] CA4: Las métricas se obtienen del `metadata.json` de cada modelo (escaneo de disco).
- [ ] CA5: Si un modelo no tiene cierta métrica, se muestra "N/D" en esa celda.

## Recurso de datos involucrado

- **Nombre del recurso:** Modelo (metadata)
- **Capa(s):** frontend (consume GET /api/models/scan)

## Subtareas

- [ ] Crear `pages/ModelComparisonPage.tsx`
- [ ] Implementar tabla comparativa con AG Grid o TanStack Table
- [ ] Resaltar fila del modelo activo
- [ ] Probar con múltiples versiones de modelos
