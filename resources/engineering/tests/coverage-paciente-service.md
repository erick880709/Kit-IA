# Cobertura — servicio de pacientes (ajuste nuevo triaje para existente)

**Fecha:** 2026-08-14
**Plan:** `resources/engineering/plans/plan-ajuste-nuevo-triaje-paciente-existente.md`

## Rojo (antes de implementar) — motivo correcto

```
$ python -m pytest tests/test_paciente_service.py -q
E   ImportError: cannot import name 'buscar_por_documento' from 'app.services.paciente_service'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
Command exited with code 1
```

## Verde — módulo de pacientes

```
$ python -m pytest tests/test_paciente_service.py -q
.................                                                        [100%]
17 passed
```

## Verde — módulos afectados (pacientes + triaje + inferencia aislada)

```
$ python -m pytest tests/test_inference_service.py::test_predecir_con_modelo_cargado tests/test_paciente_service.py tests/test_triaje_service.py -q
..................................                                       [100%]
34 passed
```

## Lint

```
$ ruff check app tests
All checks passed!
```

## Verificación funcional en navegador (evidencia manual)

- Login `medico@hospital.gov.co` → Registro de paciente → documento `CC 52148903` →
  «Verificar documento».
- Precarga visible de todos los campos (María Gómez Ruiz, contacto, Amazonas/Leticia,
  triajes previos: 3).
- «➕ Iniciar nuevo triaje» → pantalla `signos_vitales` con evento nuevo.
- BD: paciente único (sin duplicado), total eventos 3 → 4 (1:N verificado).

## Nota

`test_predecir_con_modelo_cargado` puede fallar en suite completa por contención de
CPU (wall-clock RNF-007) cuando el servidor corre a la vez; pasa aislado. Ya
documentado en `resources/engineering/perf/budget-triaje-ia.md`.
