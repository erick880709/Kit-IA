# Estructura, Tono y Tiempo Verbal por Capítulo de TFM

## Principio general: propuesta vs. hechos consumados

| Estado del proyecto | Tiempo verbal | Ejemplo |
|---|---|---|
| Predepósito / diseño aún no ejecutado | Futuro / condicional | "Se entrenarán los modelos early y late fusion y se comparará su Recall en Niveles I-II." |
| Depósito / trabajo ya ejecutado | Presente de hechos consumados / pretérito | "Se entrenaron los modelos early y late fusion; el modelo de fusión tardía obtuvo un Recall de 0.86 en Nivel I y 0.81 en Nivel II, superando a la fusión temprana (0.79 y 0.75 respectivamente)." |

**Regla de conversión:** un capítulo solo pasa de condicional a hechos consumados si existe
evidencia en `artifacts/` que respalde la afirmación. Si el pipeline se ejecutó parcialmente
(p. ej. solo el baseline, no el multimodal), el capítulo debe reflejar exactamente eso — mezclar
hechos consumados (baseline) con condicional (multimodal aún pendiente) explícitamente, nunca
generalizar el tiempo verbal a todo el capítulo por comodidad.

## Mapa de capítulos típico (TFM tipo 2+3, desarrollo + piloto experimental)

| Capítulo | Contenido | Tiempo verbal esperado en depósito | Fuente de verdad |
|---|---|---|---|
| 0. Organización del trabajo en grupo (solo TFE grupal) | Reparto de responsabilidades, objetivos por integrante, coordinación, portavoz | Presente/pasado — hecho, no plan | Info directa del equipo, nunca inventada |
| 1. Introducción | Motivación, problema, contexto | Presente atemporal | Ya redactado usualmente en fase de anteproyecto — tocar solo si cambia el alcance |
| 2. Estado del arte | Revisión de literatura, benchmarks | Presente/pasado (lo que otros hicieron) | Papers citados — no tocar salvo que se añadan benchmarks nuevos |
| 3. Objetivos y metodología | Objetivo general/específicos, metas cuantitativas, metodología | Presente (declara qué se hizo/hará) | Debe ser coherente con Cap. 5/6 — si las metas no se alcanzaron, no se editan retroactivamente aquí; se reconcilian en Conclusiones |
| 4/5. Desarrollo de la contribución | Arquitectura, pipeline, decisiones técnicas tomadas | **Hechos consumados si ya se ejecutó** | `resources/architecture/`, `src/`, decisiones cerradas del contexto del proyecto |
| 5/6. Resultados y discusión | Métricas reales, matrices de confusión, comparación con benchmarks, casos SHAP | Pretérito/hechos consumados, con cifras trazables | `artifacts/metrics/`, `artifacts/shap/` — ver `plantilla-capitulo-resultados.md` |
| 6/7. Conclusiones y trabajo futuro | Qué se logró, limitaciones reales encontradas, qué queda para trabajo futuro | Pasado (logros) + futuro solo para "trabajo futuro" explícitamente etiquetado como tal | Debe fusionar cualquier anexo tipo "Anexo A" que duplique conclusiones — un solo apartado coherente |
| Resumen / Abstract | Síntesis de todo lo anterior | Debe reflejar resultados reales, no solo metas objetivo | Se redacta o ajusta AL FINAL, después de que Resultados esté cerrado |
| Apéndices | Código relevante, tablas extendidas, checklist de cumplimiento | — | No inventar contenido de apéndice; si está vacío, dejarlo pendiente explícito |

## Reglas de estilo transversales

- **Citas:** estilo consistente con el resto del documento (APA por defecto). No mezclar estilos
  entre capítulos.
- **Cifras:** toda cifra numérica en Resultados/Resumen/Conclusiones debe ser rastreable a un
  archivo de `artifacts/`. Si no lo es, se marca `[PENDIENTE — verificar en artifacts/metrics]`.
- **Figuras:** cada figura lleva leyenda descriptiva completa (qué muestra, de qué corrida/versión
  de modelo, qué eje representa cada cosa) — nunca placeholders tipo "Enter Caption" o "Figura X".
- **Consistencia de metas vs. resultados:** si una meta cuantitativa del Cap. 3 (p. ej. F1 ≥ 0.82)
  no se alcanzó en los resultados reales, el Resumen/Abstract y las Conclusiones deben decirlo
  explícitamente y de forma honesta — no se puede depositar un TFM cuyo resumen promete una cifra
  que el propio capítulo de resultados contradice.
- **Voz activa/pasiva:** aceptar la convención que ya use el documento existente; no forzar un
  cambio de registro salvo que el capítulo completo se esté reescribiendo desde cero.
- **Limitaciones:** deben ser específicas del proyecto (hallazgos reales: qué falló, qué sesgo se
  detectó, qué no se pudo validar), no una lista genérica copiada de la literatura.
