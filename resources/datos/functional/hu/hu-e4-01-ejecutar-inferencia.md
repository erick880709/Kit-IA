---
id: HU-E4-01
type: Historia de Usuario
epic: 004-motor-ia-explicabilidad-demo
priority: Alta
points: 8
---

# HU-E4-01: Ejecutar Inferencia y Ver Resultados

## Como
Enfermera de Triaje / Médico

## Quiero
Presionar "Ejecutar IA" y ver en menos de 3 segundos el nivel de triaje sugerido (I-V), las probabilidades de cada nivel, la confianza y los metadatos del modelo

## Para
Obtener una recomendación basada en IA que apoye mi decisión clínica sin interrumpir el flujo de atención

## Criterios de Aceptación
- [ ] CA1: El botón "Ejecutar IA" se habilita solo cuando signos vitales + motivo de consulta están completos
- [ ] CA2: Al presionar, se muestra un spinner/indicador de carga (la inferencia es asíncrona, no bloquea la UI — RF-IA-010)
- [ ] CA3: En < 3 segundos se muestra:
  - Nivel sugerido (I-V) destacado visualmente (badge de color según nivel)
  - Probabilidades de los 5 niveles en gráfico de barras horizontal
  - Confianza de la predicción (score)
  - Versión del modelo utilizado
  - Tiempo de inferencia (ms)
- [ ] CA4: Si el modelo no está disponible (timeout > 5s o error), se muestra "Modelo no disponible — continúe con clasificación manual" (RNO-006)
- [ ] CA5: Si el texto libre está vacío, el pipeline continúa solo con variables estructuradas (RF-NLP-004)

## Recurso de datos involucrado
- **Nombre:** PrediccionIA (ENT-009)
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdPrediccion | UUID | Sí | Generado automáticamente |
| IdTriaje | UUID | Sí | FK a EventoTriaje |
| Modelo | Texto | Sí | Nombre del modelo |
| Version | Texto | Sí | Versión del modelo |
| FechaHora | DateTime | Sí | Automático |
| NivelPredicho | Catálogo | Sí | I, II, III, IV, V |
| Probabilidades | JSON | Sí | {I: 0.01, II: 0.72, III: 0.20, IV: 0.06, V: 0.01} |
| Confianza | Decimal | Sí | Score de confianza |
| TiempoInferencia | Decimal | Sí | Segundos |
| EstadoModelo | Texto | Sí | Activo |

### Relaciones con otros recursos
- `EventoTriaje` (N:1): múltiples predicciones por triaje (reprocesamientos)
- `ExplicacionSHAP` (1:1): cada predicción genera su explicación

## Subtareas
- [ ] Implementar carga del modelo serializado al iniciar la app
- [ ] Implementar endpoint/función de inferencia asíncrona
- [ ] Implementar visualización de resultados (nivel, probabilidades, confianza, metadatos)
- [ ] Implementar modo degradado (sin IA)
- [ ] Implementar manejo de texto vacío
