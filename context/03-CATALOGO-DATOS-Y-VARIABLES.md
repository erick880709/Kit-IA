# Catálogo de Datos y Variables — Consolidado

Extiende el catálogo de entidades ya definido en `CONTEXT_TRIA.txt` (secciones 20-24, ENT-001 a ENT-012). Aquí solo se muestran los **cambios**: campos añadidos y mapeo a fuentes de datos reales, que el documento original no tenía. El resto de entidades (ENT-006 a ENT-012) se mantiene sin cambios — consúltalas directamente en `CONTEXT_TRIA.txt`.

## 1. Campos añadidos (hallazgo #3 de la validación)

### ENT-001 Paciente — campos nuevos

| Atributo | Tipo | Obligatorio | Fuente |
|---|---|---|---|
| ViaLlegada | Catálogo (Ambulancia / Particular / Remisión) | Sí | Sistema de admisión |
| EpisodiosPreviosUrgencias | Entero | No | Historia clínica / registro hospitalario |

Ambas variables aparecen listadas como de **mayor peso predictivo** en el estado del arte revisado para el TFM, pero no existían como campo capturable en el módulo funcional original (`RF-PAC-*`). Sin este campo, el modelo no puede usar dos de sus predictores más fuertes.

### ENT-005 Antecedentes Clínicos — sin cambios de estructura, aclaración de fuente

Los atributos ya listados (diabetes, hipertensión, enfermedad renal, embarazo, cáncer, cardiopatías, enfermedad pulmonar, cirugías recientes, medicación relevante) se nutren de historia clínica; cuando no exista integración con Historia Clínica Electrónica (RF-INT-001, condicionado a disponibilidad institucional), se capturan por autorreporte/anamnesis en el módulo de Evaluación Clínica (RF-EVA-005).

## 2. Mapeo de entidades → fuentes de datos reales

Este mapeo es lo que faltaba entre el catálogo de entidades (BPM) y las fuentes de datos reales del proyecto (`01-CONTEXTO-MAESTRO-CONSOLIDADO.md` §5).

| Entidad del dominio | Fuente(s) de datos para entrenamiento | Fuente para la demo (dato en vivo) |
|---|---|---|
| ENT-001 Paciente (demográficas, régimen, vía de llegada) | MIMIC-IV-ED (demográficas/admisión) + BDUA (régimen de afiliación, perfil socioeconómico) | Formulario de registro (RF-PAC-001) |
| ENT-002 Evento de Triaje | Registro clínico Hospital San Juan de Dios + "Clasificación en Triaje Urgencias" (datos.gov.co) — distribución real de niveles I-V en Colombia | Generado por el sistema (RF-TRI-001) |
| ENT-003 Signos Vitales | MIMIC-IV-ED + Hospital San Juan de Dios | Formulario de captura (RF-VIT-*) |
| ENT-004 Motivo de Consulta | MIMIC-IV-ED (motivo estructurado) + notas de admisión | Formulario (RF-EVA-001) |
| ENT-005 Antecedentes Clínicos | Hospital San Juan de Dios (historia clínica, sujeto a autorización ya aprobada) | Formulario (RF-EVA-005) |
| ENT-008 Texto Clínico | MIMIC-IV-ED (notas de enfermería) + Hospital San Juan de Dios | Campo de texto libre (RF-EVA-007) |
| — (contexto operativo EPS/IPS, no es entidad clínica del paciente) | Datos abiertos Supersalud | No aplica a la demo — solo análisis exploratorio/contexto en el TFM |

## 3. Reglas de calidad ya vigentes que aplican a estos campos nuevos (sin cambios, ya cubiertas)

RNQ-001 (campos obligatorios no vacíos), RNQ-003 (alertas por valores fuera de rango), RNQ-004 (catálogos controlados para categóricas) — `ViaLlegada` debe implementarse como catálogo controlado, no texto libre, para que sea utilizable como feature categórica sin normalización adicional.

## 4. Anonimización (Ley 1581 de 2012, sin cambios de fondo)

Todas las fuentes anteriores deben pasar por el proceso de anonimización obligatorio (RNS-009, RNS-010, RNGD-*) antes de cualquier uso en entrenamiento — esto ya está bien cubierto en el documento funcional, se mantiene igual.
