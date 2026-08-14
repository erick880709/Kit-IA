# Runbook E2E — TriajeIA (demo local)

Skill: `qa` · Fecha: 2026-08-14 · Alcance: flujo completo de la app (E1–E6).

> Nota de evidencia: el flujo E2E se verificó durante las sesiones de `builder`
> (E1 y E2 completas). Este runbook formaliza los casos para re-ejecutar antes
> de la defensa/demo. Entorno: `python scripts/seed_demo.py` +
> `streamlit run app/main.py --server.headless true --server.port 8599`.

## Caso 1 · Autenticación y RBAC

1. Login con `medico@hospital.gov.co` / `Demo123!` → entra al home.
2. `auditor@hospital.gov.co` NO ve pantallas clínicas (router RBAC).
3. 5 intentos con contraseña incorrecta → bloqueo y mensaje de intentos.
4. Recuperación de contraseña: token de un solo uso, expira a los 15 min.

## Caso 2 · Flujo clínico completo

1. Registrar paciente (con duplicado detectado por documento+nombre).
2. Iniciar evento de triaje → signos vitales fuera de rango exigen
   confirmación explícita.
3. Evaluación clínica → Clasificación IA con probabilidades + SHAP top-5.
4. Validación profesional → cierre → PDF anonimizado (iniciales + máscara).
5. Reclasificación: evento reclasificado queda correctamente registrado.

## Caso 3 · Auditoría y trazabilidad

1. Consultar auditoría por usuario/acción/rango y verificar que el cierre del
   Caso 2 aparece.
2. Exportar CSV/Excel/PDF y abrir al menos uno.

## Caso 4 · Gestión de modelos

1. Activar/desactivar modelo alterno y verificar que la inferencia usa el
   activo (recarga del singleton).
2. Comparación de modelos muestra benchmarks y modelo propio rotulados.

## Criterios de salida

- [ ] 103/103 tests verdes (`pytest -q`) y `ruff` 0 errores antes de la demo.
- [ ] Los 4 casos completados sin excepciones en consola.
- [ ] Inferencia < 3 s por predicción (RNF-007).
