---
id: TT-E3-02
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 5
---

# TT-E3-02: Pipeline de Limpieza, Normalización y Feature Engineering

## Descripción
Implementar los pasos 3 y 4 del pipeline técnico: imputación de valores nulos, detección y tratamiento de outliers, normalización de variables numéricas (StandardScaler), codificación one-hot de variables categóricas, y creación de features derivadas.

## Criterios de Done
- [ ] Imputación de nulos: mediana para numéricas, moda para categóricas, categoría "Desconocido" donde aplique
- [ ] Detección de outliers: rango intercuartílico (IQR × 1.5) para variables numéricas, límites fisiológicos para signos vitales
- [ ] Outliers tratados como: winsorización (cap en percentil 1 y 99) para variables no fisiológicas, flag de alerta para signos vitales
- [ ] StandardScaler ajustado sobre train y aplicado a test (nunca al revés)
- [ ] OneHotEncoder para variables categóricas: Sexo, ViaLlegada, RegimenSalud, NivelConciencia, MotivoCategoria
- [ ] Features derivadas: IMC (si no está calculado), edad categorizada (pediátrico/adulto/adulto mayor), frecuencia cardíaca ajustada por edad
- [ ] Reporte de calidad de datos post-limpieza: % de nulos imputados, % de outliers detectados, distribución de cada feature

## Dependencias
TT-E3-01 (datos ingestados y anonimizados)

## Subtareas
- [ ] Implementar imputación de nulos
- [ ] Implementar detección y tratamiento de outliers
- [ ] Implementar normalización y codificación
- [ ] Implementar feature engineering
- [ ] Generar reporte de calidad de datos
