# Checklist de Cumplimiento Normativo — TFM TriajeIA (UNIR)

- **Documento base:** Predepósito (Ordinaria), 14/07/2026 — Armenia, Colombia.
- **Autores:** Medina Betancur, Diego Andrés · Rivera Villanueva, Leyniker ·
  Soto Díaz, Erick Duván (orden alfabético de portada correcto).
- **Directora:** Damaris Fuentes Lorenzo.
- **Auditoría generada:** 2026-08-14 por `tfm-redactor` contra
  `.github/skills/tfm-redactor/references/checklist-normativo-unir.md`.
- **Regla de oro aplicada:** ningún ítem se marca ✅ sin evidencia textual o de
  contexto; ante la duda se marca ⚠️ o ❌.

## Bloqueantes de depósito

| # | Regla | Estado | Evidencia / hallazgo |
|---|---|---|---|
| 1 | Organización del trabajo en grupo avalada antes de la introducción | ⚠️ **Casi resuelto** | Redactado con la información real del equipo (portavoz: Medina; reparto por integrante; reuniones cada 3 días) en `resources/tfm/capitulos/00-organizacion-trabajo-grupo.md`. Falta únicamente el **aval de la directora**. |
| 2 | Autorización del Comité de Ética (datos sanitarios de terceros) | ❌ **Bloqueante** | Se usó la cohorte del Hospital San Juan de Dios (43.594 eventos). No existe constancia de autorización en el contexto. Trámite externo obligatorio (Art. 2.7) — sin él no hay depósito ni defensa. |
| 3 | Ausencia de plagio verificada con herramienta oficial | ⚠️ Pendiente | No hay evidencia de corrida anti-plagio en el contexto. Trámite del director (Art. 11). |
| 4 | Asignaturas aprobadas antes de la convocatoria | ⚠️ Pendiente | Trámite administrativo externo — nunca verificable desde el documento. |
| 5 | Trabajo original e inédito | ⚠️ Pendiente | No verificable desde el repositorio; depende del informe anti-plagio y de la declaración del equipo. |
| 6 | Orden alfabético de autores en portada | ✅ | Medina → Rivera → Soto (confirmado en `context/brief_finalizacion_tfm.md`). |
| 7 | Autorización expresa de uso de datos personales de terceros | ⚠️ Pendiente | Se documenta anonimización técnica (Ley 1581/2012) en el sistema, pero no consta autorización del titular/comité (Art. 8.3/8.4). |

## No bloqueantes pero exigidos por rúbrica

| # | Regla | Estado | Evidencia / hallazgo |
|---|---|---|---|
| 8 | Resumen/Abstract coherente con resultados reales | ✅ | Redactado en `resources/tfm/capitulos/00-resumen-abstract.md` con cifras verificadas contra `artifacts/metrics` (AUC 0.968, F1 0.551) y con la salvedad del dataset sintético declarada. |
| 9 | Numeración coherente índice/cuerpo/pies | ⚠️ Pendiente | Los capítulos nuevos usan numeración 0/4/5/7 alineada al documento base, pero la coherencia final se verifica al maquetar en `docx`. |
| 10 | Figuras con leyenda descriptiva real | ✅ | Matriz de confusión y tablas de los capítulos nuevos llevan leyenda completa (modelo, versión, conjunto, n). Sin placeholders "Enter Caption" en el contenido generado. |
| 11 | Capítulos en "hechos consumados" | ✅ | Capítulos 4/5/7 redactados en pretérito con evidencia trazable; los ítems no ejecutados están marcados `[PENDIENTE]` explícito, sin generalizar tiempo verbal. |
| 12 | Estilo de citación consistente | ⚠️ Pendiente | El contenido nuevo referencia archivos fuente en columnas "Fuente" y cita benchmarks por autor/año; la conversión final a APA se completa al integrar en el documento Word. |
| 13 | Defensa preparada (reparto y tiempos) | ⚠️ Recordatorio | No verificable desde el documento; cada integrante debe poder defender su parte (50 % contenido individual). |

## Hallazgos de trazabilidad resueltos en el cierre (2026-08-14)

1. ✅ **Duplicación de métricas early/late:** causa raíz identificada — la suite
de tests llamaba funciones de entrenamiento que escribían en el directorio
real `artifacts/metrics/`, sobrescribiendo la evidencia del pipeline con datos
de prueba (k_folds=3). Corregido redirigiendo los tests a `tmp_path` y
regenerando las métricas reales (CV de 5 folds, valores distintos:
fusión temprana F1 0.578; tardía promedio 0.555; stacking 0.560).
2. ✅ **`modelo_ganador.json` con `por_clase` vacío:** regenerado con el
pipeline corregido; ahora incluye la tabla por clase completa (II: P 0.867,
R 0.812, F1 0.839).
3. ✅ **Caso SHAP individual:** generado `artifacts/shap/shap_caso_test_1.json`
(nivel real III → predicho III, probabilidad 0.983) y citado en la sección 5.6.

## Resumen ejecutivo para la dirección

- **Redactable por IA y ya entregado:** Resumen/Abstract, Desarrollo (Cap. 4),
  Resultados (Cap. 5), Conclusiones (Cap. 7), Organización del trabajo en
  grupo (Cap. 0, con info real del equipo) — cifras reales trazables; los
  3 hallazgos de trazabilidad resueltos.
- **Maquetación:** `TFM_TriajeIA_UNIR.docx` generado (portada, índice,
  capítulos 0/4/5/7) — pendiente integrar capítulos 1–3 del documento base.
- **Trámites preparados:** borrador de solicitud al Comité de Ética
  (`resources/tfm/tramites/solicitud-comite-etica.md`) y hoja de ruta de
  trámites externos (`pendientes-tramites.md`).
- **NO redactable (trámites/información externa):** aval de la directora,
  autorización del Comité de Ética, anti-plagio, asignaturas aprobadas,
  credenciales MIMIC, verificación de anonimización de los CSVs.
- **Recomendación:** no iniciar el depósito hasta resolver el ítem 2
  (Comité de Ética) y el aval de la directora sobre el Cap. 0.
