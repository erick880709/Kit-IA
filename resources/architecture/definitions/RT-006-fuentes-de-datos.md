# RT-006: Fuentes de Datos para Entrenamiento

**Tipo:** Requisito técnico
**Categoría:** Infraestructura / Datos
**Fuente:** `context/01-CONTEXTO-MAESTRO-CONSOLIDADO.md` §5 · `context/03-CATALOGO-DATOS-Y-VARIABLES.md` §2 · `context/07-MAPEO-Y-DESCARGA-DATASETS.md`

## Descripción
El pipeline de ingesta consume un conjunto definido de fuentes de datos, cada una con un rol específico y un estado de disponibilidad.

## Criterio medible / restricción concreta
| Fuente | Rol | Estado |
|---|---|---|
| MIMIC-IV-ED v2.2 (PhysioNet) | Entrenamiento base / preentrenamiento (422.500 admisiones) | Disponible (acceso credencializado) |
| Registro Hospital San Juan de Dios | Fine-tuning obligatorio (mitiga sesgo geográfico) | Autorizado por Comité de Ética |
| Clasificación en Triaje Urgencias (datos.gov.co) | Distribución real de niveles I–V en Colombia | Descargado (local en `datasets/`) |
| BDUA Contributivo/Subsidiado (ADRES) | Régimen de afiliación, demográficas | Descargado (local en `datasets/`) |
| Datos abiertos Supersalud | Contexto operativo EPS/IPS (no entra al modelo) | Descarga manual (portal propio) |
| MIMIC-IV-Demo 2.2 | Prototipado del pipeline (sin tablas ED) | Open access |

## Impacto en la arquitectura
Define el módulo de ingesta con adaptadores por fuente (PhysioNet, Socrata, CKAN, archivos locales) y el orden obligatorio anonimización → limpieza.

## Notas del analista
BDUA es un dataset **agregado** (conteos): calibra priors poblacionales de `Régimen`; no hace join fila a fila con pacientes. RIPS (`xveb-6jax`) devolvió 403 al intentar descarga — verificar ID republicado en datos.gov.co.

**Fuentes locales adicionales validadas (2026-08-13):**
- `MORBILIDAD_EN_EL_SERVICIO_DE_URGENCIAS` (43.594 episodios, 2023-2026): evento individual con SEXO, EDAD, TIPO_EDAD, DEPARTAMENTO, FECHA_ATENCION, DIAGNOSTICO (CIE-10), REGIMEN y EAPB — **es el mismo cohorte** del CSV custom del Hospital San Juan de Dios (misma cantidad de filas y mismos diagnósticos top).
- `dataset_urgencias_san_juan_de_dios_custom.csv`: cohorte + etiqueta de triaje + horas de entrada/salida — el vínculo entre morbilidad RIPS y el label I-V.
- Distribución de régimen en el cohorte: SUBIDIADO 77,7 % · CONTRIBUTIVO 14,4 % · ESPECIAL 2,4 % · OTRO 2,3 % · SOAT/ARL/Particular/Vinculado < 1 % c/u. **Calidad de datos:** el campo REGIMEN tiene typos (`ESPCIAL`, `EXCPECION`, `EXCEPCION`) y el campo AÑO tiene ~130 filas con valores corruptos (2027-2358) — exigen normalización en la ingesta (RF-016).
- Ninguna fuente local aporta **signos vitales**: MIMIC-IV-ED sigue siendo la única fuente para ese bloque de features.
