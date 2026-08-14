# Validación del contexto — Sistema de Triaje Multimodal IA (Colombia)

**Rol:** revisión como par experto en Máster de IA sobre el conjunto de documentos de contexto entregados.
**Documentos revisados:**
1. `CONTEXT_TRIA.txt` — *Documento Maestro de Contexto Funcional* (3558 líneas, Entregas 1-9, 57 secciones): BPM, dominio, reglas de negocio, catálogo de requerimientos funcionales, casos de uso.
2. `CONTEXTO_TRIAJE.txt` — *Contexto de la Aplicación v2.0 (16 jul 2026)*: decisiones técnicas cerradas (fusión, umbral, alcance, ética).
3. `contexto-aplicacion-ia-triaje.md` — versión anterior (v1) del documento anterior, con preguntas aún abiertas.
4. `contexto-tfm.md` — ficha de proyecto TFM: objetivos, fuentes de datos, benchmarks, estado de capítulos.
5. PDF del TFM (Cap. 1-3 redactados): introducción, estado del arte, objetivos y metodología.

## 1. Conclusión principal

Tienes **dos líneas de contexto que se desarrollaron en paralelo y nunca se fusionaron**:

- **Línea de negocio/funcional** (`CONTEXT_TRIA.txt`): extremadamente completa en BPM, roles, reglas de negocio, catálogo de entidades, casos de uso y requerimientos funcionales (RF-*, RN*). Es el mejor insumo que tienes para arquitectura de aplicación.
- **Línea técnica/ML** (`CONTEXTO_TRIAJE.txt` + `contexto-tfm.md` + PDF): contiene las decisiones de modelado (fusión early+late, prioridad de recall, fuentes de datos reales, métricas objetivo, autorización ética).

**Verifiqué por búsqueda exhaustiva y `CONTEXT_TRIA.txt` no menciona ni una sola vez**: MIMIC-IV-ED, Hospital San Juan de Dios, BDUA, Supersalud, "early fusion"/"late fusion", XGBoost, BERT/BioBERT, Random Forest, regresión logística, 10-fold cross-validation, SMOTE/class weights/focal loss, ni ninguna de las metas cuantitativas (F1≥0,82, Precisión≥0,85, Recall≥0,80, AUC-ROC≥0,87). Tampoco resuelve explícitamente la estrategia de umbral por clase para Niveles I-II, ni el estado de la aprobación ética — aunque sí tiene una regla genérica (RNA-007) de "no usar modelos no validados clínicamente en producción" que es compatible pero no dice qué se decidió.

Es decir: **el documento maestro funcional es el "cómo se construye la aplicación" y le falta por completo el "qué modelo se entrena y con qué datos"**. Antes de poder construir desarrollo (modelos + app) hace falta unir ambas líneas — eso es lo que hacen los archivos 01-04 que generé junto a este.

## 2. Documentos superados / a dejar de usar como fuente

- **`contexto-aplicacion-ia-triaje.md` (v1) queda superado por `CONTEXTO_TRIAJE.txt` (v2.0)**. La v1 lista como "pendiente con la directora" exactamente las 4 preguntas que la v2.0 ya cerró (fusión, umbral, alcance del prototipo, autorización ética). No lo uses como referencia de decisiones abiertas — solo tiene valor histórico.

## 3. Inconsistencias y vacíos detectados (con acción tomada)

| # | Hallazgo | Documento(s) | Acción |
|---|---|---|---|
| 1 | El índice de `CONTEXT_TRIA.txt` (40 secciones anunciadas) no coincide con el cuerpo real del documento (57 secciones, numeración distinta). El propio documento se desincronizó de su tabla de contenidos a medida que creció por entregas. | CONTEXT_TRIA.txt | No bloqueante, pero regenera el índice si vas a usar este documento como entregable formal del TFM. |
| 2 | Cero referencia a las fuentes de datos reales (MIMIC-IV-ED, San Juan de Dios, BDUA, datos.gov.co, Supersalud) en el documento funcional — `RF-INT-004 Dataset de Entrenamiento` solo dice "Exportación anonimizada", sin nombrar fuentes. | CONTEXT_TRIA.txt vs contexto-tfm.md | Resuelto en `03-CATALOGO-DATOS-Y-VARIABLES.md`, que mapea cada fuente real a las entidades del dominio ya definidas (ENT-001 a ENT-012). |
| 3 | Dos variables señaladas como **de mayor peso predictivo** en la literatura y en `contexto-tfm.md` — **vía de llegada** (ambulancia/particular/remisión) y **episodios previos de urgencias** — no existen como campo en ningún módulo funcional (`RF-PAC-*`, `RF-EVA-*`) ni en el catálogo de entidades (ENT-001 Paciente, ENT-005 Antecedentes). | CONTEXT_TRIA.txt vs contexto-tfm.md | Añadidas como campos en `03-CATALOGO-DATOS-Y-VARIABLES.md` (ENT-001 y ENT-005 extendidas). Esto es una omisión real que sí afecta el rendimiento del modelo si no se captura — repórtalo también en el TFM. |
| 4 | La arquitectura de modelo (`Reglas de Inteligencia Artificial`, RNA-001 a RNA-010) es agnóstica al algoritmo: no dice si hay uno o dos submodelos, ni cómo se combinan las salidas de fusión tardía. RNA-006 sí permite "coexistencia de múltiples versiones del modelo", lo cual es compatible con correr early y late fusion en paralelo, pero no lo dice explícitamente. | CONTEXT_TRIA.txt vs CONTEXTO_TRIAJE.txt | Resuelto en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`, que ata la decisión "ambas arquitecturas, se compara y se elige" a RNA-006/RF-IA-007 (Comparación de Modelos) y RF-MOD-* (Gestión de Modelos), que ya existían para soportar justo este caso. |
| 5 | No hay estrategia de umbral por clase documentada en ningún lado del documento funcional, pese a que `RF-IA-003` selecciona automáticamente "la clase con mayor probabilidad" — esto es **contradictorio** con la decisión de `CONTEXTO_TRIAJE.txt` de ajustar el umbral de decisión para maximizar Recall en Niveles I-II (que por definición implica *no* seleccionar siempre el argmax puro). | CONTEXT_TRIA.txt (RF-IA-003) vs CONTEXTO_TRIAJE.txt §6 | **Contradicción real, no solo vacío.** Resuelto (reescrito) en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`: RF-IA-003 debe leerse como "clase con mayor probabilidad **tras aplicar el umbral optimizado por clase para Niveles I-II**", no como argmax puro. Te recomiendo actualizar el texto de RF-IA-003 en el documento maestro para que no quede ambiguo en la sustentación. |
| 6 | El estado de la autorización ética del Comité del Hospital San Juan de Dios aparece como **"APROBADA"** en `CONTEXTO_TRIAJE.txt` (v2.0, 16 jul 2026) pero como **"pendiente"** en `contexto-aplicacion-ia-triaje.md` (v1) y no se menciona en absoluto en `CONTEXT_TRIA.txt` ni en el PDF del TFM (que solo dice "requiere autorización, Art. 2.7"). | Los tres | La v2.0 es la más reciente y es la que debe prevalecer — pero el PDF (que es el documento oficial entregado a UNIR) todavía no refleja la aprobación. **Acción pendiente tuya**: actualizar el Cap. 3 / apéndices del PDF con la fecha y evidencia formal de aprobación del comité antes del depósito, o el TFM quedará con una afirmación desactualizada respecto a tu propio contexto de trabajo. |
| 7 | Nivel de detalle del stack técnico: `CONTEXTO_TRIAJE.txt` menciona Streamlit/Flask como alternativas para la demo, sin decidir cuál. `CONTEXT_TRIA.txt` también menciona ambas una sola vez, igual de indeciso. | Ambos | No es una contradicción, es una decisión pendiente real. La dejo explícita en `05-PENDIENTES-PARA-DIRECTORA.md` con una recomendación (no una decisión impuesta). |

## 4. Lo que SÍ está bien resuelto y no requiere cambios

- Los 5 niveles de triaje, tiempos máximos y marco normativo (Resolución 5596/2015) son consistentes en los 5 documentos.
- Las metas cuantitativas (F1≥0,82, Precisión≥0,85, Recall≥0,80, AUC-ROC≥0,87) son consistentes entre `contexto-tfm.md`, `CONTEXTO_TRIAJE.txt` y el PDF.
- El catálogo de entidades de dominio (ENT-001 a ENT-012) y sus relaciones/cardinalidades en `CONTEXT_TRIA.txt` es sólido y reutilizable casi tal cual — solo necesitaba los dos campos faltantes de la fila 3.
- Las reglas de seguridad, auditoría y gobierno del dato (RNS-*, RNAU-*, RNGD-*) ya cubren Ley 1581 de 2012 y anonimización de forma consistente con `CONTEXTO_TRIAJE.txt` §9.

## 5. Archivos generados a partir de esta validación

- `01-CONTEXTO-MAESTRO-CONSOLIDADO.md` — fuente única de verdad, resuelve las contradicciones de la tabla anterior.
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` — spec de modelado lista para implementar (arquitectura, features, umbral, validación, XAI).
- `03-CATALOGO-DATOS-Y-VARIABLES.md` — catálogo de entidades corregido + mapeo a fuentes de datos reales.
- `04-ESPECIFICACION-APLICACION-DEMO.md` — spec funcional de la app demo, derivada de los módulos RF-* ya existentes, lista como insumo para diseño (Figma) y desarrollo.
- `05-PENDIENTES-PARA-DIRECTORA.md` — lo que de verdad sigue abierto y necesita una decisión humana, no una inferencia mía.
