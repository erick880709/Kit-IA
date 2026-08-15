# Instrumentación y Observabilidad — TriajeIA (estado al cierre)

Skill: `documentacion-observabilidad` · Fecha: 2026-08-14

## Actualización 2026-08-14 (post-cierre): logs de acciones + bug de modelo activo

**Logs por acción (solicitud del usuario):** cada acción relevante ahora emite
una línea JSON estructurada, tanto a stdout como al archivo rotativo
`triaje-ia/logs/app.log` (2 MB × 5 backups, agregado a `.gitignore`):

| Servicio | Acciones logueadas |
|---|---|
| `auth_service` | login exitoso, correo inexistente, usuario inactivo, bloqueo temporal, bloqueo por intentos, contraseña incorrecta (con intentos restantes), token de recuperación |
| `paciente_service` | paciente creado, paciente actualizado, verificación por documento (DEBUG) |
| `triaje_service` | evento creado, transición de estado (desde → hacia), signos registrados (IMC), evaluación clínica (CIE-10), clasificación IA persistida (nivel/versión/ms), validación profesional (concordancia), cierre de evento |
| `inference_service` | carga de modelo, inferencia OK (nivel/confianza/ms/versión), timeout, errores, circuit breaker |
| `main` | cierre de sesión (motivo + usuario) |

**Bug corregido (evidencia en logs del servidor 22:24:51 UTC):** la BD tenía
activo `modelo-latefusion-xgboost-v20260814` (XGBoost plano) en vez del ganador
`xgb-text-sjd`. Además `_predecir_proba` pasaba `X_txt` como 2º argumento
posicional → XGBoost lo interpretaba como `ntree_limit`/`validate_features` →
`ValueError: ambiguous truth` → fallback manual. Arreglos: (1) `_predecir_proba`
solo pasa ambos argumentos si el modelo es `LateFusionClassifier` (`sub_b`);
(2) se activó el modelo ganador vía `modelo_service.activar` (auditado).
Regresión cubierta: `test_predecir_proba_modelo_plano_sin_submodelo_texto`.
Verificado E2E en navegador: nivel IV sugerido, 919.7 ms, sin fallback.

## Instrumentación existente (verificada, no nueva)

- **Logs estructurados:** `app/infra/logging_config.py` — formato JSON con
  timestamps; módulos `inference_service`, `main` y servicios loguean errores
  y eventos sin contraseñas ni tokens (MUR-09).
- **Trazabilidad de negocio:** auditoría append-only (`app/services/audit_service.py`)
  con filtros por usuario/acción/entidad/rango y exportación CSV/Excel/PDF —
  cumple el papel de "traza" para el dominio clínico.
- **Métricas de modelo:** `artifacts/metrics/*.json` + `bench_hardening.json`
  (p50/p95/p99 de inferencia, dashboard y auditoría) — línea base de
  performance antes de producción.

## Decisiones registradas como ADR en este cierre

- ADR-005 — integridad de artefactos previa a deserialización (CWE-502).
- ADR-006 — aislamiento entre pruebas y evidencia de producción.

## Plan de instrumentación para producción (no aplica a la demo local)

1. **Métricas RED por endpoint de servicio** (rate/errors/duration) vía
   `prometheus_client` expuesto en el reverse proxy.
2. **Drift y calibración del modelo:** log periódico de la distribución de
   probabilidades y ECE/Brier en inferencia real (el benchmark de
   `scripts/bench_hardening.py` es el punto de partida).
3. **Alertas:** umbral sobre p95 de inferencia (presupuesto 3000 ms) y sobre
   fallos de carga del artefacto.
4. Trazas distribuidas solo si se separan servicios (monolito actual no lo
   requiere — decisión ADR-002).
