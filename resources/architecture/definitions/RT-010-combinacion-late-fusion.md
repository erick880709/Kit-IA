# RT-010: Método de Combinación en Late Fusion — PENDIENTE EXPERIMENTAL

**Tipo:** Requisito técnico
**Categoría:** Arquitectura
**Fuente:** `context/CONTEXTO TRIAJE.txt` §5 · `context/05-PENDIENTES-PARA-DIRECTORA.md` §4

## Descripción
En la arquitectura late fusion, la combinación de las salidas del submodelo estructurado y del submodelo de texto se determina empíricamente.

## Criterio medible / restricción concreta
- Opciones: promedio ponderado, stacking o meta-clasificador.
- Decisión: resultado experimental de Fase 3 (no requiere decisión previa).
- El método elegido y su justificación se documentan en Cap. 5.

## Impacto en la arquitectura
La implementación de late fusion debe diseñarse como estrategia parametrizable (patrón strategy) para comparar los tres métodos sin reescribir el pipeline.

## Notas del analista
No es una ambigüedad de contexto sino un resultado pendiente de experimentación; registrado para que no se pierda de vista.
