# Contexto — Captura de Síntomas, Categorización IA y Comparativa IA vs. Profesional

Detalla y extiende `04-ESPECIFICACION-APLICACION-DEMO.md` en el punto específico de captura de síntomas/motivo de consulta, la categorización automática por el modelo, y la categorización independiente del profesional — con el fin de habilitar una comparativa (concordancia) entre ambas una vez cerrados los triajes.

## 1. Objetivo de este módulo

Que cada evento de triaje quede con **dos clasificaciones registradas por separado**:
1. La sugerida por el modelo de IA a partir de síntomas/motivo de consulta + resto de variables.
2. La asignada por el profesional de salud.

Para que, después de atendidos los triajes, se pueda hacer un análisis retrospectivo (concordancia, matriz de confusión IA-vs-humano, Kappa) sin depender de reconstruir la información desde texto libre o notas sueltas.

## 2. Decisión de flujo (confirmada contigo)

**El profesional ve primero la sugerencia de la IA y luego decide su propia clasificación.** Es el flujo clínico natural y el que se implementa en la demo.

⚠️ **Nota metodológica para el TFM (documentar como limitación en Cap. 6):** este orden introduce **sesgo de anclaje** — el profesional puede verse influido por la sugerencia de la IA en lugar de dar un juicio totalmente independiente, lo cual reduce el valor de la concordancia como medida de "acuerdo entre dos evaluadores ciegos" (a diferencia del Kappa 0.43 reportado en Lidal et al. 2017 entre profesionales que no se ven entre sí). Sigue siendo válido como medida de **utilidad clínica real** (¿el profesional confía en la IA y la sigue, o la corrige?), que de hecho es una métrica más relevante para un sistema de apoyo a la decisión que para un estudio de acuerdo interobservador puro. Si en el futuro se quiere una comparativa más rigurosa, se necesitaría un segundo modo "a ciegas" — quedó registrado como opción no implementada en `05-PENDIENTES-PARA-DIRECTORA.md`.

## 3. Flujo detallado de la pantalla de clasificación

```
1. Captura de síntomas / motivo de consulta (texto libre + categoría estructurada)
        ↓
2. El sistema ejecuta el modelo (RF-IA-001) usando síntomas + signos vitales + resto de variables
        ↓
3. Se muestra al profesional: Nivel sugerido por IA + probabilidades por nivel + explicación SHAP
        ↓
4. El profesional registra SU PROPIA clasificación (I-V) — campo obligatorio,
   independiente del campo de la IA, nunca se sobreescribe ni se autocompleta con el valor de la IA
        ↓
5. Si coinciden → se registra concordancia = Sí
   Si difieren  → el sistema exige motivo de discrepancia (texto corto, catálogo o libre)
        ↓
6. Cierre del evento de triaje con ambos valores + motivo (si aplica) guardados de forma permanente
```

El paso 4 es la pieza que faltaba: el profesional **no** está "corrigiendo" el campo de la IA (eso sería sobreescritura, y perdería el dato original para la comparativa) — está llenando un campo propio y separado.

## 4. Modelo de datos — extensión de ENT-002 Evento de Triaje

`CONTEXT_TRIA.txt` (ENT-002) solo tenía un campo `NivelAsignado` genérico, insuficiente para esta comparativa. Se reemplaza por:

| Campo | Tipo | Obligatorio | Quién lo llena |
|---|---|---|---|
| NivelSugeridoIA | Catálogo I-V | Sí (si se ejecutó inferencia) | Sistema (RF-IA-003) |
| ProbabilidadesIA | JSON {nivel: prob} | Sí | Sistema |
| NivelAsignadoProfesional | Catálogo I-V | Sí | Profesional (paso 4) |
| Concordancia | Booleano (calculado) | Sí | Sistema — `NivelSugeridoIA == NivelAsignadoProfesional` |
| MotivoDiscrepancia | Texto/Catálogo | Solo si Concordancia = No | Profesional |
| VersionModeloUsado | Texto (referencia a ENT-009) | Sí | Sistema |

Esto es compatible con RNA-002 (toda predicción incluye nivel + probabilidad + confianza + versión) y con RF-TRI-004 (reclasificación) — la reclasificación posterior sigue existiendo como evento separado si cambian las condiciones clínicas del paciente, y no se confunde con este registro inicial de concordancia.

## 5. Captura de síntomas / motivo de consulta — detalle de pantalla

Extiende `RF-EVA-001` (que ya existía pero era genérico):

- **Texto libre**: campo abierto, el que alimenta el módulo NLP (`RF-NLP-*`, embeddings BERT/BioBERT-es).
- **Categoría estructurada**: catálogo controlado (dolor torácico, trauma, disnea, dolor abdominal, fiebre, etc. — ya listados como ejemplos en ENT-004) para no depender únicamente del NLP cuando el texto libre esté vacío (ya cubierto por RF-NLP-004).
- Ambos se envían juntos al modelo — el pipeline de fusión (early o late, según `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`) decide cómo combinarlos internamente; la UI no necesita saber cuál arquitectura está activa.

## 6. Reportes habilitados por esta comparativa (extiende RF-REP-005, antes solo decía "IA vs Profesional" sin detalle)

- Matriz de confusión IA vs. Profesional (no solo accuracy global — por nivel, igual que en la evaluación del modelo).
- % de concordancia global y por nivel.
- Listado filtrable de discrepancias con su motivo, para revisión clínica o para detectar patrones de error del modelo (insumo directo para el Cap. 5 del TFM y para detección de deriva, RNA-010).
- Nota: esta comparativa es sobre **casos reales operados en la demo**, distinta de la evaluación offline del modelo contra el dataset de prueba (10-fold CV) descrita en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` — son dos validaciones complementarias, no la misma métrica.

## 7. Pantallas afectadas en `04-ESPECIFICACION-APLICACION-DEMO.md`

Actualiza así las filas correspondientes del inventario de pantallas:

| Pantalla | Cambio |
|---|---|
| Ejecutar clasificación IA | Ahora incluye el campo `NivelAsignadoProfesional` en el mismo flujo (paso 4 de la sección 3 de este documento), no en una pantalla separada de "validación" posterior. |
| Validación de triaje | Se mantiene, pero ahora es donde se captura el `MotivoDiscrepancia` cuando aplica, no una simple confirmación. |
| Dashboard operativo | El indicador "concordancia IA vs. profesional" (RF-REP-005) ahora tiene datos reales que mostrar: % global, % por nivel, y acceso al listado de discrepancias. |
