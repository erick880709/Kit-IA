# RT-009: Threshold Tuning por Clase

**Tipo:** Requisito técnico
**Categoría:** Arquitectura / Evaluación
**Fuente:** `context/CONTEXTO TRIAJE.txt` §6 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §3

## Descripción
El umbral de decisión se optimiza por clase sobre la curva ROC/PR, priorizando Recall en Niveles I y II.

## Criterio medible / restricción concreta
- Técnica: threshold tuning sobre curva ROC/PR por clase.
- Niveles I–II: umbral calibrado para maximizar Recall (caída de Precisión tolerada y documentada).
- Niveles III–V: argmax estándar.
- El punto de equilibrio elegido se documenta en el capítulo de resultados.

## Impacto en la arquitectura
El componente de inferencia debe persistir el vector de umbrales junto a la versión del modelo y aplicarlo antes de emitir el nivel sugerido (RF-007, RNF-007).

## Notas del analista
Corrige la interpretación de RF-IA-003 (argmax puro) del documento funcional — contradicción resuelta (hallazgo #5).
