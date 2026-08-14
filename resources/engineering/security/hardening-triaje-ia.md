---
title: "Hardening TriajeIA — auditoría de seguridad (OWASP) y fronteras de confianza"
skill: seguridad-rendimiento
date: 2026-08-14
proyecto: TriajeIA
modulo: app (auth, inferencia, auditoría, triaje), ml/src/registry, infra
---

# Hardening TriajeIA — auditoría de seguridad (OWASP) y fronteras de confianza

Auditoría de hardening ejecutada sobre el módulo de aplicación del TFM
TriajeIA (sistema de triaje multimodal IA, demo académica con datos
sintéticos, SQLite local, Streamlit). El criterio de severidad distingue
riesgo real en producción de riesgo aceptable para una demo académica local:

- **Bloqueante** — se explota con datos/artefactos presentes en el repo; se
  corrige con prueba.
- **Advertencia** — riesgo real en producción, no explotable en la demo tal
  como está desplegada; se documenta con recomendación concreta.
- **Informativo** — decisión o configuración a revisar; sin acción de código
  en esta auditoría.

## Clasificación de fronteras de confianza

| Frontera | Superficie | Nivel de confianza | Validación aplicada |
|---|---|---|---|
| Externa (1) | Formularios de Streamlit (`login.py`, `registro_paciente.py`, `signos_vitales.py`, `evaluacion_clinica.py`, `buscar_paciente.py`) | No confiable | Allowlist de catálogos, rangos fisiológicos, formato correo/teléfono, longitud mínima de contraseña |
| Externa (1) | Artefacto `.joblib` en `artifacts/models/` | No confiable (pickle = código ejecutable) | Hash sha256 del manifiesto verificado **antes** de `joblib.load` (corregido en esta auditoría) |
| Interna (2) | Servicios propios (`triaje_service` ↔ `audit_service` ↔ `inference_service`) | Contrato de API validado | Máquina de estados, `commit=False` transaccional, decorador `@auditar` |
| Interna (2) | BD → consultas | Contrato ORM | SQLAlchemy parametrizado en todo el módulo |
| Dato confiable (3) | Columnas de migración ligera en `db.py`, mapeos `NOMBRES_CLINICOS` | Post-validación / constantes del repo | Sin revalidación (evita ruido); revisado y sin hallazgo |

## Resumen de hallazgos

| ID | Severidad | Área | Hallazgo | Estado |
|---|---|---|---|---|
| MUR-01 | 🔴 Bloqueante | A08:2021 / CWE-502 | `joblib.load` (pickle) ejecutado **antes** de verificar el hash del manifiesto; manifiesto escrito en directorio distinto al artefacto cuando el destino era otro | Resuelto con pruebas |
| MUR-02 | 🟠 Advertencia | A05:2021 | `APP_SECRET_KEY` con default literal `cambiar-en-produccion` (además, variable sin uso real) | Mitigado: aviso WARNING en arranque. Pendiente producción: fallar sin clave aleatoria |
| MUR-03 | 🟠 Advertencia | A07:2021 | Enumeración de cuentas: respuesta distinta (detalle "Intentos restantes: N") y sin verificación dummy de hash para correos inexistentes | Aceptado para demo (UX intencional, cubierto por test). Recomendación documentada |
| MUR-04 | 🟠 Advertencia | A07:2021 | `solicitar_recuperacion()` sin rate-limit por correo/usuario (en producción: email bombing) | Documentado con recomendación |
| MUR-05 | 🟠 Advertencia | A01:2021 | RBAC validado en el router y solo en 5 de 15 vistas (defensa en profundidad incompleta, sin bypass identificado) | Documentado con recomendación |
| MUR-06 | 🟠 Advertencia | A03:2021 | `st.markdown(..., unsafe_allow_html=True)` con datos interpolados en `explicacion_shap.py` (origen: nombres de features del pipeline, no input directo) | Documentado con recomendación |
| MUR-07 | 🟡 Informativo | A06:2021 | Auditoría de CVEs (`pip-audit`) ejecutada: solo `pip`/`setuptools` del venv vulnerables; actualizados y re-auditados → **sin vulnerabilidades conocidas** | Resuelto (2026-08-14) |
| MUR-08 | 🟡 Informativo | A02:2021 | bcrypt (salt), token de recuperación SHA-256 + `compare_digest`, un solo uso, 15 min — verificado correcto | Sin acción |
| MUR-09 | 🟡 Informativo | A09:2021 | Auditoría append-only con triggers ORM; logs JSON sin contraseñas ni tokens; `exc_info` con stack trace en logs (no hacia el usuario) | Sin acción |
| MUR-10 | 🟡 Informativo | A05:2021 | Sin headers de seguridad / TLS / CORS: app local sin API HTTP; pendientes para despliegue real | Documentado para producción |
| MUR-11 | 🟡 Informativo | Gestión de secretos | Sin claves hardcodeadas en `app/`, `ml/`, `scripts/`, `resources/`; `.env` gitignored; `.env.example` solo placeholders; seed de demo con `Demo123!` documentado | Sin acción |
| MUR-12 | 🟡 Informativo | A01:2021 / IDOR | RBAC por pantalla sobre pool compartido de pacientes (modelo RD-004); sin cheques de propiedad por usuario | Aceptado para demo; anotado para producción |

## Detalle de hallazgos

### MUR-01 (bloqueante, resuelto) — deserialización de pickle antes de verificar integridad

`ml/src/registry.py::cargar_paquete()` ejecutaba `joblib.load(ruta)` y solo
después comparaba el `sha256_16` del manifiesto. `joblib.load` deserializa
pickle, y pickle ejecuta código arbitrario en el proceso: un artefacto
malicioso o manipulado en `artifacts/models/` se ejecuta aunque el hash no
coincida (la verificación posterior no protege nada). Además,
`serializar_paquete()` escribía el manifiesto siempre en `ARTIFACTS_MODELS`,
incluso cuando el artefacto iba a otro directorio — la verificación de hash
quedaba ciega en esos casos.

Corrección aplicada:

- Hash del manifiesto verificado **antes** de `joblib.load`, con
  `secrets.compare_digest`.
- Fail-closed: sin manifiesto junto al artefacto, o manifiesto sin hash, la
  carga se rechaza con `ValueError` (el fallback manual de `InferenceService`
  absorbe el error sin romper el flujo clínico).
- El manifiesto se escribe siempre junto al artefacto (mismo directorio y
  nombre base).
- `ml/validacion.py::_cargar_ganador()` solo considera artefactos con
  manifiesto.

Pruebas (fallan sobre el código anterior):

- `test_cargar_paquete_verifica_hash_antes_de_deserializar` — con hash
  inválido, `joblib.load` no se invoca (se fija el orden de verificación).
- `test_cargar_paquete_rechaza_artefacto_sin_manifiesto` — fail-closed.
- `test_serializar_paquete_escribe_manifiesto_junto_al_artefacto` — el
  manifiesto viaja con el artefacto.

### MUR-02 (advertencia, mitigado) — APP_SECRET_KEY con default literal

`app/infra/config.py:25` define `app_secret` con fallback literal
`cambiar-en-produccion`; la variable no se consume en ningún punto del código
(configuración muerta con default débil). Mitigación aplicada: `main.py::bootstrap()`
emite un WARNING en el log de arranque si el valor por defecto está en uso.

Recomendación para producción: eliminar el default o fallar al arrancar si no
se define `APP_SECRET_KEY` con un valor aleatorio (p. ej.
`secrets.token_urlsafe(32)`), y usarla de verdad (firma de sesión) si se
adopta un mecanismo de sesión con cookies.

### MUR-03 (advertencia) — enumeración de cuentas en login

`auth_service.autenticar()` distingue entre correo inexistente (mensaje
genérico, sin verificación bcrypt) y contraseña incorrecta (detalle
`Intentos restantes: N` y costo bcrypt real). La diferencia de mensaje y de
tiempo permite enumerar correos institucionales.

Aceptado para la demo: el detalle es UX intencional de la HU-E1-01 y está
cubierto por `test_password_incorrecta_incrementa_intentos`. Recomendación
para producción: verificar un hash dummy cuando el correo no exista (tiempos
constantes), devolver siempre el mismo mensaje y mover el conteo de intentos
al log/auditoría, no a la respuesta.

### MUR-04 (advertencia) — recuperación de contraseña sin rate-limit

`solicitar_recuperacion()` no limita llamadas por correo, usuario o sesión.
En la demo no envía correo (el token se muestra en pantalla simulando email),
así que el abuso es inerte. En producción (SMTP real) permitiría email
bombing y una vía de DoS. Recomendación: límite de 1 solicitud cada 5 min por
cuenta (con `token_expira` ya persistido se puede derivar), y límite global
por IP en el reverse proxy.

### MUR-05 (advertencia) — RBAC sin doble verificación en todas las vistas

La verificación de rol vive en el router (`main.py` valida `pantalla` antes
del dispatch) y se repite solo en `auditoria`, `dashboard`, `gestion_modelos`
y `admin_roles`. El resto de vistas depende únicamente del router. No se
identificó bypass: `pantalla` solo se modifica por botones y el router valida
antes de enrutar; no hay lectura de `query_params`. Recomendación: repetir
`verificar_acceso` en cada vista (defensa en profundidad) y añadir chequeos
de propiedad si se introduce multitenancia.

### MUR-06 (advertencia) — HTML sin escapar en explicación SHAP

`explicacion_shap.py:51` usa `st.markdown(..., unsafe_allow_html=True)`
interpolando `clinico` y `feature`. El origen es la explicación persistida
por `inference_service.explicar()`, construida con nombres de features del
pipeline entrenado y el mapeo `NOMBRES_CLINICOS` (control del servidor), no
input directo del usuario — riesgo bajo en la demo. Recomendación: quitar
`unsafe_allow_html=True` o escapar `html.escape()`; elimina la clase de error
por completo.

### MUR-07 (informativo, resuelto) — dependencias y CVEs

Auditoría ejecutada el 2026-08-14 con `pip-audit` sobre el venv del proyecto:

- Primera corrida: vulnerabilidades SOLO en las herramientas del entorno
  (`pip 23.2.1` — PYSEC-2023-228/PYSEC-2026-* y `setuptools 65.5.0` —
  PYSEC-2022-43012/PYSEC-2025-49), ninguna en las dependencias de runtime del
  proyecto (streamlit, sqlalchemy, bcrypt, reportlab, pandas, scikit-learn,
  xgboost, shap, joblib, pyyaml, openpyxl, pydantic, etc.).
- Corrección: `pip install --upgrade pip setuptools` en el venv.
- Re-auditoría: **"No known vulnerabilities found"**.

Recomendación estructural (para CI, no bloquea la demo): versiones con pin o
lock (`pip-tools`) y `pip-audit` como quality gate del pipeline.

### MUR-08 a MUR-12 (informativos) — verificados sin acción

- **A02 (MUR-08)**: `bcrypt.hashpw` con salt aleatorio; token de recuperación
  de 32 bytes urlsafe, almacenado como SHA-256 y comparado con
  `secrets.compare_digest`, expiración 15 min y un solo uso. Correcto.
- **A09 (MUR-09)**: `auditoria` protegida con `before_update`/`before_delete`
  (append-only) a nivel ORM; logging JSON sin contraseñas ni tokens; los
  stack traces van al log, no al usuario. El detalle de auditoría incluye
  número de documento del paciente por exigencia de trazabilidad (Ley
  1581/2012, Res. 5596/2015) — decisión aceptada.
- **A05 (MUR-10)**: no hay API HTTP ni CORS en la demo (Streamlit local).
  Para despliegue real: TLS en reverse proxy, headers CSP, X-Frame-Options,
  HSTS y Referrer-Policy, y `streamlit run --server.headless true`.
- **Secretos (MUR-11)**: grep de patrones (`api_key`, `password=`, `secret`,
  `token=`, `sk-`, `AKIA`) sobre `app/`, `ml/`, `scripts/`, `tests/` y
  `resources/`: sin claves reales. Únicos literales: `Demo123!` en
  `scripts/seed_demo.py` (seed de demo, datos sintéticos, documentado en el
  propio script) y el default de `APP_SECRET_KEY` (MUR-02). `.env` está en
  `.gitignore`; `.env.example` usa solo placeholders; `.streamlit/secrets.toml`
  gitignored. `AdaptadorPhysioNet` recibe credenciales por constructor.
- **A01/IDOR (MUR-12)**: el modelo de acceso es RBAC por pantalla (RD-004)
  sobre un pool único de pacientes clínicos; no existen rutas de API por ID.
  Aceptado para la demo; si se multitenantiza, añadir ownership por usuario.

## Mapeo OWASP Top 10 (2021)

| # | Categoría | Veredicto en TriajeIA |
|---|---|---|
| A01 | Broken Access Control | Aceptable para demo (router RBAC + revisión MUR-05); reforzar vistas y propiedad en producción |
| A02 | Cryptographic Failures | Correcto (bcrypt, token SHA-256 + compare_digest, MUR-08) |
| A03 | Injection | SQL parametrizado en todo el módulo; corregir HTML sin escapar (MUR-06) |
| A04 | Insecure Design | Sin hallazgo nuevo; threat model documentado en esta sección de fronteras |
| A05 | Security Misconfiguration | MUR-02 (mitigado) y MUR-10 (producción) |
| A06 | Vulnerable and Outdated Components | `pip-audit` ejecutado: sin vulnerabilidades conocidas tras actualizar pip/setuptools (MUR-07) |
| A07 | Identification and Authentication Failures | MUR-03 y MUR-04 (advertencias documentadas) |
| A08 | Software and Data Integrity Failures | MUR-01 — bloqueante, **resuelto** con pruebas |
| A09 | Security Logging and Monitoring Failures | Correcto (append-only, sin secretos en logs) |
| A10 | SSRF | No aplica: no hay fetch de URLs controladas por usuario |

## Verificación

- [x] Ejecutar `pip-audit` (MUR-07): solo pip/setuptools vulnerables →
      actualizados → re-auditoría sin vulnerabilidades (2026-08-14).
- [x] Ejecutar `scripts/bench_hardening.py` y completar `budget-triaje-ia.md`
      con los números reales (2026-08-14: p95 inferencia 26 ms, todo cumple).
- [x] Suite completa tras el hardening: 103/103 tests verdes y ruff 0 errores.
- [ ] En producción: cerrar MUR-02, MUR-03, MUR-04 y MUR-10 antes del primer
      despliegue con datos reales.
