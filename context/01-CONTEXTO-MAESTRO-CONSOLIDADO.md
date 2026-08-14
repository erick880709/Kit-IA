# Contexto Maestro Consolidado — Sistema de Triaje Multimodal con IA (Colombia)

**Estado:** fuente única de verdad. Sustituye para efectos de desarrollo a `contexto-aplicacion-ia-triaje.md` (v1, superada). No sustituye a `CONTEXT_TRIA.txt` como documento funcional detallado — lo complementa uniéndolo con las decisiones técnicas.
**Ver también:** `00-VALIDACION-HALLAZGOS.md` (por qué existe este documento y qué resuelve).

## 1. Proyecto

| Campo | Valor |
|---|---|
| Título | Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia |
| Programa | Máster Universitario en Inteligencia Artificial — UNIR |
| Autores | Medina Betancur, Diego Andrés · Rivera Villanueva, Leyniker · Soto Díaz, Erick Duván |
| Directora | Damaris Fuentes Lorenzo |
| Tipología | Tipo 2 (Desarrollo software) + Tipo 3 (Piloto experimental/comparativa) |

## 2. Qué construye el sistema (resumen funcional)

Dado un conjunto de datos de un paciente en urgencias, predice el nivel de triaje (I-V, Resolución 5596 de 2015), con salida explicable (SHAP), como **apoyo** — nunca reemplazo — al profesional que valida.

```
Datos del paciente (estructurados + texto libre)
   → Módulo NLP (embeddings) + Módulo IA (fusión early/late)
   → Nivel I-V + probabilidad + confianza + explicación SHAP
   → Validación humana obligatoria → Registro de auditoría
```

## 3. Decisiones cerradas (fuente: `CONTEXTO_TRIAJE.txt` v2.0, 16 jul 2026 — prevalece sobre cualquier versión anterior)

| Decisión | Resultado |
|---|---|
| Arquitectura de fusión | **Ambas** (early y late fusion) — se entrenan, evalúan y compara; gana la de mejor Recall en Niveles I-II sin descuidar F1 global |
| Estrategia de umbral | **Prioriza Recall sobre Precisión en Niveles I y II**, con optimización de umbral por clase |
| Alcance del prototipo | Modelo entrenado/evaluado offline **+** demo funcional interactiva |
| Autorización ética (Hospital San Juan de Dios) | **Aprobada** por el Comité de Ética — ⚠️ pendiente reflejarlo en el PDF del TFM (ver `05-PENDIENTES-PARA-DIRECTORA.md`) |

## 4. Metas cuantitativas (consistentes en todos los documentos)

| Métrica | Meta |
|---|---|
| F1-score | ≥ 0,82 |
| Precisión | ≥ 0,85 |
| Recall | ≥ 0,80 |
| AUC-ROC | ≥ 0,87 |

Evaluación **por clase**, no solo macro-promedio (Nivel I es raro pero crítico — un buen F1 global puede esconder mal desempeño ahí). AUPRC adicional para clases minoritarias.

## 5. Fuentes de datos reales (ausentes en el documento funcional BPM — ver hallazgo #2)

| Fuente | Rol | Estado |
|---|---|---|
| MIMIC-IV-ED v2.2 (PhysioNet), 422.500 admisiones | Entrenamiento base / preentrenamiento | Disponible |
| Registro clínico Hospital San Juan de Dios | Adaptación al contexto colombiano (obligatoria — MIMIC solo no es válido por sesgo geográfico) | Autorizado |
| "Clasificación en Triaje Urgencias" (Min. Salud, datos.gov.co) | Distribución real de niveles I-V en Colombia | Disponible |
| BDUA (ADRES) | Variables demográficas, régimen de afiliación | Disponible |
| Datos abiertos Supersalud | Desempeño operativo EPS/IPS | Disponible |

Cumplimiento obligatorio: Ley 1581 de 2012 — anonimización antes de cualquier procesamiento (ya cubierto por RNS-009/RNS-010/RNGD-* del documento funcional).

## 6. Cómo se relacionan los dos documentos de origen

- **`CONTEXT_TRIA.txt`** sigue siendo tu mejor fuente para: stakeholders, roles, BPM AS-IS/TO-BE, catálogo de entidades, reglas de negocio genéricas, catálogo RF-* y casos de uso. Úsalo tal cual para esas partes.
- **Este documento + `02` + `03`** son la capa que faltaba: qué modelo, con qué datos, con qué arquitectura técnica exacta.
- Donde hay conflicto puntual (ver hallazgo #5 de la validación — RF-IA-003 vs. estrategia de umbral), **esta consolidación prevalece** y debes actualizar el texto de `CONTEXT_TRIA.txt` antes de usarlo como entregable formal.

## 7. Siguientes documentos de este set

- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` — cómo se entrena, valida y sirve el modelo.
- `03-CATALOGO-DATOS-Y-VARIABLES.md` — qué campo viene de qué fuente, con los 2 campos que faltaban añadidos.
- `04-ESPECIFICACION-APLICACION-DEMO.md` — qué construye el "skill builder" para la demo.
- `05-PENDIENTES-PARA-DIRECTORA.md` — lo que de verdad falta decidir con Damaris.
