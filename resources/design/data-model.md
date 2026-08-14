# Modelo de Datos — TriajeIA

> Generado por `genesis` a partir de la Sección 9 del `Documento_Arquitectura_TriajeIA.md` y de RD-002/RD-003 (entidades ya validadas por negocio). `builder` completa/implementa estas entidades; no las rediseña.

## Entidades existentes

### Paciente (ENT-001)
- **Tabla / Colección:** `pacientes`
- **Tipo de ID:** UUID v4 (texto)
- **Campos:**
  - `tipo_documento` TEXT (CC / TI / CE)
  - `numero_documento` TEXT (único)
  - `nombres` TEXT · `apellidos` TEXT
  - `fecha_nacimiento` DATE · `sexo` TEXT
  - `departamento` TEXT (catálogo 32) · `ciudad` TEXT (~200) · `direccion_residencia` TEXT
  - `telefono` TEXT · `correo` TEXT
  - `contacto_emergencia` TEXT · `numero_contacto_emergencia` TEXT
  - `regimen` TEXT (Contributivo / Subsidiado / Especial / No afiliado)
  - `tipo_sangre` TEXT (catálogo 8 grupos) · `alergias` TEXT
  - `via_llegada` TEXT (Ambulancia / Particular / Remisión — HU-E2-01 CA1)
  - `episodios_previos_urgencias` INTEGER
- **Relaciones:** 1—N `eventos_triaje`; 1—N `antecedentes`.
- **Auditoría:** `creado_en`, `actualizado_en`.
- **Soft delete:** no (trazabilidad clínica — los registros no se borran).
- **Estado:** ✅ implementada (HU-E2-01 — registro con detección de duplicados, validación teléfono/correo y auditoría).
- **Nota:** 11 campos decididos por `refinador` (RD-002).

### EventoTriaje (ENT-002 + RD-003 — registro dual)
- **Tabla / Colección:** `eventos_triaje`
- **Tipo de ID:** UUID v4 (texto)
- **Campos:**
  - `paciente_id` FK → `pacientes`
  - `estado` TEXT — máquina de 7 estados (HU-E2-06): Registrado → SignosVitales → EvaluacionClinica → ClasificacionIA → ValidacionProfesional → Cerrado (+ Reclasificado)
  - `nivel_sugerido_ia` TEXT (catálogo I–V, nullable si no se ejecutó inferencia)
  - `probabilidades_ia` TEXT (JSON `{nivel: prob}`)
  - `nivel_asignado_profesional` TEXT (catálogo I–V, obligatorio, nunca autocompletado)
  - `concordancia` BOOLEAN (calculado por el sistema)
  - `motivo_discrepancia` TEXT (obligatorio solo si concordancia = No)
  - `motivo_reclasificacion` TEXT · `evento_anterior_id` FK (reclasificación, HU-E2-07)
  - `version_modelo` TEXT (ref. ENT-009)
  - `algoritmo_modelo` TEXT · `fecha_inferencia` DATETIME · `tiempo_inferencia_ms` FLOAT
    · `confianza_ia` FLOAT · `explicacion_shap` TEXT (JSON top-5) — Épica E4 (HU-E4-01/02)
  - `inicio` DATETIME · `cierre` DATETIME
- **Relaciones:** N—1 `pacientes`; 1—1 `signos_vitales`, `motivos_consulta`, `evaluaciones_clinicas`; N—1 `modelos`; N—1 `usuarios`.
- **Auditoría:** transición de estado auditada (usuario + timestamp).
- **Soft delete:** no.
- **Estado:** ✅ implementada (HU-E2-06/07/08 + registro dual RD-003; E4: inferencia real con metadatos, latencia < 3 s y explicación SHAP persistidos).
- **Nota:** la reclasificación genera un evento separado (HU-E2-07 CA3).

### SignosVitales (ENT-003)
- **Tabla / Colección:** `signos_vitales`
- **Tipo de ID:** UUID v4 (texto)
- **Campos:** `evento_id` FK (único) · `temperatura` · `frecuencia_cardiaca` · `frecuencia_respiratoria` · `saturacion_o2` · `presion_sistolica` · `presion_diastolica` · `peso` · `talla` · `imc` (calculado).
- **Relaciones:** 1—1 `eventos_triaje`.
- **Estado:** ✅ implementada (HU-E2-04 — rangos fisiológicos, alertas y confirmación).

### MotivoConsulta (ENT-004)
- **Tabla / Colección:** `motivos_consulta`
- **Campos:** `evento_id` FK (único) · `codigo_cie10` · `descripcion_estructurada` · `texto_libre` (opcional, no bloquea).
- **Estado:** ✅ implementada (HU-E2-05 — doble captura).

### EvaluacionClinica (ENT-006 — supuesto, validar con negocio)
- **Tabla / Colección:** `evaluaciones_clinicas`
- **Campos:** `evento_id` FK (único) · `escala_dolor` · `glasgow` · `nivel_conciencia` · `observaciones`.
- **Estado:** ✅ implementada (HU-E2-05).

### Antecedentes (ENT-005)
- **Tabla / Colección:** `antecedentes`
- **Campos:** `paciente_id` FK (único) · `diabetes` · `hta` · `erc` · `embarazo` · `cancer` · `cardiopatias` · `epoc` · `cirugias` · `medicacion`.
- **Estado:** ✅ implementada (HU-E2-05 CA3 — autorreporte vía `HistoryConnector`/`MockHCE`, TT-E1-04).

### Discrepancia (ENT-007 — embebida en EventoTriaje)
- Sin tabla propia: `concordancia` + `motivo_discrepancia` viven en `eventos_triaje` (RD-003).

### TextoClinico (ENT-008)
- **Tabla / Colección:** `textos_clinicos`
- **Campos:** `evento_id` FK · `tipo` TEXT (admisión / narrativa) · `contenido` TEXT.
- **Relaciones:** N—1 `eventos_triaje`.

### Modelo (ENT-009)
- **Tabla / Colección:** `modelos`
- **Campos:** `version` TEXT (único) · `algoritmo` TEXT · `fecha_entrenamiento` DATE · `metricas_json` TEXT (JSON) · `ruta_artefacto` TEXT · `activo` BOOLEAN · `creado_en` DATETIME.
- **Relaciones:** 1—N `eventos_triaje`.
- **Estado:** ✅ implementada — registro automático idempotente (TT-E4-01) y gestión completa HU-E6-02: activación/rollback con un clic (la inferencia carga la versión activa), historial auditado y RBAC.

### Usuario / Rol (ENT-010/ENT-011 — supuesto)
- **Tabla / Colección:** `usuarios`, `roles`
- **Campos usuarios:** `correo` (único) · `password_hash` · `rol_id` FK · `activo` · `intentos_fallidos` · `bloqueado_hasta` · `token_recuperacion` · `token_expira`.
- **Enums rol:** `Medico`, `Enfermera`, `Administrador`, `Investigador`, `Auditor` (RF-014, HU-E1-02 CA1).
- **Estado:** ✅ implementada (HU-E1-01 login bcrypt + bloqueo; HU-E1-02 RBAC por pantalla; HU-E1-03 recuperación con token 15 min; HU-E1-04 cierre por inactividad 5 min).

### Auditoria (ENT-012 — supuesto)
- **Tabla / Colección:** `auditoria`
- **Campos:** `id` · `usuario_id` FK (nullable) · `accion` TEXT · `entidad` TEXT · `detalle` TEXT · `evento_id` FK (HU-E5-01 CA1) · `creado_en`.
- **Estado:** ✅ implementada — append-only (TT-E5-01: UPDATE/DELETE bloqueados vía eventos SQLAlchemy), decorador `@auditar`, consulta/exportación CSV/Excel/PDF (HU-E5-01) y generación de registro PDF auditada (HU-E5-02).

## Relaciones entre entidades

`Paciente 1—N EventoTriaje 1—1 SignosVitales / MotivoConsulta / EvaluacionClinica`, `EventoTriaje N—1 Modelo / Usuario`, `Paciente 1—N Antecedentes`, `Usuario N—1 Rol`, `EventoTriaje 1—N Auditoria`.
