# RT-003: Fuentes de Datos para Entrenamiento y Validación

**Tipo:** Requisito técnico
**Categoría:** Datos / Infraestructura de datos
**Fuente:** 01-CONTEXTO-MAESTRO-CONSOLIDADO.md §5; 03-CATALOGO-DATOS-Y-VARIABLES.md; contexto-tfm.md §5

## Descripción
El modelo se entrenará y validará utilizando un conjunto de fuentes de datos reales que combinan bases internacionales (preentrenamiento), registros clínicos colombianos (adaptación al contexto local) y datasets públicos del sistema de salud colombiano (distribución poblacional de referencia). La combinación de fuentes es obligatoria — un modelo entrenado solo con MIMIC-IV-ED (EE.UU.) no es válido para el contexto colombiano.

## Fuentes de datos

| Fuente | Tipo | Volumen | Rol en el proyecto | Estado |
|---|---|---|---|---|
| **MIMIC-IV-ED v2.2** (PhysioNet) | Base internacional, acceso restringido (PhysioNet Credentialed Access) | 422.500 admisiones a urgencias | Entrenamiento base / preentrenamiento del modelo | Disponible (requiere acuerdo de uso de datos) |
| **Registro clínico Hospital San Juan de Dios** | Datos clínicos reales colombianos | A determinar | Fine-tuning y adaptación al contexto colombiano — **OBLIGATORIO** (sin esto, el modelo tiene sesgo geográfico) | **Autorizado** por Comité de Ética |
| **"Clasificación en Triaje Urgencias"** (Min. Salud, datos.gov.co) | Dataset público (CSV) | Nacional | Distribución real de niveles I-V en Colombia (referencia para calibrar prevalencia) | Disponible |
| **BDUA** (ADRES — Administradora de los Recursos del Sistema General de Seguridad Social en Salud) | Dataset público (CSV) | Nacional | Variables demográficas, régimen de afiliación, perfil socioeconómico | Disponible |
| **Datos abiertos Supersalud** | Dataset público (CSV) | Nacional | Desempeño operativo EPS/IPS (contexto, no features del modelo) | Disponible |

## Reglas de uso

1. **Preprocesamiento obligatorio:** anonimización de todas las fuentes antes de cualquier paso de análisis o entrenamiento (Ley 1581 de 2012, RNS-009, RNS-010).
2. **Eliminación de identificadores directos:** nombre, número de documento, dirección, teléfono, email — en todas las fuentes.
3. **Transformación de identificadores indirectos:** fecha de nacimiento → edad (años), municipio → departamento o categoría regional.
4. **Fine-tuning con datos colombianos es obligatorio, no opcional.** Un modelo entrenado solo con MIMIC-IV-ED no es válido para el contexto colombiano por sesgo geográfico (población, perfil epidemiológico, prácticas clínicas diferentes). Debe documentarse como limitación en el Cap. 6 del TFM.
5. **MIMIC-IV-ED requiere acuerdo de uso de datos** (PhysioNet Credentialed Access) y solo puede usarse para investigación. Los datos no pueden redistribuirse.

## Mapeo de fuentes a entidades del dominio

| Entidad | Fuente principal de entrenamiento | Fuente para la demo |
|---|---|---|
| ENT-001 Paciente (demográficas, régimen, vía de llegada) | MIMIC-IV-ED + BDUA | Formulario de registro (RF-PAC-001) |
| ENT-002 Evento de Triaje | Hospital San Juan de Dios + datos.gov.co | Generado por el sistema (RF-TRI-001) |
| ENT-003 Signos Vitales | MIMIC-IV-ED + Hospital San Juan de Dios | Formulario de captura (RF-VIT-*) |
| ENT-004 Motivo de Consulta | MIMIC-IV-ED + notas de admisión | Formulario (RF-EVA-001) |
| ENT-005 Antecedentes Clínicos | Hospital San Juan de Dios | Formulario (RF-EVA-005) |
| ENT-008 Texto Clínico | MIMIC-IV-ED (notas de enfermería) + Hospital San Juan de Dios | Campo de texto libre (RF-EVA-007) |

## Impacto en la arquitectura
- El pipeline de ingesta debe unificar múltiples fuentes con esquemas diferentes en un formato común.
- La anonimización es un paso explícito del pipeline (paso 2 del pipeline técnico definido en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`).
- Para la demo, los datos se capturan mediante formularios (no se usan datos reales de pacientes en la interfaz).

## Notas del analista
- **Hallazgo #2 de la validación:** `CONTEXT_TRIA.txt` (documento funcional) no menciona ninguna de estas fuentes de datos. Este RT cubre ese vacío.
- La autorización ética del Hospital San Juan de Dios está APROBADA según `CONTEXTO_TRIAJE.txt` v2.0, pero el PDF del TFM aún dice "requiere autorización". Actualizar el PDF antes del depósito (`05-PENDIENTES-PARA-DIRECTORA.md` #2).
