# Arquitectura de los Modelos — TriajeIA

**Versión:** 1.0 · **Fecha:** 2026-08-13 · **Skill:** `archi` (modo ML)
**Relación:** complemento de `Documento_Arquitectura_TriajeIA.md` §5.1–5.4, §9.1 y §13.1.
**Diagramas oficiales:** `Diagramas_TriajeIA.drawio` → pestañas **5. ML C1 Contexto**, **6. ML C2 Pipeline**, **7. Arquitectura del Modelo**.
**ADRs de modelo:** `adr/ADR-003-desbalance-class-weights-umbrales.md`, `adr/ADR-004-fusion-tardia-vs-temprana.md`.

---

## 1. Alcance y enfoque del componente ML

El sistema clasifica un evento de triaje en 5 niveles (Res. 5596/2015) combinando **dos modalidades**:

1. **Modalidad estructurada:** signos vitales (SpO₂, FC, FR, PA, T°), demografía, antecedentes, dolor/Glasgow.
2. **Modalidad textual:** motivo de consulta libre + descripción estructurada (CIE-10).

El estudio compara **fusión temprana** (features concatenadas + clasificador único) contra **fusión tardía** (submodelos independientes + meta-modelo). Ambas son obligatorias (RT-002). La tardía es la candidata principal (ADR-004).

**El modelo sugiere; el profesional decide.** El sistema nunca autocompleta el nivel del profesional (RNF-008, RD-003).

## 2. Fuentes de datos y pipeline

| Fuente | Tipo | Volumen | Rol |
|---|---|---|---|
| MIMIC-IV-ED | Tabular + texto libre | ~425k visitas | Preentrenamiento / baseline (pendiente CITI) |
| Cohorte Hospital SJdD | Tabular (morbilidad + etiqueta triaje) | 43.594 episodios | Validación contexto local |
| datos.gov.co triaje nacional | Tabular | 89.453 eventos | Calibración de distribución I–V |
| BDUA (contributivo/subsidiado) | Tabular | ~11 M | Perfil demográfico |
| Línea 123 Bogotá | Texto | ~100 meses | NLP motivo de consulta |
| Sintéticos demo | Tabular + texto | Generados | Demo funcional (calibrados con distribuciones reales) |

### Pipeline (13 pasos — RD-006)

`Ingesta CSV → validación de esquema → limpieza (nulos/outliers/deduplicación) → anonimización (Ley 1581) → feature engineering → split estratificado 70/15/15 → entrenamiento → evaluación → selección → registro → export demo`.

**Anti-leakage (crítico):**
- El split es **estratificado por nivel** y ocurre **antes** de cualquier `fit`.
- El vectorizador de texto usa un modelo preentrenado sin reentrenar sobre test.
- Imputaciones y escaladores se ajustan **solo** con train y se aplican a val/test.
- Semilla global fija (`RANDOM_SEED=42`) y versionado de datos (`data-v<fecha>-<hash>`).

## 3. Arquitectura de entrenamiento

### 3.1 Baselines obligatorios (RT-004)

| Baseline | Entrada | Nota |
|---|---|---|
| Regresión Logística | Estructurado | Cota inferior; pesos por clase |
| Random Forest | Estructurado | Cota media |
| XGBoost | Estructurado | Baseline fuerte |

Ningún modelo complejo se declara ganador sin superar estos baselines con significancia estadística.

### 3.2 Submodelo de texto

BERT clínico en español (familia BETO / biomédica) produce el embedding `[CLS]` del motivo de consulta (RT-003). Solo fine-tuning ligero o extracción de features — no reentrenamiento completo (datos limitados).

### 3.3 Estrategias de fusión

| | Fusión temprana | Fusión tardía |
|---|---|---|
| Pipeline | features ⊕ embedding → clasificador único | XGBoost(structurado) y BERT(texto) → probs → meta-modelo |
| Meta-modelo | — | Regresión Logística (RT-010) |
| Explicabilidad | SHAP sobre el clasificador único | SHAP por submodelo + pesos del meta-modelo |
| Ventaja | Simplicidad, interacciones intermodalidad | Modularidad, aislamiento de errores, interpretación por modalidad |

### 3.4 Optimización y tracking

- **Hiperparámetros:** Optuna (bayesiana), objetivo F1-macro con restricción de recall I–II.
- **Tracking:** MLflow local (`mlruns/`): parámetros, métricas, matriz de confusión, artefacto, semillas.
- **Versionado:** convención `<algoritmo>_<fusion>_v<YYYYMMDD>.joblib` + registro en `artifacts/models/`.
- **Cómputo:** CPU local del equipo (volumen y modelos lo permiten).

## 4. Arquitectura del modelo (detalle)

```mermaid
graph LR
    S[Estructurado] --> XG[XGBoost + class weights]
    T[Texto motivo] --> BE[BERT clínico ES]
    BE --> E[[CLS] embedding]
    XG --> P1[probs estructuradas]
    BE --> P2[probs texto]
    P1 --> MM[Meta-modelo LR]
    P2 --> MM
    MM --> PR[Probs I-V]
    PR --> U[Umbrales por clase - RT-009]
    U --> N[Nivel sugerido]
    PR --> SH[SHAP: TreeExplainer + KernelExplainer]
    SH --> UX[Explicación en lenguaje clínico]
```

> Diagrama visual completo (fusión temprana vs tardía lado a lado): `Diagramas_TriajeIA.drawio` → pestaña **7. Arquitectura del Modelo**.

## 5. Evaluación y métricas

| Métrica | Meta (RNF-001) | Alcance |
|---|---|---|
| F1-score | ≥ 0.82 | Global y por clase I–V |
| Precisión | ≥ 0.85 | Global y por clase |
| Recall | ≥ 0.80 | **Prioridad I–II** (RNF-003) |
| AUC-ROC | ≥ 0.87 | One-vs-rest por nivel |

Obligatorio además:
- Matriz de confusión 5×5 del modelo ganador.
- Comparación contra baselines con **McNemar** (entre pares).
- Comparación contra benchmark de literatura (MTS/ESI — RT-008).
- Distribución real nacional como referencia de prevalencia (RNF-004).
- Curvas de calibración de probabilidades (las probs se muestran al profesional).

## 6. Explicabilidad (XAI)

- **Técnica:** SHAP — TreeExplainer (XGBoost), KernelExplainer (meta-modelo), SHAP de transformers (texto).
- **Contrato con el usuario:** top-N variables traducidas a lenguaje clínico + comparación implícita con criterios MTS; impactos +/− diferenciados (mockup `s-shap`).
- **Alcance:** local (por evento) y global (importancia agregada, Dashboard fase 2).

## 7. Inferencia y servicio

| Decisión | Valor |
|---|---|
| Modo | Online, síncrono, **en proceso** dentro de Streamlit |
| Ubicación | `artifacts/models/<artefacto>.joblib` + metadatos MLflow |
| Latencia | < 3 s (RNF-002); medición demo 1.8 s |
| Degradación | Si falla la inferencia, la app sigue usable en triaje manual (RNF-009) |
| Reentrenamiento | Manual bajo demanda (investigación); deriva monitorizada en fase 2 |

## 8. Estructura del proyecto ML (reproducibilidad)

Convención para el código de entrenamiento (guia-notebooks-python):

```
triaje-ia/ml/                       # código del pipeline offline
├── data/                           # versionado: data-v<fecha>-<hash> (DVC)
│   ├── raw/            # nunca se edita
│   └── processed/      # splits + features (generado)
├── notebooks/          # 01-eda · 02-preproceso · 03-baselines · 04-fusion · 05-evaluacion
├── src/                # lógica reutilizable (evita lógica crítica en notebooks)
│   ├── features.py     # feature engineering versionado (anti training-serving skew)
│   ├── evaluate.py     # métricas por clase + McNemar + calibración
│   └── registry.py     # guardado/registro MLflow
├── configs/            # hiperparámetros por experimento
└── artifacts/          # salidas: modelos, métricas, shap
```

Reglas: semilla fija en `configs/`, los notebooks no contienen lógica reutilizable (solo orquestan `src/`), cada experimento queda registrado en MLflow con el hash del dataset.

## 9. Gobernanza, ética y cumplimiento

- **Rol:** apoyo a la decisión humana (no autónomo) — explícito en la UI.
- **Normativa:** Ley 1581/2012 (datos personales) + Res. 5596/2015; autorización del Comité de Ética para datos clínicos (Art. 2.7 UNIR). Demo con datos **sintéticos**.
- **Sesgo:** si el entrenamiento usa MIMIC (EE. UU.), documentar la limitación de representatividad y validar con el cohorte colombiano.
- **Trazabilidad:** cada predicción persiste features relevantes, versión de modelo, output y decisión humana (RD-003).
- **Deriva:** estrategia de monitoreo de distribución de features documentada (§13 del documento de arquitectura); implementación fase 2.

## 10. Relación con los diagramas oficiales

| Contenido | Pestaña `.drawio` |
|---|---|
| Contexto del sistema ML | 5. ML C1 Contexto |
| Pipeline de datos + entrenamiento | 6. ML C2 Pipeline |
| Fusión temprana vs tardía + SHAP | 7. Arquitectura del Modelo |
| C4 de la aplicación | 1–4 |
| Despliegue y secuencias | 8–10 |
