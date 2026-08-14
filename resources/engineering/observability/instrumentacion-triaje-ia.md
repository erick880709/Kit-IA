# Instrumentación y Observabilidad — TriajeIA (estado al cierre)

Skill: `documentacion-observabilidad` · Fecha: 2026-08-14

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
