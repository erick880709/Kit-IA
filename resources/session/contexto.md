# Contexto del Proyecto — Kit IA / TFM TriajeIA

## Qué es

Kit IA es un pipeline SDD de 26 skills (negocio → arquitectura → scaffold → ingeniería → entrega → académico). Repo público `erick880709/Kit-IA` (rama `main`, MIT). Proyecto activo: **TriajeIA**, TFM UNIR — sistema de apoyo al triaje de urgencias (I–V, Res. 5596/2015) con IA multimodal (signos estructurados + CIE-10/texto), Streamlit + SQLite, monolito modular.

## Estado actual (2026-08-14)

**Desarrollo COMPLETO y auditado.** Épicas E1–E6 implementadas (auth/RBAC, flujo clínico 8 pantallas, pipeline ML, motor IA con SHAP, auditoría append-only, dashboard/modelos). Post-desarrollo: paso 1 revisión (Centinela: 3 Bloqueante + 17 Debe corregirse resueltos), paso 2 validación científica (fugas corregidas, McNemar p≈0, Brier 0.036/ECE 0.042, model card), paso 3 hardening (CWE-502 resuelto, pip-audit limpio, p95 26 ms), paso 4 entrega (7 commits atómicos en main, CI con ruff+pytest+pip-audit, checklist release v1.0.0). **103/103 tests, ruff 0.**

**Modelo ganador:** fusión tardía XGBoost estructurado (tuned: depth 5, lr 0.1, pesos balanceados) + LR sobre TF-IDF (CIE+texto, cohorte SJdD 43.594 eventos) — AUC 0.968, macro-F1 0.551 en demo-test, umbrales por clase priorizando recall I–II. Holdout SJdD honesto: F1 0.088.

## Lo que sigue

1. **tfm-redactor** (EN CURSO): capítulos con cifras reales de `artifacts/metrics` en `resources/tfm/capitulos/` + `checklist-cumplimiento.md`. Nunca inventar números; marcar `[PENDIENTE]`.
2. Trámites externos del depósito (NO redactables): Comité de Ética (Art. 2.7), anti-plagio, asignaturas, organización del trabajo en grupo.
3. Verificar macro_cv idéntico early/late fusion (posible bug de registro, paso 6 del pipeline).
4. MIMIC-IV-ED pendiente de credenciales PhysioNet (evidencia definitiva externa).

## Decisiones y preguntas abiertas

- ¿CSVs de `datasets/` realmente anonimizados? (excluidos del repo; validar antes de uso público).
- Metas RNF-001 de macro-F1 ≥ 0.82 NO alcanzadas → reconciliar honestamente en Conclusiones (el demo sintético es evidencia preliminar).

## Riesgos

- AUC demo-test optimista (CIE-10 sintético condicionado al nivel) — declararlo en Resultados.
- Confundir benchmarks (CTAS 0.882, Hong 0.93, Ueareekul 0.917) con resultados propios — fila rotulada aparte.
