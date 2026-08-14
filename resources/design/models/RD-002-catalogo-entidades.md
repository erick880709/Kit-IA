# RD-002: Catálogo de Entidades del Dominio (ENT-001 a ENT-012)

**Tipo:** Información de diseño
**Fuente:** `context/CONTEXT TRIA.txt` §20-24 · `context/03-CATALOGO-DATOS-Y-VARIABLES.md`

## Descripción
Catálogo de entidades del dominio ya definido en el documento funcional, con los cambios de la validación de hallazgos incorporados.

## Entidades principales y campos clave

| Entidad | Contenido | Cambios de la validación |
|---|---|---|
| ENT-001 Paciente | Demográficas, régimen, **ViaLlegada**, **EpisodiosPreviosUrgencias** | +2 campos nuevos (hallazgo #3) |
| ENT-001 Paciente (campos pendientes TT-E7-01) | Nombres, Apellidos, Teléfono, Correo, ContactoEmergencia, NumeroContactoEmergencia, Departamento, Ciudad, DireccionResidencia, **TipoSangre, Alergias** | +11 campos: 9 identificados en extracción previa (`resources/datos/functional/reqs/resumen-cambios-pendientes.md`) + 2 clínicos decididos por refinador (2026-08-13), con catálogos `DEPARTAMENTOS_COLOMBIA` (32), `CIUDADES_POR_DEPARTAMENTO` (~200) y `GRUPOS_SANGUINEOS` (8) |
| ENT-002 Evento de Triaje | Nivel asignado, hora de inicio/cierre | Extendida en RD-003 |
| ENT-003 Signos Vitales | FR, SpO₂, PA, FC, temperatura, peso/talla, IMC | Sin cambios |
| ENT-004 Motivo de Consulta | Código estructurado + texto libre | Aclarada la doble captura |
| ENT-005 Antecedentes Clínicos | Diabetes, HTA, ERC, embarazo, cáncer, cardiopatías, EPOC, cirugías, medicación | Sin cambios de estructura |
| ENT-006 a ENT-012 | Resto del catálogo (consúltese CONTEXT TRIA.txt) | Sin cambios |
| ENT-008 Texto Clínico | Notas de admisión / historia narrativa | — |
| ENT-009 Modelo | Versión, algoritmo, fecha, id | — |

## Mapeo a fuentes de datos reales
Ver RT-006 y `03-CATALOGO-DATOS-Y-VARIABLES.md` §2 (cada entidad → fuente de entrenamiento y fuente de la demo).

## Notas de diseño
`ViaLlegada` debe modelarse como catálogo controlado (Ambulancia / Particular / Remisión) para usarse como feature categórica sin normalización adicional (RNQ-004).

**Campos confirmados en fuentes locales (2026-08-13):**
- ENT-001: SEXO (F 55,4 % / M 44,6 %) y EDAD disponibles en el cohorte de morbilidad (43.594 episodios).
- ENT-004: el catálogo de motivos puede sembrarse con los diagnósticos CIE-10 más frecuentes: dolor abdominal (R10.4), rinofaringitis aguda (J00), cefalea, gastroenteritis, lumbago, dolor torácico, fiebre — consistente con los ejemplos ya listados en ENT-004.
- El CSV custom del hospital es el mismo cohorte de morbilidad + etiqueta de triaje: un solo origen de datos evita duplicar pacientes entre ENT-002 y ENT-004.
