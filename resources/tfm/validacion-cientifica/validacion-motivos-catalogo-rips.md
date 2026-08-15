# Validación: ¿los motivos de urgencia nuevos ayudan al diagnóstico de la IA?

**Fecha:** 2026-08-14
**Insumos:** catálogo de 71 motivos (`app/domain/catalogos.py`), dataset público
RIPS urgencias con observación (Medellín, 1.708.104 filas, 2019-2022), modelo
activo `modelo-latefusion-xgb-text-sjd-v20260814`.

## 1. Nuevo dato público descargado

| Campo | Valor |
|---|---|
| Nombre | Registro Prestación Servicios Médicos en Urgencia con observación |
| Fuente | `medata.gov.co` (federado desde datos.gov.co, view `xveb-6jax`) |
| Archivo | `datasets/rips_urgencias_observacion_medellin.csv` (207 MB, 1.708.104 filas, 23 columnas) |
| Diccionario | `datasets/diccionario_rips_urgencias_medellin.json` |
| Columnas clave | `FechaIngreso`, `CausaExterna`, `CodigoDiagnosticoPrincipalSalida` (CIE-10), `DestinoUsuario`, `EstadoSalida` (vivo/muerto), `Edad`, `Sexo`, `Ano` |
| Licencia | CC BY-SA 4.0 (Alcaldía de Medellín) |
| Nota de descarga | El portal medata.gov.co requiere `curl -k` desde esta máquina (cadena TLS no confiable) |

## 2. Cobertura del catálogo en datos reales

- **61 de 71 motivos** del catálogo aparecen en los registros reales de Medellín.
- **26,94 % de las 1,7 M de filas** corresponden a un motivo del catálogo.
- El top-15 real coincide con el catálogo (R104, N390, R51X, N23X, I10X, R074,
  K297, R509, A09X, J00X, M545…): el catálogo está bien alineado con la
  morbilidad real. Evidencia: `triaje-ia/artifacts/metrics/rips_medellin_resumen.json`.

## 3. Severidad real por motivo (mortalidad en observación)

| CIE-10 | Motivo | n | Mortalidad % |
|---|---|---|---|
| J96.0 | Insuficiencia respiratoria aguda | 1.554 | **28,31** |
| J18.9 | Neumonía no especificada | 7.800 | 7,59 |
| R06.0 | Disnea | 6.301 | 7,57 |
| T75.4 | Electrocución | 19 | 5,26 |
| R50.9 | Fiebre no especificada | 20.633 | 4,36 |
| K92.2 | Hemorragia gastrointestinal | 8.586 | 4,36 |
| R10.4 | Dolor abdominal no especificado | 54.160 | 3,10 |
| A09 | Gastroenteritis | 19.894 | 1,73 |

⚠️ **Limitación honesta:** la unidad de observación NO es severidad de triaje.
El trauma grave se deriva a cirugía/otros servicios (p. ej. W34.9 herida por
arma de fuego: n=9, mortalidad 0 % en observación), por lo que estas cifras
subestiman la severidad real del trauma. Sirven como **prior poblacional** de
severidad para condiciones médicas, no como etiqueta de triaje.

## 4. Impacto de los motivos en la inferencia actual

Validación con signos vitales fijos y cada uno de los 71 motivos
(`scripts/validacion_motivos_inferencia.py`):

- **Solo 1 de 71 motivos (1,4 %)** cambia el nivel sugerido vs. línea base sin
  motivo: `K92.2 Hemorragia gastrointestinal → I`.
- **8 motivos tienen 0 % de cobertura de vocabulario TF-IDF** (estreñimiento,
  náuseas, tos, disnea, electrocución, agitación, deshidratación, anorexia).
- Causa raíz: el submodelo de texto se entrenó con la cohorte SJdD (vocabulario
  de 600 términos); muchos términos del catálogo quedan fuera de vocabulario y
  TfidfVectorizer los ignora. Además el submodelo de texto es débil
  (holdout F1 ≈ 0,09, documentado en el cap. Resultados).

**Conclusión: los motivos nuevos mejoran la captura clínica y la cobertura del
catálogo, pero HOY no mejoran el diagnóstico de la IA.** No hay regresión: el
comportamiento es idéntico al modelo previo.

## 5. Ajuste implementado

- `VectorizadorTexto.fit(textos, textos_extra=...)`: el vocabulario TF-IDF ahora
  incluye el catálogo completo de motivos al entrenar (ajuste en
  `ml/src/models/embeddings.py` + `ml/pipeline.py`, paso 4/10).
- Test: `tests/test_embeddings.py` (3 casos: sin extra, con extra, transformar).
- **No se regeneró el artefacto** a propósito: sin nuevos textos ETIQUETADOS
  (MIMIC-IV-ED pendiente de credenciales PhysioNet), reentrenar no añade señal;
  los términos solo-de-catálogo tendrían coeficiente 0 en la LR. El vocabulario
  extendido queda listo para el reentrenamiento cuando lleguen datos etiquetados.

## 6. Recomendación

1. **MIMIC-IV-ED** (credenciales PhysioNet) sigue siendo el paso definitivo:
   chief complaint + nivel de triaje etiquetado → el submodelo de texto
   aprendería la severidad de motivos tipo trauma.
2. Usar el RIPS como **prior poblacional** de severidad en el análisis de sesgo
   y en la calibración por departamento.
3. Reejecutar `python -m ml.pipeline --n 4000 --k-folds 5` (con el vocabulario
   extendido ya cableado) únicamente cuando exista el corpus etiquetado nuevo.
