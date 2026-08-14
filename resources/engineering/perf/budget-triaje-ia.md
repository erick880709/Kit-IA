---
title: "Presupuesto de performance TriajeIA — mediciones antes/después"
skill: seguridad-rendimiento
date: 2026-08-14
proyecto: TriajeIA
modulo: inference_service, dashboard_service, audit_service, frontend Streamlit
---

# Presupuesto de performance TriajeIA — mediciones antes/después

Regla del skill: no se optimiza sin número de antes. Este documento define el
presupuesto, el protocolo de medición y deja constancia del antes/después.
Estado: **medido** con `triaje-ia/scripts/bench_hardening.py` sobre el
artefacto real `modelo-latefusion-xgb-text-sjd-v20260814.joblib` y la BD demo
(2026-08-14 14:37 UTC). No se aplicó ninguna optimización de performance: nada
excede presupuesto y el skill prohíbe optimizar a ciegas.

## Presupuestos

| Métrica | Presupuesto | Norma / RNF | Ámbito |
|---|---|---|---|
| Latencia de inferencia `predecir()` | p95 < 3000 ms (timeout del servicio en 3 s) | RNF-007 | Backend |
| `dashboard_service.calcular_indicadores()` | < 1000 ms | RNP-003 | Backend |
| `audit_service.consultar()` (página de 50) | < 1000 ms | RNP-003 | Backend |
| Import de `app.main` (sustituto de LCP/arranque) | < 5000 ms | Referencia orientativa | Frontend |
| Core Web Vitals reales (LCP/INP/CLS) | LCP < 2500 ms, INP < 200 ms, CLS < 0.1 | Referencia orientativa | Frontend (requiere servidor de pruebas) |

Nota sobre el frontend: Streamlit renderiza servidor-cliente; medir Core Web
Vitals requiere levantar un servidor de pruebas y navegación real, fuera del
alcance de esta sesión. El tiempo de importación del script principal queda
como referencia proxy mientras no se haga esa medición.

## Protocolo de medición (una sola ejecución)

```powershell
cd C:\Users\ELITEBOOK\OneDrive\Documentos\Repositorio\Trabajo\kit-ia\triaje-ia
$env:PYTHONPATH = "C:\Users\ELITEBOOK\OneDrive\Documentos\Repositorio\Trabajo\kit-ia\triaje-ia"
.venv\Scripts\python.exe scripts\bench_hardening.py
```

El script mide:

- Inferencia: 1 llamada de calentamiento (carga del artefacto real de
  `artifacts/models/` excluida de las muestras) + 30 llamadas reales;
  reporta p50/p95/p99/min/max en ms y si cumple RNF-007.
- `calcular_indicadores()` y `consultar(page=1, page_size=50)` sobre la BD
  demo `triaje.db`.
- Import de `app.main` (incluye Streamlit y las 16 vistas).
- Escribe el resultado en `artifacts/metrics/bench_hardening.json`.

## Antes / después

Medición real con `scripts/bench_hardening.py` (30 llamadas de inferencia,
artefacto real + BD demo, 2026-08-14 14:37 UTC). Evidencia cruda en
`artifacts/metrics/bench_hardening.json`.

| Métrica | Medido | Presupuesto | Estado |
|---|---|---|---|
| Inferencia p50 | 24.11 ms | < 3000 ms | ✅ cumple RNF-007 |
| Inferencia p95 | 26.09 ms | < 3000 ms | ✅ cumple RNF-007 |
| Inferencia p99 | 26.87 ms | < 3000 ms | ✅ cumple RNF-007 |
| Inferencia min/max | 22.10 / 27.13 ms | < 3000 ms | ✅ |
| `calcular_indicadores()` | 24.02 ms | < 1000 ms | ✅ cumple RNP-003 |
| `consultar()` página 50 | 6.93 ms | < 1000 ms | ✅ cumple RNP-003 |
| Import `app.main` | 566.41 ms | < 5000 ms | ✅ referencia orientativa |

Sin optimizaciones aplicadas: todo cumple el presupuesto; no hay número que
justifique tocar código. Los candidatos de optimización (materialización de
eventos en `calcular_indicadores`, doble pasada en `consultar`) quedan
documentados para el día en que una medición los active.

## Reglas si algo excede presupuesto

- Optimizar solo la métrica que supera el presupuesto, guiándose por el
  perfil (cProfile) — no por intuición.
- Volver a medir con el mismo script y registrar antes/después en la tabla
  anterior, con el commit de la optimización en `detalle`.
- Candidatos conocidos por si aparecen (no tocados en esta sesión porque no
  hay número que los justifique): cache del paquete ML ya existe
  (`_paquete` singleton); `calcular_indicadores` materializa todos los
  eventos en listas Python; `consultar` ejecuta un `COUNT`-like con
  `len(...all())` y luego la página (dos pasadas sobre el filtro).
