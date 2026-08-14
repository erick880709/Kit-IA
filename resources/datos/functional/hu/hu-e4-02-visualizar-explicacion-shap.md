---
id: HU-E4-02
type: Historia de Usuario
epic: 004-motor-ia-explicabilidad-demo
priority: Alta
points: 5
---

# HU-E4-02: Visualizar Explicación SHAP

## Como
Médico de Urgencias

## Quiero
Ver qué variables influyeron más en la predicción de la IA, en qué dirección y con qué magnitud, expresado en lenguaje clínico comprensible

## Para
Entender la lógica detrás de la recomendación y confiar (o desconfiar fundadamente) en ella antes de tomar mi decisión

## Criterios de Aceptación
- [ ] CA1: Top 5-10 variables SHAP mostradas en gráfico de barras horizontales ordenadas por importancia
- [ ] CA2: Cada variable se presenta en lenguaje clínico (ej. "Saturación de O₂ baja (88%) fue el factor de mayor peso para clasificar como Nivel II"), no con nombre técnico de columna
- [ ] CA3: Waterfall plot o force plot que muestra la contribución acumulada desde el valor base hasta la predicción final
- [ ] CA4: Colores: rojo = aumenta la probabilidad del nivel predicho, azul = la disminuye
- [ ] CA5: Comparación implícita con criterios MTS/Manchester cuando las variables coincidan (FR, SpO₂, temperatura, nivel de conciencia)
- [ ] CA6: Se puede exportar la explicación como parte del registro de triaje descargable

## Recurso de datos involucrado
- **Nombre:** ExplicacionSHAP (ENT-010)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdExplicacion | UUID | Sí | Generado automáticamente |
| IdPrediccion | UUID | Sí | FK a PrediccionIA |
| VariablesSHAP | JSON | Sí | [{variable: "SpO2", valor: 88, shap_value: +0.34, direccion: "positivo", descripcion_clinica: "Saturación de O₂ baja (88%)"}] |
| ValorBase | Decimal | Sí | Expected value del modelo |

### Relaciones con otros recursos
- `PrediccionIA` (1:1)

## Subtareas
- [ ] Integrar TreeExplainer SHAP en el pipeline de inferencia
- [ ] Diseñar visualización de barras SHAP
- [ ] Diseñar waterfall/force plot
- [ ] Implementar traducción de variables técnicas a lenguaje clínico
- [ ] Implementar comparación con criterios MTS/Manchester
