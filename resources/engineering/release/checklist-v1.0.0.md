# Checklist de Pre-Lanzamiento — TriajeIA v1.0.0

- **Fecha:** 2026-08-14 · **Alcance:** Épicas E1–E6 completas (auth/RBAC, flujo
  clínico, pipeline ML, motor IA, auditoría, dashboard/modelos)
- **Skill:** entrega-continua · **Gates previos:** revision-calidad ✓,
  validacion-cientifica-ml ✓, seguridad-rendimiento ✓

## Gates de calidad (todos verificados en esta sesión)

- [x] `pytest -q` → **103/103 tests verdes** (incluye regresiones de los 3 pasos previos)
- [x] `ruff check app ml tests scripts` → **0 errores**
- [x] `pip-audit` → **sin vulnerabilidades conocidas** (pip/setuptools del venv actualizados)
- [x] Inferencia p95 **26 ms** < presupuesto 3000 ms (RNF-007) · dashboard/auditoría < 1000 ms (RNP-003)
- [x] Diseño experimental sin fuga de datos (escalador solo en train, holdout SJdD honesto)
- [x] McNemar ganador vs regla mayoritaria p≈0 · ECE 0.042 · model card generado
- [x] Hash de artefacto verificado ANTES de deserializar (CWE-502 resuelto)

## Evidencia

| Artefacto | Ruta |
|---|---|
| Review de código (Centinela) | `resources/engineering/reviews/review-e1-e6.md` |
| Auditoría científica | `resources/tfm/validacion-cientifica/reporte-auditoria.md` |
| Model card | `resources/tfm/validacion-cientifica/model-card-modelo-latefusion-xgb-text-sjd-v20260814.md` |
| Hardening (Muralla) | `resources/engineering/security/hardening-triaje-ia.md` |
| Presupuesto performance | `resources/engineering/perf/budget-triaje-ia.md` |
| Benchmark crudo | `triaje-ia/artifacts/metrics/bench_hardening.json` |

## Rollback plan (explícito y probado)

1. **Código:** `git revert <commit-problemático>` (historia lineal en `main`).
   Cada commit atómico de esta entrega deja tests en verde, por lo que
   cualquier revert individual vuelve a un estado compilable.
2. **Base de datos demo:** `triaje.db` es local, sintética y regenerable →
   `python scripts/seed_demo.py` la reconstruye desde cero (credenciales
   demo documentadas). Las migraciones ligeras (`_COLUMNAS_NUEVAS` en
   `app/infra/db.py`) son aditivas, nunca destructivas.
3. **Modelo IA:** rollback sin redeploy — activar el modelo anterior desde la
   pantalla de gestión (`Modelo.activar/desactivar`, normaliza flags y
   recarga el singleton de inferencia). El artefacto es regenerable con
   `python -m ml.pipeline --n 4000 --k-folds 5`.
4. **Verificación del rollback:** re-ejecutar `pytest -q` + `ruff check` +
   abrir la app en `localhost:8599` y completar un triaje de prueba con
   `medico@hospital.gov.co` / `Demo123!`.

## Monitoreo activo

- **Demo local:** logs JSON estructurados (`app/infra/logging_config.py`),
  auditoría append-only consultable en la pantalla de auditoría (filtros por
  usuario/acción/rango) — activa desde el minuto uno, no después del rollout.
- **Producción futura (MUR-10):** TLS en reverse proxy, headers CSP /
  X-Frame-Options / HSTS, `streamlit run --server.headless true`, y cierre
  de MUR-02/03/04 (secret key aleatoria obligatoria, login sin enumeración,
  rate-limit en recuperación) antes del primer despliegue con datos reales.

## Feature flags y rollout escalonado

- **No aplica** a una demo local monousuario: no hay feature flags ni
  despliegue escalonado en este release. El blast radius es una máquina local
  con datos sintéticos. Queda documentado como decisión de alcance.

## Deprecaciones en este ciclo

- `use_container_width` → `width="stretch"` (deprecación oficial de
  Streamlit ≥1.57): migración completada en revisión-calidad; no queda código
  zombie usando la API vieja.
- API `verificar_metas` con AUC `None`: renombrada sin romper consumidores.
- Sin endpoints/features deprecados con fecha pendiente: todas las épicas
  fueron adiciones, no reemplazos.

## Decisión de versionado (RNF-006)

- `artifacts/models/*`, `datasets/`, `*.db`, `.env` y `mlruns/` **no se
  versionan** (datos reales y artefactos pesados). El pipeline regenera el
  artefacto; los datasets reales (MinSalud/SJdD, 350+ MB) se descargan con el
  protocolo documentado en `context/07-MAPEO-Y-DESCARGA-DATASETS.md`.

## Firma de aprobación

- [x] Gates de calidad verdes en local y reproducidos en CI (`ci.yml`)
- [x] Plan de rollback explícito y probado (paso 4 arriba)
- [x] Monitoreo/auditoría activo antes del rollout
- [x] Historia de commits atómica sin "WIP" (ver `git log` de esta entrega)
