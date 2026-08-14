---
id: TT-E3-01
type: Tarea Técnica
epic: E3 - Pipeline de Datos y Entrenamiento
priority: Highest
points: 8
---

# TT-E3-01: Pipeline de ingesta y anonimización de 5 fuentes

## Descripción
Implementar los adaptadores de ingesta de las 5 fuentes (RT-006): MIMIC-IV-ED (PhysioNet), registro Hospital San Juan de Dios (custom CSV), Clasificación Triage (datos.gov.co), BDUA (contributivo + subsidiado), Morbilidad RIPS; con anonimización obligatoria previa (Ley 1581 de 2012, RNF-006).

## Criterios de Done
- [ ] Módulo `ingesta.py` con un adaptador por fuente (CSV local, Socrata, PhysioNet).
- [ ] Paso de anonimización ejecutado SIEMPRE antes de limpieza (sin excepciones).
- [ ] Normalización de REGIMEN (typos documentados en RT-006) y filtrado de AÑO corrupto.
- [ ] Hash/drop de identificadores directos (documento, nombres) en salidas.
- [ ] Tests con fixtures de cada fuente (al menos 5 registros por fuente).

## Dependencias
E1 completo

## Subtareas
- [ ] Adaptador MIMIC-IV-ED
- [ ] Adaptador CSVs colombianos
- [ ] Módulo de anonimización
- [ ] Tests de ingesta
