---
id: HU-E4-04
type: Historia de Usuario
epic: 004-motor-ia-explicabilidad-demo
priority: Media
points: 3
---

# HU-E4-04: Comparar Modelos (Early vs. Late Fusion)

## Como
Investigador / Científico de Datos

## Quiero
Comparar el desempeño de early fusion vs. late fusion lado a lado sobre el mismo caso o dataset

## Para
Documentar la comparativa en el Capítulo 5 del TFM y justificar la elección del modelo ganador

## Criterios de Aceptación
- [ ] CA1: Pantalla "Comparación de Modelos" accesible solo para rol Investigador
- [ ] CA2: Selector de modelos: lista de versiones registradas (early fusion v1, late fusion v1, etc.)
- [ ] CA3: Al seleccionar 2 modelos y un caso/dataset, se ejecuta inferencia con ambos y se muestran lado a lado:
  - Nivel predicho por cada modelo
  - Probabilidades por nivel
  - Métricas: Accuracy, Precision, Recall, F1, AUC-ROC, matriz de confusión
- [ ] CA4: Si se selecciona un dataset (múltiples casos), las métricas son agregadas
- [ ] CA5: Exportable como tabla/CSV para incluir en el TFM

## Recurso de datos involucrado
- **Nombre:** PrediccionIA + Modelo (consulta comparativa)
- **Capa(s):** backend + frontend

## Subtareas
- [ ] Diseñar pantalla de Comparación de Modelos
- [ ] Implementar ejecución de inferencia con múltiples modelos
- [ ] Implementar visualización lado a lado
- [ ] Implementar exportación de comparativa
