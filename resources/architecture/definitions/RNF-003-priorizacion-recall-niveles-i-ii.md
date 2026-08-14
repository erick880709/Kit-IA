# RNF-003: Priorización de Recall en Niveles I y II

**Tipo:** Requerimiento no funcional
**Categoría:** Rendimiento / Seguridad clínica
**Fuente:** `context/CONTEXTO TRIAJE.txt` §6 · `context/02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §3

## Descripción
La estrategia de decisión debe minimizar los falsos negativos en los niveles críticos (I y II), aunque implique una ligera caída de Precisión.

## Criterio medible / restricción concreta
- Umbral de decisión optimizado por clase para Niveles I y II, calibrado para maximizar Recall sobre la curva ROC/PR.
- El punto de equilibrio elegido debe quedar documentado.
- La selección del modelo ganador prioriza Recall en I–II sin descuidar el F1 global.

## Impacto en la arquitectura
Exige soporte de umbrales por clase en el componente de inferencia (no argmax puro) y trazabilidad del umbral usado por predicción (RF-007).

## Notas del analista
Justificación clínica: el falso negativo en I–II es morbilidad/mortalidad evitable; el falso positivo solo genera sobrecarga operativa.
