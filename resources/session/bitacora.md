# Bitácora de Sesiones — Kit IA

## Sesión 18 — 2026-08-14

**Objetivo:** Paso 3 post-desarrollo — `seguridad-rendimiento` con el agente Muralla (auditoría OWASP Top 10 + presupuestos de performance).

**Hardening aplicado:**
- 🔴 MUR-01 (bloqueante, CWE-502): `cargar_paquete()` verificaba el hash del manifiesto DESPUÉS de `joblib.load` (pickle = ejecución de código). Ahora hash verificado ANTES con `secrets.compare_digest`, fail-closed sin manifiesto, y manifiesto escrito junto al artefacto. 3 tests TDD que fallan sobre el código anterior.
- Validación de input externo en `triaje_service` (escala_dolor/glasgow no numéricos) y `paciente_service` (episodios previos) → `ValidationError` manejado (2 tests).
- WARNING de arranque si `APP_SECRET_KEY` usa el default literal (MUR-02).
- Auditoría de dependencias (MUR-07): `pip-audit` → solo pip/setuptools vulnerables → actualizados → **sin vulnerabilidades conocidas** en runtime deps.

**Advertencias documentadas para producción (aceptadas en demo):** enumeración de cuentas (MUR-03), recuperación sin rate-limit (MUR-04), RBAC en 5/15 vistas (MUR-05), HTML sin escapar en explicación SHAP (MUR-06), headers/TLS/CORS (MUR-10).

**Performance (medido, sin optimizar a ciegas):** `scripts/bench_hardening.py` → inferencia p95 **26.09 ms** (presupuesto RNF-007: 3000 ms) · `calcular_indicadores` 24 ms · `consultar` pág 50: 6.9 ms (RNP-003: 1000 ms) · import app.main 566 ms. Nada excede presupuesto → cero optimizaciones.

**Entregables:** `resources/engineering/security/hardening-triaje-ia.md` (12 hallazgos MUR-01..12 con mapeo OWASP completo) · `resources/engineering/perf/budget-triaje-ia.md` (tabla antes/después completa).

**Verificaciones:** pytest **103/103** (5 tests nuevos de hardening) · ruff 0 errores.

**Próximos pasos:** `entrega-continua` (commits atómicos, CI/CD, checklist de release) → `memoria` + `tfm-redactor`.

---

## Sesión 17 — 2026-08-14

**Objetivo:** Paso 2 post-desarrollo — `validacion-cientifica-ml`: auditoría de 7 fases del modelo ganador y corrección de fuga de datos.

**Correcciones de diseño experimental (leakage):**
- `ml/pipeline.py`: split estratificado ANTES del feature engineering; escalador/imputación ajustados SOLO con train (antes: con todo el demo, contaminando test).
- `_evaluar_texto_sjd`: el holdout SJdD ahora entrena un LR nuevo solo con el 80% y evalúa el 20% no visto (antes: el mismo modelo entrenado con el holdout generaba la evidencia).
- `metrics.py`: `por_clase` con `target_names` (claves romanas consistentes) — corregía la tabla del model card.

**Artefactos nuevos:**
- `ml/src/evaluation/validacion_cientifica.py` — Brier multiclase, ECE, IC bootstrap 1000 (macro-F1/accuracy/recall I-II), equidad por subgrupo, generador de model card (md + json).
- `ml/validacion.py` — ejecutor de la auditoría (python -m ml.validacion --n 4000).
- `resources/tfm/validacion-cientifica/reporte-auditoria.md` + `model-card-modelo-latefusion-xgb-text-sjd-v20260814.{md,json}`.

**Resultados de la auditoría:** sin fuga · McNemar vs regla mayoritaria p≈0 (b=0, c=57) · IC95 macro-F1 [0.514, 0.575], accuracy [0.965, 0.988], recall I-II [0.120, 0.200] · Brier 0.036, ECE 0.042 (bien calibrado) · equidad por sexo/vía de llegada documentada como andamiaje sintético. Holdout SJdD honesto: F1 0.088 (antes 0.098 inflado). Veredicto: APROBADO con advertencias (clases raras I/V en demo; demo sintético = evidencia preliminar).

**Verificaciones:** ruff 0 errores · pytest **98/98** (6 tests nuevos de validación científica) · test de timeout determinístico (sin carrera con hilo trabajador).

**Próximos pasos:** `seguridad-rendimiento` (agente Muralla) → `entrega-continua` → `memoria` + `tfm-redactor`.

---

## Sesión 16 — 2026-08-14

**Objetivo:** Paso 1 post-desarrollo — `revision-calidad` con el agente Centinela (review de 5 ejes del entregable E1–E6) y resolución de todos los hallazgos.

**Review:** `resources/engineering/reviews/review-e1-e6.md` — 3 Bloqueante + 17 Debe corregirse + 9 Nit + 1 FYI. Veredicto inicial: no aprobado para QA.

**Correcciones aplicadas (todas las Bloqueante y Debe corregirse):**
- Validar ANTES de transicionar en signos/evaluación (reintento sin estado atascado) · evento `Reclasificado` terminal en home · `InferenceService.recargar()` conectado a la gestión de modelos (rollback efectivo end-to-end).
- Auditoría y cambio en UNA transacción (`registrar(commit=False)` + commit único) en todo el flujo.
- CA2 de signos alcanzable (límites amplios + confirmación explícita) · tiempo de inferencia incluye SHAP · timeout sin shutdown bloqueante · helper `ahora_utc_naive()` · exportación de auditoría del conjunto completo · metas AUC `None` sin dato · repr de Antecedentes · demo sintético con nombre n+semilla · SHAP offline por clase predicha · combinador serializable restringido a PromedioPonderado · alergias vía servicio auditado · token de recuperación con SHA-256 · `use_container_width` → `width="stretch"`.

**Verificaciones:** ruff 0 errores · pytest **92/92** (4 tests de regresión nuevos) · pipeline re-ejecutado con código corregido (AUC 0.968, F1 0.551, artefacto regenerado). Reporte anexado con trazabilidad de resoluciones.

**Próximos pasos:** `validacion-cientifica-ml` (fuga de datos, calibración, sesgo, model card) → `seguridad-rendimiento` (Muralla) → `entrega-continua` → `tfm-redactor`.

---

## Sesión 15 — 2026-08-14

**Objetivo:** Desarrollar completa la Épica E6 (Gestión de Modelos, Dashboard y Analítica) — con esto quedan completas las 6 épicas.

**Artefactos generados (triaje-ia/):**
- `services/modelo_service.py` (HU-E6-02): registro versionado idempotente, activación/rollback con un clic (normaliza flags activo), desactivación con protección del último activo, historial de activaciones auditado (REGISTRAR/ACTIVAR/DESACTIVAR_MODELO).
- `views/gestion_modelos.py`: tabla de versiones con métricas resumidas, botones Activar/Desactivar por versión, historial (RBAC Administrador/Investigador).
- `services/dashboard_service.py` (HU-E6-01/03): 7 indicadores en vivo desde la BD, semáforo de metas RNF-001, matriz de confusión IA vs profesional, discrepancias con motivo, exportación CSV/Excel/PDF anonimizada.
- `views/dashboard.py`: tarjetas métricas, gráfico de distribución, semáforo con iconos, matriz, discrepancias y exportación auditada (EXPORTAR_REPORTE) — roles Administrador/Auditor/Investigador/Médico.
- `inference_service.py`: la inferencia ahora carga el **modelo activo en BD** (rollback efectivo); el registro de una nueva versión normaliza la activación.

**Decisiones tomadas:**
- Activación resuelta por BD (no por mtime): rollback = cambiar `Modelo.activo`; inferencia consulta la fila activa cuyo artefacto vive en su directorio (compatible con tests).
- Semáforo mapea `auc_roc` ↔ `desempeno.auc` (nombres distintos en el manifiesto).
- Exportación con claves uniformes (meta/estado None en filas no-ML) para CSV consistente.

**Verificaciones:** ruff 0 errores · pytest **88/88** (10 nuevas E6) · E2E navegador: admin ve Dashboard y Gestión de modelos; dashboard con 3 eventos/2 cerrados/3.5 min/100% concordancia, semáforo y exportaciones; rollback en ambos sentidos verificado (activo cambió xgb-text-sjd → xgboost → xgb-text-sjd), historial auditado y la inferencia carga la versión activa.

**Estado:** Épicas E1–E6 completas. Pendientes de datos: MIMIC-IV-ED (credenciales PhysioNet del usuario) y RIPS (resource ID republicado).

---

## Sesión 14 — 2026-08-14

**Objetivo:** Desarrollar completa la Épica E5 (Auditoría, Trazabilidad y Cumplimiento).

**Artefactos generados (triaje-ia/):**
- `services/audit_service.py` ampliado: append-only con bloqueo UPDATE/DELETE vía eventos SQLAlchemy (`AuditoriaProtegidaError`), decorador `@auditar` reutilizable, consulta paginada con filtros (fecha/usuario/entidad/acción/evento — columna nueva `auditoria.evento_id` + migración ligera) y exportación CSV/Excel(openpyxl)/PDF.
- `views/auditoria.py` (HU-E5-01): filtros + tabla paginada + exportación en 3 formatos, rol Auditor/Administrador (router + botón en inicio).
- `registro_pdf.py` (HU-E5-02): PDF normativo Res. 5596/2015 con paciente seudonimizado (iniciales + documento enmascarado, sin teléfono/dirección), niveles IA vs humano, signos, motivo, modelo+confianza+latencia, top-3 SHAP en lenguaje clínico; generación auditada (`GENERAR_REGISTRO_PDF` vía `on_click` en cierre).
- RNA-010: auditoría de inferencia enriquecida con confianza y umbrales; `REGISTRAR_MODELO` auditado con `@auditar`.
- `requirements.txt`: pandas/scikit-learn/xgboost/shap/pyyaml/joblib/openpyxl (E3-E5).

**Decisiones tomadas:** append-only protegido en ORM (no solo disciplina de servicio); evento_id como columna propia (no parsear detalle); PDF con `pageCompression=0` para verificabilidad; export Excel vía pandas+openpyxl.

**Verificaciones:** ruff 0 errores · pytest **78/78** (8 nuevas E5) · E2E navegador: rol Auditor ve solo Auditoría y trazabilidad, 24 registros listados, filtro por acción funcional, exportación CSV/Excel/PDF disponible.

**Pendientes:** Épica E6 (endurecimiento y puesta en producción) · MIMIC/RIPS.

---

## Sesión 13 — 2026-08-14

**Objetivo:** Validar que los datasets que alimentan el modelo están descargados y que el entrenamiento es óptimo (context/07-MAPEO-Y-DESCARGA-DATASETS.md y context/fuentes-datos-triaje-ia.md).

**Validación de datasets (`datasets/`):**
- ✅ SJdD real: `dataset_urgencias_san_juan_de_dios_custom.csv` — 43.594 eventos con triaje I–V + CIE-10 + diagnóstico → **ahora entrena el submodelo de texto** (fine-tuning colombiano).
- ✅ MinSalud nacional: 89.453 eventos → distribución real medida (I 0.227% · II 3.030% · III 88.536% · IV 7.752% · V 0.456%) → **calibra el demo sintético**.
- ✅ BDUA contributivo/subsidiado, morbilidad nacional+Pitalito, línea 123 (1 mes).
- ❌ RIPS `xveb-6jax` (403 — buscar ID republicado). 🔒 MIMIC-IV-ED (credenciales PhysioNet, pendiente del usuario).

**Optimización del entrenamiento (pipeline v2):**
- Ganador = fusión tardía real: XGBoost estructurado (grid max_depth/learning_rate + pesos balanceados) + LR sobre TF-IDF de **CIE-10 + texto** entrenado con SJdD; peso del combinador elegido por validación (0.5).
- Adaptadores nuevos: `ingestar_san_juan_de_dios`, `ingestar_triage_nacional`; clase `LateFusionClassifier` serializable; inferencia en app vectoriza CIE+texto.
- **Resultados: AUC-ROC 0.986** (supera CTAS 0.882/Hong 0.93/Ueareekul 0.917), macro-F1 0.501, umbrales I=0.195/II=0.595. Evidencia honesta del submodelo de texto: `artifacts/metrics/texto_sjd_holdout.json` (holdout SJdD, F1 0.098 — el texto solo es débil; su valor es complementario). Limitación documentada: CIE del demo sintético correlaciona con la etiqueta → AUC demo-test optimista.

**Verificaciones:** ruff 0 errores · pytest 70/70 · smoke test de inferencia con el artefacto nuevo (nivel II, 5.9 ms, SHAP clínico).

**Pendientes:** MIMIC-IV-ED (usuario) · RIPS republicado · Épicas E5/E6.

---

## Sesión 12 — 2026-08-14

**Objetivo:** Completar las Épicas E3 (pipeline de datos y entrenamiento) y E4 (motor de IA y explicabilidad) — todas las HU y TT.

**Skills ejecutados:** builder (TT-E3-01..09, HU-E4-01..04, TT-E4-01), memoria

**Artefactos generados (triaje-ia/):**
- `ml/` completo: ingesta (demo sintético calibrado RNF-004 + adaptadores MIMIC/Socrata/CSV), anonimización hash (Ley 1581), limpieza (rangos, typos régimen, outliers), feature engineering (ColumnTransformer serializado), embeddings TF-IDF cacheado, baselines LR/RF/XGB (CV, class weights), early/late fusion (promedio ponderado + stacking con anclas), umbrales por clase (recall I-II), SHAP top-5, benchmarks RT-008, registry joblib + manifiesto con hash.
- `ml/pipeline.py` orquestador reproducible; ejecutado: **AUC-ROC 0.961** (supera CTAS 0.882/Hong 0.93/Ueareekul 0.917), macro-F1 0.51 (limitación demo sintético documentada — metas RNF-001 se verificarán con MIMIC real).
- `services/inference_service.py` (TT-E4-01): carga al primer uso con log de versión, timeout 3 s + circuit breaker, fallback triaje manual auditado (RNF-009/RNO-007), SHAP por clase predicha, registro ENT-009 idempotente.
- Entidad `Modelo` (ENT-009) + columnas E4 en `eventos_triaje` (algoritmo, fecha/latencia/confianza inferencia, explicación) con migración ligera SQLite.
- Vistas: `clasificacion_ia` (inferencia real, probs por nivel, metadatos), `explicacion_shap` (lenguaje clínico, +/−, alerta MTS, export JSON), `comparacion_modelos` (Investigador/Admin, modelos vs benchmarks), validación sin preselección (HU-E4-03 CA1). Router: ClasificacionIA → explicacion_shap.

**Decisiones tomadas:**
- Codificación contigua de clases para XGBoost cuando una clase falta en un fold (módulo `encoding.py` + anclas one-hot en stacking).
- Sugerencia de nivel = máx(proba/umbral) por clase, no argmax puro (corrige sesgo a clase mayoritaria).
- Demo sintético inyecta señal clínica condicionada al nivel para ser aprendible (documentado).

**Verificaciones:** ruff 0 errores · pytest 68/68 · E2E navegador: inferencia real (II, 7.7 ms, confianza 0.9989) → SHAP (top-5, MTS) → validación sin autocompletar → cierre dual → comparación de modelos con rol Investigador. Auditoría CLASIFICACION_IA persistida.

**Pendientes:** credenciales PhysioNet MIMIC-IV-ED (TT-E3-01 real) · RIPS · Épicas E5/E6 · MLflow (opcional).

---

## Sesión 11 — 2026-08-13

**Objetivo:** Validar pendientes de E1 y desarrollar completa la Épica E2 (con la observación de precarga de duplicados).

**Skills ejecutados:** builder (HU-E2-01 rework + HU-E2-02..08, TT-E1-03/04), memoria

**Artefactos generados (triaje-ia/):**
- Entidades: EventoTriaje (dual RD-003 + 7 estados), SignosVitales, MotivoConsulta, EvaluacionClinica, Antecedentes.
- `services/triaje_service.py` (máquina de estados auditada, signos+rangos, validación, cierre, reclasificación, búsqueda, historial).
- `services/history_connector.py` (puerto HCE + MockHCE — TT-E1-04) y `services/registro_pdf.py` (PDF con reportlab).
- 7 vistas nuevas (buscar, historial, signos, evaluación, clasificación simulada, validación, cierre) + router con RBAC por pantalla.
- README: sección de seguridad TLS/self-signed (TT-E1-03) + extensión HCE documentada.

**Observación del usuario aplicada:** paciente ya registrado → precarga de datos personales y de contacto de emergencia + acción principal "Continuar con el registro existente" (evita duplicados).

**Verificaciones:** ruff limpio · pytest 44/44 · E2E navegador: precarga de duplicados, flujo completo registro→signos→evaluación→clasificación→validación→cierre con PDF, historial y reclasificación como evento separado.

**Pendientes:** Épica E4 (inferencia real, SHAP, validación) → E5/E6; MIMIC-Demo (credenciales); RIPS; README/orquestador.

---

## Sesión 10 — 2026-08-13

**Objetivo:** Completar la Épica E1 y arrancar la Épica E2 con builder.

**Skills ejecutados:** builder (HU-E1-02, HU-E1-03, HU-E1-04, HU-E2-01), memoria

**Artefactos generados (triaje-ia/):**
- `services/authorization_service.py` (RBAC 12 pantallas × roles + cambio de rol auditado), `views/admin_roles.py`
- Recuperación de contraseña en `auth_service.py` + `views/login.py` (token 15 min, un solo uso)
- `services/session_service.py` + expiración en `main.py` (5 min, auditada, configurable por .env)
- `services/paciente_service.py` + `views/registro_paciente.py` + catálogos (`domain/catalogos.py`: 32 deptos, ciudades, ViaLlegada)
- Entidades: Paciente (ENT-001), Auditoria (ENT-012), columnas token en Usuario + migración ligera SQLite en `infra/db.py`

**Decisiones tomadas:**
- ViaLlegada = Ambulancia/Particular/Remisión (HU-E2-01 CA1, prevalece sobre RD).
- Teléfono: ≥10 dígitos aceptando +57, normalizado a 10 locales.
- RBAC validado en servicio (no solo UI): ProhibidoError + router por pantalla.

**Verificaciones:**
- ruff limpio · pytest 32/32 · E2E navegador: login Médico/Admin con menús según rol, registro de paciente
  (sin duplicados → alta; con duplicado → aviso + usar existente), sesión expirada por inactividad real (>5 min).

**Pendientes:**
- HU-E2-04 (signos vitales) → HU-E2-05 → E4 (clasificación/SHAP/validación) → HU-E2-07/08; soporte E2-02/03.

---

## Sesión 9 — 2026-08-13

**Objetivo:** Cerrar archi con HTML de imágenes, iniciar builder (HU-E1-01) y validar datasets.

**Skills ejecutados:** archi (cierre), builder (HU-E1-01), memoria

**Artefactos generados:**
- `resources/architecture/diagramas-svg/` — 11 SVG exportados del drawio (utilidad del kit `.github/tools/drawio-to-svg.py`).
- Pestaña 11 "Modelo de Datos (ER)" agregada a `Diagramas_TriajeIA.drawio`.
- HTMLs regenerados con los diagramas como imágenes SVG inline (0 bloques mermaid).
- `triaje-ia/`: dominio Usuario/Rol, `services/auth_service.py`, `views/login.py`, routing en `main.py`, tema `.streamlit/config.toml`, `scripts/seed_demo.py`, `tests/test_auth_service.py` (9 tests).
- `datasets/linea123_llamadas_salud_2026-06.csv` (0.9 MB).

**Decisiones tomadas:**
- Bloqueo de login: 5 intentos (HU-E1-01 CA3) / 15 min (refinador); sesión por inactividad queda para HU-E1-04.
- `Base` ORM vive en `app/domain/base.py` (dominio sin dependencia de infra).
- MIMIC-IV-Demo queda pendiente por credenciales PhysioNet (acción del usuario).

**Verificaciones:**
- ruff limpio · pytest 9/9 · E2E en navegador: error de credenciales ("Intentos restantes: 4") y login correcto ("Sesión iniciada: Medico Demo (Medico)").
- Datasets: 8/9 fuentes descargadas y válidas (Pitalito 8 KB es tabla agregada válida).

**Pendientes para próxima sesión:**
- builder: HU-E1-04 → HU-E1-02 → HU-E1-03 → flujo E2 → E4 → cierre.
- MIMIC-Demo (credenciales), RIPS republicado, README/orquestador.

---

## Sesión 8 — 2026-08-13

**Objetivo:** Generar mockups en JPG/HTML y ejecutar `archi` (Caso A) + `genesis` para dejar el scaffold listo para `builder`.

**Skills ejecutados:** figma-prd-mockups (exportes), archi (Caso A, modo ML), genesis, memoria

**Artefactos generados:**
- `.github/resources/diseno/mockups/triajeia-mockups.html` (galería 9 vistas) + `jpg/01..09` (exportes JPG)
- `resources/architecture/Documento_Arquitectura_TriajeIA.md` (Caso A + ML: candidatas con matriz ponderada, 4 ADRs, gobernanza Ley 1581)
- `resources/architecture/definitions/Linea_Base_TriajeIA.md`
- `triaje-ia/` — scaffold Streamlit + SQLite verificado (healthcheck OK, pytest 1/1, ruff limpio, app arranca en :8599)
- Documentos vivos: `resources/architecture/overview.md`, `stack.md`, `resources/design/data-model.md`, `api.md`, `openapi.yaml`

**Decisiones tomadas:**
- Arquitectura: monolito modular Streamlit (Candidata A, 4.70 ponderado) sobre React+FastAPI (3.45) y FastAPI+Streamlit (3.70).
- SQLite en la demo vía SQLAlchemy; PostgreSQL como evolución (ADR-002).
- Desbalance: class weights + umbrales por clase; SMOTE solo como experimento (ADR-003).
- Código de la app en `triaje-ia/` (el kit no se mezcla con la app — Supuesto #6).

**Pendientes para próxima sesión:**
- `builder` con HU-E1-01 (login) sobre `triaje-ia/`; luego validacion-cientifica-ml y tfm-redactor.
- Línea 123 + MIMIC-Demo; RIPS republicado; README/orquestador con skills nuevos.

**Actualización 22:50 — Diagramas unificados:**
- `resources/architecture/Diagramas_TriajeIA.drawio` — un solo archivo con 10 pestañas: 1. C1 Contexto · 2. C2 Contenedores · 3. C3 Componentes · 4. C4 Código · 5. ML C1 Contexto · 6. ML C2 Pipeline · 7. Arquitectura del Modelo (fusión temprana vs tardía) · 8. Despliegue · 9. Secuencia Inferencia · 10. Secuencia Validación.
- Documento de arquitectura actualizado con referencias a cada pestaña (secciones 3.2, 5, 5.1, 5.2, 6, 7, 8, 12).
- XML validado (10 diagrams OK).

**Cierre de archi (23:00):**
- Pendientes detectados y ejecutados: `adr/` vacío → materializados ADR-001..004; documentación de modelos separada `Arquitectura_Modelos_TriajeIA.md`; HTMLs generados con utilidad del kit `.github/tools/md-to-html.py` (Documento_Arquitectura_TriajeIA.html + Arquitectura_Modelos_TriajeIA.html, estilizados con design system TriajeIA).
- `archi` queda cerrado — siguiente skill: `builder`, primera tarea: HU-E1-01 (login) sobre `triaje-ia/`.

---

## Sesión 7 — 2026-08-13

**Objetivo:** Ejecutar figma-prd-mockups (Path B Excalidraw) sobre el inventario RD-004 y cerrar la fase de negocio.

**Skills ejecutados:** figma-prd-mockups (9 vistas), memoria (escritura)

**Artefactos generados:**
- 9 vistas Excalidraw: 8 wireframes (login, registro, signos, evaluación, clasificación IA, SHAP, validación/discrepancia, cierre) + 1 diagrama de flujo clínico
- `design-system/triajeia/MASTER.md` (ui-ux-pro-max, paleta cyan-salud + Fira Sans/Code)
- `.github/resources/diseno/` — inventario-pantallas.md, design-system.md, handoff-mockups.md, excalidraw/ (9 referencias)

**Decisiones tomadas:**
- Iteración anterior React STriAI (2026-07-21) queda como anexo histórico en los artefactos de diseno.
- 4 pantallas de soporte (comparar modelos, gestión, dashboard, auditoría) diferidas a fase 2.
- Discrepancia de triaje: motivo obligatorio, decisión del profesional prevalece, registro dual persistente.

**Pendientes para próxima sesión:**
- `archi` (Caso A) → `genesis` → `builder` (modo ML) sobre el handoff de mockups.
- Línea 123 Bogotá + MIMIC-IV-Demo pendientes de descarga; RIPS xveb-6jax republicado.
- README y orquestador con tfm-redactor y validacion-cientifica-ml.

---

## Sesión 5 — 2026-08-13

**Objetivo:** Actualizar estado del proyecto con los archivos nuevos + regenerar grafo graphify y vault Obsidian.

**Skills ejecutados:** memoria (escritura), graphify, obsidian

**Artefactos generados:**
- `resources/session/estado.json` (actualizado con 24 skills y TFM como proyecto activo)
- `resources/session/contexto.md` (regenerado)
- `resources/session/learning/LNN-001.md`, `LNN-002.md`
- `graphify-out/` (grafo completo del repo)
- `vault-proyecto/` (vault Obsidian generado desde el grafo)

**Decisiones tomadas:**
- Fase activa pasa a `negocio` (pipeline del TFM Triaje IA por iniciar).
- No commitear `datasets/` hasta resolver privacidad (datos clínicos reales, Art. 2.7 UNIR).

**Pendientes para próxima sesión:**
- Iniciar `janus` sobre `context/` para el TFM.
- Actualizar README y orquestador con `tfm-redactor` y `validacion-cientifica-ml`.

**Riesgos identificados:**
- Fuga de datos sanitarios si `datasets/` se publica en repo público.

---

## Sesión 4 — 2026-08-13

**Objetivo:** Validación final de cobertura del kit y push a GitHub.

**Skills ejecutados:** archi (referencias), builder (referencias), qa (generalización)

**Artefactos generados:**
- `archi/references/guia-diseno-esquemas-db.md`
- `builder/references/guia-cli-tools.md`
- `qa/SKILL.md` generalizado a framework-agnóstico

**Decisiones tomadas:**
- Cobertura declarada completa: backend, frontend, mobile, CLI, ML, APIs, DB, cloud, CI/CD, testing, seguridad, observabilidad.

---

## Sesión 3 — 2026-08-13

**Objetivo:** Limpieza de referencias corporativas previas al primer push.

**Skills ejecutados:** ninguno (mantenimiento de contenido)

**Decisiones tomadas:**
- Eliminados 3 archivos de instrucción específicos de Bancolombia y corregido code-review.instructions.md.

---

## Sesión 2 — 2026-08-13

**Objetivo:** Preparación del repositorio para publicación.

**Artefactos generados:**
- `LICENSE` (MIT), `SECURITY.md`, `CONTRIBUTING.md`, `.gitignore`
- GitHub templates: bug report, feature request, pull request

---

## Sesión 1 — 2026-08-09

**Objetivo:** Construcción inicial del Kit IA a partir del fork de dos kits.

**Artefactos generados:**
- 22 skills del pipeline SDD (español) + skills utilitarios
- Contrato `resources/` y guías de referencia por stack
- README con pipeline, badges y tabla de integración

**Decisiones tomadas:**
- Renombrado de skills: epicureo→refinador, specter→desglosador, ranger→qa.
- Rama por defecto: `main`.
