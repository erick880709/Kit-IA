# RNF-004: Manejo de Desbalance de Clases

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §4 · `context/CONTEXTO TRIAJE.txt` §6

## Descripción
Los niveles IV–V son mayoritarios y el Nivel I es raro pero crítico. El pipeline debe mitigar el desbalance para que el modelo no colapse hacia las clases mayoritarias.

## Criterio medible / restricción concreta
- Evaluar y comparar: class weights, SMOTE, focal loss (si se usa red neuronal).
- Reportar métricas por clase además del macro-promedio.
- AUPRC para las clases minoritarias (I, II).

## Impacto en la arquitectura
Influye en el diseño del entrenamiento (función de pérdida, muestreo) y en la matriz de evaluación; la estrategia elegida debe quedar versionada junto al modelo.

## Notas del analista
Ningún documento obliga a una técnica específica — es resultado experimental a documentar en el Cap. 5.

## Validación con datos reales (2026-08-13)
Distribución real de niveles en el dataset público "Clasificación en Triaje Urgencias" (datos.gov.co, 89.453 eventos):

| Nivel | Eventos | % |
|---|---|---|
| III | 79.198 | 88,5 % |
| IV | 6.934 | 7,8 % |
| II | 2.710 | 3,0 % |
| V | 408 | 0,5 % |
| I | 203 | 0,2 % |

**Implicación:** el supuesto "IV-V mayoritarios" es incorrecto en datos colombianos — **Nivel III domina (88,5 %)** y el Nivel I es extremadamente raro (0,2 %, solo 203 casos). El desbalance es más severo de lo asumido: refuerza la necesidad de class weights/SMOTE, evaluación por clase y Recall prioritario en I-II (RNF-003). Fuente: `datasets/clasificacion_triage_urgencias_20260813.csv`.

**Corroboración con el dataset local (Hospital San Juan de Dios, 43.594 episodios):** I = 0,2 % · II = 3,0 % · III = 88,5 % · IV = 7,8 % · V = 0,5 % — distribución **prácticamente idéntica** a la nacional. La coincidencia permite calibrar priors de clase con datos oficiales y confirma que el desbalance extremo (III dominante, I rarísimo) es estructural, no un artefacto del dataset.
