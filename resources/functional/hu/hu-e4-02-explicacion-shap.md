---
id: HU-E4-02
type: Historia de Usuario
epic: E4 - Motor de IA y Explicabilidad
priority: Highest
points: 5
---

# HU-E4-02: Visualizar explicación SHAP

## Como
Médico

## Quiero
ver la explicación SHAP de la predicción en lenguaje clínico con gráficos

## Para
confiar y validar la sugerencia del modelo (RF-009, RT-005).

## Criterios de Aceptación
- [ ] CA1: Top 5-10 variables con mayor influencia, descritas en lenguaje clínico (ej. "saturación de O₂ baja (88%) fue el factor de mayor peso").
- [ ] CA2: Impacto positivo y negativo diferenciado (RF-XAI-003/004).
- [ ] CA3: Gráficos interpretables (force plot/waterfall) integrados con `streamlit-shap` (stack decidido por refinador).
- [ ] CA4: Comparación implícita con criterio MTS/Manchester cuando coincida.
- [ ] CA5: Exportación de la explicación disponible (RF-XAI-006).

## Dependencias
HU-E4-01
