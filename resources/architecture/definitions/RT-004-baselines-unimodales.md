# RT-004: Baselines Unimodales Obligatorios

**Tipo:** Requisito técnico
**Categoría:** Arquitectura / Evaluación
**Fuente:** `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §2 · `context/contexto-tfm.md` §6

## Descripción
Para poder afirmar que el enfoque multimodal aporta valor, deben entrenarse baselines unimodales obligatorios sobre solo datos estructurados.

## Criterio medible / restricción concreta
- Baselines: Regresión Logística, Random Forest, XGBoost (unimodales, solo estructuradas).
- Los baselines se evalúan con las mismas métricas que los modelos multimodales (RNF-001, RNF-005).
- La comparativa multimodal vs. baseline se documenta en Cap. 5.

## Impacto en la arquitectura
Obliga a que el pipeline de features permita entrenar con y sin embeddings; evita que el multimodal se evalúe "contra la nada".

## Notas del analista
Sin este requisito, el aporte incremental del texto libre no sería demostrable ante el tribunal.
