# Solicitud de autorización al Comité de Ética de la Investigación (borrador)

> ⚠️ Este documento es un **borrador para presentar** al Comité de Ética.
> NO constituye evidencia de autorización. Art. 2.7 del Reglamento de
> TFG/TFM de UNIR: la autorización debe obtenerse **antes** de la recogida;
> sin ella no se permite el depósito ni la defensa. El equipo debe ajustar
> fechas y hechos reales antes de presentarlo.

## 1. Datos del proyecto

- **Título:** Desarrollo de un sistema de triaje multimodal basado en IA para
  la atención en urgencias médicas en Colombia.
- **Investigadores:** Medina Betancur, D. A. · Rivera Villanueva, L. · Soto
  Díaz, E. D. (Máster Universitario en Inteligencia Artificial, UNIR).
- **Directora:** Damaris Fuentes Lorenzo.
- **Tipo:** trabajo académico de fin de máster, sin finalidad asistencial ni
  comercial.

## 2. Datos utilizados y su origen

| Fuente | Naturaleza | Identificabilidad |
|---|---|---|
| Registro clínico de urgencias Hospital San Juan de Dios (43.594 eventos, 2023) | Cohorte clínica histórica (nivel de triaje, motivo, CIE-10) | Sin identificadores directos (sin nombres, sin documento) |
| Datasets públicos colombianos (MinSalud/datos.gov.co: triage, BDUA, Línea 123, morbilidad) | Datos abiertos publicados por el Estado | Datos abiertos (no requieren consentimiento, sujetos a términos de reuso) |
| Dataset sintético de demostración generado por software | Sintético, calibrado con la distribución nacional | No corresponde a personas reales |

## 3. Medidas de protección de datos personales

1. **Anonimización obligatoria** en el pipeline de ingesta (módulo
   `ml/src/data/anonimizacion.py`): eliminación de nombres y documentos,
   enmascaramiento en salidas (Ley 1581/2012).
2. **Los datos crudos no se publican ni comparten:** `datasets/` está
   excluido del repositorio público (`.gitignore`) y no se distribuye.
3. **Finalidad única:** entrenamiento y evaluación del modelo con fines
   académicos; no se usa para decisiones asistenciales.
4. **Hallazgos negativos también se reportarán** (transparencia metodológica).

## 4. Solicitud

Se solicita al Comité de Ética de la Investigación:

- **Autorización/aval** para el uso de la cohorte histórica anonimizada del
  Hospital San Juan de Dios en el entrenamiento y evaluación del sistema.
- Confirmación de que el uso de **datos abiertos** del Estado no requiere
  trámite adicional.

## 5. Documentos anexos (a adjuntar por el equipo)

- [ ] Convenio o autorización institucional del Hospital San Juan de Dios.
- [ ] Certificado de anonimización del dataset (verificación de que ningún
      campo es identificable).
- [ ] Protocolo de tratamiento de datos firmado por los investigadores.

**Estado:** `[PENDIENTE DE PRESENTACIÓN — fecha y número de radicado]`
