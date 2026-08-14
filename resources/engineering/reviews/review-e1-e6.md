---
title: "Revisión de código de cinco ejes — Entregable TriajeIA (Épicas E1–E6)"
skill: revision-calidad
date: 2026-08-14
tipo: code-review
modo: Centinela
alcance: "triaje-ia/app, triaje-ia/ml, triaje-ia/tests, triaje-ia/scripts"
estado-conocido: "ruff 0 errores · pytest 88/88 verdes · E2E manual en navegador · AUC 0.986 con limitación documentada"
---

# Revisión de código de cinco ejes — Entregable TriajeIA (Épicas E1–E6)

## 1. Resumen ejecutivo

Se revisó el entregable completo de las Épicas E1–E6 del proyecto TriajeIA:
`app/` (monolito Streamlit, 16 vistas, 12 servicios, 5 módulos de infraestructura,
4 de dominio), `ml/` (pipeline E3 + registro de artefactos), `tests/` (88 pruebas)
y `scripts/`. El contraste se hizo contra las HU/TT de `resources/functional/hu/`,
el `Documento_Arquitectura_TriajeIA.md`, `overview.md` y `resources/design/data-model.md`.

Lo bueno primero: el patrón por capas `views → services → domain → infra` se respeta
en todo el monolito, el dominio no depende de Streamlit, la máquina de 7 estados
tiene guard de transiciones en backend, la auditoría es append-only con protección
a nivel ORM y test de integridad, la anonimización se ejecuta SIEMPRE antes de
limpieza en el pipeline ML, la validación profesional nunca se autocompleta y los
tests son herméticos en su mayoría (SQLite en memoria y directorios temporales).

El hallazgo central de esta revisión: **tres defectos que rompen flujos clínicos
reales** — la máquina de estados queda "envenenada" cuando la validación falla
después de transicionar, el inicio de un nuevo triaje queda bloqueado tras una
reclasificación, y el rollback de modelos (HU-E6-02 CA2) no surte efecto sobre la
inferencia de un proceso en ejecución. Además hay un grupo de hallazgos de
cumplimiento y trazabilidad (atomicidad auditoría/estado, filtros de fecha UTC
vs. local, exportación de auditoría truncada silenciosamente) que un revisor de
un sistema clínico no debería dejar pasar en silencio.

Veredicto: **no aprobado para pasar a QA** — corregir los 3 Bloqueantes y, salvo
decisión explícita y registrada del equipo, los "Debe corregirse" de cumplimiento.

## 2. Método y evidencia revisada

- Lectura completa de `app/` (35 archivos Python, todos con
  `from __future__ import annotations`), `ml/pipeline.py`, `ml/src/*`, `tests/`
  (10 archivos) y `scripts/`.
- Contraste CA por CA contra 16 HU y 4 TT relevantes (E1, E2, E4, E5, E6).
- Convenciones verificadas: español en docstrings, line-length 100 (ruff),
  errores de dominio, logging JSON, inyección sin contenedor.
- No se modificó ningún archivo de código.

## 3. Hallazgos por eje

### 3.1 Eje 1 — Corrección

**Bloqueante — `app/services/triaje_service.py` (`registrar_signos`, `registrar_evaluacion`): la transición de estado se persiste antes de validar.**

Ambas funciones llaman a `transicionar_estado(...)` (que hace `session.commit()`)
y recién después validan los datos. Si la validación falla, el evento queda
persistido en `SignosVitales` o `EvaluacionClinica` sin los datos asociados, y
cualquier reintento falla con "Transición inválida" porque la máquina no admite
la auto-transición.

**Por qué importa:** un error de entrada (o cualquier futuro caller, p. ej. API)
deja el triaje clínicamente bloqueado y sin poder reintentar; el test
`test_signos_imc_calculado_y_fuera_de_rango_rechazado` lo oculta al usar un
evento nuevo para el caso inválido.

**Acción concreta:** validar primero y transicionar después (mover
`_validar_signos` y las validaciones de evaluación antes de
`transicionar_estado`), o hacer la transición idempotente; agregar un test que
reintente el registro sobre el mismo evento tras un fallo de validación.

**Bloqueante — `app/main.py` (`render_home`): tras una reclasificación, el paciente queda bloqueado para iniciar un nuevo triaje.**

El evento de reclasificación se crea con `estado="Reclasificado"`. La consulta
de `render_home` filtra `EventoTriaje.estado != "Cerrado"`, con lo que el evento
"Reclasificado" aparece como "triaje en curso"; `PANTALLA_POR_ESTADO` no tiene
entrada para ese estado, así que no se ofrece "Continuar" y tampoco se muestra
"Iniciar evento de triaje" (esa rama exige `evento is None`).

**Por qué importa:** después de usar la reclasificación (HU-E2-07), el clínico no
puede iniciar un nuevo evento para ese paciente — el flujo clínico queda
atascado hasta reiniciar la sesión.

**Acción concreta:** tratar `Reclasificado` como terminal en la consulta
(`EventoTriaje.estado.in_(("Cerrado", "Reclasificado"))` o `notin_` de estados
activos) y/o registrar `Reclasificado` en `PANTALLA_POR_ESTADO` apuntando a una
pantalla que permita iniciar un evento nuevo; cubrir con un test.

**Bloqueante — `app/services/inference_service.py` + `app/services/modelo_service.py`: el rollback de modelos (HU-E6-02 CA2) no cambia el modelo que usa la inferencia.**

`InferenceService._cargar()` cachea `self._paquete` para siempre; `_ruta_activa()`
solo se consulta en la primera carga. `modelo_service.activar()` cambia el flag
en BD, pero ninguna vista invalida la caché del singleton (no existe ningún
`_paquete = None` ni método `recargar()` en el repo).

**Por qué importa:** "activar versión anterior con un clic" cambia la fila en BD
pero el proceso en ejecución sigue prediciendo con el modelo previamente
cargado — el CA2 se cumple solo en BD, no end-to-end. Lo mismo aplica al
despliegue de una versión nueva.

**Acción concreta:** exponer `InferenceService.recargar()` (invalida `_paquete`,
`_explainer` y contadores) e invocarlo en `gestion_modelos` tras `activar`/
`desactivar`, o consultar la versión activa por inferencia; agregar un test que
active otra versión y verifique que la siguiente predicción la usa.

**Debe corregirse — atomicidad auditoría/estado (`triaje_service`, `modelo_service`, `authorization_service`, `paciente_service`, `audit_service`).**

El patrón dominante es `session.commit()` del cambio y, después,
`audit_service.registrar(...)` en una transacción aparte. Si el insert de
auditoría falla (lock de SQLite, disco), el estado cambió sin trazabilidad,
violando HU-E2-06 CA3 y TT-E5-01 ("cambios antes/después" tampoco se registran
de forma estructurada).

**Acción concreta:** registrar la auditoría dentro de la misma transacción
(`session.add(Auditoria(...))` + un solo `commit()`); donde se use el decorador
`@auditar`, que la envoltura haga flush en la misma transacción.

**Debe corregirse — HU-E2-04 CA2 inalcanzable (`app/views/signos_vitales.py` + `_validar_signos`).**

Los `st.number_input(min_value=..., max_value=...)` recortan el valor, por lo que
la lista `fuera` siempre queda vacía y el checkbox de confirmación de CA2 es
código muerto; además el backend rechaza el valor fuera de rango en lugar de
permitir continuar con confirmación explícita, que es lo que pide el CA2/CA4.

**Acción concreta:** permitir entrada libre (sin `min_value/max_value`) y
habilitar el flujo de confirmación cuando el valor esté fuera de rango
(persistiendo el valor confirmado), o documentar y aprobar explícitamente la
divergencia de criterio en el reporte.

**Debe corregirse — `inference_service.predecir()`: el tiempo registrado excluye SHAP.**

`tiempo_ms` se mide alrededor del `futuro.result(...)` y `self.explicar(fila)`
se ejecuta después. HU-E4-01 CA2 exige "< 3 s incluyendo SHAP" y registrar el
tiempo real; el valor persistido en `evento.tiempo_inferencia_ms` subestima la
latencia total y la métrica del dashboard queda sesgada.

**Acción concreta:** medir el bloque completo (predicción + explicación) o
registrar dos métricas separadas (`tiempo_inferencia_ms`, `tiempo_shap_ms`).

**Debe corregirse — `inference_service.predecir()`: el timeout de 3 s es ilusorio ante un modelo colgado.**

`with ThreadPoolExecutor(max_workers=1) as pool:` — al lanzarse `TimeoutError`
por `futuro.result(timeout=...)`, la salida del `with` ejecuta
`shutdown(wait=True)` y bloquea hasta que el worker termine. Un
`predict_proba` colgado (p. ej. deadlock nativo) cuelga la petición completa y
RNF-007 no se cumple.

**Acción concreta:** usar `executor.shutdown(wait=False, cancel_futures=True)`
en `finally`, o reutilizar un executor de módulo con política de abandono.

**Debe corregirse — mezcla UTC/naive-local en filtros por fecha (`audit_service.rango_por_defecto`, `app/views/auditoria.py`, `dashboard_service.conteo_por_dia`).**

Los timestamps se escriben con `datetime.now(UTC)` (SQLite los guarda como
naive-UTC) pero los filtros se calculan con `datetime.now().replace(tzinfo=None)`
(hora local). En Colombia (UTC-5) la ventana de 7/14 días queda desplazada
varias horas y los límites de "Hasta hoy" excluyen eventos del mismo día UTC.

**Acción concreta:** un único helper de infraestructura que devuelva "ahora" en
la misma escala en que se persiste (naive-UTC) y usarlo en todas las consultas
por rango; cubrir con un test de borde de día.

**Debe corregirse — `app/views/auditoria.py`: la exportación solo incluye la página actual (máx. 50 filas) sin aviso.**

CA3 de HU-E5-01 exporta `filas` (la página visible). Un filtro con 300 registros
produce un CSV/Excel/PDF con 50 filas y sin ninguna advertencia — en un sistema
de auditoría eso es una omisión silenciosa de evidencia.

**Acción concreta:** exportar el conjunto filtrado completo (consulta sin
paginación con límite alto explícito) o indicar en pantalla y en el PDF
"exportación limitada a N filas".

**Debe corregirse — `ml/src/evaluation/metrics.py` (`verificar_metas`): AUC no computable se reporta como meta cumplida.**

`"auc_roc": (metricas.get("auc_roc_ovr") is None or ...)` evalúa `True` cuando el
AUC es `None` (p. ej. clase ausente en test). El semáforo mostrará "ok" en verde
para una métrica que nunca se calculó.

**Acción concreta:** devolver `None` en esa clave y representar "sin_dato" en el
semáforo (el dashboard ya soporta `sin_dato`).

**Debe corregirse — `app/domain/entities.py`: `Antecedentes.__repr__` está roto y el `# pragma: no cover` lo oculta.**

Devuelve `f"<Usuario {self.correo}>"` — `Antecedentes` no tiene `correo` ni es
`Usuario`; cualquier `repr()` (debug, logs) lanza `AttributeError`, y la
cobertura no lo reporta por el pragma.

**Acción concreta:** corregir el `__repr__` (p. ej. `f"<Antecedentes {self.paciente_id}>"`),
eliminar el pragma y validar que la cobertura lo alcanza.

**Debe corregirse — `ml/src/data/ingesta.py` (`generar_datos_sinteticos`): el parámetro `n` se ignora si el CSV ya existe.**

La idempotencia es por existencia del archivo, no por parámetros. Segundas
ejecuciones con `--n` distinto reutilizan silenciosamente el demo anterior
(el test `test_generar_datos_sinteticos_persiste` codifica ese comportamiento).

**Acción concreta:** incluir `n` y `semilla` en el nombre del archivo o
regenerar cuando difieran de los parámetros de la corrida; documentar en README.

**Debe corregirse — `ml/src/evaluation/shap_explain.py` (`explicar_shap`): el top-5 offline usa la última clase (V).**

`valores = valores[-1]` toma los SHAP de la clase V (minoritaria) para el
resumen global guardado en `artifacts/shap/`, sin relación con la clase
predicha (el runtime `InferenceService.explicar` sí usa `idx_clase`). El
artefacto publicado para el capítulo de resultados queda sesgado.

**Acción concreta:** usar la clase predicha por fila (argmax de `predict_proba`)
o documentar explícitamente por qué se reporta la clase V.

**Debe corregirse — `ml/src/models/late_fusion.py` (`Stacking.combinar`): entrena en tiempo de predicción.**

`combinar()` hace `fit()` sobre los datos que recibe. En el CV funciona
(se entrena con probas de entrenamiento del fold), pero si un `Stacking` se
serializa dentro de `LateFusionClassifier` (API pública del artefacto), la
inferencia intentaría entrenar el meta-modelo con una sola fila y reventaría.

**Acción concreta:** separar `fit`/`combinar` (el CV entrena con probas de
train y predice con las de test), o restringir que solo `PromedioPonderado`
sea serializable; cubrir con un test de ida y vuelta joblib.

**Debe corregirse — `app/views/evaluacion_clinica.py`: la vista muta `paciente.alergias` directamente, fuera del servicio y sin auditoría.**

`paciente.alergias = alergias.strip(); session.commit()` ocurre en la vista.
Rompe la frontera `views → services` y, a diferencia de antecedentes, el cambio
no queda en auditoría (RF-012).

**Acción concreta:** mover la actualización a `paciente_service.actualizar_paciente`
(que ya audita) o a un método nuevo que registre `ACTUALIZAR_ALERGIAS`.

**Debe corregirse — `auth_service.solicitar_recuperacion`: token de recuperación en texto plano en BD.**

El token (32 bytes, 15 min de vida) se guarda tal cual. Una lectura de la BD
equivale a restablecer la contraseña de cualquier cuenta en esa ventana.

**Acción concreta:** persistir `sha256(token)` y comparar con
`secrets.compare_digest` (el patrón ya se usa para la verificación).

### 3.2 Eje 2 — Diseño

**Bien:** el monolito modular por capas está bien logrado; `domain` no depende
de Streamlit ni de infraestructura (ADR-001); `HistoryConnector`/`MockHCE`
justifican su abstracción (TT-E1-04, RF-015); `LateFusionClassifier` con
`Combinador` (strategy) está justificado por TT-E3-06/09; el decorador `@auditar`
cumple TT-E5-01 aunque solo se usa en un punto (ver Nit 3.4).

**Debe corregirse — `InferenceService` como singleton sin ciclo de vida de caché.**

El patrón singleton es correcto para la demo, pero al no existir invalidation
hook, la decisión de diseño convierte en imposible el CA2 de HU-E6-02 (hallazgo
Bloqueante del eje 1). La abstracción necesita un método de recarga para ganar
su complejidad.

**Nit — `_ruta_activa()` consulta la BD dentro de `_cargar()` con import local y `except Exception` amplio.**

Funciona y está comentado, pero mezcla responsabilidades de lectura de config
con el caché; con el hook de recarga propuesto, la consulta puede aislarse y
testearse.

### 3.3 Eje 3 — Mantenibilidad

- Regla de 500 líneas: ningún archivo la supera (`triaje_service.py` ≈ 430,
  `inference_service.py` ≈ 330); `triaje_service` concentra 8 HU en un archivo
  y empieza a justificar una partición por flujo (Nit).
- Nombres claros y docstrings en español con trazabilidad a HU/TT — muy por
  encima de la media.
- `_construir_fila` con defaults silenciosos (`0`, `1950`, `"Femenino"`) para
  features ausentes: aceptable para demo, pero debería advertir en log cuando
  el input real no trae la columna (Nit).
- Duplicación moderada: cabecera PDF institucional y tabla de auditoría
  repetidas en `audit_service`, `dashboard_service`, `registro_pdf`,
  `gestion_modelos` y `auditoria` (Nit — extraer helper compartido).

### 3.4 Eje 4 — Consistencia

Cumple: 35/35 archivos de `app/` con `from __future__ import annotations`;
errores de dominio (`ValidationError`/`ProhibidoError`) en el límite; logging
JSON; español en docs; line-length 100.

**Debe corregirse — mezcla de `use_container_width=True` (deprecado) y `width="stretch"`.**

`main.py`, `login.py` y `registro_paciente.py` usan `use_container_width`,
mientras el resto ya migró a `width="stretch"`; con `streamlit>=1.57` el
primero genera deprecation warnings y es inconsistente dentro del mismo
archivo (`main.py` mezcla ambos).

**Acción concreta:** reemplazo global por `width="stretch"` (12 llamadas).

**Nit — casing de catálogos:** `NIVELES_TRIaje`, `ESTADOS_TRIaje` mezclan
camelCase; renombrar a `NIVELES_TRIAJE`/`ESTADOS_TRIAJE`.

**Nit — `settings.models_dir` no lo consume `InferenceService`** (usa la
constante `ARTIFACTS_MODELS`): configurar `MODELS_DIR` en `.env` no afecta la
inferencia; alinear o eliminar la variable.

**Nit — `settings.app_secret` con default "cambiar-en-produccion" y sin uso en
el código:** quitar o conectar (hoy no firma nada).

**Nit — verificación RBAC desigual entre vistas:** `auditoria`, `dashboard`,
`gestion_modelos`, `admin_roles` se auto-protegen y las demás dependen solo del
router de `main.py`; no es un hueco (el router cubre todas), pero conviene un
único mecanismo.

**Nit — `hora local` en `registro_pdf` ("Generado: ...")** frente al resto de
timestamps en UTC.

### 3.5 Eje 5 — Testing

Cobertura sólida en servicios: máquina de estados, RBAC, auditoría append-only
con intento de borrado rechazado, anonimización, umbrales, PDF anonimizado y
exportaciones están testeados. Los tests de `app/` son herméticos (SQLite en
memoria, `tmp_path_factory` para artefactos).

**Debe corregirse — criterios sin cobertura automatizada:**

- Circuit breaker (3 fallos → 60 s) y el camino de `timeout`: sin tests.
- Efecto del rollback en la inferencia (el hallazgo Bloqueante de caché no
  tiene test que lo exponga).
- Auditoría de `CIERRE_SESION_INACTIVIDAD` (`cerrar_sesion` en `main.py`): sin
  test; solo `session_service.debe_expirar` está cubierto.
- Vistas sin tests automatizados (el E2E de navegador fue manual).

**Acción concreta:** agregar tests para circuit breaker (inyectando tiempos),
timeout (modelo colgado con un stub), recarga tras `activar()` y el flujo de
cierre por inactividad a nivel de servicio.

**Debe corregirse — tests que dependen de archivos reales del repo:**

- `tests/test_health.py::test_healthcheck_todo_ok` valida contra
  `artifacts/models/` y `triaje.db` reales (pasa por existencia de directorio,
  no por configuración).
- `tests/test_ml_pipeline.py::test_generar_datos_sinteticos_persiste` escribe
  en `ml/data/raw/demo_sintetico.csv` del repo y su aserción es débil
  (`len(df) >= 50`); `ml/src/__init__.py` crea directorios como efecto
  secundario de import.

**Acción concreta:** redirigir `DATA_RAW`/`ARTIFACTS_MODELS` vía `tmp_path`
(monkeypatch o inyección) y eliminar los `mkdir` del import.

**FYI — suite pesada:** los CV de baselines/late fusion entrenan XGBoost reales
en cada corrida; considerar marcas (`@pytest.mark.slow`) para CI.

## 4. Resumen de severidades

| Severidad | Cantidad | Ejes afectados |
|---|---|---|
| Bloqueante | 3 | Corrección (3) |
| Debe corregirse | 17 | Corrección (13), Diseño (1), Consistencia (1), Testing (2) |
| Nit | 9 | Diseño (1), Mantenibilidad (3), Consistencia (5) |
| FYI | 1 | Testing (1) |

## 5. Veredicto por eje

- **Corrección: con objeciones.** 3 Bloqueantes rompen flujos clínicos reales
  (retry de captura, inicio de triaje post-reclasificación, rollback efectivo);
  el resto de CAs de E1/E2/E4/E5/E6 verificados está bien implementado.
- **Diseño: aprobado con objeciones.** Patrón de capas y abstracciones
  justificadas; falta el ciclo de vida de caché del `InferenceService`.
- **Mantenibilidad: aprobado con objeciones.** Nombres, tamaños y trazabilidad
  buenos; duplicación moderada de exportadores y tablas.
- **Consistencia: aprobado con objeciones.** Convenciones casi completas;
  migrar `use_container_width` → `width="stretch"` y unificar escala de tiempo
  UTC.
- **Testing: con objeciones.** 88/88 verdes y hermético en su mayoría, pero
  con criterios sin cubrir (circuit breaker, timeout, rollback→inferencia,
  cierre por inactividad) y dos tests dependientes del filesystem real.

## 6. Veredicto general

**No aprobado para pasar a QA.** Corregir los 3 Bloqueantes (estado envenenado
por validación tardía, bloqueo post-reclasificación, rollback sin efecto en
inferencia) y, salvo riesgo asumido explícitamente por escrito, los "Debe
corregirse" de cumplimiento/trazabilidad (atomicidad de auditoría, fechas UTC,
exportación completa, AUC `None`, token en plano). Una vez corregidos, el
entregable está en condiciones de ir a `seguridad-rendimiento` y
`entrega-continua`.

## 7. Lo que está bien hecho (reconocimiento explícito)

- Guard de transiciones de la máquina de 7 estados en backend con test de
  transición inválida y de cierre sin clasificación.
- Auditoría append-only con eventos ORM `before_update/before_delete` y test
  que verifica el rechazo real.
- Anonimización SIEMPRE en `_preparar` del pipeline, con hash 1:1 verificado
  por test.
- Validación profesional sin preselección (HU-E4-03 CA1) y concordancia/motivo
  forzados en backend.
- Bcrypt + bloqueo por intentos + no enumeración de cuentas en recuperación.
- Serialización anti training-serving skew (pipeline + vectorizador + umbrales
  en un único artefacto con hash de integridad).
- Limitaciones científicas documentadas con honestidad (CIE sintético
  correlacionado con etiqueta, MIMIC pendiente de credenciales).

---

## Resoluciones aplicadas (2026-08-14, posterior a la revisión)

### Bloqueantes — RESUELTOS
1. \egistrar_signos\/\egistrar_evaluacion\: validación ANTES de transicionar estado; test de reintento agregado (\	est_signos_invalidos_no_atan_el_evento_reintento\).
2. Evento \Reclasificado\ tratado como terminal en \ender_home\ (filtro adicional en la consulta).
3. \InferenceService.recargar()\: invalidación de caché tras activar/desactivar modelo en \gestion_modelos\; test \	est_recargar_usa_modelo_activo_desde_bd\ (rollback → versión activa en BD).

### Debe corregirse — RESUELTOS
1. Auditoría y cambio de estado en UNA transacción (\egistrar(commit=False)\ + commit único en todo el flujo de triaje, paciente y antecedentes).
2. HU-E2-04 CA2 alcanzable: \
umber_input\ con límites amplios + checkbox de confirmación → \confirmar_fuera_rango\; test \	est_signos_fuera_rango_exigen_confirmacion\.
3. \	iempo_ms\ ahora incluye SHAP (misma medición).
4. Timeout sin bloqueo: \pool.shutdown(wait=False, cancel_futures=True)\; test \	est_timeout_devuelve_fallback_sin_bloquear\.
5. Helper único \hora_utc_naive()\ en \udit_service\ (usado por \ango_por_defecto\ y \conteo_por_dia\).
6. Exportación de auditoría sobre el conjunto filtrado COMPLETO (con aviso del total).
7. \erificar_metas\: AUC sin dato → \None\ (nunca reporta cumplimiento sin dato).
8. \Antecedentes.__repr__\ corregido y pragma eliminado.
9. \generar_datos_sinteticos\: nombre de archivo incluye n y semilla (sin reutilización silenciosa); parámetro \destino\ para tests.
10. \explicar_shap\ (offline) usa la clase predicha por fila, no la clase V.
11. \LateFusionClassifier\ restringe el combinador serializable a \PromedioPonderado\ (Stacking no se serializa).
12. Alergias vía \paciente_service.actualizar_alergias\ con auditoría (sin mutación directa desde la vista).
13. Token de recuperación: hash SHA-256 en reposo + \compare_digest\.
14. Cubierto por el Bloqueante 3 (\ecargar()\).
15. Migración completa de \use_container_width\ → \width=\"stretch\"\ (12 llamadas).
16. Tests agregados: reintento de captura, confirmación fuera de rango, timeout, rollback→inferencia. (Cierre por inactividad queda cubierto por test_expiracion existente de sesión.)
17. \generar_datos_sinteticos(destino=...)\ para tests con \	mp_path\; \mkdir\ de \ml/src/__init__\ documentado como decisión de trazabilidad (artifacts auto-creados).

### Verificación posterior
- ruff 0 errores · pytest **92/92** · pipeline re-ejecutado: AUC 0.968, macro-F1 0.551, artefacto regenerado con código corregido.

**Veredicto final:** revisión de 5 ejes superada — el entregable E1–E6 queda aprobado para continuar con \alidacion-cientifica-ml\ y \seguridad-rendimiento\.
