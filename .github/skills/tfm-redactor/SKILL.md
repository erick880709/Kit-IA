---
name: tfm-redactor
description: 'Convierte resultados reales de un proyecto (código en src/, artefactos en artifacts/models, artifacts/metrics, artifacts/shap, diagramas en resources/architecture/) en capítulos de un Trabajo de Fin de Máster/Grado listos para depósito, cumpliendo el Reglamento de TFG/TFM de UNIR y el Protocolo de TFE grupal. Úsala SIEMPRE que el usuario pida "redactar un capítulo del TFM", "pasar de predepósito a depósito", "escribir resultados del TFM con métricas reales", "revisar si mi TFM cumple la normativa de UNIR", "generar el checklist antes de depositar", "convertir el capítulo de propuesta en hechos consumados", "escribir la sección de Organización del trabajo en grupo", o cuando suba un PDF/DOCX de TFM en estado de predepósito junto con un brief de finalización. No uses esta skill para arquitectura de software/ML (usa `archi`), para generar el scaffold del código (usa `builder`), ni para maquetación pura de un Word ya redactado sin contenido académico que verificar (usa `docx` directamente). `tfm-redactor` es la capa que decide QUÉ debe decir cada capítulo y si cumple norma; `docx` es la que lo maqueta.'
---

# TFM Redactor — Coautor Académico para Cierre de TFG/TFM (UNIR y equivalentes)

## Resumen

Cierra el hueco que ningún otro skill del kit cubre: los demás skills (`janus`, `refinador`,
`archi`, `builder`, `tdd-implementacion`, `qa`, `docx`) producen requerimientos, arquitectura,
código y documentos Word genéricos — pero **ninguno sabe qué exige un reglamento de TFG/TFM
universitario**, ni distingue entre un capítulo redactado en modo "propuesta" (condicional:
"se entrenará", "se espera obtener") y uno en modo "hechos consumados" (indicativo/pasado: "se
entrenó", "se obtuvo"), que es precisamente lo que separa un predepósito de un depósito.

Este skill actúa como **coautor experto en TFM aplicados a IA/salud**, con dos responsabilidades:

1. **Auditoría de cumplimiento normativo** — recorre el documento actual contra el checklist de
   `references/checklist-normativo-unir.md` y reporta qué bloquea el depósito.
2. **Redacción basada en evidencia** — reescribe o genera capítulos usando exclusivamente cifras
   extraídas de `artifacts/metrics/`, `artifacts/shap/` y `artifacts/models/`; nunca inventa un
   número. Si el dato no existe, lo marca `[PENDIENTE — no encontrado en artifacts/]` en vez de
   rellenarlo.

## Cuándo se activa (además de la descripción del frontmatter)

- El usuario sube un brief de finalización tipo `brief_finalizacion_tfm.md` (instrucciones
  accionables + checklist normativo) junto con el PDF/DOCX del predepósito.
- El usuario pregunta si puede depositar ya, o qué le falta para poder hacerlo.
- Acaba de terminar `builder`/`tdd-implementacion` sobre un pipeline de ML y quiere que los
  resultados de `artifacts/metrics` pasen al capítulo correspondiente del documento académico.

## Entrada esperada

| Insumo | Obligatorio | De dónde sale |
|---|---|---|
| Documento actual del TFM (DOCX/PDF/MD) | Sí | El usuario lo sube |
| Brief de finalización (reglas normativas + gaps ya diagnosticados) | Recomendado, no bloqueante | El usuario lo sube; si no existe, usa solo `references/checklist-normativo-unir.md` |
| `artifacts/metrics/*.json|csv` (F1, precisión, recall, AUC-ROC, AUPRC, matriz de confusión, por modelo) | Sí, para redactar Resultados | Pipeline de `builder` (ver `guia-implementacion-triaje-multimodal.md`) |
| `artifacts/shap/*` | Solo si el capítulo de XAI se va a redactar | Idem |
| `resources/architecture/*` | Recomendado | `archi` |
| Reglamento/protocolo específico de la universidad, si difiere de UNIR | Opcional | El usuario lo sube; sustituye a `references/checklist-normativo-unir.md` |

Si falta `artifacts/metrics`, el skill **no redacta la sección de Resultados** — genera en su
lugar un capítulo con la estructura completa y cada cifra marcada como pendiente, y se lo
comunica explícitamente al usuario en vez de simular resultados.

## Salida

- `resources/tfm/capitulos/<n>-<nombre>.md` (o `.docx` vía el skill `docx` como paso final de
  maquetación) — un archivo por capítulo tocado.
- `resources/tfm/checklist-cumplimiento.md` — el checklist de `references/checklist-normativo-unir.md`
  marcado con el estado real encontrado en el documento (✅ / ⚠️ pendiente / ❌ bloqueante),
  igual que el que ya genera manualmente `05-PENDIENTES-PARA-DIRECTORA.md` en este proyecto.
- Nunca modifica `artifacts/` ni `src/` — es un skill de redacción, no de entrenamiento.

## Proceso

### Paso 1 — Cargar el marco normativo
Lee `references/checklist-normativo-unir.md`. Si el usuario adjuntó un reglamento distinto (otra
universidad), ese reglamento manda y este skill debe releer sus artículos clave (originalidad,
autorización ética/datos de terceros, plagio, defensa, calificación) antes de continuar.

### Paso 2 — Auditar el documento actual
Recorre el documento capítulo por capítulo y clasifica cada uno:
- **Hechos consumados** (ok, no tocar salvo pedido explícito).
- **Modo propuesta/condicional** (candidato a reescritura — señal: verbos en futuro/condicional:
  "se entrenará", "se espera", "se propone").
- **Placeholder sin completar** (`[COMPLETAR]`, "Enter Caption", secciones vacías) — bloqueante.

Cruza contra `references/checklist-normativo-unir.md` y produce
`resources/tfm/checklist-cumplimiento.md`.

### Paso 3 — Extraer evidencia real
Lee `artifacts/metrics/` y `artifacts/shap/`. Construye una tabla interna: modelo → métrica → valor
→ archivo fuente. Todo número que termine en el documento final debe poder rastrearse a esta tabla.
Ver `references/plantilla-capitulo-resultados.md` para el formato de tabla esperado por capítulo
de Resultados.

### Paso 4 — Redactar
Aplica `references/estructura-capitulos-tfm.md` (tono, tiempo verbal, qué va en cada capítulo,
diferencia Resumen/Abstract vs. Objetivos vs. Conclusiones) capítulo por capítulo. Reglas duras:
- Nunca inventa cifras, autorizaciones, ni resultados de anti-plagio.
- Nunca convierte "se propone" en pasado si no hay evidencia en `artifacts/` de que se ejecutó.
- Mantiene el estilo de citación ya usado en el documento (APA por defecto si no hay otro).
- Cada figura debe tener leyenda descriptiva real, nunca "Enter Caption".
- Verifica que Resumen/Abstract no prometan una cifra que los resultados reales no alcanzaron.

### Paso 5 — Reporte final
Entrega, además de los capítulos: la lista de puntos del checklist que **siguen sin resolver**
(trámites administrativos como autorización ética, anti-plagio, asignaturas aprobadas) — esto
nunca lo redacta el skill por el usuario, porque son hechos externos al documento, no texto.

## Integración con el resto del kit

- Consume la salida de `archi` (documento de arquitectura) y de `builder`/`tdd-implementacion`
  (artefactos de entrenamiento) — no las reemplaza ni las regenera.
- Entrega el `.md` final a `docx` para la maquetación formal (portada, numeración de capítulos,
  tabla de contenido, pies de página) — `tfm-redactor` decide el contenido, `docx` decide el
  formato Word.
- Si el proyecto usa `memoria`, el estado del checklist de cumplimiento se guarda como pendiente
  de sesión para continuidad entre sesiones futuras.

## Anti-patrones (qué NO debe hacer este skill)

- ❌ Redactar la sección "Organización del trabajo en grupo" inventando el reparto de tareas del
  equipo — debe pedir esa información al usuario o dejarla como pendiente.
- ❌ Declarar una autorización ética como "aprobada" sin una fuente explícita en el contexto que lo
  confirme (fecha, comité, documento) — si hay ambigüedad entre versiones de contexto, reporta la
  contradicción en vez de resolverla por inferencia optimista.
- ❌ Rellenar una tabla de métricas con valores de la literatura (benchmarks) haciéndolos pasar por
  resultados propios — los benchmarks solo se usan para la fila de comparación, claramente rotulados
  como tales.
- ❌ Generar el capítulo de Resultados cuando `artifacts/metrics` no existe — en ese caso el capítulo
  se entrega con estructura y placeholders explícitos, no con números plausibles.
