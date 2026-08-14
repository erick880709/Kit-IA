# Brief maestro para finalizar el TFM
### "Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia"

**Autores:** Medina Betancur, Diego Andrés; Rivera Villanueva, Leyniker; Soto Díaz, Erick Duván
**Directora:** Damaris Fuentes Lorenzo
**Titulación:** Máster Universitario en Inteligencia Artificial (UNIR)
**Estado del documento base:** Predepósito (Ordinaria) — Armenia, Colombia, 14/07/2026

---

## 0. Propósito de este documento

Este archivo es el **briefing operativo** que debe entregarse a la IA (junto con el código del
aplicativo, los notebooks/scripts de `src/`, los artefactos en `artifacts/` y los resultados reales
de entrenamiento/evaluación) para que redacte, con el nivel de rigor exigido por UNIR, **todo lo que
falta** para pasar de "predepósito" a un TFM depositable y defendible.

No es un resumen del trabajo: es una **lista de instrucciones accionables** organizada por sección,
con las reglas normativas que condicionan cada una y el criterio de "hecho" (definition of done) que
debe cumplir el texto generado.

---

## 1. Reglas normativas aplicables (resumen ejecutivo)

### 1.1 Reglamento de TFG/TFM de UNIR (documento general)

- **Art. 2.1** — El TFM puede ser grupal si la memoria/guía docente lo permite y la Dirección del
  Título lo autoriza, **pero la defensa y la evaluación de cada estudiante son siempre individuales**.
- **Art. 2.2** — El trabajo debe ser **original e inédito**: no puede ser, en todo o en parte, plagiado
  ni haber sido presentado o publicado antes. No es original un trabajo con exceso de información de
  otras fuentes (aunque estén citadas); no es inédito uno que repite trabajos previos del propio
  estudiante.
- **Art. 2.7 (CRÍTICO / BLOQUEANTE)** — Si el TFM recaba datos personales de terceros, especialmente
  **datos sanitarios** (caso del registro clínico del Hospital San Juan de Dios), es obligatorio
  solicitar autorización previa al **Comité de Ética de la Investigación** antes de iniciar la
  recogida. **Sin esa autorización, no se permite ni el depósito ni la defensa.**
- **Art. 7** — La matrícula da derecho a convocatoria ordinaria y extraordinaria en el mismo curso.
  Para defender en ordinaria, el resto de asignaturas deben estar aprobadas en su convocatoria
  ordinaria.
- **Art. 8.3/8.4** — Prohibido usar datos personales de terceros sin autorización del titular; usar
  ayuda de terceros no autorizada expresamente por el director es conducta antiacadémica sancionable.
- **Art. 9** — El director debe autorizar el depósito y proponer la calificación de estructura y
  contenido (según rúbrica de la Comisión Académica) **antes** de que el trabajo se remita a la
  comisión evaluadora. En TFM, la comisión evaluadora puede dictaminar una calificación distinta a la
  propuesta del director sin necesidad de escalar a la Comisión Académica.
- **Art. 10** — Entre el depósito y la defensa deben transcurrir entre **30 y 90 días naturales**;
  UNIR publica el calendario con 10 días de antelación. La defensa es oral, pública, y puede
  completarse con recursos tecnológicos; si es en línea, se graba.
- **Art. 11 (Plagio)** — El director debe comprobar la ausencia de plagio con las herramientas
  anti-plagio de UNIR antes de autorizar el depósito. El plagio implica suspenso automático y, si hay
  falsa autoría, expediente disciplinario.
- **Art. 12 (Calificación)** — Escala 0–10 (Suspenso / Aprobado / Notable / Sobresaliente). Tres
  componentes: **estructura, contenido y defensa**. Es obligatorio obtener al menos el 50 % de los
  puntos de defensa para aprobar la asignatura. Matrícula de honor solo para calificación ≥ 9.7 y
  máximo 2.5 % de los matriculados en la convocatoria.
- **Art. 13** — Solo con calificación ≥ 9.0 y autorización expresa del autor, el trabajo puede
  depositarse en el repositorio público institucional (licencia Creative Commons).

### 1.2 Protocolo TFE grupal (documento específico)

- **Composición**: grupo de 2–3 estudiantes (cumple: 3 integrantes).
- **Organización del trabajo en grupo**: el portavoz entrega el documento "Organización del trabajo
  en grupo", que debe detallar (i) en qué parte se centra cada estudiante, (ii) los objetivos
  perseguidos en cada parte y (iii) los mecanismos de coordinación. **Debe estar avalado por la
  directora antes de iniciar el trabajo** y se incluye como apartado específico **antes de la
  introducción** — es exactamente el Capítulo 1 del documento actual, y hoy está sin completar
  (placeholders `[COMPLETAR]`).
- **Portada**: nombres de todos los integrantes por **orden alfabético** (Medina → Rivera → Soto:
  correcto en el documento actual).
- **Normas de estilo/citación**: las mismas que el TFE individual.
- **Defensa grupal**: todos los miembros participan; presentación conjunta dividida en tantas partes
  equitativas como integrantes; **máximo 30 minutos de exposición total en TFM** (se busca no superar
  60 minutos contando preguntas del tribunal); cada miembro defiende su parte pero puede ser
  interpelado sobre cualquier parte del trabajo.
- **Evaluación (pesos oficiales)**:
  | Componente | Peso | Naturaleza |
  |---|---|---|
  | Estructura del TFE | 20 % | Grupal — misma nota para todos |
  | Exposición individual | 30 % | Individual |
  | Contenido individual | 50 % | Individual |
  - Parte individual total = 80 % de la nota; parte grupal = 20 %.
- **Incidencias**: incumplimiento de la planificación puede derivar en apercibimiento o expulsión del
  grupo; baja voluntaria posible en los primeros 20 días naturales desde el inicio de la dirección.

---

## 2. Diagnóstico del predepósito actual (gaps frente al estándar exigido)

El documento actual tiene una estructura formalmente correcta (portada, índices, resumen/abstract,
capítulos 1–6, apéndices, referencias), pero **mezcla una propuesta/diseño con un TFM terminado**.
Los siguientes puntos son los que la IA debe resolver, ordenados por bloqueo/severidad:

### 2.1 Bloqueantes normativos (impiden depósito/defensa si no se resuelven)

1. **Capítulo 1 — Organización del trabajo en grupo**: contiene `[COMPLETAR]` en reparto de
   responsabilidades, objetivos por integrante, mecanismos de coordinación y portavoz. Es
   obligatorio y debe quedar avalado por la directora. **No puede depositarse con placeholders.**
2. **Autorización del Comité de Ética** para el uso del registro clínico del Hospital San Juan de
   Dios (dato sanitario de terceros, Art. 2.7). El documento debe declarar explícitamente el estado
   real: (a) si se obtuvo la autorización (adjuntar referencia/fecha), o (b) si finalmente **no** se
   usaron datos reales del hospital y el trabajo se validó solo con fuentes públicas/abiertas
   (MIMIC-IV-ED, datos.gov.co, BDUA, Supersalud) — en cuyo caso hay que **reescribir la sección 3.2 y
   el checklist del Apéndice A.2** para reflejar esa decisión y justificarla como limitación, no
   dejarlo ambiguo.
3. **Anti-plagio**: el checklist (Apéndice A.2, ítem 4) indica que el paso por la herramienta
   anti-plagio de UNIR sigue pendiente. Debe ejecutarse y su resultado (porcentaje de coincidencia)
   debe quedar registrado antes del depósito real.
4. **Verificación de asignaturas aprobadas** (Art. 7.1/2.3-2.4) antes de la convocatoria de defensa
   — ítem 5 del checklist, pendiente de confirmación.

### 2.2 Contenido incompleto o solo "de diseño" (Capítulo 6 y Anexo A)

El propio Anexo A.1 del predepósito reconoce: *"el Capítulo 5 (Desarrollo del trabajo) recoge la
especificación de la arquitectura y el pipeline pendientes de implementación y ejecución; y el
capítulo de Conclusiones se completará una vez obtenidos los resultados experimentales."* Esto es
el núcleo del trabajo que falta y es exactamente lo que la IA debe redactar usando el código y los
resultados reales del aplicativo:

- **6.4 / 6.4.2 Pipeline técnico**: hoy describe el pipeline en condicional ("se propone", "se
  entrenará"). Debe reescribirse en pasado/presente de hechos consumados, con las decisiones
  realmente tomadas (qué modelo ganó, qué hiperparámetros, qué preprocesamiento se aplicó
  finalmente) y con referencias exactas a los módulos (`src/data_ingestor.py`,
  `src/preprocessor.py`, `src/embeddings.py`, `src/trainer.py`, `src/evaluator.py`,
  `src/explainer.py`).
- **Falta un capítulo/sección de "Resultados"**: no hay tablas con las métricas reales obtenidas
  (F1, precisión, recall, AUC-ROC, AUPRC) por modelo (baseline vs. fusión temprana vs. fusión
  tardía), ni matriz de confusión real, ni comparación cuantitativa contra los benchmarks de la
  Tabla 3.3 (Raita et al. 0.87 AUC-ROC, Hong et al. 0.93, Ueareekul et al. 0.917/0.629,
  CTAS 0.882, Levin et al. F1 0.81). Hay que sustituir las metas objetivo (Tabla 5.1) por los
  valores realmente alcanzados y contrastarlos.
- **6.6 Explicabilidad (XAI)**: falta al menos un caso clínico ilustrativo real con salida de SHAP
  (nivel predicho, probabilidad, top variables influyentes) generado por `src/explainer.py`, no solo
  la descripción conceptual del mecanismo.
- **6.7 Manejo del desbalance de clases**: falta indicar qué técnica se aplicó finalmente (class
  weights / SMOTE / focal loss) y su efecto medible en recall de las clases minoritarias (Nivel I y
  II), no solo enumerarlas como opciones.
- **Figuras 6.1–6.4**: todas tienen el pie de figura por defecto **"Enter Caption"**. Deben llevar
  una leyenda descriptiva real (p. ej. "Figura 6.1. Arquitectura modular del pipeline de triaje
  multimodal").
- **6.11 Conclusiones y trabajo futuro** (y el Anexo A "Conclusiones y Trabajo Futuro", que hoy está
  duplicado/incompleto): debe reescribirse a partir de los resultados obtenidos, no de expectativas.
  Actualmente el Anexo A.1 declara el trabajo como "pendiente de resultados experimentales"; esa
  frase debe desaparecer del documento final.
- **Nota de estructura**: el documento tiene el capítulo de "Conclusiones y Trabajo Futuro" **dos
  veces** (como 6.11 dentro del cuerpo y como Anexo A independiente, con contenido parcialmente
  redundante y con numeración de capítulo inconsistente respecto al índice, que enumera "Contexto y
  Estado del Arte" como capítulo 3 pero el pie de página del propio documento lo llama "Capítulo 2").
  Hay que unificar esto en una sola sección de conclusiones y corregir la numeración de capítulos en
  índice, cuerpo y pies de página para que sean coherentes entre sí.

### 2.3 Mejoras de calidad esperadas por un evaluador de UNIR

- Justificar con más detalle la elección final entre fusión temprana y fusión tardía (hoy el
  documento deja ambas como alternativas "a decidir por métricas", pero un TFM terminado debe
  mostrar la decisión ya tomada y motivada).
- Completar la Tabla 3.2 (fuentes de datos) indicando volumen real utilizado por fuente (no solo el
  rol).
- Reforzar el apartado de limitaciones con los hallazgos reales del proyecto (no solo limitaciones
  genéricas de sesgo geográfico y calidad de datos).
- Revisar consistencia de cifras entre Resumen/Abstract (que ya anuncian F1 ≥ 0.82 y AUC-ROC ≥ 0.87
  como si fueran objetivos) y los resultados reales: si los resultados reales no alcanzan esas
  cifras, el Resumen debe ajustarse para no sobre-prometer.

---

## 3. Checklist de cumplimiento normativo (a marcar antes del depósito real)

- [ ] Capítulo 1 "Organización del trabajo en grupo" completado y avalado por la directora Damaris
      Fuentes Lorenzo.
- [ ] Orden alfabético de autores verificado en portada (Medina → Rivera → Soto) — **ya correcto**.
- [ ] Autorización del Comité de Ética de la Investigación tramitada (o, alternativamente, retirado
      el uso de datos del Hospital San Juan de Dios y documentado como tal).
- [ ] Trabajo pasado por la herramienta anti-plagio de UNIR, con porcentaje de coincidencia
      registrado, antes de solicitar la autorización de depósito al director.
- [ ] Resto de asignaturas del plan de estudios aprobadas antes de la convocatoria de defensa.
- [ ] Defensa conjunta preparada en tres partes equitativas, sin exceder 30 minutos de exposición
      total (TFM).
- [ ] Todas las figuras con leyenda descriptiva real (sin "Enter Caption").
- [ ] Resultados experimentales reales incorporados (tablas de métricas, matrices de confusión,
      comparación contra benchmarks).
- [ ] Resumen/Abstract, Objetivos (Tabla 5.1) y Conclusiones coherentes con los resultados
      finalmente obtenidos.
- [ ] Numeración de capítulos coherente entre índice, cuerpo del texto y pies de página.

---

## 4. Instrucciones para la IA redactora (qué contexto darle y qué debe producir)

Al ejecutar esta tarea con otra sesión/IA, hay que **adjuntar además de este brief**:

1. El código fuente completo de `src/` (`data_ingestor.py`, `preprocessor.py`, `embeddings.py`,
   `trainer.py`, `evaluator.py`, `explainer.py`, `main.py`).
2. Los artefactos generados: `artifacts/models`, `artifacts/metrics`, `artifacts/shap`.
3. Los tres diagramas de `resources/architecture/` (`Documento_Arquitectura_Triage_Multimodal_IA.md`,
   `Despliegue_Triage_Multimodal_IA.drawio`, `Flujo_Experimentacion_Triage_Multimodal_IA.drawio`).
4. El PDF actual del predepósito (para mantener estilo, numeración y referencias ya citadas).

Y pedirle explícitamente que:

- **No invente cifras.** Todo resultado numérico (F1, AUC-ROC, recall, matrices de confusión) debe
  extraerse de `artifacts/metrics` y `artifacts/shap`; si un dato no existe, debe marcarlo como
  pendiente en vez de inventarlo.
- Redacte el **Capítulo 1** en base a lo que realmente hizo cada integrante (a completar por el
  equipo si la IA no tiene esa información — no debe inventar el reparto de tareas).
- Convierta el Capítulo 6 de modo condicional/propuesta a modo indicativo de hechos consumados,
  añadiendo la sección de **Resultados** que hoy falta, con tablas comparativas contra los
  benchmarks de la Tabla 3.3.
- Genere leyendas reales para las Figuras 6.1–6.4.
- Reescriba **Conclusiones y trabajo futuro** unificando el capítulo 6.11 y el Anexo A en un único
  apartado coherente, y ajuste el Resumen/Abstract a los resultados reales.
- Verifique y corrija la numeración de capítulos en índice, cuerpo y pie de página.
- Mantenga el estilo de citación APA ya usado en las referencias existentes.
- Señale explícitamente, al final de su entrega, cualquier punto del checklist de la Sección 3 de
  este brief que siga sin resolverse (p. ej. autorización ética o anti-plagio), porque son trámites
  administrativos que el equipo debe cerrar fuera del documento.

---

## 5. Prompt maestro sugerido (listo para pegar a la IA junto con el contexto anterior)

```
Actúa como coautor experto en la redacción de Trabajos de Fin de Máster de UNIR, especializado en
sistemas de IA aplicados a salud. Tienes acceso al código fuente del proyecto (src/), a los
artefactos de entrenamiento y evaluación (artifacts/), a los diagramas de arquitectura
(resources/architecture/) y al PDF del predepósito actual del TFM "Desarrollo de un sistema de
triaje multimodal basado en IA para la atención en urgencias médicas en Colombia".

Tu tarea es completar el documento para llevarlo de "predepósito" a "listo para depósito real",
cumpliendo el Reglamento de TFG/TFM de UNIR y el Protocolo de TFE grupal (resumidos en las
secciones 1 y 2 de este brief). Concretamente:

1. Redacta el Capítulo 1 "Organización del trabajo en grupo" (reparto de responsabilidades,
   objetivos por integrante, mecanismos de coordinación, portavoz) usando la información real
   del equipo que te proporcione; si falta algún dato, indícalo como pendiente en vez de
   inventarlo.
2. Reescribe el Capítulo 6 "Desarrollo del trabajo" en modo de hechos consumados (no de
   propuesta), incorporando una sección nueva de "Resultados" con las métricas reales extraídas
   de artifacts/metrics (F1, precisión, recall, AUC-ROC, AUPRC, matriz de confusión) por modelo
   (baseline, fusión temprana, fusión tardía) y comparándolas contra los benchmarks de la Tabla
   3.3 del documento original.
3. Añade al menos un caso clínico ilustrativo con la salida real de SHAP (artifacts/shap):
   nivel predicho, probabilidad, variables más influyentes.
4. Precisa qué técnica de balanceo de clases se aplicó finalmente y su efecto medible en las
   clases minoritarias.
5. Escribe leyendas descriptivas reales para las Figuras 6.1 a 6.4 (elimina "Enter Caption").
6. Unifica y reescribe "Conclusiones y trabajo futuro" (fusiona el actual 6.11 con el Anexo A)
   en un único apartado coherente con los resultados reales obtenidos, sin frases que indiquen
   trabajo pendiente de ejecución si ya se ejecutó.
7. Ajusta el Resumen y el Abstract para que reflejen los resultados realmente alcanzados en vez
   de solo las metas objetivo.
8. Corrige la numeración de capítulos para que sea coherente entre índice, cuerpo y pie de
   página.
9. No inventes cifras, autorizaciones éticas ni resultados de anti-plagio: si no dispones de
   esa información, dedícale una nota explícita de "pendiente de confirmar por el equipo antes
   del depósito".
10. Mantén el estilo de citación APA y el tono académico ya usado en el documento original.

Entrega el documento actualizado completo en el mismo formato (LaTeX/Markdown según corresponda),
y al final añade una lista de los puntos del checklist normativo que siguen sin resolver.
```

---

## 6. Notas de contexto adicionales (recordar al usar este brief)

- El proyecto ya empaqueta el contexto funcional del aplicativo en un "Documento Maestro de
  Contexto Funcional" (`CONTEXT_TRIA.txt`, ~3500 líneas) con reglas de negocio y entidades de
  dominio: conviene aportarlo también a la IA redactora para que el Capítulo 6 sea coherente con
  el diseño funcional ya definido.
- El equipo ha venido usando un protocolo de reducción de ambigüedad y ficheros `.skill` de Claude
  para mantener continuidad entre sesiones; este brief está pensado para integrarse en ese mismo
  flujo de trabajo.
