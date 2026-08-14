# Trámites externos pendientes — TFM TriajeIA (hoja de ruta)

> Lista de trámites que la IA **no puede ejecutar** (hechos externos al
> documento). Cada uno con su responsable y criterio de cierre.

| # | Trámite | Responsable | Criterio de cierre | Estado |
|---|---|---|---|---|
| 1 | Aval de la directora a la organización del trabajo en grupo | Directora Fuentes Lorenzo | Firma/confirmación en `00-organizacion-trabajo-grupo.md` | ⏳ |
| 2 | Autorización del Comité de Ética (Art. 2.7) | Equipo + comité | Radicado + acta; adjuntar `solicitud-comite-etica.md` con anexos | ⏳ Bloqueante |
| 3 | Comprobación de plagio con la herramienta oficial de UNIR | Directora (Art. 11) | Informe con porcentaje registrado, anexar al TFM | ⏳ |
| 4 | Asignaturas del plan aprobadas (Art. 7) | Secretaría/estudiantes | Constancia administrativa | ⏳ |
| 5 | Credenciales PhysioNet + curso CITI para MIMIC-IV-ED | Equipo | `AdaptadorPhysioNet(usuario, password)` ya está implementado en `ml/src/data/ingesta.py` — solo falta ejecutar `descargar_ed_stays()` con credenciales reales y re-auditar el modelo con `ml/validacion.py` | ⏳ (validación externa) |
| 6 | Verificación de anonimización efectiva de los CSVs de `datasets/` | Equipo | Confirmación escrita de que ningún campo es identificable (documento del hospital o auto-verificación) | ⏳ |

## Orden recomendado

1. Ítem 2 (bloqueante) — presentar la solicitud con los anexos del hospital.
2. Ítems 1 y 3 en paralelo con la directora.
3. Ítem 5 cuando lleguen las credenciales (re-ejecutar `validacion-cientifica-ml`
   y regenerar el capítulo de Resultados con datos externos reales).
4. Ítem 6 antes de cualquier uso público de los CSVs.

Nota: los capítulos generados (`resources/tfm/capitulos/`) ya cumplen el resto
del checklist UNIR (hechos consumados, cifras trazables, benchmarks rotulados).
