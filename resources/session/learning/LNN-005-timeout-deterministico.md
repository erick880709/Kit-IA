---
fecha: 2026-08-14
fase: entrega
tags: [testing, flaky, threads, pytest]
severidad: media
---

# LNN-005: Timeout con timeout=0 en tests es una carrera — hacerlo determinístico parcheando al trabajador

## Contexto

`test_timeout_devuelve_fallback_sin_bloquear` usaba `InferenceService(timeout_s=0.0)` y esperaba fallback. Falló intermitentemente: si el hilo trabajador terminaba antes que `future.result(timeout=0)`, la predicción devolvía `ok` en vez de `indisponible`.

## Regla

Para probar timeouts de forma determinística, NO depender de la velocidad del trabajador: parchear el método ejecutado (`monkeypatch.setattr(servicio, "_predecir_proba", lambda *a, **k: time.sleep(0.5))`). Así `result(timeout=0)` siempre levanta `TimeoutError` y el test verifica el camino de fallback + shutdown no bloqueante (medir que el test tarda < sleep).

## Nota

Usar sleeps cortos (0.5 s) y asegurarse de que el shutdown no bloqueante evita esperar al hilo parcheado.
