# 0. Organización del trabajo en grupo — TFM TriajeIA

> Ubicación exigida: **antes de la introducción** (Protocolo TFE grupal UNIR).
> Estado: redactado con la información real del equipo (2026-08-14).
> ⚠️ Pendiente único: **aval explícito de la directora** antes del depósito.

**Título del TFM:** Desarrollo de un sistema de triaje multimodal basado en IA
para la atención en urgencias médicas en Colombia.

## Integrantes (orden alfabético)

| Integrante | Correo institucional |
|---|---|
| Medina Betancur, Diego Andrés | `[COMPLETAR con el correo UNIR]` |
| Rivera Villanueva, Leyniker | `[COMPLETAR con el correo UNIR]` |
| Soto Díaz, Erick Duván | `[COMPLETAR con el correo UNIR]` |

**Portavoz del grupo:** Medina Betancur, Diego Andrés — responsable de la
comunicación oficial con la directora y de la entrega de la presente
organización para su aval.

## Reparto de responsabilidades

| Integrante | Partes del trabajo |
|---|---|
| Medina Betancur, Diego Andrés | Introducción y estado del arte (capítulos 1–2): motivación del triaje en Colombia, revisión de literatura y benchmarks del estado del arte. |
| Rivera Villanueva, Leyniker | Metodología y desarrollo de la contribución (capítulos 3–4): diseño experimental, arquitectura del sistema y pipeline de entrenamiento. |
| Soto Díaz, Erick Duván | Resultados, discusión y conclusiones (capítulos 5–7): evaluación experimental, comparación con benchmarks, limitaciones y trabajo futuro. |

## Objetivos perseguidos en cada parte

1. **Introducción y estado del arte (Medina):** contextualizar el problema del
   triaje de urgencias en Colombia (Res. 5596/2015), fundamentar la necesidad
   de apoyo automatizado y sintetizar los benchmarks de referencia (CTAS,
   Hong et al., Ueareekul et al., Levin et al.).
2. **Metodología y desarrollo (Rivera):** documentar el diseño experimental
   reproducible (semilla fija, split estratificado, CV, umbrales por clase) y
   la construcción del sistema (arquitectura monolito modular, pipeline de 10
   pasos, integración de la cohorte San Juan de Dios).
3. **Resultados y conclusiones (Soto):** presentar las métricas reales con
   trazabilidad a artefactos, discutir la comparación honesta con la
   literatura y extraer conclusiones y trabajo futuro.

## Mecanismos de coordinación

- **Reuniones de avance cada 3 días** (sincrónicas, con acta breve de
  acuerdos y bloqueos).
- **Repositorio compartido** `erick880709/Kit-IA` (rama `main`): todo
  artefacto (código, métricas, capítulos) se versiona y cada commit queda
  trazable por autor.
- **Herramientas de comunicación:** mensajería grupal permanente + correo
  institucional para comunicaciones formales con la directora.
- **Regla de integración:** ninguna cifra entra a los capítulos sin su
  archivo fuente en `triaje-ia/artifacts/` (trazabilidad de resultados).

## Aval

- [ ] Firma/aval de la directora: `[COMPLETAR fecha y confirmación]`
