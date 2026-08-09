# Plantilla: Documento de Arquitectura para Sistemas con Componente de ML/IA

Extiende `references/plantilla-documento-arquitectura.md` — no la reemplaza. Usa esta versión cuando `references/guia-ml-arquitectura.md` determinó que el sistema tiene un componente de ML relevante (entrena modelo propio y/o tiene pipeline de datos no trivial). Las secciones 1 a 3, 10, 11, 13, 16 y 17 son idénticas a la plantilla base — solo se muestran aquí las secciones que cambian o se insertan.

```markdown
# Documento de Arquitectura de Software: [Nombre del Proyecto]

[... Secciones 1-3 idénticas a la plantilla base: Introducción y Objetivos, Restricciones, Alcance y Contexto ...]

En la Sección 1.3 (Atributos de calidad), agrega explícitamente las métricas de modelo como
requerimiento no funcional (ej. F1-score ≥ 0,82, AUC-ROC ≥ 0,87) — son tan vinculantes como
un SLA de disponibilidad.

## 4. Estrategia de Solución

[Igual que la plantilla base, pero además: por qué el problema se aborda con ML (y no con
reglas de negocio explícitas) — justifícalo, no lo asumas. Si el sistema combina reglas de
negocio deterministas con el modelo (ej. umbrales de alerta clínica), documenta cómo se
dividen las responsabilidades entre ambos.]

## 5. Vista de Contenedores (C4 Nivel 2)

[Igual que la base — pero el contenedor de "servicio de predicción/modelo" se documenta con
el mismo detalle que cualquier otro contenedor: tecnología de serving, y su relación con el
pipeline de datos y el registro de modelos.]

## 5.1 Arquitectura de Datos

[Ver references/guia-ml-arquitectura.md sección 2. Tabla de fuentes de datos, diagrama de
pipeline de datos (references/diagramas-ml-ejemplos.md), y decisiones de feature engineering
y split train/val/test.]

## 5.2 Arquitectura de Entrenamiento

[Ver references/guia-ml-arquitectura.md sección 3. Diagrama de pipeline de entrenamiento,
modelos baseline vs. candidatos, framework, cómputo usado, tracking de experimentos y
versionado de modelos/datos.]

## 5.3 Evaluación y Métricas

[Ver references/guia-ml-arquitectura.md sección 4. Tabla de métricas objetivo vs. obtenidas
(global y por clase), matriz de confusión, comparación contra baseline y benchmarks externos,
estrategia de manejo de desbalance de clases si aplica.]

## 5.4 Explicabilidad (XAI)

[Ver references/guia-ml-arquitectura.md sección 5. Técnica usada, qué se muestra al usuario
final, alcance (global/local) de la explicación.]

## 6. Vista de Componentes (C4 Nivel 3)

[Igual que la base — aplica al contenedor de aplicación/API. El pipeline de entrenamiento no
necesita descomponerse a Nivel 3 salvo que tenga lógica interna especialmente compleja.]

## 7. [Opcional] Vista de Código (C4 Nivel 4)

[Igual que la base.]

## 8. Vistas de Ejecución: Diagramas de Secuencia

[Igual que la base — incluye el flujo de inferencia end-to-end (usuario envía datos → 
preprocesamiento → modelo → explicación → respuesta) como uno de los flujos críticos
obligatorios.]

## 9. Modelo de Datos

[Igual que la base, para el modelo de datos operacional del sistema (no confundir con las
features de entrenamiento, que van en 5.1).]

## 9.1 Arquitectura de Inferencia / Servicio del Modelo

[Ver references/guia-ml-arquitectura.md sección 6. Modo de inferencia (tiempo real/batch),
dónde vive el modelo servido, latencia objetivo, y diagrama de la sección correspondiente en
references/diagramas-ml-ejemplos.md. Incluye el mecanismo de reentrenamiento (manual,
programado, o disparado por deriva).]

## 10. Conceptos Transversales

[Igual que la base, agregando explícitamente: reproducibilidad del entrenamiento (semillas,
versionado de datos/dependencias — ver references/guia-notebooks-python.md), y monitoreo de
deriva de datos/modelo en producción.]

## 11. Decisiones Arquitectónicas (ADRs)

[Igual que la base — incluye aquí las decisiones específicas de modelo (ej. "ADR: Fusión
tardía sobre fusión temprana", "ADR: XGBoost sobre red neuronal para el submodelo
estructurado") con el mismo rigor de contexto/alternativas/consecuencias que cualquier ADR de
software.]

## 12. Vista de Despliegue

[Igual que la base — pero el cómputo de entrenamiento (si es distinto al de servicio del
modelo) se documenta como un componente de infraestructura separado: dónde corre el
entrenamiento (notebook cloud, cluster, GPU dedicada) vs. dónde corre la inferencia en
producción.]

## 13. Riesgos y Deuda Técnica

[Igual que la base, agregando riesgos propios de ML si aplican: training-serving skew,
ausencia de monitoreo de deriva, dataset no representativo del contexto real de uso, falta de
tracking de experimentos que impida reproducir el modelo actual.]

## 13.1 Gobernanza, Ética y Cumplimiento

[Ver references/guia-ml-arquitectura.md sección 7. Rol del sistema (apoyo vs. autónomo),
marco normativo de datos personales/sensibles aplicable, sesgo/representatividad de los
datos, trazabilidad de predicciones, estrategia de detección de deriva.]

[... Secciones 14-17 (Gap Analysis, Roadmap, Supuestos, Glosario) idénticas a la plantilla
base cuando aplican ...]
```

## Reglas

- No dupliques contenido entre 5.1-5.4/9.1/13.1 y las secciones base — son inserciones, no un documento paralelo.
- Si el proyecto es puramente de investigación/tesis sin componente de despliegue en producción real (ej. un TFM que entrega un modelo evaluado offline sin interfaz funcional), omite honestamente 9.1 y la parte de infraestructura de servicio de la Sección 12 — no inventes un despliegue que no existe; dilo explícitamente en Supuestos ("el alcance del proyecto es el modelo entrenado y evaluado offline; no se implementó una arquitectura de servicio en producción").
- Sigue usando `references/diagramas-c4-ejemplos.md` para todo lo que sea C4 puro (Contexto, Contenedores, Componentes de la aplicación) — esta plantilla no reemplaza esos diagramas, solo agrega los específicos de ML.
